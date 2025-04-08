import math
import os

import commonroad_crime.utility.visualization as crime_vis
import numpy as np
from commonroad.scenario.scenario import Scenario  # type: ignore
from commonroad_crime.data_structure.crime_interface import CriMeConfiguration, CriMeInterface
from commonroad_crime.data_structure.type import TypeMonotone


def open_figure() -> None:
    crime_vis.plt.figure()


def render_time_steps_into_figure(
    scenario: Scenario,
    plot_limit,
    time_steps: list[int],
    print_obstacle_ids: bool = False,
    print_lanelet_ids: bool = False,
    ego_id: int | None = None,
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

        color = crime_vis.TUMcolor.TUMblue if obs.obstacle_id != ego_id else crime_vis.TUMcolor.TUMdarkred

        crime_vis.draw_state_list(
            rnd,
            obs.prediction.trajectory.state_list[plot_traj_begin_index : plot_traj_end_index + 1],
            color=color,
            linewidth=5,
        )
        for ts in time_steps:
            if plot_traj_begin_time_step - 1 <= ts <= plot_traj_end_time_step:
                crime_vis.draw_dyn_vehicle_shape(rnd, obs, ts, color=color)


def show_figure() -> None:
    crime_vis.plt.show()


def save_current_fig(workdir: str, filename_wo_suffix: str, suffix: str = "pdf") -> str:
    # crime_vis.plt.title(filename_wo_suffix)
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
    crime_config: CriMeConfiguration,
    workdir: str,
    time_steps: list[int],
    print_obstacle_ids: bool = False,
    print_lanelet_ids: bool = False,
    file_format: str = "png",  # ["png", "pdf", "svg"]
) -> str:
    crime_vis.plt.figure(figsize=(12, 8))
    render_time_steps_into_figure(
        crime_config.scenario,
        plot_limit=crime_config.debug.plot_limits,
        time_steps=time_steps,
        print_obstacle_ids=print_obstacle_ids,
        print_lanelet_ids=print_lanelet_ids,
        ego_id=crime_config.vehicle.ego_id,
    )

    timesteps_for_path: str = "_".join([str(time_step) for time_step in time_steps])
    filename_wo_suffix = f"{crime_config.scenario.scenario_id}_at_timesteps_{timesteps_for_path}"
    figure_path: str = save_current_fig(workdir=workdir, filename_wo_suffix=filename_wo_suffix, suffix=file_format)
    crime_vis.plt.close()
    return figure_path


def save_delta_criticality_curve(res_interface: CriMeInterface, sut_interface: CriMeInterface, workdir: str) -> str:
    file_name_wo_suffix: str = f"{res_interface.config.scenario.scenario_id}_delta_crit_curve"
    plot_delta_criticality_curve(res_interface, sut_interface)
    figure_path = save_current_fig(workdir=workdir, filename_wo_suffix=file_name_wo_suffix, suffix="png")
    close_current_fig()
    return figure_path


def plot_delta_criticality_curve(
    res_crime: CriMeInterface, sut_crime: CriMeInterface, nr_per_row: int = 2, flag_latex: bool = True
):
    if flag_latex:
        configure_latex()
    if res_crime.measures is not None and res_crime.time_start is not None and res_crime.time_end is not None:
        nr_metrics = len(res_crime.measures)
        if nr_metrics > nr_per_row:
            nr_column = nr_per_row
            nr_row = math.ceil(nr_metrics / nr_column)
        else:
            nr_column = nr_metrics
            nr_row = 1
        fig, axs = crime_vis.plt.subplots(nr_row, nr_column, figsize=(7.5 * nr_column, 5 * nr_row))

        count_row, count_column = 0, 0
        for measure in res_crime.measures:
            if nr_metrics == 1:
                ax = axs
            elif nr_row == 1:
                ax = axs[count_column]
            else:
                ax = axs[count_row, count_column]

            plot_measure(measure, res_crime, sut_crime, ax)

            count_column += 1
            if count_column > nr_per_row - 1:
                count_column = 0
                count_row += 1
        crime_vis.plt.show()


def plot_measure(measure, res_crime, sut_crime, ax) -> None:
    res_criticality_list_list: list = []  # y axis values reference system
    sut_criticality_list_list: list = []  # y axis values system under test
    time_list: list = []  # x axis values

    for time_step in range(res_crime.time_start, res_crime.time_end + 1):
        if measure.measure_name.value in res_crime.criticality_dict[time_step]:
            res_criticality_list_list.append(res_crime.criticality_dict[time_step][measure.measure_name.value])
            sut_criticality_list_list.append(sut_crime.criticality_dict[time_step][measure.measure_name.value])
            time_list.append(time_step)
    res_criticality_list: np.ndarray = np.array(res_criticality_list_list)
    sut_criticality_list: np.ndarray = np.array(sut_criticality_list_list)

    res_min_value, res_max_value = get_min_max_values(res_criticality_list)
    sut_min_value, sut_max_value = get_min_max_values(sut_criticality_list)
    res_criticality_list_clean = clean_criticality_list(res_criticality_list, res_min_value, res_max_value)
    sut_criticality_list_clean = clean_criticality_list(sut_criticality_list, sut_min_value, sut_max_value)

    # Do the actual plots!
    ax.plot(time_list, res_criticality_list_clean)
    ax.plot(time_list, sut_criticality_list_clean)

    min_value = min(res_min_value, sut_min_value)
    max_value = max(res_max_value, sut_max_value)
    criticality_lists = [res_criticality_list, sut_criticality_list]
    customize_y_axis_ticks_and_labels(min_value, max_value, criticality_lists)

    ax.axis(xmin=time_list[0], xmax=time_list[-1])
    ax.title.set_text(measure.measure_name.value)

    if measure.monotone == TypeMonotone.NEG:
        ax.invert_yaxis()


def customize_y_axis_ticks_and_labels(min_value, max_value, criticality_lists) -> None:
    ticks, _ = crime_vis.plt.yticks()
    # Update ticks and labels
    new_ticks = [tick for tick in ticks if min_value <= tick <= max_value]  # Keep ticks within the finite range
    new_labels = ["{:.4g}".format(tick) for tick in new_ticks]  # Limit to 4 significant digits

    # Check for infinities and add custom labels
    for criticality_list in criticality_lists:
        if np.any(np.isposinf(criticality_list)):
            new_ticks.append(max_value)  # Place at max finite value or a predefined position
            new_labels.append("inf")

        if np.any(np.isneginf(criticality_list)):
            new_ticks = [min_value] + new_ticks  # Place at min finite value or a predefined position
            new_labels = ["-inf"] + new_labels

    # Apply the updated ticks and labels to the plot
    crime_vis.plt.yticks(new_ticks, new_labels)


def get_min_max_values(criticality_list: np.ndarray) -> tuple[float, float]:
    # Apply the mask and find the maximum value among the remaining elements
    if np.any(np.isinf(criticality_list)):
        # This mask keeps only the values that are neither nan nor inf
        mask = ~np.isnan(criticality_list) & ~np.isinf(criticality_list)

        if len(criticality_list[mask]) > 0:
            # Set new max/min value to 10 above/below the remaining normal max/min
            max_value = np.max(criticality_list[mask]) + 10
            min_value = np.min(criticality_list[mask]) - 10
        else:
            # Default max/min values if all values are nan or inf
            max_value = 10
            min_value = 10
    else:
        max_value = np.nanmax(criticality_list)
        min_value = np.nanmin(criticality_list)

    return min_value, max_value


def clean_criticality_list(criticality_list: np.ndarray, min_value, max_value) -> np.ndarray:
    if np.any(np.isinf(criticality_list)):
        # First, replace np.inf with max_value
        criticality_list_clean = np.where(criticality_list == np.inf, max_value, criticality_list)
        # Then, replace -np.inf with min_value
        criticality_list_clean = np.where(criticality_list_clean == -np.inf, min_value, criticality_list_clean)
    else:
        return criticality_list

    return criticality_list_clean


def configure_latex() -> None:
    # use Latex font
    FONTSIZE = 28
    crime_vis.plt.rcParams["text.latex.preamble"] = r"\usepackage{lmodern}"
    pgf_with_latex = {  # setup matplotlib to use latex for output
        "pgf.texsystem": "pdflatex",  # change this if using xetex or lautex
        "text.usetex": True,  # use LaTeX to write all text
        "font.family": "lmodern",
        # blank entries should cause plots
        "font.sans-serif": [],  # ['Avant Garde'],              # to inherit fonts from the document
        # 'text.latex.unicode': True,
        "font.monospace": [],
        "axes.labelsize": FONTSIZE,  # LaTeX default is 10pt font.
        "font.size": FONTSIZE - 10,
        "legend.fontsize": FONTSIZE,  # Make the legend/label fonts
        "xtick.labelsize": FONTSIZE,  # a little smaller
        "ytick.labelsize": FONTSIZE,
        "pgf.preamble": r"\usepackage[utf8x]{inputenc}"
        + r"\usepackage[T1]{fontenc}"
        + r"\usepackage[detect-all,locale=DE]{siunitx}",
    }
    crime_vis.matplotlib.rcParams.update(pgf_with_latex)
