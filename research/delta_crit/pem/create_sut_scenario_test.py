import os
import sys
import tempfile

import pytest
from commonroad.scenario.scenario import Scenario  # type: ignore

from research.delta_crit.crime_utils.crime_utils import CriMeConfiguration
from research.delta_crit.pem.create_sut_scenario import create_sut_scenario, create_sut_scenario_files
from research.delta_crit.pem.pem_config import PemConfig


def test_create_sut_scenario(
    example_pem_config: PemConfig, example_scenario_garching: Scenario, example_config_garching: CriMeConfiguration
) -> None:
    sut_scenario, sut_config = create_sut_scenario(
        original_scenario=example_scenario_garching, crime_config=example_config_garching, pem_config=example_pem_config
    )

    # Assertions
    # TODO semantic assertions that the chosen object actually has x and y coordinates moved according to the PEM config specification
    assert False


def test_create_sut_scenario_files(scenario_id_garching: str, example_pem_config_path: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define output paths
        sut_scenario_path: str = os.path.join(temp_dir, f"{scenario_id_garching}.xml")
        sut_crime_config_path: str = os.path.join(temp_dir, f"{scenario_id_garching}.yaml")

        # Function under test
        create_sut_scenario_files(
            scenario_id=scenario_id_garching,
            pem_config_path=example_pem_config_path,
            sut_scenario_path=sut_scenario_path,
            sut_crime_config_path=sut_crime_config_path,
        )

        # Assertions
        # TODO just assert the file IO. The semantics are asserted in the other test.
        assert False


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
