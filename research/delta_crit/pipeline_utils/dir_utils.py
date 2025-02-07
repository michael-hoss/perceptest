import os
import shutil
import tempfile
import uuid
from datetime import datetime

from research.delta_crit.crime_utils.crime_utils import get_config_yaml, get_scenario_xml


def create_empty_workdir() -> str:
    datetime_str: str = datetime.now().strftime("%Y%m%d_%H%M%S.%f")
    random_suffix = uuid.uuid4().hex[:8]
    workdir: str = os.path.join(tempfile.gettempdir(), "delta_crit", f"{datetime_str}_{random_suffix}")

    os.makedirs(workdir)
    return workdir


def copy_example_files_to_workdir(scenario_id: str, workdir: str) -> None:
    """Copy example CriMe config and CommonRoad scenario to the workdir."""
    config_yaml_path = get_config_yaml(scenario_id=scenario_id)
    scenario_xml_path = get_scenario_xml(scenario_id=scenario_id)
    shutil.copy(src=config_yaml_path, dst=workdir)
    shutil.copy(src=scenario_xml_path, dst=workdir)


def set_up_populated_workdir(example_scenario_id: str) -> str:
    workdir: str = create_empty_workdir()
    copy_example_files_to_workdir(scenario_id=example_scenario_id, workdir=workdir)
    return workdir
