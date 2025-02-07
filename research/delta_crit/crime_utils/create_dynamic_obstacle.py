import numpy as np
from commonroad.geometry.shape import Rectangle  # type: ignore
from commonroad.prediction.prediction import TrajectoryPrediction  # type: ignore
from commonroad.scenario.obstacle import DynamicObstacle, ObstacleType  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import ExtendedPMState, InitialState  # type: ignore
from commonroad.scenario.trajectory import Trajectory  # type: ignore


def create_steady_dynamic_obstacle(
    obstacle_id: int,
    obstacle_type: ObstacleType = ObstacleType.CAR,
    position_x: float = 0,
    position_y: float = 0,
    velocity: float = 0,
    orientation: float = 0,
    initial_time_step: int = 0,
    final_time_step: int = 20,
    width: float = 1.8,
    length: float = 4.5,
) -> Scenario:
    """Inspired by official converters
    https://gitlab.lrz.de/tum-cps/dataset-converters/-/blob/master/src/highD/obstacle_utils.py?ref_type=heads#L48
    """

    dynamic_obstacle_initial_state: InitialState = InitialState(
        time_step=initial_time_step,
        position=np.array([position_x, position_y]),
        velocity=velocity,
        orientation=orientation,
    )

    after_initial_state_list: list[ExtendedPMState] = []
    for timestep in range(initial_time_step + 1, final_time_step + 1):
        state = ExtendedPMState(
            position=np.array([position_x, position_y]),
            velocity=velocity,
            orientation=orientation,
            time_step=timestep,
        )
        after_initial_state_list.append(state)

    dynamic_obstacle_shape = Rectangle(width=width, length=length)

    dynamic_obstacle_trajectory = Trajectory(initial_time_step + 1, after_initial_state_list)
    dynamic_obstacle_prediction = TrajectoryPrediction(dynamic_obstacle_trajectory, dynamic_obstacle_shape)

    return DynamicObstacle(
        obstacle_id=obstacle_id,
        obstacle_type=obstacle_type,
        obstacle_shape=dynamic_obstacle_shape,
        initial_state=dynamic_obstacle_initial_state,
        prediction=dynamic_obstacle_prediction,
    )
