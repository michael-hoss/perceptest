import os

import commonroad_crime.utility.visualization as crime_vis
from commonroad.scenario.scenario import Scenario  # type: ignore

from research.delta_crit.crime_utils.crime_utils import get_crime_config


def open_figure() -> None:
    crime_vis.plt.figure()


def render_time_steps_into_figure(
    scenario: Scenario,
    plot_limit,
    time_steps: list[int],
    print_obstacle_ids: bool = False,
    print_lanelet_ids: bool = False,
):
    rnd = crime_vis.MPRenderer(plot_limits=plot_limit)

    assert isinstance(time_steps, list)
    plot_begin: int = min(time_steps)
    plot_end: int = max(time_steps)
    rnd.draw_params.time_begin = plot_begin
    rnd.draw_params.time_end = plot_end

    rnd.draw_params.trajectory.draw_trajectory = False
    rnd.draw_params.dynamic_obstacle.draw_icon = True
    rnd.draw_params.dynamic_obstacle.show_label = print_obstacle_ids
    rnd.draw_params.lanelet_network.lanelet.show_label = print_lanelet_ids
    scenario.draw(rnd)
    rnd.render()
    for obs in scenario.obstacles:
        plot_traj_begin_time_step = max(obs.prediction.initial_time_step, plot_begin)
        plot_traj_end_time_step = min(obs.prediction.final_time_step, plot_end)
        plot_traj_begin_index = plot_traj_begin_time_step - obs.prediction.initial_time_step
        plot_traj_end_index = plot_traj_end_time_step - obs.prediction.initial_time_step

        crime_vis.draw_state_list(
            rnd,
            obs.prediction.trajectory.state_list[plot_traj_begin_index : plot_traj_end_index + 1],
            color=crime_vis.TUMcolor.TUMblue,
            linewidth=5,
        )
        for ts in time_steps:
            if plot_traj_begin_time_step - 1 <= ts <= plot_traj_end_time_step:
                crime_vis.draw_dyn_vehicle_shape(rnd, obs, ts, color=crime_vis.TUMcolor.TUMblue)


def show_figure() -> None:
    crime_vis.plt.show()


def save_current_fig(workdir: str, filename_wo_suffix: str, suffix: str = "pdf") -> str:
    crime_vis.plt.title(filename_wo_suffix)
    figure_path: str = os.path.join(workdir, f"{filename_wo_suffix}.{suffix}")
    crime_vis.plt.savefig(
        figure_path,
        format=suffix,
        bbox_inches="tight",
        transparent=False,
    )
    return figure_path


def close_current_fig() -> None:
    crime_vis.plt.close()


def save_scenario_figure_at_time_steps(
    config_name: str,
    workdir: str,
    time_steps: list[int],
    print_obstacle_ids: bool = False,
    print_lanelet_ids: bool = False,
    file_format: str = "png",  # ["png", "pdf", "svg"]
) -> str:
    original_config = get_crime_config(scenario_id=config_name, custom_workdir=workdir)
    crime_vis.plt.figure(figsize=(12, 8))
    render_time_steps_into_figure(
        original_config.scenario,
        plot_limit=original_config.debug.plot_limits,
        time_steps=time_steps,
        print_obstacle_ids=print_obstacle_ids,
        print_lanelet_ids=print_lanelet_ids,
    )

    timesteps_for_path: str = "_".join([str(time_step) for time_step in time_steps])
    filename_wo_suffix = f"{config_name}_at_timesteps_{timesteps_for_path}"
    figure_path: str = save_current_fig(workdir=workdir, filename_wo_suffix=filename_wo_suffix, suffix=file_format)
    crime_vis.plt.close()
    return figure_path
