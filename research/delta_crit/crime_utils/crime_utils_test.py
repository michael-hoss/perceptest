import os
import sys
import tempfile
from typing import Union

import pytest
from commonroad.scenario.obstacle import DynamicObstacle, Obstacle, StaticObstacle  # type: ignore

from research.delta_crit.crime_utils.crime_utils import (  # type: ignore
    CriMeConfiguration,
    Scenario,
    get_crime_config,
    get_scenario,
    write_crime_config_shallow,
    write_scenario,
)


def test_get_crime_config_from_crime_examples_pass(scenario_id_garching) -> None:
    config: CriMeConfiguration = get_crime_config(scenario_id=scenario_id_garching)

    assert isinstance(config, CriMeConfiguration)
    assert config.time.braking_vel_threshold == 0.2
    assert isinstance(config.scenario, Scenario)
    assert "Michael Hoss" not in config.scenario.author


def test_get_crime_config_from_own_examples_pass(scenario_id_garching_sut) -> None:
    config: CriMeConfiguration = get_crime_config(scenario_id=scenario_id_garching_sut)

    assert isinstance(config, CriMeConfiguration)
    assert config.time.braking_vel_threshold == 0.2
    assert isinstance(config.scenario, Scenario)
    assert "Michael Hoss" in config.scenario.author


def test_get_scenario_from_crime_examples_pass(scenario_id_garching) -> None:
    scenario: Scenario = get_scenario(scenario_id=scenario_id_garching)

    assert isinstance(scenario, Scenario)
    obstacle: Union[Obstacle, DynamicObstacle, StaticObstacle, None] = scenario.obstacle_by_id(obstacle_id=200)
    assert isinstance(obstacle, DynamicObstacle)
    assert "Michael Hoss" not in scenario.author


def test_get_scenario_from_own_examples_pass(scenario_id_garching_sut) -> None:
    scenario: Scenario = get_scenario(scenario_id=scenario_id_garching_sut)

    assert isinstance(scenario, Scenario)
    obstacle: Union[Obstacle, DynamicObstacle, StaticObstacle, None] = scenario.obstacle_by_id(obstacle_id=200)
    assert isinstance(obstacle, DynamicObstacle)
    assert "Michael Hoss" in scenario.author


def test_write_scenario(scenario_id_garching: str) -> None:
    scenario: Scenario = get_scenario(scenario_id=scenario_id_garching)

    with tempfile.TemporaryDirectory() as temp_dir:
        output_filename = os.path.join(temp_dir, f"{scenario_id_garching}.xml")

        # function under test
        write_scenario(scenario=scenario, file_path=output_filename)

        # assertions
        assert os.path.isfile(path=output_filename)


def test_write_scenario_config(scenario_id_garching: str) -> None:
    scenario_config: Scenario = get_crime_config(scenario_id=scenario_id_garching)

    with tempfile.TemporaryDirectory() as temp_dir:
        output_filename = os.path.join(temp_dir, f"{scenario_id_garching}.yaml")

        # function under test
        write_crime_config_shallow(config=scenario_config, file_path=output_filename)

        # assertions
        assert os.path.isfile(path=output_filename)

        # test if written config is actually valid and can be loaded again
        written_config = CriMeConfiguration.load(output_filename, scenario_id_garching)
        written_config.update()

        # Unfortunately, there is no __eq__ method on CriMeConfiguration to assert that
        # written_config and scenario_config are the same.


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
