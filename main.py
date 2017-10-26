from utils import *
from src.collect_data import collect_data_from_RSS_feeds


def prepare_structure():
    for directory in [DATA_DIR, CLEANED_DATA_DIR, EXTERNAL_DATA_DIR, RAW_DATA_DIR]:
        make_dir(directory)


if __name__ == '__main__':
    # First we want prepare projects dirs to make project clearer.
    # We want obtain the structure like this:
    #  |-data
    #  |  |-external
    #  |  |      |----portals.xls
    #  |  |-raw
    #  |  |
    #  |  |-cleaned
    #  |  |
    #  |   \_features
    #  |
    #  |---src
    #  |    |--collect_data.py
    #  |    |--extract_features.py
    #  |    |--train_model.py
    #  |
    #  |---requirements.txt

    prepare_structure()
    # Next step - data collecting. Take list of feeds and collect articles
    # Articles from particular portal will be saved in appropriate JSON file
    collect_data_from_RSS_feeds()

    # Then data must be processed. Feature extraction.
    # Features should be stored as a matrix in memory.
    # extract_features()

    # Then we train model with
    # train_model()
