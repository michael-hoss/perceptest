import pytest
from commonroad.scenario.obstacle import DynamicObstacle  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.scenario.state import TraceState  # type: ignore
from commonroad_crime.data_structure.configuration import CriMeConfiguration  # type: ignore

from research.delta_crit.crime_utils.crime_utils import get_scenario, get_scenario_config


@pytest.fixture
def scenario_id_garching() -> str:
    return "DEU_Gar-1_1_T-1"


@pytest.fixture
def example_scenario_garching(scenario_id_garching: str) -> Scenario:
    return get_scenario(scenario_id=scenario_id_garching)


@pytest.fixture
def example_config_garching(scenario_id_garching: str) -> CriMeConfiguration:
    return get_scenario_config(scenario_id=scenario_id_garching)


def simplify_scenario(scenario: Scenario, ego_id: int, offset_east: float = 10, offset_north: float = 0) -> Scenario:
    # Modify ego state
    ego_obstacle: DynamicObstacle = scenario.obstacle_by_id(obstacle_id=ego_id)
    ego_obstacle.initial_state.orientation = 0.0
    ego_obstacle.initial_state.position[0] = 0
    ego_obstacle.initial_state.position[1] = 0

    for timestep in range(ego_obstacle.prediction.initial_time_step, ego_obstacle.prediction.final_time_step):
        ego_state: TraceState = ego_obstacle.state_at_time(time_step=timestep)
        ego_state.position = ego_obstacle.initial_state.position
        ego_state.orientation = ego_obstacle.initial_state.orientation

    # Modify other vehicles
    for dyn_obs in scenario.dynamic_obstacles:
        if dyn_obs.obstacle_id == ego_id:
            continue

        dyn_obs.initial_state.position[0] = ego_obstacle.initial_state.position[0] + offset_east
        dyn_obs.initial_state.position[1] = ego_obstacle.initial_state.position[1] + offset_north
        dyn_obs.initial_state.orientation = 0.0

        for timestep in range(dyn_obs.prediction.initial_time_step, dyn_obs.prediction.final_time_step):
            ego_state = ego_obstacle.state_at_time(time_step=timestep)
            obs_state: TraceState = dyn_obs.state_at_time(time_step=timestep)

            obs_state.position[0] = ego_state.position[0] + offset_east
            obs_state.position[1] = ego_state.position[1] + offset_north
            obs_state.orientation = 0.0

    return scenario


@pytest.fixture
def scenario_simplified_straight(example_scenario_garching: Scenario) -> Scenario:
    scenario = simplify_scenario(example_scenario_garching, ego_id=200)
    return scenario


@pytest.fixture
def scenario_simplified_side(example_scenario_garching: Scenario) -> Scenario:
    scenario = simplify_scenario(example_scenario_garching, ego_id=200, offset_east=0, offset_north=10)
    return scenario


@pytest.fixture
def config_simplified_straight(
    example_config_garching: CriMeConfiguration, scenario_simplified_straight: Scenario
) -> CriMeConfiguration:
    example_config_garching.scenario = scenario_simplified_straight
    example_config_garching.debug.plot_limits = [-40, 70, -30, 30]
    return example_config_garching


@pytest.fixture
def config_simplified_side(
    example_config_garching: CriMeConfiguration, scenario_simplified_side: Scenario
) -> CriMeConfiguration:
    example_config_garching.scenario = scenario_simplified_side
    example_config_garching.debug.plot_limits = [-40, 70, -30, 30]
    return example_config_garching
