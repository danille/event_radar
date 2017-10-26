import os
from datetime import datetime


TODAY = datetime.now().strftime('%Y-%m-%d')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, 'external')
CLEANED_DATA_DIR = os.path.join(DATA_DIR, 'cleaned')
SRC_DIR = os.path.join(BASE_DIR, 'src')


def make_dir(path):
    """
    Creates directory at specified path, if it does not already exist.
    :param path: absolute path to dir which should be created
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)