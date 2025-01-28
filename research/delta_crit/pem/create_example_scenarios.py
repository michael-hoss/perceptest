import os

import commonroad_crime.utility.visualization as utils_vis

from research.delta_crit.crime_utils.crime_utils import (
    get_crime_configs_dir,
    get_scenario_config,
    get_scenarios_dir,
)
from research.delta_crit.pem.create_sut_scenario import create_sut_scenario_files
from research.delta_crit.pem.pem_config import PemConfig, Perror


def main() -> None:
    scenario_id: str = "DEU_Gar-1_1_T-1"
    scenario_id_sut: str = f"{scenario_id}_sut"
    my_pem_config: PemConfig = [
        Perror(
            start_timestep=10,
            end_timestep=15,
            offset_range=-10,
        )
    ]
    sut_config_path = os.path.join(get_crime_configs_dir(), f"{scenario_id_sut}.yaml")
    sut_scenario_path = os.path.join(get_scenarios_dir(), f"{scenario_id_sut}.xml")

    create_sut_scenario_files(
        scenario_id=scenario_id,
        pem_config=my_pem_config,
        sut_crime_config_path=sut_config_path,
        sut_scenario_path=sut_scenario_path,
    )

    # DEBUG FOR ANALYSIS:
    # Visual Insights
    # new_scenario = get_scenario(scenario_id=scenario_id_sut)
    new_config = get_scenario_config(scenario_id=scenario_id_sut)
    utils_vis.visualize_scenario_at_time_steps(
        new_config.scenario,
        plot_limit=new_config.debug.plot_limits,
        time_steps=[0],
        print_obstacle_ids=True,
        print_lanelet_ids=True,
    )


if __name__ == "__main__":
    main()
