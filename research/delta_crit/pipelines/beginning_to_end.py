import os

from commonroad_crime.data_structure.base import CriMeBase
from commonroad_crime.data_structure.crime_interface import CriMeInterface  # type: ignore
from commonroad_crime.measure import BTN, CI, DA, HW, PF, STN, ALongReq, TTCStar  # type: ignore

from research.delta_crit.crime_utils.crime_utils import get_crime_config
from research.delta_crit.crime_utils.vis_utils import (
    close_current_fig,
    save_delta_criticality_curve,
    save_scenario_figure_at_time_steps,
)
from research.delta_crit.delta_crime.delta_crime import compute_delta
from research.delta_crit.pem.create_sut_scenario import create_sut_crime_config_files
from research.delta_crit.pem.pem_config import PemConfig, Perror, pem_config_to_json
from research.delta_crit.pipeline_utils.dir_utils import set_up_populated_workdir


def main() -> None:
    # Define input data
    scenario_id: str = "DEU_Gar-1_1_T-1"
    workdir: str = set_up_populated_workdir(example_scenario_id=scenario_id)

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
    scenario_id_sut: str = create_sut_crime_config_files(
        scenario_id=scenario_id,
        pem_config=my_pem_config,
        workdir=workdir,
    )

    # Handle intermediate results
    pem_config_to_json(my_pem_config, os.path.join(workdir, "pem_config.json"))
    res_config = get_crime_config(scenario_id=scenario_id, custom_workdir=workdir)
    sut_config = get_crime_config(scenario_id=scenario_id_sut, custom_workdir=workdir)
    res_config.debug.save_plots = True
    sut_config.debug.save_plots = True
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

    used_measures: list[CriMeBase] = [
        CI,
        DA,
        HW,
        # TTC,
        TTCStar,
        # TTR,
        ALongReq,
        # LongJ,
        BTN,
        STN,
        # P_MC makes problems for SUT
        PF,
    ]
    # used_measures = [TTC]
    # res_interface.evaluate_scenario(used_measures, time_start=8, time_end=17)
    sut_interface.evaluate_scenario(used_measures, time_start=8, time_end=17)

    res_interface.save_to_file(output_dir=workdir)
    sut_interface.save_to_file(output_dir=workdir)

    # Save criticality results to files
    example_time_step = int(0.5 * (start_toi + end_toi))
    example_time_step = start_toi

    res_interface.visualize(time_step=example_time_step)
    close_current_fig()
    sut_interface.visualize(time_step=example_time_step)
    close_current_fig()

    # For more plotting opportunities, see also
    # https://commonroad.in.tum.de/tutorials/commonroad-crime-more

    # Analyze the delta criticality
    delta_dict = compute_delta(sut=sut_interface, res=res_interface)
    delta_dict

    save_delta_criticality_curve(res_interface=res_interface, sut_interface=sut_interface, workdir=workdir)
    pass


if __name__ == "__main__":
    main()
