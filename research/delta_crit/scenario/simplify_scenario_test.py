import sys
from math import isclose

import commonroad_crime.utility.visualization as utils_vis  # type: ignore
import pytest
from commonroad.geometry.shape import Rectangle  # type: ignore
from commonroad.prediction.prediction import Occupancy, TrajectoryPrediction  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import ExtendedPMState, InitialState  # type: ignore
from commonroad_crime.data_structure.configuration import CriMeConfiguration  # type: ignore

from research.delta_crit.scenario.simplify_scenario import simplify_scenario


def test_simplify_scenario_all_properties_match(example_config_garching: CriMeConfiguration) -> None:
    # Function under test
    ego_id: int = 200
    scenario: Scenario = simplify_scenario(scenario=example_config_garching.scenario, ego_id=ego_id)

    # Assertions
    ego_id = 200
    abs_tol: float = 1e-11
    for timestep in range(0, 22):
        for obs_id in [200, 201, 202, 203]:
            if timestep == 21:
                assert scenario.obstacle_by_id(obs_id).state_at_time(timestep) is None
                continue

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

    # Assertions differently formulated
    # TODO THIS IS INSANITY
    # WRITE ASSERTION UTILITIES TO SIMPLIFY IT
    seen_obstacle_ids = []
    for obstacle in scenario.dynamic_obstacles:
        seen_obstacle_ids.append(obstacle.obstacle_id)

        expected_east = 0 if obstacle.obstacle_id == ego_id else 10
        expected_north = 0
        expected_orientation = 0

        # Check initial state
        assert isclose(obstacle.initial_state.position[0], expected_east, abs_tol=abs_tol)
        assert isclose(obstacle.initial_state.position[1], expected_north, abs_tol=abs_tol)
        assert isclose(obstacle.initial_state.orientation, expected_orientation, abs_tol=abs_tol)

        obs_prediction: TrajectoryPrediction = obstacle.prediction

        # Check states of trajectory prediction
        seen_trajectory_state_timestamps = []
        for state in obs_prediction.trajectory.state_list:
            seen_trajectory_state_timestamps.append(state.time_step)
            assert isinstance(state, ExtendedPMState)
            assert isclose(state.position[0], expected_east, abs_tol=abs_tol)
            assert isclose(state.position[1], expected_north, abs_tol=abs_tol)
            assert isclose(state.orientation, expected_orientation, abs_tol=abs_tol)

        assert sorted(seen_trajectory_state_timestamps) == list(range(1, 21))

        # Check occupancies of trajectory prediction
        seen_occupancy_timestamps = []
        for occupancy in obs_prediction.occupancy_set:
            seen_occupancy_timestamps.append(occupancy.time_step)
            assert isinstance(occupancy.shape, Rectangle)
            assert occupancy.shape.center[0] == expected_east
            assert occupancy.shape.center[1] == expected_north
            assert occupancy.shape.orientation == expected_orientation
        assert sorted(seen_occupancy_timestamps) == list(range(1, 21))

        expected_lanelet_id: int = 47240
        expected_initial_lanelet_ids = set([expected_lanelet_id])
        # Check lanelet references in obstacle
        assert obstacle.initial_shape_lanelet_ids == expected_initial_lanelet_ids
        assert obstacle.initial_center_lanelet_ids == expected_initial_lanelet_ids

        # Check lanelet references in obstacle prediction
        # They also added the initial state's lanelet assignment, which is a bag, but not a tragic one,
        # so we tolerate it here.
        # See also https://github.com/CommonRoad/commonroad-io/issues/13#issuecomment-2607990143
        prediction_lanelet_assignment = {i: expected_initial_lanelet_ids for i in range(1, 21)}
        prediction_lanelet_assignment_their_bug = {i: expected_initial_lanelet_ids for i in range(0, 21)}
        assert (
            obs_prediction.shape_lanelet_assignment == prediction_lanelet_assignment
            or obs_prediction.shape_lanelet_assignment == prediction_lanelet_assignment_their_bug
        )
        assert (
            obs_prediction.center_lanelet_assignment == prediction_lanelet_assignment
            or obs_prediction.center_lanelet_assignment == prediction_lanelet_assignment_their_bug
        )

        # Other direction: check obstacle references in lanelets
        expected_object_ids_on_lanelet = set([200, 201, 202, 203])
        for time_step, ids in obs_prediction.shape_lanelet_assignment.items():
            for lanelet_id in ids:
                lanelet_dict = scenario.lanelet_network.find_lanelet_by_id(lanelet_id).dynamic_obstacles_on_lanelet
                assert lanelet_dict[time_step] == expected_object_ids_on_lanelet

    assert sorted(seen_obstacle_ids) == [200, 201, 202, 203]

    # Visual Insights
    utils_vis.visualize_scenario_at_time_steps(
        scenario,
        # plot_limit=example_config_garching.debug.plot_limits,
        plot_limit=[-40, 70, -30, 30],
        time_steps=[0, 20],
        print_obstacle_ids=True,
    )
    pass


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
