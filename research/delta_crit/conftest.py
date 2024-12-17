import pytest
from commonroad.scenario.scenario import Scenario  # type: ignore
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
