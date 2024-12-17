import argparse
from copy import deepcopy

from research.delta_crit.crime_utils.crime_utils import (
    CriMeConfiguration,
    Scenario,
    get_scenario,
    get_scenario_config,
    write_scenario,
    write_scenario_config,
)
from research.delta_crit.pem.pem_config import PemConfig


def create_sut_scenario_files(
    scenario_id: str, pem_config_path: str, sut_scenario_path: str, sut_crime_config_path: str
) -> None:
    crime_config: CriMeConfiguration = get_scenario_config(scenario_id=scenario_id)
    original_scenario: Scenario = get_scenario(scenario_id=scenario_id)
    pem_config: PemConfig = PemConfig.from_json_file(json_path=pem_config_path)

    sut_scenario, sut_config = create_sut_scenario(
        original_scenario=original_scenario, crime_config=crime_config, pem_config=pem_config
    )

    write_scenario(scenario=sut_scenario, filename=sut_scenario_path)
    write_scenario_config(config=sut_config, filename=sut_crime_config_path)


def create_sut_scenario(
    original_scenario: Scenario, crime_config: CriMeConfiguration, pem_config: PemConfig
) -> tuple[Scenario, CriMeConfiguration]:
    # Dummy functionality for now: just copy-paste
    # TODO actually implement the perception error model!
    sut_scenario = deepcopy(original_scenario)
    sut_config = deepcopy(crime_config)
    return sut_scenario, sut_config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply a perception error model (PEM) to a CommonRoad scenario in order to synthesize an SUT scenario."
    )
    parser.add_argument("--scenario_id", type=str, help="Original CommonRoad scenario ID")
    parser.add_argument("--pem_config", type=str, help="Path to PEM config json")
    parser.add_argument("--sut_scenario", type=str, help="Output path of synthesized CommonRoad scenario.")
    parser.add_argument("--sut_crime_config", type=str, help="Output path to SUT CriMe config")
    args = parser.parse_args()

    create_sut_scenario_files(
        scenario_id=args.scenario_id,
        pem_config_path=args.pem_config,
        sut_scenario_path=args.sut_scenario,
        sut_crime_config_path=args.sut_crime_config,
    )


if __name__ == "__main__":
    main()
