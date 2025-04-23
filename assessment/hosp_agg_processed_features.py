from datetime import timedelta
import pandas as pd
import numpy as np
from pathlib import Path


from loguru import logger
from tqdm import tqdm

from assessment.config import PROCESSED_HOSP_DATA_DIR

def process_merge_hosp_data(merged_df):
    # Remove columns with "_x" or "_y" suffix
    merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith(('_x', '_y'))]
    logger.info("Removed columns with '_x' or '_y' suffix")

    return merged_df
       


# Write a function to merge all csvs in a directory on "subject_id and saves it"
def merge_csvs_in_dir(dir_path = PROCESSED_HOSP_DATA_DIR, on = 'subject_id') -> pd.DataFrame:
    """
    Merges all csv files in a directory on the specified column and saves the merged DataFrame to a csv file.
    """
    logger.info(f"Merging csvs in {dir_path} on {on}")
    all_csv_files = list(dir_path.glob("*.csv"))
    logger.info(f"Found {len(all_csv_files)} files to merge")

    # Read all csv files into a list of DataFrames
    merged_data = pd.DataFrame()
    for csv_file_name in all_csv_files:
        
        logger.info(f"Reading {csv_file_name}")
        df = pd.read_csv(csv_file_name)
        if merged_data.empty:
            merged_data = df
        else:
            merged_data = pd.merge(merged_data, df, on=on, how='inner')
    
    logger.info(f"Merged {len(all_csv_files)} files into one DataFrame")

    # Process the merged DataFrame
    merged_data = process_merge_hosp_data(merged_data)
    logger.info("Processed merged data")

    # Save the merged DataFrame to a csv file
    OUTPUT_DIR = PROCESSED_HOSP_DATA_DIR / "../hosp_ttl.csv"
    merged_data.to_csv(OUTPUT_DIR, index=False)
    logger.info(f"Saved merged data to {OUTPUT_DIR}")


    return merged_data