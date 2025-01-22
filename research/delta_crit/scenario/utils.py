# import numpy as np
from copy import deepcopy
from typing import Optional

from commonroad.common.reader.file_reader_xml import DynamicObstacleFactory  #  type: ignore

# from commonroad.geometry.shape import Rectangle  # type: ignore
from commonroad.prediction.prediction import TrajectoryPrediction  # type: ignore
from commonroad.scenario.lanelet import LaneletNetwork  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import InitialState, SignalState, TraceState  # type: ignore

# from commonroad.scenario.trajectory import Trajectory  # type: ignore


def refresh_dynamic_obstacles(scenario: Scenario) -> Scenario:
    """Call this function after modifying objects' positions or orientations.
    It makes sure the scenario properties stay consistent."""

    obstacle_ids: list[int] = [obs.obstacle_id for obs in scenario.dynamic_obstacles]

    clear_dynamic_obstacles_from_lanelets(lanelet_network=scenario.lanelet_network)

    for obstacle_id in obstacle_ids:
        old_obstacle: DynamicObstacle = scenario.obstacle_by_id(obstacle_id)
        new_obstacle = deepcopy(old_obstacle)
        scenario.remove_obstacle(old_obstacle)
        refresh_dynamic_obstacle(obstacle=old_obstacle, lanelet_network=scenario.lanelet_network)
        scenario.add_objects(new_obstacle)

    return scenario


def clear_dynamic_obstacles_from_lanelets(lanelet_network: LaneletNetwork) -> LaneletNetwork:
    for lanelet in lanelet_network.lanelets:
        lanelet.dynamic_obstacles_on_lanelet = {}
    return lanelet_network


def refresh_dynamic_obstacle(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    """See https://github.com/CommonRoad/commonroad-io/issues/12"""

    if not isinstance(obstacle.prediction, TrajectoryPrediction):
        raise ValueError("Can only refresh TrajectoryPrediction")

    recompute_lanelet_assignments(obstacle=obstacle, lanelet_network=lanelet_network)
    recompute_occupancy_set(obstacle.prediction)

    return obstacle


def recompute_occupancy_set(prediction: TrajectoryPrediction) -> TrajectoryPrediction:
    prediction._invalidate_occupancy_set()
    _ = prediction.occupancy_set  # recompute it
    return prediction


def reset_initial_state(
    obstacle: DynamicObstacle,
    state: TraceState,
    signal_state: Optional[SignalState] = None,
) -> DynamicObstacle:
    """Modification of official `update_initial_state`.
    Here, without doing a time step. No history gets appended and no prediction gets invalidated.
    Also without recomputing lanelet assignments, as this is done elsewhere."""
    obstacle.initial_state = state
    obstacle.initial_signal_state = signal_state
    return obstacle


def recompute_lanelet_assignments(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    """
    Based on modified
    - obstacle.prediction.trajectory
    - obstacle.initial_state,
    recompute which lanelets their shapes and centers are on.

    Adds the new obstacle information to the lanelets, but does not delete the old one.

    See also https://github.com/CommonRoad/commonroad-io/blob/95511a554a9ed97fb9e3a88b6c1d1101839e2d49/commonroad/common/reader/file_reader_xml.py#L1254"""

    recompute_initial_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)
    recompute_prediction_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)
    return obstacle


def recompute_initial_lanelet_assignment(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    initial_state: InitialState = obstacle.initial_state

    # Recompute initial lanelet ids
    # TODO: this might be buggy, take care.
    rotated_shape = obstacle.obstacle_shape.rotate_translate_local(initial_state.position, initial_state.orientation)
    obstacle.initial_shape_lanelet_ids = set(lanelet_network.find_lanelet_by_shape(rotated_shape))
    obstacle.initial_center_lanelet_ids = set(lanelet_network.find_lanelet_by_position([initial_state.position])[0])

    # Add initial state to these newly-computed lanelet ids
    add_initial_state_to_its_lanelets(obstacle=obstacle, lanelet_network=lanelet_network)
    return obstacle


def add_initial_state_to_its_lanelets(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> LaneletNetwork:
    """Adds, but does not delete any existing states from the lanelets."""
    for l_id in obstacle.initial_shape_lanelet_ids:
        lanelet_network.find_lanelet_by_id(l_id).add_dynamic_obstacle_to_lanelet(
            obstacle_id=obstacle.obstacle_id, time_step=obstacle.initial_state.time_step
        )
    return lanelet_network


def recompute_prediction_lanelet_assignment(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork
) -> DynamicObstacle:
    # Input checks and syntactic sugar
    if not isinstance(obstacle.prediction, TrajectoryPrediction):
        raise ValueError("Can only recompute lanelet assignment for TrajectoryPrediction")
    prediction: TrajectoryPrediction = obstacle.prediction
    initial_state: InitialState = obstacle.initial_state

    # Actual recomputation
    prediction.shape_lanelet_assignment = DynamicObstacleFactory.find_obstacle_shape_lanelets(
        initial_state, prediction.trajectory.state_list, lanelet_network, obstacle.obstacle_id, obstacle.obstacle_shape
    )
    prediction.center_lanelet_assignment = DynamicObstacleFactory.find_obstacle_center_lanelets(
        initial_state, prediction.trajectory.state_list, lanelet_network
    )
    return obstacle
