from commonroad.prediction.prediction import TrajectoryPrediction  # type: ignore
from commonroad.scenario.lanelet import LaneletNetwork  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import InitialState  # type: ignore


def refresh_dynamic_obstacles(scenario: Scenario) -> Scenario:
    """
    Recomputes:
    - assignments lanelets <-> obstacle
    - occupancies
    based on positions, orientations, and shape.

    See also https://github.com/CommonRoad/commonroad-io/issues/12
    """

    assert_predictions_are_trajectories(scenario=scenario)

    for old_obstacle in scenario.dynamic_obstacles:
        refresh_dynamic_obstacle(scenario=scenario, obstacle=old_obstacle)
    return scenario


def assert_predictions_are_trajectories(scenario: Scenario) -> None:
    for obstacle in scenario.dynamic_obstacles:
        assert isinstance(obstacle.prediction, TrajectoryPrediction)


def clear_dynamic_obstacles_from_lanelets(lanelet_network: LaneletNetwork) -> LaneletNetwork:
    """Use with caution!
    Must be accompanied with setting the obstacle's references to lanelets to None.
    Otherwise, key errors occur in scenario._remove_dynamic_obstacle_from_lanelets()."""
    for lanelet in lanelet_network.lanelets:
        lanelet.dynamic_obstacles_on_lanelet = {}
    return lanelet_network


def refresh_dynamic_obstacle(scenario: Scenario, obstacle: DynamicObstacle) -> Scenario:
    """Remove obstacle by ID from scenario deeply; then re-add obstacle deeply."""

    # This also removes the obstacle from its old lanelets.
    # We can continue using the obstacle here after it is no longer part of the scenario.
    scenario.remove_obstacle(obstacle)

    add_obstacle_deeply(scenario=scenario, obstacle=obstacle)


def add_obstacle_deeply(scenario: Scenario, obstacle: DynamicObstacle) -> Scenario:
    recompute_lanelet_assignments(obstacle=obstacle, lanelet_network=scenario.lanelet_network)
    recompute_occupancies(obstacle=obstacle)
    scenario.add_objects(obstacle)  # This also adds the obstacle to its new lanelets


def recompute_occupancies(obstacle: DynamicObstacle) -> DynamicObstacle:
    assert isinstance(obstacle.prediction, TrajectoryPrediction)
    obstacle.prediction._invalidate_occupancy_set()
    _ = obstacle.prediction.occupancy_set  # recompute prediction's occupancy

    # Recompute initial state's occupancy
    obstacle.initial_state = obstacle.initial_state
    return obstacle


def recompute_lanelet_assignments(obstacle: DynamicObstacle, lanelet_network: LaneletNetwork) -> DynamicObstacle:
    """
    Recompute references in both directions (obstacle <-> lanelet_network).

    Both for prediction.trajectory and initial_state.

    Inspiration:
    - https://github.com/CommonRoad/commonroad-io/issues/12#issuecomment-2593494787
    - https://github.com/CommonRoad/commonroad-io/blob/95511a554a9ed97fb9e3a88b6c1d1101839e2d49/commonroad/common/reader/file_reader_xml.py#L1254
    """

    recompute_initial_state_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)
    recompute_prediction_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)
    return obstacle


def recompute_initial_state_lanelet_assignment(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork
) -> DynamicObstacle:
    """Based on `initial_state` and `obstacle_shape`, recompute `initial_{shape|center}_lanelet_ids`.
    Then, add the initial state to the lanelet network."""

    # Direction obstacle -> lanelets (needs to go first)
    recompute_lanelet_ids_in_initial_state(obstacle=obstacle, lanelet_network=lanelet_network)

    # Direction lanelets -> obstacle (needs to go last)
    add_initial_state_to_lanelet_network(obstacle=obstacle, lanelet_network=lanelet_network)
    return obstacle


def recompute_prediction_lanelet_assignment(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork
) -> DynamicObstacle:
    """Based on `obstacle.prediction`, recompute `obstacle.prediction.{shape|center}_lanelet_assignment`.
    Then, add the prediction to the lanelet network."""

    # Direction obstacle -> lanelets (needs to go first)
    recompute_shape_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)
    recompute_center_lanelet_assignment(obstacle=obstacle, lanelet_network=lanelet_network)

    # Direction lanelets -> obstacle (needs to go last)
    add_prediction_to_lanelet_network(obstacle=obstacle, lanelet_network=lanelet_network)
    return obstacle


def recompute_lanelet_ids_in_initial_state(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork
) -> DynamicObstacle:
    initial_state: InitialState = obstacle.initial_state
    rotated_shape = obstacle.obstacle_shape.rotate_translate_local(initial_state.position, initial_state.orientation)
    obstacle.initial_shape_lanelet_ids = set(lanelet_network.find_lanelet_by_shape(rotated_shape))
    obstacle.initial_center_lanelet_ids = set(lanelet_network.find_lanelet_by_position([initial_state.position])[0])


def add_initial_state_to_lanelet_network(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork, use_shape: bool = True
) -> LaneletNetwork:
    """Use shape lanelets by default because the shape covers more lanelets than just the center."""

    lanelet_ids = obstacle.initial_shape_lanelet_ids if use_shape else obstacle.initial_center_lanelet_ids
    assert lanelet_ids is not None, "Lanelet IDs must be computed first"

    for l_id in lanelet_ids:
        lanelet_network.find_lanelet_by_id(l_id).add_dynamic_obstacle_to_lanelet(
            obstacle_id=obstacle.obstacle_id, time_step=obstacle.initial_state.time_step
        )
    return lanelet_network


def recompute_shape_lanelet_assignment(
    obstacle: DynamicObstacle,
    lanelet_network: LaneletNetwork,
) -> None:
    """Of an obstacle's prediction"""

    assert isinstance(obstacle.prediction, TrajectoryPrediction)
    # Maps the state's time step to a set of lanelets
    lanelet_ids_per_state: dict[int, set[int]] = {}

    for state in obstacle.prediction.trajectory.state_list:
        rotated_shape = obstacle.obstacle_shape.rotate_translate_local(state.position, state.orientation)
        lanelet_ids = lanelet_network.find_lanelet_by_shape(rotated_shape)
        lanelet_ids_per_state[state.time_step] = set(lanelet_ids)
    obstacle.prediction.shape_lanelet_assignment = lanelet_ids_per_state


def recompute_center_lanelet_assignment(
    obstacle: DynamicObstacle,
    lanelet_network: LaneletNetwork,
) -> None:
    """Of an obstacle's prediction"""

    assert isinstance(obstacle.prediction, TrajectoryPrediction)
    # Maps the state's time step to a set of lanelets
    lanelet_ids_per_state: dict[int, set[int]] = {}

    for state in obstacle.prediction.trajectory.state_list:
        lanelet_ids = lanelet_network.find_lanelet_by_position([state.position])[0]
        lanelet_ids_per_state[state.time_step] = set(lanelet_ids)

    obstacle.prediction.center_lanelet_assignment = lanelet_ids_per_state


def add_prediction_to_lanelet_network(
    obstacle: DynamicObstacle, lanelet_network: LaneletNetwork, use_shape: bool = True
) -> LaneletNetwork:
    """Use shape lanelets by default because the shape covers more lanelets than just the center."""

    assert isinstance(obstacle.prediction, TrajectoryPrediction)
    if use_shape:
        lanelet_assignment = obstacle.prediction.shape_lanelet_assignment
    else:
        lanelet_assignment = obstacle.prediction.center_lanelet_assignment

    assert lanelet_assignment is not None, "Lanelet assignment must be computed first"
    for time_step, lanelet_ids in lanelet_assignment.items():
        for l_id in lanelet_ids:
            lanelet_network.find_lanelet_by_id(l_id).add_dynamic_obstacle_to_lanelet(
                obstacle_id=obstacle.obstacle_id, time_step=time_step
            )
    return lanelet_network
