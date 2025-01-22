# import numpy as np
from copy import deepcopy

from commonroad.common.reader.file_reader_xml import DynamicObstacleFactory  #  type: ignore

# from commonroad.geometry.shape import Rectangle  # type: ignore
from commonroad.prediction.prediction import TrajectoryPrediction  # type: ignore
from commonroad.scenario.lanelet import LaneletNetwork  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import InitialState  # type: ignore

# from commonroad.scenario.trajectory import Trajectory  # type: ignore


def refresh_dynamic_obstacles(scenario: Scenario) -> Scenario:
    """Call this function after modifying obstacles' positions, orientations, and/or shape.
    It makes sure the scenario properties stay consistent. Especially:
    - assignments lanelet <-> obstacle
    - occupancy

    See also https://github.com/CommonRoad/commonroad-io/issues/12
    """

    assert_predictions_are_trajectories(scenario=scenario)
    clear_dynamic_obstacles_from_lanelets(lanelet_network=scenario.lanelet_network)

    for old_obstacle in scenario.dynamic_obstacles:
        exchange_by_fresh_obstacle(scenario=scenario, obstacle=old_obstacle)
    return scenario


def assert_predictions_are_trajectories(scenario: Scenario) -> None:
    for obstacle in scenario.dynamic_obstacles:
        if not isinstance(obstacle.prediction, TrajectoryPrediction):
            raise ValueError("Can only refresh TrajectoryPrediction")


def clear_dynamic_obstacles_from_lanelets(lanelet_network: LaneletNetwork) -> LaneletNetwork:
    for lanelet in lanelet_network.lanelets:
        lanelet.dynamic_obstacles_on_lanelet = {}
    return lanelet_network


def exchange_by_fresh_obstacle(scenario: Scenario, obstacle: DynamicObstacle) -> Scenario:
    new_obstacle = deepcopy(obstacle)
    scenario.remove_obstacle(obstacle)  # This also removes the obstacle from its old lanelets

    recompute_lanelet_assignments(obstacle=new_obstacle, lanelet_network=scenario.lanelet_network)
    scenario.add_objects(new_obstacle)  # This also adds the obstacle to its new lanelets
    recompute_occupancy_set(new_obstacle.prediction)


def recompute_occupancy_set(prediction: TrajectoryPrediction) -> TrajectoryPrediction:
    prediction._invalidate_occupancy_set()
    _ = prediction.occupancy_set  # recompute it
    return prediction


def recompute_lanelet_assignments(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    """
    Based on modified
    - obstacle.prediction.trajectory
    - obstacle.initial_state,
    recompute which lanelets their shapes and centers are on.

    See also https://github.com/CommonRoad/commonroad-io/blob/95511a554a9ed97fb9e3a88b6c1d1101839e2d49/commonroad/common/reader/file_reader_xml.py#L1254"""

    recompute_initial_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)
    recompute_prediction_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)
    return obstacle


def recompute_initial_lanelet_assignment(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    # We first need to recompute lanelet ids in the initial state,
    # and only then add the initial state to the lanelet network.
    recompute_lanelet_ids_in_initial_state(obstacle=obstacle, lanelet_network=lanelet_network)
    add_initial_state_to_lanelet_network(obstacle=obstacle, lanelet_network=lanelet_network)
    return obstacle


def recompute_lanelet_ids_in_initial_state(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork
) -> DynamicObstacle:
    """Based on `initial_state` and `obstacle_shape`, recompute `initial_{shape|center}_lanelet_ids`."""

    initial_state: InitialState = obstacle.initial_state
    rotated_shape = obstacle.obstacle_shape.rotate_translate_local(initial_state.position, initial_state.orientation)
    obstacle.initial_shape_lanelet_ids = set(lanelet_network.find_lanelet_by_shape(rotated_shape))
    obstacle.initial_center_lanelet_ids = set(lanelet_network.find_lanelet_by_position([initial_state.position])[0])


def add_initial_state_to_lanelet_network(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> LaneletNetwork:
    for l_id in obstacle.initial_shape_lanelet_ids:
        lanelet_network.find_lanelet_by_id(l_id).add_dynamic_obstacle_to_lanelet(
            obstacle_id=obstacle.obstacle_id, time_step=obstacle.initial_state.time_step
        )
    return lanelet_network


def recompute_prediction_lanelet_assignment(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork
) -> DynamicObstacle:
    """Based on `obstacle.prediction`, recompute `obstacle.prediction.{shape|center}_lanelet_assignment`."""

    prediction: TrajectoryPrediction = obstacle.prediction  # for better type hinting

    # Note that the following two functions also add the initial_state's lanelets to the
    # prediction's {shape|center}_lanelet_assignment.
    # If the intial state is one step earlier than prediction.trajectory.state_list[0],
    # its lanelets will be stored under a separate dict key.
    # If the intial state is at the same time step as prediction.trajectory.state_list[0],
    # then the following functions overwrite the initial_state's lanelets by the ones of
    # prediction.trajectory.state_list[0].
    # In general, the initial_state should be 1 time step before the prediction's first state:
    # https://github.com/CommonRoad/commonroad-io/issues/13

    # This seems a bit messy to me, but
    # apparently, this is how it works in commonroad. Most likely, it is safe to assume
    # that the initial_state is the prediction.trajectory.state_list[0] anyway.
    # In the scenario xml file, initial_state can be a time step earlier.

    # This also adds the shape lanelets to the lanelet network!
    prediction.shape_lanelet_assignment = DynamicObstacleFactory.find_obstacle_shape_lanelets(
        obstacle.initial_state,
        prediction.trajectory.state_list,
        lanelet_network,
        obstacle.obstacle_id,
        obstacle.obstacle_shape,
    )

    # This does *not* add the center lanelets to the lanelet network, most likely because they are
    # a subset of the shape lanelets anyway, which got added above already.
    prediction.center_lanelet_assignment = DynamicObstacleFactory.find_obstacle_center_lanelets(
        obstacle.initial_state, prediction.trajectory.state_list, lanelet_network
    )

    return obstacle
