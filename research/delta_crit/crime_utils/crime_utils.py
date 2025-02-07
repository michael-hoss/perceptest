import os
from copy import deepcopy

import commonroad_crime.utility.visualization as utils_vis
from commonroad.common.file_reader import CommonRoadFileReader  # type: ignore
from commonroad.common.file_writer import CommonRoadFileWriter  # type: ignore
from commonroad.planning.planning_problem import PlanningProblemSet  # type: ignore
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad.visualization.mp_renderer import MPRenderer  # type: ignore
from commonroad_crime.data_structure.configuration import CriMeConfiguration, GeneralConfiguration  # type: ignore
from omegaconf import DictConfig, OmegaConf

from base.dict_utils.dict_utils import remove_key_recursively


def get_local_crime_root() -> str:
    PERCEPTEST_ROOT = os.environ.get("PERCEPTEST_REPO")
    assert isinstance(PERCEPTEST_ROOT, str)
    crime_root = os.path.join(PERCEPTEST_ROOT, "third_party/commonroad-crime")
    return crime_root


def get_delta_crit_root() -> str:
    PERCEPTEST_ROOT = os.environ.get("PERCEPTEST_REPO")
    assert isinstance(PERCEPTEST_ROOT, str)
    delta_crit_root = os.path.join(PERCEPTEST_ROOT, "research/delta_crit")
    return delta_crit_root


def get_scenarios_dir() -> str:
    delta_crit_root: str = get_delta_crit_root()
    return os.path.join(delta_crit_root, "example_data/scenarios")


def get_crime_configs_dir() -> str:
    delta_crit_root: str = get_delta_crit_root()
    return os.path.join(delta_crit_root, "example_data/crime_configs")


def get_pem_configs_dir() -> str:
    delta_crit_root: str = get_delta_crit_root()
    return os.path.join(delta_crit_root, "example_data/pem_configs")


delta_crit_paths = GeneralConfiguration(
    path_scenarios=get_scenarios_dir(),
    path_scenarios_batch=os.path.join(get_scenarios_dir(), "batch"),
    path_output_abs=os.path.join(get_delta_crit_root(), "example_data/crime_outputs"),
    path_logs=os.path.join(get_delta_crit_root(), "example_data/crime_outputs/logs"),
    path_icons=os.path.join(get_local_crime_root(), "docs/icons"),
)


def crime_paths_factory_for_delta_crit(scenario_name: str) -> GeneralConfiguration:
    general_config: GeneralConfiguration = deepcopy(delta_crit_paths)
    general_config.set_scenario_name(scenario_name=scenario_name)
    return general_config


def get_config_yaml(scenario_id: str) -> str:
    """Get scenario config yaml path.
    Search priority:
    1) research/delta_crit/example_data/crime_configs/
    2) third_party/commonroad-crime/config_files/
    """
    delta_crit_path: str = os.path.join(get_crime_configs_dir(), f"{scenario_id}.yaml")
    if os.path.isfile(delta_crit_path):
        return delta_crit_path
    else:
        crime_root: str = get_local_crime_root()
        crime_path: str = os.path.join(crime_root, f"config_files/{scenario_id}.yaml")
        assert os.path.isfile(crime_path)
        return crime_path


def get_crime_config(scenario_id: str) -> CriMeConfiguration:
    config_yaml_path = get_config_yaml(scenario_id=scenario_id)
    config = CriMeConfiguration.load(config_yaml_path, scenario_id)
    config.update()  # Here, we could specify/overwrite the ego_id, too!
    return config


def get_scenario_xml(scenario_id: str) -> str:
    """Get scenario xml path.
    Search priority:
    1) research/delta_crit/scenarios/
    2) third_party/commonroad-crime/scenarios/
    """
    delta_crit_path: str = os.path.join(get_scenarios_dir(), f"{scenario_id}.xml")
    if os.path.isfile(delta_crit_path):
        return delta_crit_path
    else:
        crime_root: str = get_local_crime_root()
        crime_path: str = os.path.join(crime_root, f"scenarios/{scenario_id}.xml")
        assert os.path.isfile(crime_path)
        return crime_path


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
    config = get_crime_config(scenario_id=scenario_id)

    utils_vis.visualize_scenario_at_time_steps(
        config.scenario, plot_limit=config.debug.plot_limits, time_steps=time_steps
    )


def write_scenario(scenario: Scenario, file_path: str) -> None:
    dummy_planning_problem_set = PlanningProblemSet()
    file_writer = CommonRoadFileWriter(scenario=scenario, planning_problem_set=dummy_planning_problem_set)
    file_writer.write_scenario_to_file(filename=file_path)


def write_crime_config_shallow(config: CriMeConfiguration, file_path: str) -> None:
    """Only write the config yaml itself, not the referenced scenario xml."""

    _, file_suffix = os.path.splitext(file_path)
    assert file_suffix == ".yaml", f"File type {file_suffix} is unsupported! Please use .yaml!"

    config_dict_omega: DictConfig = OmegaConf.structured(config)  # encode the object

    config_dict: dict = remove_key_recursively(
        original_dict=config_dict_omega, key_to_remove="_BaseConfig__initialized", input_type=DictConfig
    )
    config_dict_omega = DictConfig(config_dict)

    # TODO potentially tidy up config_dict s.th. it only contains the non-default values
    # and no private variables of the config dataclass

    OmegaConf.save(config=config_dict_omega, f=file_path)


def write_crime_config_deep(config: CriMeConfiguration, custom_path_for_config: str | None = None) -> None:
    """
    Write both the config yaml and the referenced scenario xml.

    The config yaml basename is adopted from the name of the scenario.
    The scenario path and basename are taken from the config path settings.
    """
    if custom_path_for_config is None:
        config_path = os.path.join(get_crime_configs_dir(), f"{config.general.name_scenario}.yaml")
    else:
        config_path = custom_path_for_config

    write_crime_config_shallow(config=config, file_path=config_path)
    write_scenario(scenario=config.scenario, file_path=config.general.path_scenario)
