import os

import commonroad_crime.utility.visualization as utils_vis
from commonroad.common.file_reader import CommonRoadFileReader  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.visualization.mp_renderer import MPRenderer  # type: ignore
from commonroad_crime.data_structure.configuration import CriMeConfiguration  # type: ignore


def get_local_crime_root() -> str:
    PERCEPTEST_ROOT = os.environ.get("PERCEPTEST_REPO")
    assert PERCEPTEST_ROOT
    CRIME_ROOT = os.path.join(PERCEPTEST_ROOT, "third_party/commonroad-crime")
    return CRIME_ROOT


def get_scenario_config_yaml(scenario_id: str) -> str:
    """Get scenario config yaml from the committed ones in the crime submodue"""
    crime_root: str = get_local_crime_root()
    return os.path.join(crime_root, f"config_files/{scenario_id}.yaml")


def get_scenario_config(scenario_id: str) -> CriMeConfiguration:
    scenario_yaml_path = get_scenario_config_yaml(scenario_id=scenario_id)
    config = CriMeConfiguration.load(scenario_yaml_path, scenario_id)
    config.update()
    return config


def get_scenario_xml(scenario_id: str) -> str:
    """Get scenario description xml from the committed ones in the crime submodue"""
    crime_root: str = get_local_crime_root()
    return os.path.join(crime_root, f"scenarios/{scenario_id}.xml")


def get_scenario(scenario_id: str) -> Scenario:
    scenario_xml = get_scenario_xml(scenario_id=scenario_id)
    scenario, planning_problem_set = CommonRoadFileReader(scenario_xml).open()
    return scenario


def visualize_statically(scenario_id: str) -> None:
    """Plot the scenario as a static drawing with dots indicating future trajectory points"""
    scenario: Scenario = get_scenario(scenario_id=scenario_id)
    rnd = MPRenderer(figsize=(25, 10))
    scenario.draw(rnd)
    rnd.render(show=True)


def visualize_time_steps(scenario_id: str, time_steps: list[int]) -> None:
    config = get_scenario_config(scenario_id=scenario_id)

    utils_vis.visualize_scenario_at_time_steps(
        config.scenario, plot_limit=config.debug.plot_limits, time_steps=time_steps
    )
