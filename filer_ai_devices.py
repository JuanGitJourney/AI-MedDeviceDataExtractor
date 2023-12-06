import re
import pandas as pd
import os
from extract_ai_metadata import copy_aiml_htmls, copy_csv_rows


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