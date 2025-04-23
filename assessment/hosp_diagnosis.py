from datetime import timedelta
import pandas as pd
import numpy as np
from pathlib import Path


from loguru import logger
from tqdm import tqdm

from assessment.config import ICD_CONDITION_MAP

def create_diagnosis_features(cohort_df, diagnoses_df):
    feature_rows = []
    
    for sid, group in tqdm(cohort_df.groupby('subject_id')):
        patient_diag = diagnoses_df[diagnoses_df['subject_id'] == sid]
        admissions_sorted = group.sort_values('admittime')
        
        if len(admissions_sorted) < 2:
            continue  # no prior admissions to compare with
        
        final_adm = admissions_sorted.iloc[-1]
        prior_adms = admissions_sorted.iloc[:-1]
        final_hadm_id = final_adm['hadm_id']
        final_adm_time = final_adm['admittime']

        prior_diag = patient_diag[patient_diag['hadm_id'].isin(prior_adms['hadm_id'])]
        icd_codes = prior_diag['icd_code'].astype(str)

        # Count Features
        count_prior_adm = len(prior_adms)
        unique_icd = icd_codes.nunique()
        avg_diag_per_adm = prior_diag.groupby('hadm_id')['icd_code'].count().mean()

        # Condition flags
        flags = {f"flag_history_{k}": int(any(icd.startswith(tuple(v)) for icd in icd_codes)) 
                 for k, v in ICD_CONDITION_MAP.items()}
        
        # Longitudinal features
        condition_stats = {}
        for condition, codes in ICD_CONDITION_MAP.items():
            cond_mask = icd_codes.apply(lambda x: any(x.startswith(code) for code in codes))
            relevant_hadm_ids = prior_diag[cond_mask]['hadm_id'].unique()
            condition_stats[f'count_prior_admissions_with_{condition}'] = len(relevant_hadm_ids)
            
            relevant_diag = prior_diag[cond_mask]
            if not relevant_diag.empty:
                merged_dates = relevant_diag.merge(cohort_df[['hadm_id', 'admittime']], on='hadm_id')
                time_first = (final_adm_time - merged_dates['admittime'].min()).days / 365.0
                condition_stats[f'time_since_first_diagnosis_{condition}_years'] = round(time_first, 2)
            else:
                condition_stats[f'time_since_first_diagnosis_{condition}_years'] = np.nan
        
        # Time since last admission
        time_last_discharge = prior_adms['dischtime'].max()
        time_since_last = (final_adm_time - time_last_discharge).days
        one_year_ago = final_adm_time - timedelta(days=365)
        prior_in_last_year = prior_adms[prior_adms['admittime'] >= one_year_ago]

        row = {
            'subject_id': sid,
            'hadm_id': final_hadm_id,
            'count_prior_admissions': count_prior_adm,
            'count_unique_diagnoses_prior': unique_icd,
            'avg_diagnoses_per_prior_admission': avg_diag_per_adm,
            'time_since_last_admission_days': time_since_last,
            'admission_frequency_last_year': len(prior_in_last_year),
            **flags,
            **condition_stats
        }
        
        feature_rows.append(row)

    return pd.DataFrame(feature_rows)
