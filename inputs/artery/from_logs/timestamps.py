from copy import deepcopy
from typing import Optional, Sequence

from matplotlib import pyplot

from inputs.artery.artery_format import ArteryData, ArteryObject, TimeStamps


def tidy_up_timestamps(artery_data: ArteryData, expect_no_shift: bool = True) -> ArteryData:
    """After loading the raw artery logs, the time stamps might be untidy.
    This function tidies them up."""

    common_begin, common_end = _determine_common_time_range(artery_data=artery_data)
    remove_overhanging_time_frames(artery_data=artery_data, begin=common_begin, end=common_end)

    # Use ego time stamps as common time stamps because they (should) have no gaps in them
    artery_data.timestamps = _get_timestamps(artery_data.ego_vehicle)

    artery_data = _shift_to_nearby_common_stamps(artery_data=artery_data, expect_no_shift=expect_no_shift)
    return artery_data


def remove_overhanging_time_frames(artery_data: ArteryData, begin: int, end: int) -> None:
    """Remove frames of artery_data outside of beginning and end time stamps."""

    for id, res_object_traj in artery_data.objects_res.items():
        artery_data.objects_res[id] = _trim_to_time_range(trajectory=res_object_traj, begin=begin, end=end)

    for id, out_object_traj in artery_data.objects_out.items():
        artery_data.objects_out[id] = _trim_to_time_range(trajectory=out_object_traj, begin=begin, end=end)

    artery_data.ego_vehicle = _trim_to_time_range(trajectory=artery_data.ego_vehicle, begin=begin, end=end)

    # Remove trajectories that are empty after trimming
    artery_data.objects_res = {key: value for key, value in artery_data.objects_res.items() if value != []}
    artery_data.objects_out = {key: value for key, value in artery_data.objects_out.items() if value != []}
    assert artery_data.ego_vehicle != []  # Ego vehicle trajectory should never be empty


def _determine_common_time_range(artery_data: ArteryData) -> tuple[int, int]:
    """Dermine the time range, where all of OuT, ReS, and ego data are present.
    In case of no overlap, common_begin can be after common_end."""

    time_stamps: TimeStamps = extract_time_stamps(artery_data=artery_data)

    out_begin: int = min([out_traj[0] for out_traj in time_stamps.out.values()])
    res_begin: int = min([res_traj[0] for res_traj in time_stamps.res.values()])
    out_end: int = max([out_traj[-1] for out_traj in time_stamps.out.values()])
    res_end: int = max([res_traj[-1] for res_traj in time_stamps.res.values()])

    common_begin: int = max(time_stamps.ego[0], out_begin, res_begin)
    common_end: int = min(time_stamps.ego[-1], out_end, res_end)
    if common_end < common_begin:
        raise ValueError("No common time range found.")
    return common_begin, common_end


def extract_time_stamps(artery_data: ArteryData) -> TimeStamps:
    # Extract timestamps from the artery data
    timestamps_out: dict[int, list[int]] = {}
    timestamps_res: dict[int, list[int]] = {}
    timestamps_ego: list[int] = []

    for res_id, res_object_traj in artery_data.objects_res.items():
        timestamps_res[res_id] = _get_timestamps(res_object_traj)
    for out_id, out_object_traj in artery_data.objects_out.items():
        timestamps_out[out_id] = _get_timestamps(out_object_traj)
    timestamps_ego = _get_timestamps(artery_data.ego_vehicle)

    return TimeStamps(out=timestamps_out, res=timestamps_res, ego=timestamps_ego)


def _trim_to_time_range(trajectory: list[ArteryObject], begin: int, end: int) -> list[ArteryObject]:
    """Remove frames of trajectory outside a common beginnging and end time stamps.
    :param trajectory: list of frames of an artery object"""
    if not trajectory:
        return trajectory

    # Define auxiliary list that is easier to work with
    trajectory_stamps: list[int] = _get_timestamps(trajectory)

    # Trajectory is either entirely before begin, or entirely after end
    if trajectory_stamps[-1] < begin or trajectory_stamps[0] > end:
        return []

    # From here on, we know that at least one frame of the trajectory is in [begin, end]
    cut_begin = _find_index_of_fuzzy_value(list=trajectory_stamps, value=begin, use_smaller=False)
    cut_end = _find_index_of_fuzzy_value(list=trajectory_stamps, value=end, use_smaller=True)

    # Finally, cut the trajectory
    return trajectory[cut_begin : cut_end + 1]


def _find_index_of_fuzzy_value(list: list[int], value: int, use_smaller: bool) -> int:
    """Find the list index of the given value.
    :param list: sorted list of integers.
    :param value: value to search for. Can be outside of the list or between its elements.
    :param use_smaller: if between two elements, return the smaller index (or the larger index if False).
    :return: index. If value is outside of the list, return the closest index."""

    if not list:
        raise ValueError("List must not be empty")

    try:
        return list.index(value)
    except ValueError:
        for iter_index, iter_stamp in enumerate(list):
            if iter_stamp >= value:
                return max(iter_index - int(use_smaller), 0)
        return len(list) - 1


def _shift_to_nearby_common_stamps(artery_data: ArteryData, expect_no_shift: bool = True) -> ArteryData:
    """From artery data v5 onwards, the timestamps of OuT, ReS, and ego already lie
    on the same common equidistant points in time. Thus, we expect no shift."""

    if expect_no_shift:
        initial_artery_data = deepcopy(artery_data)

    for trajectory_res in artery_data.objects_res.values():
        _shift_trajectory_to_common_stamps(trajectory=trajectory_res, common_timestamps=artery_data.timestamps)

    for trajectory_out in artery_data.objects_out.values():
        _shift_trajectory_to_common_stamps(trajectory=trajectory_out, common_timestamps=artery_data.timestamps)

    _shift_trajectory_to_common_stamps(trajectory=artery_data.ego_vehicle, common_timestamps=artery_data.timestamps)

    if expect_no_shift:
        assert initial_artery_data == artery_data
    return artery_data


def _shift_trajectory_to_common_stamps(trajectory: Sequence[ArteryObject], common_timestamps: list[int]) -> None:
    moving_common_index: int = 0
    for frame in trajectory:
        # Move moving common index after stamp_to_replace
        while common_timestamps[moving_common_index] < frame["origin"]["timestamp"]:
            moving_common_index += 1
        # Replace stamp_to_replace by the closest common stamp *after* it
        frame["origin"]["timestamp"] = common_timestamps[moving_common_index]


def _get_timestamps(trajectory: list[ArteryObject]) -> list[int]:
    return [frame["origin"]["timestamp"] for frame in trajectory]


def visualize_time_stamps(time_stamps: TimeStamps, additional_heading: Optional[str] = None) -> None:
    additional_heading = additional_heading or ""

    # Create a figure and axis
    fig, ax = pyplot.subplots(figsize=(11, 7))

    # Plot each array of timestamps as vertical lines
    all_labels: list[str] = []
    timelines_count = 0
    for object_out_id, object_out_timestamps in time_stamps.out.items():
        current_label = f"out[{object_out_id}]"
        all_labels.append(current_label)
        ax.vlines(
            object_out_timestamps,
            ymin=timelines_count,
            ymax=timelines_count + 1,
            colors="r",
            label=current_label,
            linewidth=2,
        )
        timelines_count += 1

    for object_res_id, object_res_timestamps in time_stamps.res.items():
        current_label = f"res[{object_res_id}]"
        all_labels.append(current_label)
        ax.vlines(
            object_res_timestamps,
            ymin=timelines_count,
            ymax=timelines_count + 1,
            colors="g",
            label=current_label,
            linewidth=2,
        )
        timelines_count += 1

    current_label = "ego"
    all_labels.append(current_label)
    ax.vlines(  # short thick line in ego row
        time_stamps.ego, ymin=timelines_count, ymax=timelines_count + 1, colors="b", label=current_label, linewidth=2
    )
    reference_anchor_color = (0.6, 0.8, 1.0, 0.6)  # color of reference time frame long line
    ax.vlines(  # long thin line across all rows
        time_stamps.ego, ymin=0, ymax=timelines_count, colors=reference_anchor_color, label=current_label, linewidth=1
    )
    timelines_count += 1

    # Set the y-axis labels for each array
    ax.set_yticks([x + 0.5 for x in range(timelines_count)])
    ax.set_yticklabels(all_labels)

    # Add a legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    pyplot.subplots_adjust(right=0.8)

    # Set the title and labels
    ax.set_title("Timestamp Alignment Overview: " + additional_heading)
    ax.set_xlabel("Timestamps")
    ax.set_ylim(0, timelines_count)

    # timestep_length: float = time_stamps.ego[1] - time_stamps.ego[0]
    # pyplot.xlim(time_stamps.ego[0] - timestep_length, time_stamps.ego[15])  # Set x-axis limits

    # Show the plot
    pyplot.show(block=False)
    pass  # line for potential breakpoint
