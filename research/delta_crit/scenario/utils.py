# import numpy as np
# from commonroad.geometry.shape import Rectangle  # type: ignore
# from commonroad.prediction.prediction import TrajectoryPrediction  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore

# from commonroad.scenario.state import ExtendedPMState, InitialState  # type: ignore
# from commonroad.scenario.trajectory import Trajectory  # type: ignore


def refresh_dynamic_obstacles(scenario: Scenario) -> Scenario:
    """Call this function after modifying object's positions or orientations.
    It makes sure the scenario properties stay consistent."""

    obstacle_ids: list[int] = [obs.obstacle_id for obs in scenario.dynamic_obstacles]

    for obstacle_id in obstacle_ids:
        previous_obstacle: DynamicObstacle = scenario.obstacle_by_id(obstacle_id)
        fresh_copy_of_obstacle: DynamicObstacle = refresh_dynamic_obstacle(previous_obstacle)
        scenario.remove_obstacle(previous_obstacle)
        scenario.add_objects(fresh_copy_of_obstacle)

    return scenario


def refresh_dynamic_obstacle(obstacle: DynamicObstacle) -> DynamicObstacle:
    """Maybe I just need to call obstacle.update_prediction()???"""

    # TODO GO ON HERE!
    obstacle.update_prediction()
    obstacle.update_initial_state()
    return obstacle

    # initial_time_step: int = obstacle.initial_state.time_step

    # ###
    # dynamic_obstacle_initial_state: InitialState = InitialState(
    #     time_step=initial_time_step,
    #     position=np.array([position_x, position_y]),
    #     velocity=velocity,
    #     orientation=orientation,
    # )

    # after_initial_state_list: list[ExtendedPMState] = []
    # for timestep in range(initial_time_step + 1, final_time_step + 1):
    #     state = ExtendedPMState(
    #         position=np.array([position_x, position_y]),
    #         velocity=velocity,
    #         orientation=orientation,
    #         time_step=timestep,
    #     )
    #     after_initial_state_list.append(state)

    # dynamic_obstacle_shape = Rectangle(width=width, length=length)

    # dynamic_obstacle_trajectory = Trajectory(initial_time_step + 1, after_initial_state_list)
    # dynamic_obstacle_prediction = TrajectoryPrediction(dynamic_obstacle_trajectory, dynamic_obstacle_shape)

    # ###
    # obstacle = DynamicObstacle(
    #     obstacle_id=obstacle.obstacle_id,
    #     obstacle_type=obstacle.obstacle_type,
    #     obstacle_shape=obstacle.obstacle_shape,
    #     initial_state=dynamic_obstacle_initial_state,
    #     prediction=dynamic_obstacle_prediction,
    #     initial_center_lanelet_ids=obstacle.initial_center_lanelet_ids,
    # )
    # return obstacle
