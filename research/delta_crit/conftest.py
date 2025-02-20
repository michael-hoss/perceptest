import pytest
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad_crime.data_structure.configuration import CriMeConfiguration  # type: ignore

from research.delta_crit.crime_utils.crime_utils import get_crime_config, get_scenario
from research.delta_crit.crime_utils.simplify_scenario import strip_down_to_test_scenario


@pytest.fixture
def scenario_id_garching() -> str:
    return "DEU_Gar-1_1_T-1"


@pytest.fixture
def scenario_id_garching_sut() -> str:
    return "DEU_Gar-1_1_T-48977"


@pytest.fixture
def example_scenario_garching(scenario_id_garching: str) -> Scenario:
    return get_scenario(scenario_id=scenario_id_garching)


@pytest.fixture
def example_config_garching(scenario_id_garching: str) -> CriMeConfiguration:
    return get_crime_config(scenario_id=scenario_id_garching)


@pytest.fixture
def scenario_simplified_straight(example_scenario_garching: Scenario) -> Scenario:
    scenario = strip_down_to_test_scenario(example_scenario_garching, ego_id=200)
    return scenario


@pytest.fixture
def scenario_simplified_side(example_scenario_garching: Scenario) -> Scenario:
    scenario = strip_down_to_test_scenario(example_scenario_garching, ego_id=200, targets_east=0, targets_north=10)
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
