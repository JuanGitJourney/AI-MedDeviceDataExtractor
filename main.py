import os
import re
import pandas as pd
from download import download_html, get_pma_and_501k_list_from_date, get_website_link
from get_pdfs_from_html_refactored import parse_metadata_from_html
from extract_text_from_pdf import extract_text
from extract_ai_metadata import copy_aiml_htmls, copy_csv_rows
from study_features import get_study_features


def scrap(month, year, htmls_path, pdfs_path_pmas, pdfs_path_501ks, texts_path_pmas, texts_path_501ks):

    # First part: Download HTMLS from the specified date
    approval_numbers = get_pma_and_501k_list_from_date(month, year)
    links = get_website_link(approval_numbers)
    download_html(links, htmls_path)

    # Second part: Pull PDFS from HTMLS
    parse_metadata_from_html(htmls_path, True, month, year)

    # Third part: Extract text from pdfs and store in .txt files
    extract_text(pdfs_path_pmas, texts_path_pmas)
    extract_text(pdfs_path_501ks, texts_path_501ks)


def filter_ai(text_path_pmas, text_path_501ks):
    my_list_pmas = []
    my_list_501ks = []
    ai_words = ['neural network', 'deep learning', 'machine learning', 'artificial intelligence', ' ai ',
                'image recognition', 'pattern recognition']

    for fn in os.listdir(text_path_pmas):
        with open(os.path.join(text_path_pmas, fn), 'r', errors='ignore') as fp:
            text = fp.read()
            text = text.lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            text = re.sub('[^0-9a-zA-Z]+', ' ', text)
            num = fn.split('.')[0]

            for word in ai_words:
                if word in text:
                    my_list_pmas.append(num.upper())
                    break

    unique_identifiers_pmas = list(set(my_list_pmas))
    pd.DataFrame(unique_identifiers_pmas).to_csv('aiml_dfs/aiml_list_pmas.csv')

    for fn in os.listdir(text_path_501ks):
        with open(os.path.join(text_path_501ks, fn), 'r', errors='ignore') as fp:
            text = fp.read()
            text = text.lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            text = re.sub('[^0-9a-zA-Z]+', ' ', text)
            num = fn.split('.')[0]

            for word in ai_words:
                if word in text:
                    my_list_501ks.append(num.upper())
                    break

    unique_identifiers_501k = list(set(my_list_501ks))
    pd.DataFrame(unique_identifiers_501k).to_csv('aiml_dfs/aiml_list_501ks.csv')

    combined_set = set(my_list_pmas).union(set(my_list_501ks))

    # print(f"Devices found: {len(combined_set)}")
    combined_list = list(combined_set)
    pd.DataFrame(combined_list).to_csv('aiml_dfs/aiml_list.csv')

    return combined_list


def extract_metadata(ai_devices, src, dest):
    copy_aiml_htmls(ai_devices, src, dest)
    copy_csv_rows('501k_scrape.csv', 'pmas_scrape.csv',
                  'aiml_dfs/aiml_501ks.csv', 'aiml_dfs/aiml_pmas.csv', ai_devices)


if __name__ == '__main__':
    """
    Main function to execute the workflow.
    """
    month, year = 10, 2018
    htmls_path = 'HTMLS/'
    ai_htmls_path = 'AIML_HTMLS'
    pdfs_pmas_path = 'PDFS_PMAS'
    pdfs_501k_path = 'PDFS_501K'
    texts_pmas_path = 'TEXTS_PMAS'
    texts_501ks_path = 'TEXTS_501K'
    try:
        # Scraping HTML and PDF files
        # scrap(month, year, htmls_path, pdfs_pmas_path, pdfs_501k_path, texts_pmas_path, texts_501ks_path)

        # Filtering AI-related devices from texts
        # ai_devices_list = filter_ai(texts_pmas_path, texts_501ks_path)

        #  Extracting metadata and studying features

        get_study_features()
        print("Process completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
