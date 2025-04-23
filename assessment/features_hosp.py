from pathlib import Path
import pandas as pd
import numpy as np

from loguru import logger
from tqdm import tqdm

from assessment.config import PROCESSED_DATA_DIR, LAB_KEYWORDS, INTERIM_DATA_DIR, FILTER_OVER_AGE_18
from assessment.datasets import load_admissions_data, load_patients_data, load_d_labitems_data



def preprocess_admissions_data(admissions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the admissions data.
    """
    # Convert admit time and discharge time to datetime
    admissions_df['admittime'] = pd.to_datetime(admissions_df['admittime'])
    admissions_df['dischtime'] = pd.to_datetime(admissions_df['dischtime'])

    # Remove columns where admit time and discharge time are null
    admissions_df = admissions_df.dropna(subset=['admittime', 'dischtime'])

    # Remove rows where the discharge time is before the admit time
    admissions_df = admissions_df[admissions_df['dischtime'] >= admissions_df['admittime']]

    # Create a new column for the length of stay (LOS) in hours
    admissions_df['los'] = pd.to_timedelta(admissions_df["dischtime"] - admissions_df["admittime"], unit='h')
    admissions_df['los'] = admissions_df['los'].astype(str)
    admissions_df[['days', 'dummy','hours']] = admissions_df['los'].str.split(' ', expand=True)
    admissions_df['los']=pd.to_numeric(admissions_df['days'])
    admissions_df=admissions_df.drop(columns=['days', 'dummy','hours'])

    return admissions_df

def preprocess_patients_data(patients_df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the patients data.
    """
    # Convert anchor_year to datetime
    patients_df['year_of_birth']= patients_df['anchor_year'] - patients_df['anchor_age']  # get yob to ensure a given visit is from an adult
    patients_df['min_valid_year'] = patients_df['anchor_year'] + (2019 - patients_df['anchor_year_group'].str.slice(start=-4).astype(int))

    # Create a new column for the age
    patients_df['age'] = patients_df['anchor_age']

    # Clip any age < 0 (data noise)
    patients_df['age'] = patients_df['age'].clip(lower=0)

    return patients_df

def process_cohort(merged_df: pd.DataFrame) -> pd.DataFrame:

    """Applies labels to individual visits according to whether or not a death has occurred within
    the times of the specified admit_col and disch_col"""

    cohort = merged_df.loc[(~merged_df["admittime"].isna()) & (~merged_df["dischtime"].isna())]
    
    cohort['label'] = 0
    cohort['time_to_death'] = 0

    pos_cohort=cohort[~cohort["dod"].isna()]
    neg_cohort=cohort[cohort["dod"].isna()]
    neg_cohort=neg_cohort.fillna(0)
    pos_cohort=pos_cohort.fillna(0)
    pos_cohort["dod"] = pd.to_datetime(pos_cohort["dod"])

    pos_cohort['label'] = np.where((pos_cohort["dod"] >= pos_cohort["admittime"]) & (pos_cohort["dod"] <= pos_cohort["dischtime"]),1,0)
    pos_cohort['time_to_death'] = pd.to_timedelta(pos_cohort['dod'] - pos_cohort['admittime']).dt.total_seconds() / (3600 * 24)
    
    pos_cohort['label'] = pos_cohort['label'].astype("Int32")
    cohort=pd.concat([pos_cohort,neg_cohort], axis=0)

    cohort=cohort.sort_values(by=["subject_id","admittime"])

    logger.info(f"Positive cohort size: {cohort[cohort['label']==1].shape[0]}")
    logger.info(f"Negative cohort size: {cohort[cohort['label']==0].shape[0]}")
    logger.info(f"Total cohort size: {len(cohort)}")


    # Extract subject ids where label = 1
    subject_ids = cohort[cohort['label'] == 1]['subject_id'].unique()
    # Filter cohort to only include data for these subject ids
    cohort = cohort[cohort['subject_id'].isin(subject_ids)] 

    logger.info(f"Filtered cohort size with patiends that have died eventually: {len(cohort)}")

    # Keep only relevant columns:
    cohort = cohort[['subject_id', 'hadm_id', 'admittime', 'dischtime', 'age', 'gender', 'race', 'insurance', 'label', 
                     'dod', 'time_to_death','admission_type','admission_location','discharge_location']]

    return cohort

def prepare_cohort(filter_over_age_18 = FILTER_OVER_AGE_18) -> pd.DataFrame:

    '''
    Prepare the base dataframe by loading, preprocessing, and merging admissions and patients data.
    '''

    # use above functions to load data
    admissions_df = load_admissions_data()
    patients_df = load_patients_data()

    logger.info(f"Loaded {len(admissions_df)} rows of admissions data.")
    logger.info(f"Loaded {len(patients_df)} rows of patients data.")

    # Preprocess admissions data
    admissions_df = preprocess_admissions_data(admissions_df)
    logger.info(f"Preprocessed admissions data has {len(admissions_df)} rows.")

    # Preprocess patients data
    patients_df = preprocess_patients_data(patients_df)
    logger.info(f"Preprocessed patients data has {len(patients_df)} rows.")

    # Filter patients over 18 years old
    if filter_over_age_18:
        patients_df = patients_df[patients_df['anchor_age'] >= 18]
        logger.info(f"Filtered patients data has {len(patients_df)} rows after removing under 18.")    
    
    # Merge patient info into admissions
    merged_df = admissions_df.merge(patients_df, on='subject_id', how='inner')

    logger.info(f"Merged data has {len(merged_df)} rows.")
    logger.info(f"Unique hadm_id: {len(merged_df['hadm_id'].unique())}")
    logger.info(f"Unique subject_id: {len(merged_df['subject_id'].unique())}")

    # Process the merged dataframe
    merged_df = process_cohort(merged_df)

    # Sanity check
    assert merged_df['hadm_id'].is_unique, "hadm_id is not unique, which shouldn't happen at this stage."

    return merged_df


def filter_time_to_death_dataframe(base_df) -> pd.DataFrame:
    """
    Prepare the time to death dataframe using the labels from the merged dataframe. labels = 1 will be filtered. 
    """
    # Filter the dataframe to only include patients that died
    filtered_df = base_df[base_df['label'] == 1].copy()

    # Remove columns that are not needed
    return filtered_df





# def aggregate_procedures(procedures_df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Aggregates procedure data per admission:
#     - Number of unique ICD codes per hadm_id
#     - Binary indicator if any procedure exists
#     """
#     logger.info("Aggregating procedures data")
#     procedures_df = procedures_df.groupby("hadm_id").agg(
#         num_procedures=("icd_code", "nunique"),
#         any_procedure=("icd_code", "size"),
#     ).reset_index()

#     # Rename columns
#     procedures_df.rename(columns={"num_procedures": "num_procedures"}, inplace=True)

#     return procedures_df


# def extract_labs_first_24h(labs_df: pd.DataFrame, final_df: pd.DataFrame, identified_lab_item_ids = pd.DataFrame()) -> pd.DataFrame:

#     # Extracts lab data for the relevant itemids and admissions id
#     logger.info("Extracting lab data for the relevant itemids and admissions id")
#     labs_df = labs_df[labs_df['itemid'].isin(identified_lab_item_ids["itemid"])]
#     labs_df = labs_df[labs_df['hadm_id'].isin(final_df['hadm_id'])]

#     # 3. Merge admittime from final_df

#     logger.info("Merging admittime from final_df")
#     admittime_map = final_df.set_index('hadm_id')['admittime']
#     labs_df['admittime'] = labs_df['hadm_id'].map(admittime_map)
#     labs_df['charttime'] = pd.to_datetime(labs_df['charttime'])
#     labs_df['admittime'] = pd.to_datetime(labs_df['admittime'])
#     labs_df['time_since_admit'] = labs_df['charttime'] - labs_df['admittime']

#     # 4. Filter lab data to first 24 hours
#     logger.info("Filtering lab data to first 24 hours")
#     # Filter lab data to first 24 hour
#     labs_df = labs_df[(labs_df['time_since_admit'] >= pd.Timedelta(0)) &
#                     (labs_df['time_since_admit'] <= pd.Timedelta(days=1))]
    
#     # 5. Get first value per hadm_id + itemid
#     labs_df = labs_df.sort_values(['hadm_id', 'itemid', 'charttime'])
#     first_labs = labs_df.groupby(['hadm_id', 'itemid'])['valuenum'].first().unstack()

#     # 6. Rename columns to human-readable lab names

#     logger.info("Current columns: {}".format(first_labs.columns))
#     # Rename columns to human-readable lab names
#     first_labs.columns = ["first_" + identified_lab_item_ids.loc[identified_lab_item_ids['itemid'] == col, 'label'].values[0] for col in first_labs.columns]
    
    
    
#     logger.info("Renamed columns: {}".format(first_labs.columns))
#     return first_labs


# # Use presciptions to extract relevant medications
# def extract_prescription_features(prescriptions_df: pd.DataFrame, final_df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Extracts relevant medications from prescriptions data
#     """
#     final_df = final_df.copy()

#     logger.info("Extracting relevant medications from prescriptions data")
#     # Filter prescriptions for relevant itemids
#     prescriptions_df = prescriptions_df[prescriptions_df['hadm_id'].isin(final_df['hadm_id'])]
    
#     # Group and aggregate prescriptions data
#     logger.info("Grouping and aggregating prescriptions data")
#     grouped = prescriptions_df.groupby('hadm_id').agg(
#         num_distinct_drugs=('drug', 'nunique'),
#         num_prescriptions=('drug', 'count'),
#         num_routes=('route', 'nunique'),
#     )
#     # Add missing indicator
#     grouped['has_prescriptions'] = 1

#     # Save grouped data to interim file
#     logger.info("Saving grouped prescription data to interim file")
#     OUTPUT_PATH = INTERIM_DATA_DIR / "interim_prescriptions_data.csv"
#     grouped.to_csv(OUTPUT_PATH, index=True)

#     # Merge grouped data with base dataframe
#     logger.info("Merging grouped data with base dataframe")
#     final_df = final_df.merge(grouped, how='left', left_on='hadm_id', right_index=True)
#     final_df['has_prescriptions'] = final_df['has_prescriptions'].fillna(0).astype(int)

#     # Fill NaNs in other features with 0
#     final_df['num_distinct_drugs'] = final_df['num_distinct_drugs'].fillna(0)
#     final_df['num_prescriptions'] = final_df['num_prescriptions'].fillna(0)
#     final_df['num_routes'] = final_df['num_routes'].fillna(0)
    
#     return final_df