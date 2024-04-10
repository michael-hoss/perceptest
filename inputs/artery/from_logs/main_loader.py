from inputs.artery.artery_format import ArteryData, ArterySimLog
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs
from inputs.artery.from_logs.timestamps import tidy_up_timestamps
from inputs.artery.from_logs.transform_coordinates import transform_to_local_metric_coords


def pull_artery_data(artery_sim_log: ArterySimLog) -> ArteryData:
    artery_data: ArteryData = load_from_artery_logs(file_paths=artery_sim_log)
    artery_data = transform_to_local_metric_coords(artery_data=artery_data)
    artery_data = tidy_up_timestamps(artery_data=artery_data)
    return artery_data
