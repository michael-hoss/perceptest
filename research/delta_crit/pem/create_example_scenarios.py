import commonroad_crime.utility.visualization as utils_vis

from research.delta_crit.crime_utils.crime_utils import (
    get_crime_config,
)
from research.delta_crit.pem.create_sut_scenario import create_sut_crime_config_files
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
    # config_path = get_crime_config(scenario_id=scenario_id)  # debugging

    create_sut_crime_config_files(
        scenario_id=scenario_id,
        pem_config=my_pem_config,
    )

    # DEBUG FOR ANALYSIS:
    # Visual Insights
    # new_scenario = get_scenario(scenario_id=scenario_id_sut)
    new_config = get_crime_config(scenario_id=scenario_id_sut)
    utils_vis.visualize_scenario_at_time_steps(
        new_config.scenario,
        plot_limit=new_config.debug.plot_limits,
        time_steps=[0],
        print_obstacle_ids=True,
        print_lanelet_ids=True,
    )


if __name__ == "__main__":
    main()
