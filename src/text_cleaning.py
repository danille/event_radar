import re
from utils import *


def remove_html_tags(usr_input: str) -> str:
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    no_tags = tag_re.sub('', usr_input)
    return no_tags


def remove_html_special_chars(usr_input: str) -> str:
    html_escape_table = ["&amp;", "&quot;", "&apos;", "&gt;", "&lt;", "&nbsp;", "&#160;"]
    for special_char in html_escape_table:
        usr_input = usr_input.replace(special_char, '')
    return usr_input


def remove_special_chars_from_string(usr_string: str) -> str:
    result = re.sub(r'[()\n]?', '', usr_string)
    return result


def remove_numbers_from_string(usr_string: str) -> str:
    result = re.sub(r'\d+', '', usr_string)
    return result


def clean_data():
    clean_string = lambda x: remove_special_chars_from_string(
        remove_numbers_from_string(remove_html_special_chars(remove_html_tags(x))))
    # First, we have to prepare place where cleaned data can be stored
    make_dir(TODAY_CLEANED_DATA_DIR)

    # Then raw data should be read
    raw_json_list = get_list_of_files_in_dir(TODAY_RAW_DATA_DIR)

    for json_file in raw_json_list:
        json_content = read_list_from_JSON(os.path.join(TODAY_RAW_DATA_DIR, json_file))
        cleaned_articles = []
        for article in json_content:
            cleaned_summary = clean_string(article['summary'])
            cleaned_title = clean_string(article['title'])

            cleaned_article = {'title': cleaned_title,
                               'summary': cleaned_summary,
                               'link': article['link']}
            cleaned_articles.append(cleaned_article)

        write_list_to_JSON(cleaned_articles, os.path.join(TODAY_CLEANED_DATA_DIR, json_file))
