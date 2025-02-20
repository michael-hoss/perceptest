import argparse
import math
from copy import deepcopy

import numpy as np
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.state import TraceState  # type: ignore

from research.delta_crit.crime_utils.crime_utils import (
    CriMeConfiguration,
    Scenario,
    crime_paths_factory_for_delta_crit_example_data,
    get_crime_config,
    write_crime_config_deep,
)
from research.delta_crit.crime_utils.refresh_dynamic_obstacles import refresh_dynamic_obstacles
from research.delta_crit.pem.pem_config import (
    PemConfig,
    Perror,
    int_hash_of_pem_config,
    pem_config_from_path_or_instance,
)


def create_sut_crime_config_files(workdir: str, scenario_id: str, pem_config: str | PemConfig) -> str:
    """All files are read from workdir and written to workdir."""

    pem_config_parsed: PemConfig = pem_config_from_path_or_instance(pem_config=pem_config)
    crime_config: CriMeConfiguration = get_crime_config(scenario_id=scenario_id, custom_workdir=workdir)

    sut_config = create_sut_crime_config(crime_config=crime_config, pem_config=pem_config_parsed)

    write_crime_config_deep(config=sut_config, output_dir=workdir)
    return str(sut_config.scenario.scenario_id)


def create_sut_crime_config(crime_config: CriMeConfiguration, pem_config: PemConfig) -> CriMeConfiguration:
    sut_config = deepcopy(crime_config)

    apply_pem_to_crime_config(crime_config=sut_config, pem=pem_config)

    sut_config.scenario = adjust_scenario_metadata(scenario=sut_config.scenario, pem_config=pem_config)
    sut_config.general = crime_paths_factory_for_delta_crit_example_data(scenario_name=sut_config.scenario.scenario_id)

    return sut_config


def adjust_scenario_metadata(scenario: Scenario, pem_config: PemConfig) -> Scenario:
    original_scenario_id: str = str(scenario.scenario_id)

    if "Michael Hoss" not in scenario.author:
        scenario.author = "Michael Hoss, " + scenario.author

    if "Spleenlab" not in scenario.affiliation:
        scenario.affiliation = "Spleenlab GmbH, " + scenario.affiliation
    scenario.source = "Disturbed version of original scenario " + original_scenario_id

    # TODO solve scenario_id differently, as just appending "_sut" does not comply with
    # the workings of CR's ScenarioID class.
    # Probably I should use `prediction_id`: enumerates different predictions for the same initial configuration (e.g. 1) and just increment it by 1??
    # Or by an int hash of the applied PEM??
    scenario.scenario_id.prediction_id = int_hash_of_pem_config(pem_config=pem_config)
    return scenario


def apply_pem_to_crime_config(crime_config: CriMeConfiguration, pem: PemConfig) -> None:
    scenario = crime_config.scenario

    ego_vehicle: DynamicObstacle = scenario.obstacle_by_id(crime_config.vehicle.ego_id)

    for perror in pem:
        apply_perror_to_scenario(scenario=scenario, perror=perror, ego_vehicle=ego_vehicle)

    refresh_dynamic_obstacles(scenario=scenario)


def apply_perror_to_scenario(scenario: Scenario, perror: Perror, ego_vehicle: DynamicObstacle) -> None:
    obstacles_to_modify: list[DynamicObstacle] = obtain_obstacles_to_modify(
        scenario=scenario, perror=perror, ego_vehicle=ego_vehicle
    )
    for obstacle in obstacles_to_modify:
        time_range_to_modify: list[int] = obtain_time_range_to_modify(perror=perror, obstacle=obstacle)

        for timestep in time_range_to_modify:
            ego_state: TraceState = ego_vehicle.state_at_time(time_step=timestep)
            obstacle_state: TraceState = obstacle.state_at_time(time_step=timestep)

            add_offset_long_lat(ego_state=ego_state, obstacle_state=obstacle_state, perror=perror)
            add_offset_range_azimuth(ego_state, obstacle_state=obstacle_state, perror=perror)


def obtain_time_range_to_modify(perror: Perror, obstacle: DynamicObstacle) -> list[int]:
    start_timestep: int = max(perror.start_timestep, obstacle.initial_state.time_step)

    if perror.end_timestep == -1:
        end_timestep = obstacle.prediction.final_time_step
    else:
        end_timestep = min(perror.end_timestep, obstacle.prediction.final_time_step)

    return list(range(start_timestep, end_timestep + 1))


def obtain_obstacles_to_modify(
    scenario: Scenario, perror: Perror, ego_vehicle: DynamicObstacle
) -> list[DynamicObstacle]:
    if perror.object_id == -1:
        obstacles_to_modify = []
        for dynamic_obstacle in scenario.dynamic_obstacles:
            if dynamic_obstacle.obstacle_id != ego_vehicle.obstacle_id:
                obstacles_to_modify.append(dynamic_obstacle)
    else:
        obstacles_to_modify = [scenario.obstacle_by_id(perror.object_id)]
    return obstacles_to_modify


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
    parser.add_argument("--workdir", type=str, help="Directory for reading and writing all files")
    parser.add_argument("--scenario_id", type=str, help="Original CommonRoad scenario ID")
    parser.add_argument("--pem_config", type=str, help="Path to PEM config json")

    args = parser.parse_args()

    sut_scenario_id: str = create_sut_crime_config_files(
        workdir=args.workdir,
        scenario_id=args.scenario_id,
        pem_config=args.pem_config,
    )
    print(f"Created files for new scenario ID {sut_scenario_id}")


if __name__ == "__main__":
    main()
