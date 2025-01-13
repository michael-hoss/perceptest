import argparse
import math
from copy import deepcopy

import numpy as np
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.state import TraceState  # type: ignore

from research.delta_crit.crime_utils.crime_utils import (
    CriMeConfiguration,
    Scenario,
    get_scenario_config,
    write_scenario,
    write_scenario_config,
)
from research.delta_crit.pem.pem_config import PemConfig, Perror, pem_config_from_json


def create_sut_scenario_files(
    scenario_id: str, pem_config_path: str, sut_scenario_path: str, sut_crime_config_path: str
) -> None:
    crime_config: CriMeConfiguration = get_scenario_config(scenario_id=scenario_id)
    pem_config: PemConfig = pem_config_from_json(json_path=pem_config_path)

    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=pem_config)

    write_scenario(scenario=sut_scenario, filename=sut_scenario_path)
    write_scenario_config(config=sut_config, filename=sut_crime_config_path)


def create_sut_scenario(crime_config: CriMeConfiguration, pem_config: PemConfig) -> tuple[Scenario, CriMeConfiguration]:
    sut_config = deepcopy(crime_config)
    sut_scenario = sut_config.scenario

    ego_vehicle: DynamicObstacle = sut_scenario.obstacle_by_id(crime_config.vehicle.ego_id)

    for perror in pem_config:
        if perror.object_id == -1:
            obstacles_to_modify = []
            for dynamic_obstacle in sut_scenario.dynamic_obstacles:
                if dynamic_obstacle.obstacle_id != ego_vehicle.obstacle_id:
                    obstacles_to_modify.append(dynamic_obstacle)
        else:
            obstacles_to_modify = [sut_scenario.obstacle_by_id(perror.object_id)]

        for obstacle in obstacles_to_modify:
            # TODO handle -1 timestep for end
            # function to get final timestep?

            start_timestep = max(perror.start_timestep, obstacle.prediction.trajectory.initial_time_step)

            end_timestep = min(perror.end_timestep, obstacle.prediction.trajectory.final_state.time_step)
            if perror.end_timestep == -1:
                end_timestep = obstacle.prediction.trajectory.final_state.time_step

            for timestep in range(start_timestep, end_timestep):
                ego_state: TraceState = ego_vehicle.state_at_time(time_step=timestep)
                obstacle_state: TraceState = obstacle.state_at_time(time_step=timestep)
                add_offset_long_lat(ego_state=ego_state, obstacle_state=obstacle_state, perror=perror)
                add_offset_range_azimuth(ego_state, obstacle_state=obstacle_state, perror=perror)
    return sut_scenario, sut_config


def add_offset_long_lat(ego_state: TraceState, obstacle_state: TraceState, perror: Perror) -> None:
    """Add offsets along the ego vehicle's longitudinal and lateral directions to the target obstacle's position."""

    ego_orientation: float = ego_state.orientation
    offset_long: float = perror.offset_longitudinal
    offset_lat: float = perror.offset_lateral

    offset_east = offset_long * math.cos(ego_orientation) - offset_lat * math.sin(ego_orientation)
    offset_north = offset_long * math.sin(ego_orientation) + offset_lat * math.cos(ego_orientation)

    obstacle_state.position[0] += offset_east
    obstacle_state.position[1] += offset_north


def add_offset_range_azimuth(ego_state: TraceState, obstacle_state: TraceState, perror: Perror) -> None:
    """Add offsets along the ego vehicle's range and azimuth directions to the target obstacle's position."""

    ego_orientation: float = ego_state.orientation
    offset_range: float = perror.offset_range
    offset_azimuth: float = perror.offset_azimuth * math.pi / 180

    # Add offset in relative (ego-specific) coordinates
    rel_position = obstacle_state.position - ego_state.position
    target_range = np.linalg.norm(rel_position[:2]) + offset_range
    target_azimuth = math.atan2(rel_position[1], rel_position[0]) - ego_orientation + offset_azimuth

    # Transform back to east/west coordinates
    rel_position[0] = target_range * math.cos(target_azimuth + ego_orientation)
    rel_position[1] = target_range * math.sin(target_azimuth + ego_orientation)

    obstacle_state.position = ego_state.position + rel_position


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply a perception error model (PEM) to a CommonRoad scenario in order to synthesize an SUT scenario."
    )
    parser.add_argument("--scenario_id", type=str, help="Original CommonRoad scenario ID")
    parser.add_argument("--pem_config", type=str, help="Path to PEM config json")
    parser.add_argument("--sut_scenario", type=str, help="Output path of synthesized CommonRoad scenario.")
    parser.add_argument("--sut_crime_config", type=str, help="Output path to SUT CriMe config")
    args = parser.parse_args()

    create_sut_scenario_files(
        scenario_id=args.scenario_id,
        pem_config_path=args.pem_config,
        sut_scenario_path=args.sut_scenario,
        sut_crime_config_path=args.sut_crime_config,
    )


if __name__ == "__main__":
    main()
