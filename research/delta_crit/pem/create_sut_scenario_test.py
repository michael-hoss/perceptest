import os
import sys
from math import isclose

# import commonroad_crime.utility.visualization as utils_vis
import pytest
from commonroad.scenario.state import ExtendedPMState, InitialState  # type: ignore

from research.delta_crit.crime_utils.assertion_utils import (
    assert_constant_obstacle,
    assert_obstacles_present,
)
from research.delta_crit.crime_utils.crime_utils import CriMeConfiguration
from research.delta_crit.pem.create_sut_scenario import create_sut_crime_config, create_sut_crime_config_files
from research.delta_crit.pem.pem_config import PemConfig
from research.delta_crit.pipeline_utils.dir_utils import set_up_populated_workdir


def test_create_sut_scenario_apply_to_all_objects(
    all_objects_pem_config: PemConfig, config_simplified_straight: CriMeConfiguration
) -> None:
    crime_config = config_simplified_straight
    sut_config = create_sut_crime_config(crime_config=crime_config, pem_config=all_objects_pem_config)
    sut_scenario = sut_config.scenario
    # Visual Insights
    # utils_vis.visualize_scenario_at_time_steps(
    #     sut_scenario,
    #     plot_limit=crime_config.debug.plot_limits,
    #     time_steps=[0],
    #     print_obstacle_ids=True,
    #     print_lanelet_ids=True,
    # )

    # Assertions
    ego_id = 200
    assert_obstacles_present(scenario=sut_scenario, expected_obstacle_ids=[200, 201, 202, 203])
    for obstacle in sut_scenario.dynamic_obstacles:
        assert_constant_obstacle(
            obstacle=obstacle,
            expected_east=0 if obstacle.obstacle_id == ego_id else -20,
            expected_north=0,
            expected_orientation=0,
            expected_initial_state_stamp=0,
            expected_final_time_stamp=20,
            expected_lanelet_ids=set([47240]),
            lanelet_network=sut_scenario.lanelet_network,
        )


def test_create_sut_scenario_multiple_timesteps(
    temporal_pem_config: PemConfig, config_simplified_straight: CriMeConfiguration
) -> None:
    crime_config = config_simplified_straight
    sut_config = create_sut_crime_config(crime_config=crime_config, pem_config=temporal_pem_config)
    sut_scenario = sut_config.scenario

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
    sut_config = create_sut_crime_config(crime_config=crime_config, pem_config=geometrical_pem_config)
    sut_scenario = sut_config.scenario

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
    sut_config = create_sut_crime_config(crime_config=crime_config, pem_config=geometrical_pem_config)
    sut_scenario = sut_config.scenario

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
    sut_config = create_sut_crime_config(crime_config=crime_config, pem_config=geometrical_pem_config)
    sut_scenario = sut_config.scenario

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
    workdir: str = set_up_populated_workdir(example_scenario_id=scenario_id_garching)

    # Function under test
    sut_scenario_id: str = create_sut_crime_config_files(
        workdir=workdir,
        scenario_id=scenario_id_garching,
        pem_config=geometrical_pem_config_path,
    )

    expected_scenario_path: str = os.path.join(workdir, f"{sut_scenario_id}.xml")
    expected_crime_config_path: str = os.path.join(workdir, f"{sut_scenario_id}.yaml")

    # Assert files are present
    assert os.path.isfile(expected_scenario_path)
    assert os.path.isfile(expected_crime_config_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
