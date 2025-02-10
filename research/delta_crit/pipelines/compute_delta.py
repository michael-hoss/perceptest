from commonroad_crime.data_structure.crime_interface import CriMeConfiguration, CriMeInterface
from commonroad_crime.measure import TTC  # type: ignore

from research.delta_crit.crime_utils.crime_utils import get_crime_config


def main() -> None:
    # TODO compute delta criticality between two configs.
    config_res: CriMeConfiguration = get_crime_config("DEU_Gar-1_1_T-1")
    crime_interface = CriMeInterface(config_res)

    crime_interface.evaluate_scene(measures=[TTC], time_step=0, vehicle_id=200)
    crime_interface.evaluate_scenario([TTC], time_start=0, time_end=20)


if __name__ == "__main__":
    main()
