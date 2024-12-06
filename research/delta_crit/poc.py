from commonroad_crime.data_structure.configuration import CriMeConfiguration
from commonroad_crime.data_structure.crime_interface import CriMeInterface
from commonroad_crime.measure import TTCStar

from .crime_utils.crime_utils import get_scenario_config_yaml

scenario_id = "DEU_Gar-1_1_T-1"


scenario_yaml: str = get_scenario_config_yaml(scenario_id=scenario_id)
config = CriMeConfiguration.load(scenario_yaml, scenario_id)
config.update()
config.print_configuration_summary()

crime_interface = CriMeInterface(config)
crime_interface.evaluate_scene(measures=[TTCStar], time_step=0, vehicle_id=200)
crime_interface.evaluate_scenario([TTCStar])

crime_interface.visualize()
pass
