import json
import os
from datetime import datetime

TODAY = datetime.now().strftime('%Y-%m-%d')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, 'external')
CLEANED_DATA_DIR = os.path.join(DATA_DIR, 'cleaned')
SRC_DIR = os.path.join(BASE_DIR, 'src')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
TODAY_RAW_DATA_DIR = os.path.join(RAW_DATA_DIR, TODAY)
TODAY_CLEANED_DATA_DIR = os.path.join(CLEANED_DATA_DIR, TODAY)


def make_dir(path):
    """
    Creates directory at specified path, if it does not already exist.
    :param path: absolute path to dir which should be created
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)


def write_list_to_JSON(list_of_objects, path_to_json: str) -> None:
    with open(path_to_json + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(list_of_objects, json_file)


def read_list_from_JSON(path_to_json: str) -> list:
    with open(path_to_json, mode='r') as json_file:
        json_content = json.load(json_file)
    return json_content


def get_list_of_files_in_dir(path_to_dir: str) -> list:
    return [filename for filename in os.listdir(path_to_dir) if
            os.path.isfile(os.path.join(path_to_dir, filename))]
