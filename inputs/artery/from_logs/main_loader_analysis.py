from typing import TYPE_CHECKING

from conftest import use_debugpy
from inputs.artery.conftest import obtain_test_case_dump
from inputs.artery.from_logs.main_loader import pull_artery_sim_log
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs
from inputs.artery.from_logs.timestamps import extract_time_stamps, visualize_time_stamps

if TYPE_CHECKING:
    from inputs.artery.artery_format import ArterySimLog, TimeStamps


def manual_data_analysis() -> None:
    """Manual testing by plotting data"""
    artery_log_raw: ArterySimLog = load_from_artery_logs(sim_log_dump=obtain_test_case_dump())
    raw_time_stamps: TimeStamps = extract_time_stamps(artery_sim_log=artery_log_raw)
    visualize_time_stamps(time_stamps=raw_time_stamps, additional_heading="Raw time stamps")

    artery_log_timestamps_tidy: ArterySimLog = pull_artery_sim_log(artery_sim_log_dump=obtain_test_case_dump())
    tidy_time_stamps: TimeStamps = extract_time_stamps(artery_sim_log=artery_log_timestamps_tidy)
    visualize_time_stamps(time_stamps=tidy_time_stamps, additional_heading="Tidy time stamps")

    # Set breakpoint here to see plots
    pass


if __name__ == "__main__":
    use_debugpy()
    manual_data_analysis()
