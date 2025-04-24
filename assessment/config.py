from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
# logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

PROCESSED_HOSP_DATA_DIR = PROCESSED_DATA_DIR / "hosp/"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Project specific directories

MIMIC_DATA_DIR = RAW_DATA_DIR / "mimiciv/2.1/"
MIMIC_HOSP_DATA_DIR = MIMIC_DATA_DIR / "hosp/"
MIMIC_ICU_DATA_DIR = MIMIC_DATA_DIR / "icu/"

# GENERIC MIMIC IV DATA
ADMISSIONS_PATH = MIMIC_HOSP_DATA_DIR / "admissions.csv"
PATIENTS_PATH = MIMIC_HOSP_DATA_DIR / "patients.csv"

# HOSPITAL SPECIFIC MIMIC IV DATA
DIAGNOSES_ICD_PATH = MIMIC_HOSP_DATA_DIR / "diagnoses_icd.csv"
PROCEDURES_ICD_PATH = MIMIC_HOSP_DATA_DIR / "procedures_icd.csv"
LABEVENTS_PATH = MIMIC_HOSP_DATA_DIR / "labevents.csv"
D_LABITEMS_PATH = MIMIC_HOSP_DATA_DIR / "d_labitems.csv"
PRESCRIPTIONS_PATH = MIMIC_HOSP_DATA_DIR / "prescriptions.csv"

# ICU SPECIFIC MIMIC IV DATA


# DIAGONISIS ICD
ICD_CONDITION_MAP = {
    "CHF_ICD_CODES" : ['428', 'I50'],
    "DIABETES_ICD_CODES" : ['250', 'E08'],
    "CKD_ICD_CODES" : ['585', 'N18'],
    "CANCER_ICD_CODES" : ['140', '141', '142', '143', '144', '145', '146', '147', '148', '149','C00', 'C'],
    "COPD_ICD_CODES" : ['491', '492', '496', 'J44'],
    "LIVER_DISEASE_ICD_CODES" : ['571', 'K7'],
    "MI_ICD_CODES" : ['410', "I21"],
    "STROKE_ICD_CODES" : ['434', '436', 'I630'],
    "SEPSIS_ICD_CODES" : ['99591', '99592', 'A400','A41'],
    "AKI_ICD_CODES" : ['584',"N17"]
}


# PROCEDURES ICD
PROCEDURE_ICD_MAP = {
    'major_surgery': ['361', '352', '815', '8151'],  # e.g., valve surgery, CABG, resections
    'mech_vent': ['967'],  # mechanical ventilation
    'dialysis': ['3995', '5498'],  # dialysis codes
    'biopsy': ['9021', '9022', '9023'],  # biopsy
}

# MEDICATIONS MAP
DRUG_CLASS_MAP = {
    "insulin": ["insulin"],
    "diuretics": ["furosemide", "lasix"],
    "anticoagulants": ["warfarin", "heparin", "apixaban", "rivaroxaban"],
    "steroids": ["prednisone", "methylprednisolone", "dexamethasone"],
    "chemotherapy": ["cyclophosphamide", "doxorubicin", "cisplatin"]
}


# LAB ITEM MAP
LAB_KEYWORDS = [
    'creatinine', # Kidney function marker – elevated levels may indicate AKI or CKD
    'urea nitrogen',
    'lactate', # Marker for tissue hypoperfusion associated with sepsis and shock.
    'white blood',
    'hemoglobin',
    'platelet',
    'hematocrit',
    'sodium',
    'potassium',
    'glucose', # Metabolic status; critical in diabetes and acute illness.
    'bicarbonate',
    'bilirubin',
    'albumin',
    'bun',
    'alt',
    'ast',
]

# MADE FROM
LAB_ITEM_ID_MAP = {
    'glucose': [50809, 50931, 51478, 51981, 52569], 
    'hemoglobin': [50811, 51222, 51640], 
    'lactate': [50813, 52442], 
    'potassium': [50833, 50971, 52610], 
    'albumin': [50862, 53085], 
    'bicarbonate': [50882], 
    'creatinine': [50912, 52546], 
    'sodium': [50983, 52623], 
    'urea nitrogen': [51006, 52647], 
    'hematocrit': [51221, 51480, 51638, 51639, 52028], 
    'bilirubin': [51464, 51966], 
    'wbc': [51516, 52407], 
    'bun': [51842]
}

# LAB ABNORMAL THRESHOLDS
ANEMIA_THRESH= 10
HYPONATREMIA_THRESH = 125
AKI_RISE_THRESH = 0.3


HOSP_COLUMNS_TO_REMOVE = [
    "subject_id",
    "hadm_id",
    "deathtime",
    "dod",
    "dischtime",
    "admittime",
    "admission_type"
    "admission_location",
    "discharge_location",
    "language",
]



# Project specific constants
FILTER_OVER_AGE_18 = True  # Filter out patients under 18 years old

# -------------------------------------------------------------------------
#                      PROCESSED HOSP DATA CONSTANTS
# -------------------------------------------------------------------------

# From diagnoses_icd.csv and d_icd_diagnoses.csv
# Note: d_icd_diagnoses.csv is used to get the label of the diagnoses
DIAGNOSIS_ICD_COLUMNS = [
    'count_prior_admissions',
    'count_unique_diagnoses_prior', 'avg_diagnoses_per_prior_admission',
    'time_since_last_admission_days', 'admission_frequency_last_year',
    'flag_history_CHF_ICD_CODES', 'flag_history_DIABETES_ICD_CODES',
    'flag_history_CKD_ICD_CODES', 'flag_history_CANCER_ICD_CODES',
    'flag_history_COPD_ICD_CODES', 'flag_history_LIVER_DISEASE_ICD_CODES',
    'flag_history_MI_ICD_CODES', 'flag_history_STROKE_ICD_CODES',
    'flag_history_SEPSIS_ICD_CODES', 'flag_history_AKI_ICD_CODES',
    'count_prior_admissions_with_CHF_ICD_CODES',
    'time_since_first_diagnosis_CHF_ICD_CODES_years',
    'count_prior_admissions_with_DIABETES_ICD_CODES',
    'time_since_first_diagnosis_DIABETES_ICD_CODES_years',
    'count_prior_admissions_with_CKD_ICD_CODES',
    'time_since_first_diagnosis_CKD_ICD_CODES_years',
    'count_prior_admissions_with_CANCER_ICD_CODES',
    'time_since_first_diagnosis_CANCER_ICD_CODES_years',
    'count_prior_admissions_with_COPD_ICD_CODES',
    'time_since_first_diagnosis_COPD_ICD_CODES_years',
    'count_prior_admissions_with_LIVER_DISEASE_ICD_CODES',
    'time_since_first_diagnosis_LIVER_DISEASE_ICD_CODES_years',
    'count_prior_admissions_with_MI_ICD_CODES',
    'time_since_first_diagnosis_MI_ICD_CODES_years',
    'count_prior_admissions_with_STROKE_ICD_CODES',
    'time_since_first_diagnosis_STROKE_ICD_CODES_years',
    'count_prior_admissions_with_SEPSIS_ICD_CODES',
    'time_since_first_diagnosis_SEPSIS_ICD_CODES_years',
    'count_prior_admissions_with_AKI_ICD_CODES',
    'time_since_first_diagnosis_AKI_ICD_CODES_years'
]

# From d_labitems.csv and labevents.csv
# Note: d_labitems.csv is used to get the label of the lab tests
LABEVENT_COLUMNS = [
    'count_prior_labevents',
    'count_unique_labs_tested_prior',
    'albumin_prior_avg',
    'albumin_prior_min',
    'albumin_prior_max',
    'albumin_prior_std',
    'bicarbonate_prior_avg',
    'bicarbonate_prior_min',
    'bicarbonate_prior_max',
    'bicarbonate_prior_std',
    'creatinine_prior_avg',
    'creatinine_prior_min',
    'creatinine_prior_max',
    'creatinine_prior_std',
    'potassium_prior_avg',
    'potassium_prior_min',
    'potassium_prior_max',
    'potassium_prior_std',
    'sodium_prior_avg',
    'sodium_prior_min',
    'sodium_prior_max',
    'sodium_prior_std',
    'urea nitrogen_prior_avg',
    'urea nitrogen_prior_min',
    'urea nitrogen_prior_max',
    'urea nitrogen_prior_std',
    'hematocrit_prior_avg',
    'hematocrit_prior_min',
    'hematocrit_prior_max',
    'hematocrit_prior_std',
    'hemoglobin_prior_avg',
    'hemoglobin_prior_min',
    'hemoglobin_prior_max',
    'hemoglobin_prior_std',
    'glucose_prior_avg',
    'glucose_prior_min',
    'glucose_prior_max',
    'glucose_prior_std',
    'wbc_prior_avg',
    'wbc_prior_min',
    'wbc_prior_max',
    'wbc_prior_std',
    'last_glucose_value_prior',
    'last_hemoglobin_value_prior',
    'last_lactate_value_prior',
    'last_potassium_value_prior',
    'last_albumin_value_prior',
    'last_bicarbonate_value_prior',
    'last_creatinine_value_prior',
    'last_sodium_value_prior',
    'last_urea nitrogen_value_prior',
    'last_hematocrit_value_prior',
    'last_bilirubin_value_prior',
    'last_wbc_value_prior',
    'last_bun_value_prior',
    'count_prior_severe_hyponatremia',
    'flag_chronic_anemia_prior',
    'lactate_prior_avg',
    'lactate_prior_min',
    'lactate_prior_max',
    'lactate_prior_std'
]

# From prescriptions.csv
PRESCRIPTIONS_COLUMNS = [
    'count_prior_prescriptions',
    'count_unique_drugs_prior',
    'avg_drugs_per_prior_admission',
    'flag_history_on_insulin',
    'count_prior_admissions_on_insulin',
    'flag_history_on_diuretics',
    'count_prior_admissions_on_diuretics',
    'flag_history_on_anticoagulants',
    'count_prior_admissions_on_anticoagulants',
    'flag_history_on_steroids',
    'count_prior_admissions_on_steroids',
    'flag_history_on_chemotherapy',
    'count_prior_admissions_on_chemotherapy',
    'flag_on_steroids_last_prior_admission'
]

# From procedures_icd.csv and d_icd_procedures.csv
# Note: d_icd_procedures.csv is used to get the label of the procedures
PROCEDURE_ICD_COLUMNS = [
    'count_prior_procedures',
    'count_unique_procedures_prior',
    'count_prior_admissions_with_procedure',
    'time_since_last_major_surgery_years',
    'flag_procedure_in_last_prior_admission',
    'flag_history_major_surgery',
    'flag_history_mech_vent',
    'flag_history_dialysis',
    'flag_history_biopsy'
]

# From d_labitems.csv and labevents.csv
# Note: d_labitems.csv is used to get the label of the lab tests
TEMPORAL_LAB_EVENTS_COLUMNS = [

    'window_365d_count_labevents',
    'window_365d_count_unique_labs',
    'window_365d_hematocrit_avg',
    'window_365d_hematocrit_min',
    'window_365d_hematocrit_max',
    'window_365d_hematocrit_std',
    'window_365d_hemoglobin_avg',
    'window_365d_hemoglobin_min',
    'window_365d_hemoglobin_max',
    'window_365d_hemoglobin_std',
    'window_365d_albumin_avg',
    'window_365d_albumin_min',
    'window_365d_albumin_max',
    'window_365d_albumin_std',
    'window_365d_bicarbonate_avg',
    'window_365d_bicarbonate_min',
    'window_365d_bicarbonate_max',
    'window_365d_bicarbonate_std',
    'window_365d_creatinine_avg',
    'window_365d_creatinine_min',
    'window_365d_creatinine_max',
    'window_365d_creatinine_std',
    'window_365d_potassium_avg',
    'window_365d_potassium_min',
    'window_365d_potassium_max',
    'window_365d_potassium_std',
    'window_365d_sodium_avg',
    'window_365d_sodium_min',
    'window_365d_sodium_max',
    'window_365d_sodium_std',
    'window_365d_urea nitrogen_avg',
    'window_365d_urea nitrogen_min',
    'window_365d_urea nitrogen_max',
    'window_365d_urea nitrogen_std',
    'window_365d_glucose_avg',
    'window_365d_glucose_min',
    'window_365d_glucose_max',
    'window_365d_glucose_std',
    'window_365d_lactate_avg',
    'window_365d_lactate_min',
    'window_365d_lactate_max',
    'window_365d_lactate_std',
    'window_365d_wbc_avg',
    'window_365d_wbc_min',
    'window_365d_wbc_max',
    'window_365d_wbc_std',
    'window_365d_last_creatinine',
    'window_365d_last_wbc',
    'window_365d_last_hematocrit',
    'window_365d_last_hemoglobin',
    'window_365d_last_sodium',
    'window_365d_last_bilirubin',
    'window_365d_last_potassium',
    'window_365d_last_glucose',
    'window_365d_last_urea nitrogen',
    'window_365d_last_albumin',
    'window_365d_last_lactate',
    'window_365d_last_bun',
    'window_365d_last_bicarbonate',
    'window_365d_count_severe_hyponatremia',
    'window_365d_flag_chronic_anemia',
    'window_180d_count_labevents',
    'window_180d_count_unique_labs',
    'window_180d_hematocrit_avg',
    'window_180d_hematocrit_min',
    'window_180d_hematocrit_max',
    'window_180d_hematocrit_std',
    'window_180d_hemoglobin_avg',
    'window_180d_hemoglobin_min',
    'window_180d_hemoglobin_max',
    'window_180d_hemoglobin_std',
    'window_180d_bicarbonate_avg',
    'window_180d_bicarbonate_min',
    'window_180d_bicarbonate_max',
    'window_180d_bicarbonate_std',
    'window_180d_creatinine_avg',
    'window_180d_creatinine_min',
    'window_180d_creatinine_max',
    'window_180d_creatinine_std',
    'window_180d_potassium_avg',
    'window_180d_potassium_min',
    'window_180d_potassium_max',
    'window_180d_potassium_std',
    'window_180d_sodium_avg',
    'window_180d_sodium_min',
    'window_180d_sodium_max',
    'window_180d_sodium_std',
    'window_180d_urea nitrogen_avg',
    'window_180d_urea nitrogen_min',
    'window_180d_urea nitrogen_max',
    'window_180d_urea nitrogen_std',
    'window_180d_glucose_avg',
    'window_180d_glucose_min',
    'window_180d_glucose_max',
    'window_180d_glucose_std',
    'window_180d_wbc_avg',
    'window_180d_wbc_min',
    'window_180d_wbc_max',
    'window_180d_wbc_std',
    'window_180d_albumin_avg',
    'window_180d_albumin_min',
    'window_180d_albumin_max',
    'window_180d_albumin_std',
    'window_180d_lactate_avg',
    'window_180d_lactate_min',
    'window_180d_lactate_max',
    'window_180d_lactate_std',
    'window_180d_last_creatinine',
    'window_180d_last_wbc',
    'window_180d_last_hematocrit',
    'window_180d_last_hemoglobin',
    'window_180d_last_sodium',
    'window_180d_last_bilirubin',
    'window_180d_last_potassium',
    'window_180d_last_glucose',
    'window_180d_last_urea nitrogen',
    'window_180d_last_albumin',
    'window_180d_last_lactate',
    'window_180d_last_bun',
    'window_180d_last_bicarbonate',
    'window_180d_count_severe_hyponatremia',
    'window_180d_flag_chronic_anemia',
    'window_90d_count_labevents',
    'window_90d_count_unique_labs',
    'window_90d_bicarbonate_avg',
    'window_90d_bicarbonate_min',
    'window_90d_bicarbonate_max',
    'window_90d_bicarbonate_std',
    'window_90d_creatinine_avg',
    'window_90d_creatinine_min',
    'window_90d_creatinine_max',
    'window_90d_creatinine_std',
    'window_90d_glucose_avg',
    'window_90d_glucose_min',
    'window_90d_glucose_max',
    'window_90d_glucose_std',
    'window_90d_potassium_avg',
    'window_90d_potassium_min',
    'window_90d_potassium_max',
    'window_90d_potassium_std',
    'window_90d_sodium_avg',
    'window_90d_sodium_min',
    'window_90d_sodium_max',
    'window_90d_sodium_std',
    'window_90d_urea nitrogen_avg',
    'window_90d_urea nitrogen_min',
    'window_90d_urea nitrogen_max',
    'window_90d_urea nitrogen_std',
    'window_90d_hematocrit_avg',
    'window_90d_hematocrit_min',
    'window_90d_hematocrit_max',
    'window_90d_hematocrit_std',
    'window_90d_hemoglobin_avg',
    'window_90d_hemoglobin_min',
    'window_90d_hemoglobin_max',
    'window_90d_hemoglobin_std',
    'window_90d_lactate_avg',
    'window_90d_lactate_min',
    'window_90d_lactate_max',
    'window_90d_lactate_std',
    'window_90d_albumin_avg',
    'window_90d_albumin_min',
    'window_90d_albumin_max',
    'window_90d_albumin_std',
    'window_90d_wbc_avg',
    'window_90d_wbc_min',
    'window_90d_wbc_max',
    'window_90d_wbc_std',
    'window_90d_last_creatinine',
    'window_90d_last_wbc',
    'window_90d_last_hematocrit',
    'window_90d_last_hemoglobin',
    'window_90d_last_sodium',
    'window_90d_last_bilirubin',
    'window_90d_last_potassium',
    'window_90d_last_glucose',
    'window_90d_last_urea nitrogen',
    'window_90d_last_albumin',
    'window_90d_last_lactate',
    'window_90d_last_bun',
    'window_90d_last_bicarbonate',
    'window_90d_count_severe_hyponatremia',
    'window_90d_flag_chronic_anemia',
    'window_30d_count_labevents',
    'window_30d_count_unique_labs',
    'window_30d_bicarbonate_avg',
    'window_30d_bicarbonate_min',
    'window_30d_bicarbonate_max',
    'window_30d_bicarbonate_std',
    'window_30d_creatinine_avg',
    'window_30d_creatinine_min',
    'window_30d_creatinine_max',
    'window_30d_creatinine_std',
    'window_30d_glucose_avg',
    'window_30d_glucose_min',
    'window_30d_glucose_max',
    'window_30d_glucose_std',
    'window_30d_potassium_avg',
    'window_30d_potassium_min',
    'window_30d_potassium_max',
    'window_30d_potassium_std',
    'window_30d_sodium_avg',
    'window_30d_sodium_min',
    'window_30d_sodium_max',
    'window_30d_sodium_std',
    'window_30d_urea nitrogen_avg',
    'window_30d_urea nitrogen_min',
    'window_30d_urea nitrogen_max',
    'window_30d_urea nitrogen_std',
    'window_30d_wbc_avg',
    'window_30d_wbc_min',
    'window_30d_wbc_max',
    'window_30d_wbc_std',
    'window_30d_hematocrit_avg',
    'window_30d_hematocrit_min',
    'window_30d_hematocrit_max',
    'window_30d_hematocrit_std',
    'window_30d_hemoglobin_avg',
    'window_30d_hemoglobin_min',
    'window_30d_hemoglobin_max',
    'window_30d_hemoglobin_std',
    'window_30d_albumin_avg',
    'window_30d_albumin_min',
    'window_30d_albumin_max',
    'window_30d_albumin_std',
    'window_30d_lactate_avg',
    'window_30d_lactate_min',
    'window_30d_lactate_max',
    'window_30d_lactate_std',
    'window_30d_last_creatinine',
    'window_30d_last_wbc',
    'window_30d_last_hematocrit',
    'window_30d_last_hemoglobin',
    'window_30d_last_sodium',
    'window_30d_last_bilirubin',
    'window_30d_last_potassium',
    'window_30d_last_glucose',
    'window_30d_last_urea nitrogen',
    'window_30d_last_albumin',
    'window_30d_last_lactate',
    'window_30d_last_bun',
    'window_30d_last_bicarbonate',
    'window_30d_count_severe_hyponatremia',
    'window_30d_flag_chronic_anemia',
    'window_7d_count_labevents',
    'window_7d_count_unique_labs',
    'window_7d_albumin_avg',
    'window_7d_albumin_min',
    'window_7d_albumin_max',
    'window_7d_albumin_std',
    'window_7d_bicarbonate_avg',
    'window_7d_bicarbonate_min',
    'window_7d_bicarbonate_max',
    'window_7d_bicarbonate_std',
    'window_7d_creatinine_avg',
    'window_7d_creatinine_min',
    'window_7d_creatinine_max',
    'window_7d_creatinine_std',
    'window_7d_glucose_avg',
    'window_7d_glucose_min',
    'window_7d_glucose_max',
    'window_7d_glucose_std',
    'window_7d_potassium_avg',
    'window_7d_potassium_min',
    'window_7d_potassium_max',
    'window_7d_potassium_std',
    'window_7d_sodium_avg',
    'window_7d_sodium_min',
    'window_7d_sodium_max',
    'window_7d_sodium_std',
    'window_7d_urea nitrogen_avg',
    'window_7d_urea nitrogen_min',
    'window_7d_urea nitrogen_max',
    'window_7d_urea nitrogen_std',
    'window_7d_hematocrit_avg',
    'window_7d_hematocrit_min',
    'window_7d_hematocrit_max',
    'window_7d_hematocrit_std',
    'window_7d_hemoglobin_avg',
    'window_7d_hemoglobin_min',
    'window_7d_hemoglobin_max',
    'window_7d_hemoglobin_std',
    'window_7d_wbc_avg',
    'window_7d_wbc_min',
    'window_7d_wbc_max',
    'window_7d_wbc_std',
    'window_7d_lactate_avg',
    'window_7d_lactate_min',
    'window_7d_lactate_max',
    'window_7d_lactate_std',
    'window_7d_last_creatinine',
    'window_7d_last_wbc',
    'window_7d_last_hematocrit',
    'window_7d_last_hemoglobin',
    'window_7d_last_sodium',
    'window_7d_last_bilirubin',
    'window_7d_last_potassium',
    'window_7d_last_glucose',
    'window_7d_last_urea nitrogen',
    'window_7d_last_albumin',
    'window_7d_last_lactate',
    'window_7d_last_bun',
    'window_7d_last_bicarbonate',
    'window_7d_count_severe_hyponatremia',
    'window_7d_flag_chronic_anemia'
]

# From admissions.csv and patients.csv
TIME_TO_DEATH_COLUMNS = [
    'subject_id',
    'hadm_id',
    'admittime',
    'dischtime',
    'age',
    'gender',
    'race',
    'insurance',
    'label',
    'dod',
    'time_to_death',
    'los',
    'admission_type',
    'admission_location',
    'discharge_location'
]

ETHNICITY_MAPPING = {
    "WHITE": "White",
    "WHITE - OTHER EUROPEAN": "White",
    "WHITE - RUSSIAN": "White",
    "WHITE - EASTERN EUROPEAN": "White",
    "WHITE - BRAZILIAN": "White",
    "PORTUGUESE": "White",

    "BLACK/AFRICAN AMERICAN": "Black/African American",
    "BLACK/CARIBBEAN ISLAND": "Black/African American",
    "BLACK/CAPE VERDEAN": "Black/African American",
    "BLACK/AFRICAN": "Black/African American",

    "HISPANIC/LATINO - PUERTO RICAN": "Hispanic/Latino",
    "HISPANIC OR LATINO": "Hispanic/Latino",
    "HISPANIC/LATINO - DOMINICAN": "Hispanic/Latino",
    "HISPANIC/LATINO - GUATEMALAN": "Hispanic/Latino",
    "HISPANIC/LATINO - SALVADORAN": "Hispanic/Latino",
    "HISPANIC/LATINO - COLUMBIAN": "Hispanic/Latino",
    "HISPANIC/LATINO - HONDURAN": "Hispanic/Latino",
    "HISPANIC/LATINO - CUBAN": "Hispanic/Latino",
    "HISPANIC/LATINO - CENTRAL AMERICAN": "Hispanic/Latino",
    "HISPANIC/LATINO - MEXICAN": "Hispanic/Latino",
    "SOUTH AMERICAN": "Hispanic/Latino",

    "ASIAN - CHINESE": "Asian",
    "ASIAN": "Asian",
    "ASIAN - SOUTH EAST ASIAN": "Asian",
    "ASIAN - ASIAN INDIAN": "Asian",
    "ASIAN - KOREAN": "Asian",

    
    "OTHER": "Other",
    "UNKNOWN": "Other",
    "UNABLE TO OBTAIN": "Other",
    "PATIENT DECLINED TO ANSWER": "Other",
    "MULTIPLE RACE/ETHNICITY": "Other",
    "AMERICAN INDIAN/ALASKA NATIVE": "Other",
    "NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER": "Other",
    }

ADMISSION_TYPE_MAPPING = {
    "EW EMER" : "EMERGENCY",
    "OBSERVATION ADMIT" : "EMERGENCY",
    "URGENT" : "EMERGENCY",
    "DIRECT EMER." : "EMERGENCY",
    "EU OBSERVATION" : "EMERGENCY",
    "DIRECT OBSERVATION" : "EMERGENCY",
    "AMBULATORY OBSERVATION" : "EMERGENCY",
    "ELECTIVE" : "ELECTIVE",
    "SURGICAL SAME DAY ADMISSION" : "ELECTIVE"
}



# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass

