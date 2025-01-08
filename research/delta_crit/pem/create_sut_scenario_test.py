import os
import sys
import tempfile
from math import isclose

# import commonroad_crime.utility.visualization as utils_vis
import pytest

from research.delta_crit.crime_utils.crime_utils import (
    CriMeConfiguration,
)
from research.delta_crit.pem.create_sut_scenario import create_sut_scenario, create_sut_scenario_files
from research.delta_crit.pem.pem_config import PemConfig


def test_create_sut_scenario_straight_targets(
    example_pem_config: PemConfig, config_simplified_straight: CriMeConfiguration
) -> None:
    crime_config = config_simplified_straight
    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=example_pem_config)

    example_timestep = 10
    abs_tol = 1e-11
    assert isclose(sut_scenario.obstacle_by_id(201).state_at_time(example_timestep).position[0], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(201).state_at_time(example_timestep).position[1], 20, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(202).state_at_time(example_timestep).position[0], -30, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(202).state_at_time(example_timestep).position[1], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(203).state_at_time(example_timestep).position[0], 0, abs_tol=abs_tol)
    assert isclose(sut_scenario.obstacle_by_id(203).state_at_time(example_timestep).position[1], -25, abs_tol=abs_tol)

    # Visual Insights
    # utils_vis.visualize_scenario_at_time_steps(
    #     sut_scenario,
    #     plot_limit=crime_config.debug.plot_limits,
    #     time_steps=[10],
    #     print_obstacle_ids=True,
    # )
    # pass


def test_create_sut_scenario_side_targets(
    example_pem_config: PemConfig, config_simplified_side: CriMeConfiguration
) -> None:
    crime_config = config_simplified_side
    sut_scenario, sut_config = create_sut_scenario(crime_config=crime_config, pem_config=example_pem_config)

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


def test_create_sut_scenario_files(scenario_id_garching: str, example_pem_config_path: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define output paths
        sut_scenario_path: str = os.path.join(temp_dir, f"{scenario_id_garching}.xml")
        sut_crime_config_path: str = os.path.join(temp_dir, f"{scenario_id_garching}.yaml")

        # Function under test
        create_sut_scenario_files(
            scenario_id=scenario_id_garching,
            pem_config_path=example_pem_config_path,
            sut_scenario_path=sut_scenario_path,
            sut_crime_config_path=sut_crime_config_path,
        )

        # Assert files are present
        assert os.path.isfile(sut_scenario_path)
        assert os.path.isfile(sut_crime_config_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
