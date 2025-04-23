from datetime import timedelta
import pandas as pd
import numpy as np
from pathlib import Path


from loguru import logger
from tqdm import tqdm

from assessment.config import PROCEDURE_ICD_MAP


def create_procedures_features(cohort_df, procedures_df):
    feature_rows = []
    admissions_df = cohort_df.copy()

    for sid, group in tqdm(admissions_df.groupby('subject_id')):
        patient_proc = procedures_df[procedures_df['subject_id'] == sid]
        admissions_sorted = group.sort_values('admittime')

        if len(admissions_sorted) < 2:
            continue

        final_adm = admissions_sorted.iloc[-1]
        prior_adms = admissions_sorted.iloc[:-1]
        final_hadm_id = final_adm['hadm_id']
        final_adm_time = final_adm['admittime']

        prior_proc = patient_proc[patient_proc['hadm_id'].isin(prior_adms['hadm_id'])]
        proc_codes = prior_proc['icd_code'].astype(str)

        # Count features
        count_proc = len(proc_codes)
        count_unique_proc = proc_codes.nunique()
        count_adm_with_proc = prior_proc['hadm_id'].nunique()

        # Specific procedure flags
        flags = {f"flag_history_{k}": int(any(code.startswith(tuple(v)) for code in proc_codes))
                 for k, v in PROCEDURE_ICD_MAP.items()}

        # Longitudinal: time since last major surgery
        major_surg_codes = PROCEDURE_ICD_MAP['major_surgery']
        major_surg_mask = proc_codes.apply(lambda x: any(x.startswith(code) for code in major_surg_codes))
        prior_major_surg = prior_proc[major_surg_mask]
        if not prior_major_surg.empty:
            merged_dates = prior_major_surg.merge(admissions_df[['hadm_id', 'admittime']], on='hadm_id')
            time_since_major_surg = (final_adm_time - merged_dates['admittime'].max()).days / 365.0
        else:
            time_since_major_surg = np.nan

        # Flag: procedure in last prior admission
        last_prior_adm = prior_adms.iloc[-1]['hadm_id']
        had_proc_last_adm = int(last_prior_adm in prior_proc['hadm_id'].unique())

        row = {
            'subject_id': sid,
            'hadm_id': final_hadm_id,
            'count_prior_procedures': count_proc,
            'count_unique_procedures_prior': count_unique_proc,
            'count_prior_admissions_with_procedure': count_adm_with_proc,
            'time_since_last_major_surgery_years': round(time_since_major_surg, 2) if pd.notnull(time_since_major_surg) else np.nan,
            'flag_procedure_in_last_prior_admission': had_proc_last_adm,
            **flags
        }

        feature_rows.append(row)

    return pd.DataFrame(feature_rows)
