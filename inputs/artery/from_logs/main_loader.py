from inputs.artery.artery_format import ArterySimLog, ArterySimLogDump
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs
from inputs.artery.from_logs.timestamps import tidy_up_timestamps
from inputs.artery.from_logs.transform_coordinates import transform_to_local_metric_coords


def pull_artery_sim_log(artery_sim_log_dump: ArterySimLogDump) -> ArterySimLog:
    artery_sim_log: ArterySimLog = load_from_artery_logs(sim_log_dump=artery_sim_log_dump)
    artery_sim_log = transform_to_local_metric_coords(artery_sim_log=artery_sim_log)
    artery_sim_log = tidy_up_timestamps(artery_sim_log=artery_sim_log)
    return artery_sim_log
