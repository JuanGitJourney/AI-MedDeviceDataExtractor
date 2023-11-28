import os.path

import pandas as pd
import re
import numpy as np


def get_classification_features(product_code) -> dict:
    classification_df = pd.read_csv('raw_files/foiclass.csv',  delimiter='|')
    device_class = classification_df[classification_df['PRODUCTCODE'] == product_code]['DEVICECLASS'].iloc[0]
    medical_speciality = classification_df[classification_df['PRODUCTCODE'] == product_code]['MEDICALSPECIALTY'].iloc[0]
    third_party_review = classification_df[classification_df['PRODUCTCODE'] == product_code]['THIRDPARTYFLAG'].iloc[0]
    gmp_exempt_flag = classification_df[classification_df['PRODUCTCODE'] == product_code]['GMPEXEMPTFLAG'].iloc[0]
    implant_flag = classification_df[classification_df['PRODUCTCODE'] == product_code]['Implant_Flag'].iloc[0]
    life_sustain_flag = classification_df[classification_df['PRODUCTCODE'] == product_code]['Life_Sustain_support_flag'].iloc[0]
    target_area = classification_df[classification_df['PRODUCTCODE'] == product_code]['TARGETAREA'].iloc[0]
    technical_method = classification_df[classification_df['PRODUCTCODE'] == product_code]['TECHNICALMETHOD'].iloc[0]
    physical_state = classification_df[classification_df['PRODUCTCODE'] == product_code]['PHYSICALSTATE'].iloc[0]
    definition = classification_df[classification_df['PRODUCTCODE'] == product_code]['DEFINITION'].iloc[0]

    return {
        'Device Class': device_class,
        'Medical Specialty': medical_speciality,
        'Third Party Review': third_party_review,
        'GMP Exempt Flag': gmp_exempt_flag,
        'Implant Flag': implant_flag,
        'Life Sustain/Support Flag': life_sustain_flag,
        'Target Area': target_area,
        'Technical Method': technical_method,
        'Physical State': physical_state,
        'Definition': definition
    }


def get_study_features():
    device_features = []
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
                classification_features = get_classification_features(product_code.upper())
                device_features.append(classification_features)  # Storing the entire dictionary
                product_codes.append(product_code)
                device_list.append(device)

    df = pd.DataFrame({
        'query_id': device_list,
        'product_code': product_codes,
        'device_class': [feature['Device Class'] for feature in device_features],
        'medical_specialty': [feature['Medical Specialty'] for feature in device_features],
        'third_party_review': [feature['Third Party Review'] for feature in device_features],
        'gmp_exempt_flag': [feature['GMP Exempt Flag'] for feature in device_features],
        'implant_flag': [feature['Implant Flag'] for feature in device_features],
        'life_sustain_flag': [feature['Life Sustain/Support Flag'] for feature in device_features],
        'target_area': [feature['Target Area'] for feature in device_features],
        'technical_method': [feature['Technical Method'] for feature in device_features],
        'physical_state': [feature['Physical State'] for feature in device_features],
        'definition': [feature['Definition'] for feature in device_features]

    })

    df.to_csv('aiml_dfs/features/devices_features.csv', index=False)
