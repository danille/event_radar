import pandas as pd
import feedparser as fp
import json
import os
from utils import EXTERNAL_DATA_DIR, RAW_DATA_DIR, TODAY, make_dir


# This module provides function for data collection from RSS feeds.
# Presented here function allows to parse RSS feeds, providing their URL,
# and save parsed data to JSON files as a
#
def get_feeds_list(path_to_file: str) -> list:
    excel = pd.read_excel(path_to_file)
    rss = excel['RSS']
    return rss


def parse_feed(feed_url: str):
    d = fp.parse(feed_url)
    return d


def get_feed_title_from_url(feed_url: str) -> str:
    """
    This function allows to obtain RSS feed's title from it's URL, via parsing URL with regex.
    :param feed_url: RSS feed's URL, which title should be extracted
    :return: title of RSS feed
    """

    
def write_list_to_JSON(list_of_objects, path_to_json: str) -> None:
    with open(path_to_json, 'w') as json_file:
        json.dump(list_of_objects, json_file)


def collect_data_from_RSS_feeds():
    path_to_RSS = os.path.join(EXTERNAL_DATA_DIR, 'feeds.xlsx')
    rss_urls = get_feeds_list(path_to_RSS)
    for rss_url in rss_urls:
        feeds = []
        feed = parse_feed(rss_url)
        feeds.append(feed)

        make_dir(os.path.join(RAW_DATA_DIR, TODAY))

        feed_title = feed.feed.title
        json_file_path = os.path.join(RAW_DATA_DIR, TODAY, feed_title)

        write_list_to_JSON(feeds, json_file_path)
