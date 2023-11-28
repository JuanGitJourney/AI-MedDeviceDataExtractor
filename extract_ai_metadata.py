import os
import re
import shutil
import pandas as pd


def copy_aiml_htmls(ai_devices, src, dest):
    # Ensure the destination directory exists
    os.makedirs(dest, exist_ok=True)

    for device in ai_devices:
        source_file = os.path.join(src, f"{device}.html")
        target_file = os.path.join(dest, f"{device}.html")

        if os.path.exists(target_file):
            continue
        else:
            shutil.copy2(source_file, target_file)


def copy_csv_rows(input_501ks_csv, input_pmas_csv, output_501ks_csv, output_pmas_csv, device_classifications):
    input_csvs = [input_501ks_csv, input_pmas_csv]
    output_csvs = [output_501ks_csv, output_pmas_csv]

    # print(len(device_classifications))
    for index, i_csv in enumerate(input_csvs):
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(i_csv)

        # Ensure the desired column exists and then filter the DataFrame based on the device_classifications
        if 'query_id' in df.columns:
            filtered_df = df[df['query_id'].isin(device_classifications)]

            # Only proceed if there are matching rows
            if not filtered_df.empty:
                # Reset the '0' to have a new sequential order
                filtered_df = filtered_df.reset_index(drop=True)
                filtered_df.loc[:, '0'] = filtered_df.index + 1

                # Write the filtered DataFrame to the corresponding new CSV file
                filtered_df.to_csv(output_csvs[index], index=False)
            else:
                print(f"No rows matched the desired device classifications in {i_csv}.")
