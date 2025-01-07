import os
import sys
import tempfile
from typing import Union

import pytest
from commonroad.scenario.obstacle import DynamicObstacle, Obstacle, StaticObstacle  # type: ignore

from research.delta_crit.crime_utils.crime_utils import (  # type: ignore
    CriMeConfiguration,
    Scenario,
    get_scenario,
    get_scenario_config,
    write_scenario,
    write_scenario_config,
)


def test_get_scenario_config(scenario_id_garching) -> None:
    config: CriMeConfiguration = get_scenario_config(scenario_id=scenario_id_garching)

    assert isinstance(config, CriMeConfiguration)
    assert config.time.braking_vel_threshold == 0.2
    assert isinstance(config.scenario, Scenario)


def test_get_scenario(scenario_id_garching) -> None:
    scenario: Scenario = get_scenario(scenario_id=scenario_id_garching)

    assert isinstance(scenario, Scenario)
    obstacle: Union[Obstacle, DynamicObstacle, StaticObstacle, None] = scenario.obstacle_by_id(obstacle_id=200)
    assert isinstance(obstacle, DynamicObstacle)


def test_write_scenario(scenario_id_garching: str) -> None:
    scenario: Scenario = get_scenario(scenario_id=scenario_id_garching)

    with tempfile.TemporaryDirectory() as temp_dir:
        output_filename = os.path.join(temp_dir, f"{scenario_id_garching}.xml")

        # function under test
        write_scenario(scenario=scenario, filename=output_filename)

        # assertions
        assert os.path.isfile(path=output_filename)


def test_write_scenario_config(scenario_id_garching: str) -> None:
    scenario_config: Scenario = get_scenario_config(scenario_id=scenario_id_garching)

    with tempfile.TemporaryDirectory() as temp_dir:
        output_filename = os.path.join(temp_dir, f"{scenario_id_garching}.yaml")

        # function under test
        write_scenario_config(config=scenario_config, filename=output_filename)

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
