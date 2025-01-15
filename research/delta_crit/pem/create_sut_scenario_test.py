import os
import sys
import tempfile
from math import isclose

import commonroad_crime.utility.visualization as utils_vis
import pytest
from commonroad.geometry.shape import Rectangle  # type: ignore
from commonroad.prediction.prediction import Occupancy  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.state import ExtendedPMState, InitialState  # type: ignore

from research.delta_crit.crime_utils.crime_utils import (
    CriMeConfiguration,
)
from research.delta_crit.pem.create_sut_scenario import create_sut_scenario, create_sut_scenario_files
from research.delta_crit.pem.pem_config import PemConfig


def test_create_sut_scenario_apply_to_all_objects(
    all_objects_pem_config: PemConfig, config_simplified_straight: CriMeConfiguration
) -> None:
    crime_config = config_simplified_straight
    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=all_objects_pem_config)

    # Assertions
    ego_id = 200
    abs_tol: float = 1e-11
    for timestep in range(0, 22):
        for obs_id in [200, 201, 202, 203]:
            if timestep == 21:
                assert sut_scenario.obstacle_by_id(obs_id).state_at_time(timestep) is None
                continue

            expected_east: float = 0 if obs_id == ego_id else -20
            expected_north: float = 0
            expected_orientation: float = 0

            obstacle: DynamicObstacle = sut_scenario.obstacle_by_id(obs_id)

            obstacle_state = obstacle.state_at_time(timestep)
            assert isinstance(obstacle_state, InitialState if timestep == 0 else ExtendedPMState)

            assert isclose(obstacle_state.position[0], expected_east, abs_tol=abs_tol)
            assert isclose(obstacle_state.position[1], expected_north, abs_tol=abs_tol)
            assert isclose(obstacle_state.orientation, expected_orientation, abs_tol=abs_tol)

            obstacle_occupancy: Occupancy = obstacle.occupancy_at_time(timestep)
            assert isinstance(obstacle_occupancy.shape, Rectangle)
            assert obstacle_occupancy.shape.center[0] == expected_east
            assert obstacle_occupancy.shape.center[1] == expected_north
            assert obstacle_occupancy.shape.orientation == expected_orientation

    # Visual Insights
    utils_vis.visualize_scenario_at_time_steps(
        sut_scenario,
        plot_limit=crime_config.debug.plot_limits,
        time_steps=[0, 1, 2, 3, 18, 19, 20],
        print_obstacle_ids=True,
    )
    pass


def test_create_sut_scenario_multiple_timesteps(
    temporal_pem_config: PemConfig, config_simplified_straight: CriMeConfiguration
) -> None:
    crime_config = config_simplified_straight
    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=temporal_pem_config)

    expected_east_modified: float = 20
    expected_east_original: float = 10
    for timestep in range(0, 20):
        sut_scenario.obstacle_by_id(201).state_at_time(timestep).position[0] == expected_east_modified

        if timestep == 0:
            sut_scenario.obstacle_by_id(202).state_at_time(timestep).position[0] == expected_east_original
            sut_scenario.obstacle_by_id(203).state_at_time(timestep).position[0] == expected_east_original
        else:
            sut_scenario.obstacle_by_id(202).state_at_time(timestep).position[0] == expected_east_modified
            sut_scenario.obstacle_by_id(203).state_at_time(timestep).position[0] == expected_east_modified

    assert sut_scenario.obstacle_by_id(203).state_at_time(21) is None

    # Visual Insights
    # utils_vis.visualize_scenario_at_time_steps(
    #     sut_scenario,
    #     plot_limit=crime_config.debug.plot_limits,
    #     time_steps=[0, 1, 2, 3, 18, 19, 20],
    #     print_obstacle_ids=True,
    # )
    # pass


def test_create_sut_scenario_keep_rest_constant(
    geometrical_pem_config: PemConfig, config_simplified_straight: CriMeConfiguration
) -> None:
    crime_config = config_simplified_straight
    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=geometrical_pem_config)

    modified_timestep: int = 10
    ego_id: int = 200
    abs_tol: float = 1e-11
    for timestep in range(0, 20):
        for obstacle_id in [200, 201, 202, 203]:
            if obstacle_id == ego_id or timestep != modified_timestep:
                original_state = crime_config.scenario.obstacle_by_id(obstacle_id).state_at_time(timestep)
                assert isclose(original_state.position[0], 0 if obstacle_id == ego_id else 10, abs_tol=abs_tol)
                assert isclose(original_state.position[1], 0, abs_tol=abs_tol)
                assert isclose(original_state.orientation, 0, abs_tol=abs_tol)

                actual_state = sut_scenario.obstacle_by_id(obstacle_id).state_at_time(timestep)
                assert actual_state == original_state

                if timestep == 0:
                    assert isinstance(original_state, InitialState)
                    assert isinstance(actual_state, InitialState)
                else:
                    assert isinstance(original_state, ExtendedPMState)
                    assert isinstance(actual_state, ExtendedPMState)


def test_create_sut_scenario_straight_targets(
    geometrical_pem_config: PemConfig, config_simplified_straight: CriMeConfiguration
) -> None:
    crime_config = config_simplified_straight
    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=geometrical_pem_config)

    modified_timestep = 10
    abs_tol = 1e-11
    assert isclose(sut_scenario.obstacle_by_id(201).state_at_time(modified_timestep).position[0], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(201).state_at_time(modified_timestep).position[1], 20, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(202).state_at_time(modified_timestep).position[0], -30, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(202).state_at_time(modified_timestep).position[1], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(203).state_at_time(modified_timestep).position[0], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(203).state_at_time(modified_timestep).position[1], -25, abs_tol=abs_tol)

    # Visual Insights
    # utils_vis.visualize_scenario_at_time_steps(
    #     sut_scenario,
    #     plot_limit=crime_config.debug.plot_limits,
    #     time_steps=[10],
    #     print_obstacle_ids=True,
    # )
    # pass


def test_create_sut_scenario_side_targets(
    geometrical_pem_config: PemConfig, config_simplified_side: CriMeConfiguration
) -> None:
    crime_config = config_simplified_side
    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=geometrical_pem_config)

    example_timestep = 10
    abs_tol = 1e-11
    assert isclose(sut_scenario.obstacle_by_id(201).state_at_time(example_timestep).position[0], -20, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(201).state_at_time(example_timestep).position[1], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(202).state_at_time(example_timestep).position[0], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(202).state_at_time(example_timestep).position[1], -30, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(203).state_at_time(example_timestep).position[0], 25, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(203).state_at_time(example_timestep).position[1], 0, abs_tol=abs_tol)

    # Visual Insights
    # utils_vis.visualize_scenario_at_time_steps(
    #     sut_scenario,
    #     plot_limit=crime_config.debug.plot_limits,
    #     time_steps=[10],
    #     print_obstacle_ids=True,
    # )
    # pass


def test_create_sut_scenario_files(scenario_id_garching: str, geometrical_pem_config_path: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define output paths
        sut_scenario_path: str = os.path.join(temp_dir, f"{scenario_id_garching}.xml")
        sut_crime_config_path: str = os.path.join(temp_dir, f"{scenario_id_garching}.yaml")

        # Function under test
        create_sut_scenario_files(
            scenario_id=scenario_id_garching,
            pem_config_path=geometrical_pem_config_path,
            sut_scenario_path=sut_scenario_path,
            sut_crime_config_path=sut_crime_config_path,
        )

        # Assert files are present
        assert os.path.isfile(sut_scenario_path)
        assert os.path.isfile(sut_crime_config_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
