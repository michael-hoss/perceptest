import os

import pytest

from research.delta_crit.pem.pem_config import PemConfig


@pytest.fixture
def example_pem_config_path() -> str:
    PERCEPTEST_ROOT = os.environ.get("PERCEPTEST_REPO")
    assert PERCEPTEST_ROOT
    file_path: str = os.path.join(PERCEPTEST_ROOT, "research/delta_crit/pem/example_config.json")
    return file_path


@pytest.fixture
def example_pem_config_json(example_pem_config_path: str) -> str:
    with open(example_pem_config_path, "r") as file:
        json_string = file.read()
    return json_string


@pytest.fixture
def example_pem_config(example_pem_config_path: str) -> PemConfig:
    return PemConfig.from_json_file(example_pem_config_path)
