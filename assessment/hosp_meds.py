from datetime import timedelta
import pandas as pd
import numpy as np
from pathlib import Path


from loguru import logger
from tqdm import tqdm

from assessment.config import DRUG_CLASS_MAP


def create_meds_features(cohort_df, prescriptions_df):
    feature_rows = []

    # Ensure datetime columns are correct
    prescriptions_df['starttime'] = pd.to_datetime(prescriptions_df['starttime'], errors='coerce')
    prescriptions_df['stoptime'] = pd.to_datetime(prescriptions_df['stoptime'], errors='coerce')

    for sid, group in tqdm(cohort_df.groupby('subject_id')):
        patient_presc = prescriptions_df[prescriptions_df['subject_id'] == sid].copy()
        group = group.sort_values('admittime')

        # Identify final admission
        final_admission = group.sort_values('admittime').iloc[-1]
        final_hadm = final_admission['hadm_id']
        final_admit_time = final_admission['admittime']

        # Admissions before final one
        prior_admits = group[group['admittime'] < final_admit_time]['hadm_id'].values
        prior_presc = patient_presc[patient_presc['hadm_id'].isin(prior_admits)]

        feature = {
            'subject_id': sid,
            'count_prior_prescriptions': len(prior_presc),
            'count_unique_drugs_prior': prior_presc['drug'].nunique(),
            'avg_drugs_per_prior_admission': (
                prior_presc.groupby('hadm_id')['drug'].nunique().mean() if len(prior_admits) > 0 else 0
            ),
        }

        # Flags for drug classes
        drug_list = prior_presc['drug'].str.lower().dropna().unique()
        for drug_class, keywords in DRUG_CLASS_MAP.items():
            match = any(any(kw in drug for kw in keywords) for drug in drug_list)
            feature[f'flag_history_on_{drug_class}'] = int(match)

            matched_hadm = prior_presc[
                prior_presc['drug'].str.lower().str.contains('|'.join(keywords), na=False)
            ]['hadm_id'].unique()
            feature[f'count_prior_admissions_on_{drug_class}'] = len(matched_hadm)

        # Flag for drug class in last prior admission
        if len(prior_admits) > 0:
            last_admit = group[group['admittime'] < final_admit_time].sort_values('admittime').iloc[-1]
            last_presc = patient_presc[patient_presc['hadm_id'] == last_admit['hadm_id']]
            last_steroids = last_presc['drug'].str.lower().str.contains('|'.join(DRUG_CLASS_MAP['steroids']), na=False).any()
            feature['flag_on_steroids_last_prior_admission'] = int(last_steroids)
        else:
            feature['flag_on_steroids_last_prior_admission'] = 0

        feature_rows.append(feature)

    return pd.DataFrame(feature_rows)
