# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from src.model_training import *

from utils import *
from src.collect_data import collect_data_from_RSS_feeds
from src.text_cleaning import clean_data

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
    print('Starting to collect data from RSS feeds...')
    collect_data_from_RSS_feeds()

    # Data must be cleaned.
    print('Cleaning the data...')
    clean_data()

    # Then data must be processed. Feature extraction.
    # Features should be stored as a matrix in memory.
    articles = []
    articles_corpus = []
    feeds_json_list = get_list_of_files_in_dir(TODAY_CLEANED_DATA_DIR)
    for json_file_path in feeds_json_list:
        json_content = read_list_from_JSON(os.path.join(TODAY_CLEANED_DATA_DIR, json_file_path))
        feed_articles = []
        for article in json_content:
            new_article = Article(title=article['title'], summary=article['summary'], link=article['link'])
            article_title_and_summary = ' '.join([article['title'], article['summary']])
            feed_articles.append(article_title_and_summary)
            articles.append(new_article)
        articles_corpus.extend(feed_articles)

    vectorizer = TfidfVectorizer(max_df=1.0, stop_words='english', use_idf=True, norm='l2')

    tfidf_matrix = vectorizer.fit_transform(articles_corpus)

    previous_article_features = None
    for article, article_features in zip(articles, tfidf_matrix):
        article.features = article_features.todense()
        previous_article_features = article.features

    # Then we train model with
    # train_model()
    for threshold in range(1, 10, 1):
        threshold = round(threshold * 0.1, 2)
        clusters = build_model(articles, threshold=threshold)

        prepared_model = [cluster.to_dict() for cluster in clusters]
        model_file_name = str(threshold).replace('.', '_') + '.json'
        path_to_model_file = os.path.join(MODELS_DIR, TODAY, model_file_name)
        write_list_to_JSON(prepared_model, path_to_model_file)

    print(f'All processes have been done. Models are built and saved in {TODAY_MODELS_DIR}')
