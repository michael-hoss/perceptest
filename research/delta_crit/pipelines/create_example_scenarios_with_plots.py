import os

from commonroad_crime.data_structure.crime_interface import CriMeInterface  # type: ignore
from commonroad_crime.measure import TTC  # type: ignore

from research.delta_crit.crime_utils.crime_utils import get_crime_config
from research.delta_crit.crime_utils.vis_utils import save_scenario_figure_at_time_steps
from research.delta_crit.pem.create_sut_scenario import create_sut_crime_config_files
from research.delta_crit.pem.pem_config import PemConfig, Perror, pem_config_to_json
from research.delta_crit.pipeline_utils.dir_utils import set_up_populated_workdir


def main() -> None:
    # Define input data
    scenario_id: str = "DEU_Gar-1_1_T-1"
    workdir: str = set_up_populated_workdir(example_scenario_id=scenario_id)

    sut_suffix: str = "sut"
    scenario_id_sut: str = f"{scenario_id}_{sut_suffix}"

    start_toi = 10
    end_toi = 15
    plot_timesteps = [start_toi - 1, end_toi + 1]

    # Define artificial perception errors
    my_pem_config: PemConfig = [
        Perror(
            start_timestep=start_toi,
            end_timestep=end_toi,
            offset_azimuth=-20,
            offset_range=3,
            object_id=201,
        )
    ]

    # Create SUT scenario with perception errors
    create_sut_crime_config_files(
        scenario_id=scenario_id,
        pem_config=my_pem_config,
        sut_suffix=sut_suffix,
        workdir=workdir,
    )

    # Handle intermediate results
    pem_config_to_json(my_pem_config, os.path.join(workdir, "pem_config.json"))
    res_config = get_crime_config(scenario_id=scenario_id, custom_workdir=workdir)
    sut_config = get_crime_config(scenario_id=scenario_id_sut, custom_workdir=workdir)
    save_scenario_figure_at_time_steps(
        crime_config=res_config,
        workdir=workdir,
        time_steps=plot_timesteps,
    )
    save_scenario_figure_at_time_steps(
        crime_config=sut_config,
        workdir=workdir,
        time_steps=plot_timesteps,
    )

    # Compute criticality of scenarios
    res_interface = CriMeInterface(res_config)
    sut_interface = CriMeInterface(sut_config)

    res_interface.evaluate_scenario([TTC], time_start=0, time_end=20)
    sut_interface.evaluate_scenario([TTC], time_start=0, time_end=20)

    # TODO: make sense of these dots in the visualization
    res_interface.visualize(time_step=int(0.5 * (start_toi + end_toi)))
    sut_interface.visualize(time_step=int(0.5 * (start_toi + end_toi)))

    # TODO fix the weird renaming of scenario_id
    res_interface.save_to_file(output_dir=workdir)
    sut_interface.save_to_file(output_dir=workdir)


if __name__ == "__main__":
    main()
