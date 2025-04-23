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
    'creatinine',
    'urea nitrogen',
    'lactate',
    'white blood',
    'hemoglobin',
    'platelet',
    'hematocrit',
    'sodium',
    'potassium',
    'glucose',
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

