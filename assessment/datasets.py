from pathlib import Path

from loguru import logger
from tqdm import tqdm

import pandas as pd

from assessment.config import (
    PROCESSED_DATA_DIR, RAW_DATA_DIR, INTERIM_DATA_DIR, ADMISSIONS_PATH, PATIENTS_PATH, DIAGNOSES_ICD_PATH,
    PROCEDURES_ICD_PATH, LABEVENTS_PATH, D_LABITEMS_PATH, PRESCRIPTIONS_PATH
)


def load_admissions_data() -> pd.DataFrame:
    """
    Load admissions data from the specified path.
    """
    logger.info(f"Loading admissions data from {ADMISSIONS_PATH}")
    df = pd.read_csv(ADMISSIONS_PATH)
    logger.info(f"Loaded {len(df)} rows of admissions data.")
    return df


def load_patients_data() -> pd.DataFrame:
    """
    Load patients data from the specified path.
    """
    logger.info(f"Loading patients data from {PATIENTS_PATH}")
    df = pd.read_csv(PATIENTS_PATH)
    logger.info(f"Loaded {len(df)} rows of patients data.")
    return df


def load_cohort_data() -> pd.DataFrame:
    """
    Load cohort data from the specified path.
    """
    logger.info(f"Loading cohort data from {INTERIM_DATA_DIR}/cohort.csv")
    df = pd.read_csv(f"{INTERIM_DATA_DIR}/cohort.csv")
    logger.info(f"Loaded {len(df)} rows of cohort data.")
    return df


def load_diagnoses_data() -> pd.DataFrame:
    """
    Load diagnoses data from the specified path.
    """
    logger.info(f"Loading diagnoses data from {DIAGNOSES_ICD_PATH}")
    df = pd.read_csv(DIAGNOSES_ICD_PATH)
    logger.info(f"Loaded {len(df)} rows of diagnoses data.")
    return df

def load_procedures_data() -> pd.DataFrame:
    """
    Load procedures data from the specified path.
    """
    logger.info(f"Loading procedures data from {PROCEDURES_ICD_PATH}")
    df = pd.read_csv(PROCEDURES_ICD_PATH)
    logger.info(f"Loaded {len(df)} rows of procedures data.")
    return df

def load_labevents_data(usecols = ['subject_id', 'hadm_id', 'itemid', 'charttime', 'valuenum']) -> pd.DataFrame:
    """
    Load labevents data from the specified path.
    """
    logger.info(f"Loading labevents data from {LABEVENTS_PATH}")
    df = pd.read_csv(LABEVENTS_PATH, usecols=usecols, nrows=100000)
    logger.info(f"Loaded {len(df)} rows of labevents data.")
    return df

def load_d_labitems_data() -> pd.DataFrame:
    """
    Load d_labitems data from the specified path.
    """
    logger.info(f"Loading d_labitems data from {D_LABITEMS_PATH}")
    df = pd.read_csv(D_LABITEMS_PATH)
    logger.info(f"Loaded {len(df)} rows of d_labitems data.")
    return df

def load_prescriptions_data(usecols = ['hadm_id', 'drug', 'route', 'starttime', 'stoptime']) -> pd.DataFrame:
    """
    Load prescriptions data from the specified path.
    """
    logger.info(f"Loading prescriptions data from {PRESCRIPTIONS_PATH}")
    df = pd.read_csv(PRESCRIPTIONS_PATH)
    logger.info(f"Loaded {len(df)} rows of prescriptions data.")
    return df