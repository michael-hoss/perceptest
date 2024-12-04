import os


def get_local_crime_root() -> str:
    PERCEPTEST_ROOT = os.environ.get("PERCEPTEST_REPO")
    assert PERCEPTEST_ROOT
    CRIME_ROOT = os.path.join(PERCEPTEST_ROOT, "third_party/commonroad-crime")
    return CRIME_ROOT


def get_scenario_config_yaml(scenario_id: str) -> str:
    """Get scenario config yaml from the committed ones in the crime submodue"""
    crime_root: str = get_local_crime_root()
    return os.path.join(crime_root, f"config_files/{scenario_id}.yaml")


def get_scenario_xml(scenario_id: str) -> str:
    """Get scenario description xml from the committed ones in the crime submodue"""
    crime_root: str = get_local_crime_root()
    return os.path.join(crime_root, f"scenarios/{scenario_id}.xml")
