import os

from commonroad_crime.data_structure.configuration import CriMeConfiguration
from commonroad_crime.data_structure.crime_interface import CriMeInterface
from commonroad_crime.measure import TTC

from research.delta_crit.crime_utils.crime_utils import get_crime_config

# Note that `CriMeConfiguration.general: GeneralConfiguration` holds all the necessary paths
# for locating the (scenario) files.
config: CriMeConfiguration = get_crime_config("DEU_Gar-1_1_T-1")
PERCEPTEST_ROOT = os.environ.get("PERCEPTEST_REPO")

crime_interface = CriMeInterface(config)
crime_interface.evaluate_scene(measures=[TTC], time_step=0, vehicle_id=200)
crime_interface.evaluate_scenario([TTC], time_start=0, time_end=20)
crime_interface.visualize(time_step=19)
crime_interface.save_to_file(output_dir=PERCEPTEST_ROOT)

pass
