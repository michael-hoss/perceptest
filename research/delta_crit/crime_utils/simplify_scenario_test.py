import sys

# import commonroad_crime.utility.visualization as utils_vis  # type: ignore
import pytest
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad_crime.data_structure.configuration import CriMeConfiguration  # type: ignore

from research.delta_crit.crime_utils.assertion_utils import (
    assert_constant_obstacle,
    assert_obstacles_present,
)
from research.delta_crit.crime_utils.simplify_scenario import strip_down_to_test_scenario


def test_strip_down_scenario_all_properties_match(example_config_garching: CriMeConfiguration) -> None:
    # Function under test
    ego_id: int = 200
    scenario: Scenario = strip_down_to_test_scenario(scenario=example_config_garching.scenario, ego_id=ego_id)

    # Assertions
    ego_id = 200
    assert_obstacles_present(scenario=scenario, expected_obstacle_ids=[200, 201, 202, 203])
    for obstacle in scenario.dynamic_obstacles:
        assert_constant_obstacle(
            obstacle=obstacle,
            expected_east=0 if obstacle.obstacle_id == ego_id else 10,
            expected_north=0,
            expected_orientation=0,
            expected_initial_state_stamp=0,
            expected_final_time_stamp=20,
            expected_lanelet_ids=set([47240]),
            lanelet_network=scenario.lanelet_network,
        )

    # Visual Insights
    # utils_vis.visualize_scenario_at_time_steps(
    #     scenario,
    #     # plot_limit=example_config_garching.debug.plot_limits,
    #     plot_limit=[-40, 70, -30, 30],
    #     time_steps=[0, 20],
    #     print_obstacle_ids=True,
    # )
    # pass


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
