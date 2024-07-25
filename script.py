import os
import pandas as pd
import json
from tqdm import tqdm
import argparse
import numpy as np

def clean_name(first_name, last_name, full_name):
    if pd.isna(first_name) and pd.isna(last_name) and pd.isna(full_name):
        return "", ""

    if last_name == '0':
        last_name = ''

    if first_name == '0' or not first_name:
        names = full_name.split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

    return first_name, last_name

def generate_attributes(row):
    attributes = {
        "timezone": row.get('Timezone', np.nan),
        "ip_address": row.get('IP Address', np.nan),
        "conference": row.get('Conference', np.nan),
        "tag": row.get('Tag', np.nan),
        "username": row.get('Username', np.nan),
        "tags": row.get('Tags', np.nan)
    }
    # Remove keys with NaN values
    attributes = {k: v for k, v in attributes.items() if not pd.isna(v)}
    return json.dumps(attributes)

def split_dataframe(df, num_splits):
    chunk_size = int(np.ceil(len(df) / num_splits))
    return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

def save_splitted_files(dfs, base_filename):
    for i, df in enumerate(dfs):
        df.to_csv(f"{base_filename}_part_{i + 1}.csv", index=False)

def process_files(directory, split=None):
    combined_data = []

    files = [f for f in os.listdir(directory) if f.endswith(".csv")]

    for filename in tqdm(files, desc="Processing files"):
        file_path = os.path.join(directory, filename)

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        df_subscribed = df[df["Subscribed"] == True]

        for _, row in df_subscribed.iterrows():
            first_name, last_name = clean_name(row['First Name'], row['Last Name'], row['Full Name'])
            name = f"{first_name} {last_name}".strip()
            email = row['Email Address']
            attributes_json = generate_attributes(row)

            combined_data.append([email, name, attributes_json])

    combined_df = pd.DataFrame(combined_data, columns=['email', 'name', 'attributes'])

    if split and split > 0:
        split_dfs = split_dataframe(combined_df, split)
        save_splitted_files(split_dfs, "combined-exported-leads")
    else:
        combined_df.to_csv("combined-exported-leads.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and combine CSV files.")
    parser.add_argument("--split", type=int, default=None,
                        help="Number of files to split the combined CSV into.")
    args = parser.parse_args()
    export_directory = "export"
    process_files(export_directory, args.split)