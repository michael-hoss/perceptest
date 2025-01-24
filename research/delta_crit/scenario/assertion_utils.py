from math import isclose

from commonroad.geometry.shape import Rectangle  # type: ignore
from commonroad.prediction.prediction import Occupancy, TrajectoryPrediction  # type: ignore
from commonroad.scenario.lanelet import LaneletNetwork  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import ExtendedPMState  # type: ignore


def assert_obstacles_present(scenario: Scenario, expected_obstacle_ids: list[int], allow_subset: bool = False) -> None:
    seen_obstacle_ids = []
    for obstacle in scenario.dynamic_obstacles:
        seen_obstacle_ids.append(obstacle.obstacle_id)

    if not allow_subset:
        assert sorted(seen_obstacle_ids) == sorted(expected_obstacle_ids)
    else:
        assert set(seen_obstacle_ids) in set(expected_obstacle_ids)


def assert_constant_obstacle_properties(
    obstacle: DynamicObstacle,
    expected_east: float,
    expected_north: float,
    expected_orientation: float,
    expected_initial_state_stamp: int,
    expected_final_time_stamp: int,
    abs_tol: float = 1e-11,
) -> None:
    # Check initial state
    assert isclose(obstacle.initial_state.position[0], expected_east, abs_tol=abs_tol)
    assert isclose(obstacle.initial_state.position[1], expected_north, abs_tol=abs_tol)
    assert isclose(obstacle.initial_state.orientation, expected_orientation, abs_tol=abs_tol)

    # Check initial occupancy
    initial_occupancy: Occupancy = obstacle.occupancy_at_time(obstacle.initial_state.time_step)
    assert isinstance(initial_occupancy.shape, Rectangle)
    assert initial_occupancy.shape.center[0] == expected_east
    assert initial_occupancy.shape.center[1] == expected_north
    assert initial_occupancy.shape.orientation == expected_orientation

    obs_prediction: TrajectoryPrediction = obstacle.prediction

    # Check states of trajectory prediction
    seen_trajectory_state_timestamps = []
    for state in obs_prediction.trajectory.state_list:
        seen_trajectory_state_timestamps.append(state.time_step)
        assert isinstance(state, ExtendedPMState)
        assert isclose(state.position[0], expected_east, abs_tol=abs_tol)
        assert isclose(state.position[1], expected_north, abs_tol=abs_tol)
        assert isclose(state.orientation, expected_orientation, abs_tol=abs_tol)

    # Check occupancies of trajectory prediction
    seen_occupancy_timestamps = []
    for occupancy in obs_prediction.occupancy_set:
        seen_occupancy_timestamps.append(occupancy.time_step)
        assert isinstance(occupancy.shape, Rectangle)
        assert occupancy.shape.center[0] == expected_east
        assert occupancy.shape.center[1] == expected_north
        assert occupancy.shape.orientation == expected_orientation

    # Check timing consistency
    assert obstacle.initial_state.time_step == expected_initial_state_stamp
    assert obs_prediction.initial_time_step == expected_initial_state_stamp + 1
    expected_trajectory_time_stamps = list(range(expected_initial_state_stamp + 1, expected_final_time_stamp + 1))
    assert sorted(seen_trajectory_state_timestamps) == expected_trajectory_time_stamps
    assert sorted(seen_occupancy_timestamps) == expected_trajectory_time_stamps


def assert_constant_lanelet_refs_in_obstacle(obstacle: DynamicObstacle, expected_lanelet_ids: set) -> None:
    """Assumes shape lanelets and center lanelets are the same and constant over time."""

    obs_prediction: TrajectoryPrediction = obstacle.prediction

    # Check lanelet references in obstacle (initial state)
    assert obstacle.initial_shape_lanelet_ids == expected_lanelet_ids
    assert obstacle.initial_center_lanelet_ids == expected_lanelet_ids

    # Check lanelet references in obstacle prediction
    expected_prediction_lanelet_assignment = {
        i: expected_lanelet_ids for i in range(obs_prediction.initial_time_step, obs_prediction.final_time_step + 1)
    }
    assert obs_prediction.shape_lanelet_assignment == expected_prediction_lanelet_assignment
    assert obs_prediction.center_lanelet_assignment == expected_prediction_lanelet_assignment


def assert_obstacle_referenced_by_lanelet_network(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> None:
    obs_prediction: TrajectoryPrediction = obstacle.prediction

    for time_step, lanelet_ids in obs_prediction.shape_lanelet_assignment.items():
        for lanelet_id in lanelet_ids:
            lanelet_dict = lanelet_network.find_lanelet_by_id(lanelet_id).dynamic_obstacles_on_lanelet
            assert obstacle.obstacle_id in lanelet_dict[time_step]

    for time_step, lanelet_ids in obs_prediction.center_lanelet_assignment.items():
        for lanelet_id in lanelet_ids:
            lanelet_dict = lanelet_network.find_lanelet_by_id(lanelet_id).dynamic_obstacles_on_lanelet
            assert obstacle.obstacle_id in lanelet_dict[time_step]


def assert_constant_obstacle(
    obstacle: DynamicObstacle,
    expected_east: float,
    expected_north: float,
    expected_orientation: float,
    expected_initial_state_stamp: int,
    expected_final_time_stamp: int,
    expected_lanelet_ids: set,
    lanelet_network: LaneletNetwork,
    abs_tol: float = 1e-11,
) -> None:
    assert_constant_obstacle_properties(
        obstacle=obstacle,
        expected_east=expected_east,
        expected_north=expected_north,
        expected_orientation=expected_orientation,
        expected_initial_state_stamp=expected_initial_state_stamp,
        expected_final_time_stamp=expected_final_time_stamp,
        abs_tol=abs_tol,
    )

    assert_constant_lanelet_refs_in_obstacle(obstacle=obstacle, expected_lanelet_ids=expected_lanelet_ids)
    assert_obstacle_referenced_by_lanelet_network(obstacle=obstacle, lanelet_network=lanelet_network)
