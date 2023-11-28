import os.path

import pandas as pd
import re
import numpy as np


def get_device_class(product_code) -> int:
    classification_df = pd.read_csv('raw_files/foiclass.csv',  delimiter='|')
    device_class = classification_df[classification_df['PRODUCTCODE'] == product_code]['DEVICECLASS'].iloc[0]

    return device_class


def get_study_features():
    device_classes = []
    device_list = []
    product_codes = []


    input_csvs = ['aiml_dfs/aiml_501ks.csv', 'aiml_dfs/aiml_pmas.csv']

    for index, i_csv in enumerate(input_csvs):
        # Set product code column name according to file
        if i_csv == 'aiml_dfs/aiml_501ks.csv':
            search_term = 'classification_product_code'
        else:
            search_term = 'product_code'

        if os.path.getsize(input_csvs[index]) > 5:
            df = pd.read_csv(input_csvs[index])
            names_list = df['query_id'].tolist()

            for device in names_list:
                product_code = df[df['query_id'] == device][search_term].iloc[0]

                device_classes.append(get_device_class(product_code.upper()))
                product_codes.append(product_code)
                device_list.append(device)

    print(len(device_classes))
    df = pd.DataFrame({
        'query_id': device_list,
        'product_code': product_codes,
        'device_class': device_classes
    })
    df.to_csv('aiml_dfs/features/devices_classes.csv', index=False)
