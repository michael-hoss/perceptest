from research.delta_crit.crime_utils.vis_utils import save_scenario_figure_at_time_steps
from research.delta_crit.pem.create_sut_scenario import create_sut_crime_config_files
from research.delta_crit.pem.pem_config import PemConfig, Perror
from research.delta_crit.pipeline_utils.dir_utils import set_up_populated_workdir


def main() -> None:
    scenario_id: str = "DEU_Gar-1_1_T-1"
    workdir: str = set_up_populated_workdir(example_scenario_id=scenario_id)

    sut_suffix: str = "sut"
    scenario_id_sut: str = f"{scenario_id}_{sut_suffix}"

    start_timestep = 10
    end_timestep = 15
    plot_timesteps = [start_timestep - 1, end_timestep + 1]

    my_pem_config: PemConfig = [
        Perror(
            start_timestep=start_timestep,
            end_timestep=end_timestep,
            offset_azimuth=-20,
            offset_range=3,
            object_id=201,
        )
    ]

    create_sut_crime_config_files(
        scenario_id=scenario_id,
        pem_config=my_pem_config,
        sut_suffix=sut_suffix,
        workdir=workdir,
    )

    save_scenario_figure_at_time_steps(
        config_name=scenario_id,
        workdir=workdir,
        time_steps=plot_timesteps,
    )

    save_scenario_figure_at_time_steps(
        config_name=scenario_id_sut,
        workdir=workdir,
        time_steps=plot_timesteps,
    )


if __name__ == "__main__":
    main()
