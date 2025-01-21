# import numpy as np
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
    """Call this function after modifying object's positions or orientations.
    It makes sure the scenario properties stay consistent."""

    obstacle_ids: list[int] = [obs.obstacle_id for obs in scenario.dynamic_obstacles]

    for obstacle_id in obstacle_ids:
        previous_obstacle: DynamicObstacle = scenario.obstacle_by_id(obstacle_id)
        scenario.lanelet_network
        fresh_copy_of_obstacle: DynamicObstacle = refresh_dynamic_obstacle(
            obstacle=previous_obstacle, lanelet_network=scenario.lanelet_network
        )
        scenario.remove_obstacle(previous_obstacle)
        scenario.add_objects(fresh_copy_of_obstacle)

    return scenario


def refresh_dynamic_obstacle(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    """See https://github.com/CommonRoad/commonroad-io/issues/12"""

    # TODO update the following
    # TODO update initial state like this https://github.com/CommonRoad/commonroad-io/blob/95511a554a9ed97fb9e3a88b6c1d1101839e2d49/commonroad/scenario/obstacle.py#L675
    # TODO fill arguments
    if not isinstance(obstacle.prediction, TrajectoryPrediction):
        raise ValueError("Can only refresh TrajectoryPrediction")

    prediction: TrajectoryPrediction = obstacle.prediction
    prediction._invalidate_occupancy_set()
    prediction.occupancy_set  # recompute it

    # reset_initial_state(obstacle=obstacle, state=TODO)
    obstacle.initial_shape_lanelet_ids
    obstacle.initial_center_lanelet_ids

    # needs to be computed manually and updated via the corresponding setter
    # see also https://github.com/CommonRoad/commonroad-io/blob/95511a554a9ed97fb9e3a88b6c1d1101839e2d49/commonroad/common/reader/file_reader_xml.py#L1254
    obstacle.prediction.shape_lanelet_assignment
    obstacle.prediction.center_lanelet_assignment

    # TODO fill arguments
    obstacle.update_prediction()
    return obstacle


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


def recompute_lanelet_assignment(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    """Input: obstacle.prediction.trajectory

    See also https://github.com/CommonRoad/commonroad-io/blob/95511a554a9ed97fb9e3a88b6c1d1101839e2d49/commonroad/common/reader/file_reader_xml.py#L1254"""

    if not isinstance(obstacle.prediction, TrajectoryPrediction):
        raise ValueError("Can only recompute lanelet assignment for TrajectoryPrediction")
    prediction: TrajectoryPrediction = obstacle.prediction
    initial_state: InitialState = obstacle.initial_state

    # TODO: this might be buggy, take care.
    rotated_shape = obstacle.obstacle_shape.rotate_translate_local(initial_state.position, initial_state.orientation)
    obstacle.initial_shape_lanelet_ids = set(lanelet_network.find_lanelet_by_shape(rotated_shape))
    obstacle.initial_center_lanelet_ids = set(lanelet_network.find_lanelet_by_position([initial_state.position])[0])

    # TODO: clear all existing dynamic obstacles from the lanelets before adding the refreshed ones
    for l_id in obstacle.initial_shape_lanelet_ids:
        lanelet_network.find_lanelet_by_id(l_id).add_dynamic_obstacle_to_lanelet(
            obstacle_id=obstacle.obstacle_id, time_step=initial_state.time_step
        )

    prediction.shape_lanelet_assignment = DynamicObstacleFactory.find_obstacle_shape_lanelets(
        initial_state, prediction.trajectory.state_list, lanelet_network, obstacle.obstacle_id, obstacle.obstacle_shape
    )
    prediction.center_lanelet_assignment = DynamicObstacleFactory.find_obstacle_center_lanelets(
        initial_state, prediction.trajectory.state_list, lanelet_network
    )

    return obstacle
