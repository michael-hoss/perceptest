from os import getenv

from inputs.artery.to_nuscenes.to_nuscenes_constants import ArteryConstants
from inputs.nuscenes.nuscenes_format import TrackingSubmission

NUSCENES_EVAL_CONFIG_PATH = ArteryConstants().nuscenes_eval_config_path
NUSCENES_OUT_RESULTS_FILE = TrackingSubmission.json_filename
NUSCENES_METRICS_OUTPUT_DIR = "tracking_metrics"
NUSCENES_DATAROOT = getenv("NUSCENES", "/data/sets/KIT_V2X/v6/nuscenes_conversion/")
