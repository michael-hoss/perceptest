import os
import sys
import tempfile

# import commonroad_crime.utility.visualization as utils_vis
import pytest

from research.delta_crit.crime_utils.crime_utils import (
    CriMeConfiguration,
)
from research.delta_crit.pem.create_sut_scenario import create_sut_scenario, create_sut_scenario_files
from research.delta_crit.pem.pem_config import PemConfig


def test_create_sut_scenario(example_pem_config: PemConfig, config_stripped: CriMeConfiguration) -> None:
    sut_scenario, sut_config = create_sut_scenario(crime_config=config_stripped, pem_config=example_pem_config)

    # Assertions
    # TODO semantic assertions that the chosen object actually has east and north coordinates moved
    # according to the PEM config specification.

    # Visual Insights
    # utils_vis.visualize_scenario_at_time_steps(
    #     sut_scenario,
    #     plot_limit=config_stripped.debug.plot_limits,
    #     time_steps=[10, 11],
    #     print_obstacle_ids=True,
    # )


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

        # Assert files are present
        assert os.path.isfile(sut_scenario_path)
        assert os.path.isfile(sut_crime_config_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
