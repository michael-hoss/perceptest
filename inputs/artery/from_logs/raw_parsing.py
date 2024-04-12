import json
import os
import re
from typing import Literal

from inputs.artery.artery_format import ArteryData, ArteryObject, ArterySimLog, ObjectType


class LineIsListError(json.JSONDecodeError):
    def __init__(self, message="We expect this line to be a json object, not a list"):
        self.message = message
        super().__init__(self.message)


def hacks_to_make_it_work(line: str) -> str:
    line = add_missing_double_quotes(line)
    line = remove_additional_double_quotes(line)
    return line


def remove_additional_double_quotes(line: str) -> str:
    pattern_to_detect_1 = '"uncertainty"=100,"length"=1'
    pattern_to_replace_1 = "uncertainty=100,length=1"
    line = line.replace(pattern_to_detect_1, pattern_to_replace_1)

    pattern_to_detect_2 = '"uncertainty"=0,"length"=1'
    pattern_to_replace_2 = "uncertainty=0,length=1"
    line = line.replace(pattern_to_detect_2, pattern_to_replace_2)

    pattern_to_detect_3 = '"length":1",'
    pattern_to_replace_3 = '"length":1,'
    line = line.replace(pattern_to_detect_3, pattern_to_replace_3)
    return line


def add_missing_double_quotes(line: str) -> str:
    pattern = r'(?<!")(\b\w+\b)(?=:)'  # matches keys that are not enclosed in double quotes
    formatted_json = re.sub(pattern, r'"\1"', line)  # add double quotes to keys that did not have them
    return formatted_json


def load_log_file_raw(full_path: str) -> list[dict]:
    # Obtain list[dict] from the log files
    parsed_data = []
    with open(full_path, "r") as input_file:
        for line in input_file:
            line = hacks_to_make_it_work(line=line)
            try:
                # We have to load json objects line by line
                json_dict = json.loads(line)
                if isinstance(json_dict, list):
                    raise LineIsListError
                parsed_data.append(json_dict)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")

    return parsed_data


def get_object_list_from_parsed_log_of_mv_global(parsed_log: list[dict]) -> list[ArteryObject]:
    # Flatten and put into TypedDict
    artery_object_list: list[ArteryObject] = []
    for datapoint in parsed_log:
        top_level_key = "Motion_Vector_Global" if "Motion_Vector_Global" in datapoint else "State"
        artery_object: ArteryObject = datapoint[top_level_key]
        artery_object_list.append(artery_object)
    return artery_object_list


def load_data_from_log_file(file_path: str, object_type: ObjectType) -> dict[int, list[ArteryObject]]:
    # distinguish between ground truth object id and id given by the tracker under test
    id_key: Literal["idlocal", "id"] = "idlocal" if object_type == ObjectType.UNDER_TEST else "id"

    loaded_log_file = load_log_file_raw(full_path=file_path)
    artery_objects_merged: list[ArteryObject] = get_object_list_from_parsed_log_of_mv_global(parsed_log=loaded_log_file)

    # Disentangle: let each object have its own list
    artery_objects: dict[int, list[ArteryObject]] = {}  # map object ID to trajectory over time
    for individual_object_frame in artery_objects_merged:
        if individual_object_frame["origin"][id_key] not in artery_objects:
            artery_objects[individual_object_frame["origin"][id_key]] = []
        artery_objects[individual_object_frame["origin"][id_key]].append(individual_object_frame)

    return artery_objects


def load_ego_data(file_path: str) -> list[ArteryObject]:
    artery_objects: dict[int, list[ArteryObject]] = load_data_from_log_file(
        file_path=file_path, object_type=ObjectType.EGO
    )
    assert len(artery_objects) == 1, f"Expected only one object in ego file, got {len(artery_objects)}"
    ego_data = list(artery_objects.values())[0]
    return ego_data


def get_name_of_sim_log(file_paths: ArterySimLog) -> str:
    return os.path.basename(file_paths.root_dir)


def load_from_artery_logs(file_paths: ArterySimLog) -> ArteryData:
    # Time stamps are not yet aligned here.
    # Locations are still in WGS84.

    out_list = load_data_from_log_file(
        file_path=os.path.join(file_paths.root_dir, file_paths.out_file), object_type=ObjectType.UNDER_TEST
    )
    res_list = load_data_from_log_file(
        file_path=os.path.join(file_paths.root_dir, file_paths.res_file), object_type=ObjectType.REFERENCE
    )
    ego_info = load_ego_data(file_path=os.path.join(file_paths.root_dir, file_paths.ego_file))

    return ArteryData(
        objects_out=out_list,
        objects_res=res_list,
        ego_vehicle=ego_info,
        timestamps=[],  # timestamps are not yet aligned and are therefore still empty
        name=get_name_of_sim_log(file_paths=file_paths),
    )
