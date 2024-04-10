from typing import TYPE_CHECKING

from conftest import use_debugpy
from inputs.artery.conftest import get_test_case_paths
from inputs.artery.from_logs.main_loader import pull_artery_data
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs
from inputs.artery.from_logs.timestamps import extract_time_stamps, visualize_time_stamps

if TYPE_CHECKING:
    from inputs.artery.artery_format import ArteryData, TimeStamps


def manual_data_analysis() -> None:
    """Manual testing by plotting data"""
    artery_data_raw: ArteryData = load_from_artery_logs(file_paths=get_test_case_paths())
    raw_time_stamps: TimeStamps = extract_time_stamps(artery_data=artery_data_raw)
    visualize_time_stamps(time_stamps=raw_time_stamps, additional_heading="Raw time stamps")

    artery_data_timestamps_tidy: ArteryData = pull_artery_data(artery_sim_log=get_test_case_paths())
    tidy_time_stamps: TimeStamps = extract_time_stamps(artery_data=artery_data_timestamps_tidy)
    visualize_time_stamps(time_stamps=tidy_time_stamps, additional_heading="Tidy time stamps")

    # Set breakpoint here to see plots
    pass


if __name__ == "__main__":
    use_debugpy()
    manual_data_analysis()
