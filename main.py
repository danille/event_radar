# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer

from utils import *
from src.collect_data import collect_data_from_RSS_feeds
from src.text_cleaning import clean_data


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
    # collect_data_from_RSS_feeds()

    # Data must be cleaned.
    clean_data()

    # Then data must be processed. Feature extraction.
    # Features should be stored as a matrix in memory.
    articles = []
    feeds_json_list = get_list_of_files_in_dir(TODAY_CLEANED_DATA_DIR)
    for json_file_path in feeds_json_list:
        json_content = read_list_from_JSON(os.path.join(TODAY_CLEANED_DATA_DIR, json_file_path))
        feed_articles = []
        for article in json_content:
            article_title_and_summary = ' '.join([article['title'], article['summary']])
            feed_articles.append(article_title_and_summary)
        articles.extend(feed_articles)

    vectorizer = TfidfVectorizer(max_df=1.0, stop_words='english', use_idf=True, norm='l2')

    tfidf_matrix = vectorizer.fit_transform(articles)

    print(tfidf_matrix)
    print(vectorizer.get_feature_names())

    # Then we train model with
    # train_model()
