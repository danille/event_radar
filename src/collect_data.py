# -*- coding: utf-8 -*-
import os
import re

import feedparser as fp
import pandas as pd

from utils import EXTERNAL_DATA_DIR, RAW_DATA_DIR, TODAY, make_dir, write_list_to_JSON


# This module provides function for data collection from RSS feeds.
# Presented here function allows to parse RSS feeds, providing their URL,
# and save parsed data to JSON files as a
#


def get_feeds_list(path_to_file: str) -> list:
    excel = pd.read_excel(path_to_file)
    rss = excel['RSS']
    return rss


def parse_feed(feed_url: str) -> list:
    d = fp.parse(feed_url)
    entries = []
    for entry in d.entries:

        entry_title_ = entry['title']
        entry_link_ = entry['link']
        entry_dict = {'title': entry_title_,
                      'link': entry_link_}
        try:
            entry_summary_ = entry['summary']
            entry_dict['summary'] = entry_summary_
        except KeyError:
            print(f'Unable to get summary field from article with title {entry_title_}')
        entries.append(entry_dict)
    return entries


def get_feed_title_from_url(feed_url: str) -> str:
    """
    This function allows to obtain RSS feed's title from it's URL, via parsing URL with regex.
    :param feed_url: RSS feed's URL, which title should be extracted
    :return: title of RSS feed
    """
    feed_title = str(re.search(r"//[w\d.]*([\S][^/]+)", feed_url).group(1))
    return feed_title


def collect_data_from_RSS_feeds():
    path_to_rss = os.path.join(EXTERNAL_DATA_DIR, 'feeds.xlsx')
    rss_urls = get_feeds_list(path_to_rss)
    for rss_url in rss_urls:
        print(f'Collecting data from {rss_url}')
        feed = parse_feed(rss_url)

        make_dir(os.path.join(RAW_DATA_DIR, TODAY))

        feed_title = get_feed_title_from_url(rss_url)
        feed_file_name = feed_title + '.json'
        json_file_path = os.path.join(RAW_DATA_DIR, TODAY, feed_file_name)

        write_list_to_JSON(feed, json_file_path)
