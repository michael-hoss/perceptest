import sys
from math import isclose

import commonroad_crime.utility.visualization as utils_vis  # type: ignore
import pytest
from commonroad.geometry.shape import Rectangle  # type: ignore
from commonroad.prediction.prediction import Occupancy  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import ExtendedPMState, InitialState  # type: ignore
from commonroad_crime.data_structure.configuration import CriMeConfiguration  # type: ignore

from research.delta_crit.scenario.simplify_scenario import simplify_scenario


def test_simplify_scenario_all_properties_match(config_simplified_straight: CriMeConfiguration) -> None:
    # Function under test
    ego_id: int = 200
    scenario: Scenario = simplify_scenario(scenario=config_simplified_straight.scenario, ego_id=ego_id)

    # Assertions
    ego_id = 200
    abs_tol: float = 1e-11
    for timestep in range(0, 20):
        for obs_id in [200, 201, 202, 203]:
            expected_east: float = 0 if obs_id == ego_id else 10
            expected_north: float = 0
            expected_orientation: float = 0

            obstacle: DynamicObstacle = scenario.obstacle_by_id(obs_id)

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
        scenario,
        plot_limit=config_simplified_straight.debug.plot_limits,
        time_steps=[0, 20],
        print_obstacle_ids=True,
    )
    pass


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
