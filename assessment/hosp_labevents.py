import pandas as pd
import numpy as np
from collections import defaultdict
from pathlib import Path

import os


from loguru import logger
from tqdm import tqdm

from assessment.config import LAB_ITEM_ID_MAP, LAB_KEYWORDS, ANEMIA_THRESH, HYPONATREMIA_THRESH, AKI_RISE_THRESH
from assessment.datasets import load_d_labitems_data


# Identify relevant itemids from d_labitems for keywords in LAB_KEYWORDS
def identify_itemids_from_d_labelitems(lab_keywords = LAB_KEYWORDS) -> pd.DataFrame:
    """
    Identify relevant itemids from d_labitems for keywords in LAB_KEYWORDS
    """
    # Load d_labitems data
    d_labelitems_df = load_d_labitems_data()
    logger.info("Loading d_labitems data")

    logger.info("Identifying relevant itemids from d_labitems")
    # Filter d_labitems for relevant itemids
    # d_labelitems_df = d_labelitems_df[d_labelitems_df["label"].str.contains(lab_keywords, case=False, na=False)]
    
    # Make the label lowercase
    d_labelitems_df["label"] = d_labelitems_df["label"].str.lower()
    # Filter d_labitems for relevant itemids
    d_labelitems_df = d_labelitems_df[d_labelitems_df["label"].isin(LAB_KEYWORDS)]
    # Select relevant columns
    d_labelitems_df = d_labelitems_df[["itemid", "label"]]

    lab_to_itemids = defaultdict(list)
    # Create a dictionary to store the labname with all possible itemids that match labname
    for row in d_labelitems_df[["itemid", "label"]].to_dict(orient='records'):
        itemid = row["itemid"]
        labname = row["label"]
        # Add the itemid to the list of itemids for the labname
        lab_to_itemids[labname].append(itemid)
    
    return d_labelitems_df, lab_to_itemids

def create_labsevents_features_chunked(cohort_df, labevents_path, lab_keywords = LAB_KEYWORDS, chunksize=100000):
    """
    labevents_path: Path to labevents.csv
    lab_itemid_map: Dict[itemid] = 'lab_name', e.g., {50912: 'creatinine'}
    """

    d_labelitems_df, lab_to_itemids = identify_itemids_from_d_labelitems(lab_keywords)
    lab_itemid_map = {row['itemid']: row['label'] for _, row in d_labelitems_df.iterrows()}



    # Prepare structures
    cohort_subjects = set(cohort_df['subject_id'])
    final_hadm_map = cohort_df.set_index('subject_id')['hadm_id'].to_dict()


    
    # Collect all prior hadm_ids for each subject
    prior_hadm_lookup = defaultdict(list)
    for sid, group in cohort_df.groupby('subject_id'):
        if sid in final_hadm_map:
            final_admit_time = cohort_df[cohort_df['subject_id'] == sid]['admittime'].iloc[-1]
            prior_admissions = group[group['admittime'] < final_admit_time]
            prior_hadm_lookup[sid] = list(prior_admissions['hadm_id'])


    # Aggregation structures
    lab_stats = defaultdict(lambda: defaultdict(list))                  # sid → lab_name → [values...]
    last_lab_values = defaultdict(dict)                                 # sid → lab_name → (last_time, value)
    lab_abnormal_counts = defaultdict(lambda: defaultdict(int))         # sid → abnormality type → count


    # Estimate number of chunks for progress bar
    file_size_bytes = os.path.getsize(labevents_path)
    num_chunks = (file_size_bytes // (chunksize * 100)) + 1

    # Read in chunks
    logger.info(f"Reading labevents from {labevents_path} in chunks of {chunksize}...")
    for chunk in tqdm(pd.read_csv(labevents_path, chunksize=chunksize), total=num_chunks, desc="Processing Chunks"):
        chunk = chunk[chunk['subject_id'].isin(cohort_subjects)]
        chunk = chunk[chunk['hadm_id'].isin(chunk['subject_id'].map(prior_hadm_lookup).explode())]
        chunk = chunk[chunk['itemid'].isin(d_labelitems_df["itemid"])]
        chunk['charttime'] = pd.to_datetime(chunk['charttime'], errors='coerce')

        

        for _, row in chunk.iterrows():
            sid = row['subject_id']
            hadm_id = row['hadm_id']
            val = row['valuenum']
            itemid = row['itemid']

            lab_name = lab_itemid_map.get(itemid, None)
            if lab_name is None or pd.isna(val):
                continue

            # Stats collection
            lab_stats[sid][lab_name].append(val)

            # Last prior value
            current_last = last_lab_values[sid].get(lab_name, (pd.Timestamp.min, np.nan))
            if row['charttime'] > current_last[0]:
                last_lab_values[sid][lab_name] = (row['charttime'], val)

            # Abnormality flags
            if lab_name == 'hemoglobin' and val < ANEMIA_THRESH:
                lab_abnormal_counts[sid]['chronic_anemia'] += 1
            if lab_name == 'sodium' and val < HYPONATREMIA_THRESH:
                lab_abnormal_counts[sid]['severe_hyponatremia'] += 1
            if lab_name == 'creatinine' and val >= AKI_RISE_THRESH:
                lab_abnormal_counts[sid]['chronic_kidney_disease'] += 1

    logger.info("Aggregating lab events data...")
    logger.info(f"Number of subjects whose lab events were aggregated: {len(lab_stats)}")
    logger.info(f"Number of subjects with last lab values: {len(last_lab_values)}")
    logger.info(f"Number of subjects with abnormal counts: {len(lab_abnormal_counts)}")
    logger.info(f"Number of subjects in cohort: {len(cohort_subjects)}")


    # Final aggregation
    feature_rows = []
    for sid in cohort_subjects:
        row = {'subject_id': sid}
        labs = lab_stats.get(sid, {})
        
        row['count_prior_labevents'] = sum(len(vals) for vals in labs.values())
        row['count_unique_labs_tested_prior'] = len(labs)

        for lab, values in labs.items():
            row[f'{lab}_prior_avg'] = np.mean(values)
            row[f'{lab}_prior_min'] = np.min(values)
            row[f'{lab}_prior_max'] = np.max(values)
            row[f'{lab}_prior_std'] = np.std(values)

        for lab in lab_itemid_map.values():
            last_val = last_lab_values[sid].get(lab, (None, np.nan))[1]
            row[f'last_{lab}_value_prior'] = last_val

        # Abnormal flags
        row['count_prior_severe_hyponatremia'] = lab_abnormal_counts[sid].get('severe_hyponatremia', 0)
        row['flag_chronic_anemia_prior'] = int(lab_abnormal_counts[sid].get('chronic_anemia', 0) >= 2)

        feature_rows.append(row)

    return pd.DataFrame(feature_rows)
