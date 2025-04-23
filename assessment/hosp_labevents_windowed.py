from datetime import timedelta
import pandas as pd
import numpy as np
from collections import defaultdict
from pathlib import Path

import os


from loguru import logger
from tqdm import tqdm

from assessment.config import LAB_ITEM_ID_MAP, LAB_KEYWORDS, ANEMIA_THRESH, HYPONATREMIA_THRESH, AKI_RISE_THRESH
from assessment.datasets import load_d_labitems_data
from assessment.hosp_labevents import identify_itemids_from_d_labelitems

# Thresholds for conditions
HGB_LOW = 10  # g/dL
NA_CRIT_LOW = 120  # mEq/L
AKI_DELTA = 0.3  # mg/dL rise in creatinine

# Let's re-import required packages since execution state has been reset
def create_longitudinal_lab_features(cohort_df, labevents_path, lab_keywords = LAB_KEYWORDS, 
                                     window_days=[365, 180, 90, 30, 7], chunksize=100000):
    """
    Generates longitudinal lab features from labevents in defined time windows prior to final admission.
    """

    d_labelitems_df, lab_to_itemids = identify_itemids_from_d_labelitems(lab_keywords)
    lab_itemid_map = {row['itemid']: row['label'] for _, row in d_labelitems_df.iterrows()}

    # Precompute cohort metadata
    cohort_subjects = cohort_df['subject_id'].unique()

    cohort_df['admittime'] = pd.to_datetime(cohort_df['admittime'], errors='coerce')
    final_admit_time = cohort_df.groupby('subject_id')['admittime'].max().to_dict()

    # Create time boundaries for each subject per window
    time_boundaries = {
        sid: {days: final_admit_time[sid] - timedelta(days=days) for days in window_days}
        for sid in cohort_subjects
    }

    # Initialize data stores
    lab_stats = {days: defaultdict(lambda: defaultdict(list)) for days in window_days}
    last_lab_values = {days: defaultdict(dict) for days in window_days}
    abnormal_counts = {days: defaultdict(lambda: defaultdict(int)) for days in window_days}

    # Map itemid to lab name (handle duplicates)
    itemid_to_lab = {}
    for iid, lname in lab_itemid_map.items():
        itemid_to_lab.setdefault(iid, lname)

    reader = pd.read_csv(labevents_path, chunksize=chunksize)
    for chunk in tqdm(reader, desc="Processing labevents in chunks"):
        chunk = chunk[chunk['subject_id'].isin(cohort_subjects)]
        chunk = chunk[chunk['itemid'].isin(itemid_to_lab.keys())]
        chunk['charttime'] = pd.to_datetime(chunk['charttime'], errors='coerce')
        chunk = chunk.dropna(subset=['charttime', 'valuenum'])

        for _, row in chunk.iterrows():
            sid = row['subject_id']
            charttime = row['charttime']
            val = row['valuenum']
            lab_name = itemid_to_lab.get(row['itemid'], None)
            if lab_name is None:
                continue

            for days in window_days:
                if charttime >= time_boundaries[sid][days]:
                    lab_stats[days][sid][lab_name].append(val)

                    # last value
                    curr_last = last_lab_values[days][sid].get(lab_name, (pd.Timestamp.min, np.nan))
                    if charttime > curr_last[0]:
                        last_lab_values[days][sid][lab_name] = (charttime, val)

                    # abnormality tracking
                    if lab_name == 'hemoglobin' and val < ANEMIA_THRESH:
                        abnormal_counts[days][sid]['chronic_anemia'] += 1
                    if lab_name == 'sodium' and val < HYPONATREMIA_THRESH:
                        abnormal_counts[days][sid]['severe_hyponatremia'] += 1
                    if lab_name == 'creatinine' and val >= AKI_RISE_THRESH:
                        abnormal_counts[days][sid]['chronic_kidney_disease'] += 1
    
    logger.info("Aggregating lab features for each time window")
    # Print len of lab_stats
    for days in window_days:
        logger.info(f"Window {days} days: {len(lab_stats[days])} subjects with lab data")
        logger.info(f"Window {days} days: {len(last_lab_values[days])} subjects with last lab values")
        logger.info(f"Window {days} days: {len(abnormal_counts[days])} subjects with abnormal counts")
        logger.info("-" * 50)
        

    # Aggregate features
    feature_rows = []
    for sid in cohort_subjects:
        row = {'subject_id': sid}
        for days in window_days:
            prefix = f'window_{days}d'
            labs = lab_stats[days].get(sid, {})

            row[f'{prefix}_count_labevents'] = sum(len(vals) for vals in labs.values())
            row[f'{prefix}_count_unique_labs'] = len(labs)

            for lab, values in labs.items():
                row[f'{prefix}_{lab}_avg'] = np.mean(values)
                row[f'{prefix}_{lab}_min'] = np.min(values)
                row[f'{prefix}_{lab}_max'] = np.max(values)
                row[f'{prefix}_{lab}_std'] = np.std(values)

            for lab in set(itemid_to_lab.values()):
                row[f'{prefix}_last_{lab}'] = last_lab_values[days][sid].get(lab, (None, np.nan))[1]

            # abnormal counts
            row[f'{prefix}_count_severe_hyponatremia'] = abnormal_counts[days][sid].get('severe_hyponatremia', 0)
            row[f'{prefix}_flag_chronic_anemia'] = int(abnormal_counts[days][sid].get('chronic_anemia', 0) >= 2)

        feature_rows.append(row)

    return pd.DataFrame(feature_rows)
