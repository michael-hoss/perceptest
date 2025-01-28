import json
import os

import pytest

from research.delta_crit.crime_utils.crime_utils import get_pem_configs_dir
from research.delta_crit.pem.pem_config import PemConfig, pem_config_from_json


@pytest.fixture
def geometrical_pem_config_path() -> str:
    return os.path.join(get_pem_configs_dir(), "geometrical.json")


@pytest.fixture
def geometrical_pem_config_json(geometrical_pem_config_path: str) -> str:
    with open(geometrical_pem_config_path, "r") as file:
        json_string = file.read()
    return json_string


@pytest.fixture
def geometrical_pem_config_list_of_dicts(geometrical_pem_config_path: str) -> list[dict]:
    with open(geometrical_pem_config_path, "r") as file:
        json_string = file.read()
        my_list: list[dict] = json.loads(json_string)
    return my_list


@pytest.fixture
def geometrical_pem_config(geometrical_pem_config_path: str) -> PemConfig:
    return pem_config_from_json(geometrical_pem_config_path)


@pytest.fixture
def temporal_pem_config_path() -> str:
    return os.path.join(get_pem_configs_dir(), "temporal.json")


@pytest.fixture
def temporal_pem_config(temporal_pem_config_path: str) -> PemConfig:
    return pem_config_from_json(temporal_pem_config_path)


@pytest.fixture
def all_objects_pem_config_path() -> str:
    return os.path.join(get_pem_configs_dir(), "all_objects.json")


@pytest.fixture
def all_objects_pem_config(all_objects_pem_config_path: str) -> PemConfig:
    return pem_config_from_json(all_objects_pem_config_path)
