import argparse
import math
from copy import deepcopy

from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.state import TraceState  # type: ignore

from research.delta_crit.crime_utils.crime_utils import (
    CriMeConfiguration,
    Scenario,
    get_scenario,
    get_scenario_config,
    write_scenario,
    write_scenario_config,
)
from research.delta_crit.pem.pem_config import PemConfig


def create_sut_scenario_files(
    scenario_id: str, pem_config_path: str, sut_scenario_path: str, sut_crime_config_path: str
) -> None:
    crime_config: CriMeConfiguration = get_scenario_config(scenario_id=scenario_id)
    original_scenario: Scenario = get_scenario(scenario_id=scenario_id)
    pem_config: PemConfig = PemConfig.from_json_file(json_path=pem_config_path)

    sut_scenario, sut_config = create_sut_scenario(
        original_scenario=original_scenario, crime_config=crime_config, pem_config=pem_config
    )

    write_scenario(scenario=sut_scenario, filename=sut_scenario_path)
    write_scenario_config(config=sut_config, filename=sut_crime_config_path)


def create_sut_scenario(
    original_scenario: Scenario, crime_config: CriMeConfiguration, pem_config: PemConfig
) -> tuple[Scenario, CriMeConfiguration]:
    sut_scenario = deepcopy(original_scenario)
    sut_config = deepcopy(crime_config)

    ego_vehicle: DynamicObstacle = sut_scenario._dynamic_obstacles[crime_config.vehicle.ego_id]

    obstacle: DynamicObstacle = sut_scenario._dynamic_obstacles[pem_config.object_id]
    for timestep in range(pem_config.start_timestep, pem_config.end_timestep):
        ego_orientation: float = ego_vehicle.state_at_time(time_step=timestep).orientation
        offset_long: float = pem_config.offset_longitudinal
        offset_lat: float = pem_config.offset_lateral
        offset_east = offset_long * math.cos(ego_orientation) + offset_lat * math.sin(ego_orientation)
        offset_north = offset_long * math.sin(ego_orientation) + offset_lat * math.cos(ego_orientation)

        obstacle_state: TraceState = obstacle.state_at_time(time_step=timestep)
        obstacle_state.position[0] += offset_east
        obstacle_state.position[1] += offset_north
    return sut_scenario, sut_config


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
