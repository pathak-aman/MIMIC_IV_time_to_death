from loguru import logger

import warnings
warnings.filterwarnings("ignore")

from assessment.config import FILTER_OVER_AGE_18, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, LABEVENTS_PATH, PROCESSED_HOSP_DATA_DIR
from assessment.datasets import load_diagnoses_data, load_procedures_data, load_prescriptions_data
from assessment.features_hosp import prepare_cohort, filter_time_to_death_dataframe

from assessment.hosp_diagnosis import create_diagnosis_features
from assessment.hosp_procedure import create_procedures_features
from assessment.hosp_meds import create_meds_features
from assessment.hosp_labevents import create_labsevents_features_chunked, identify_itemids_from_d_labelitems
from assessment.hosp_labevents_windowed import create_longitudinal_lab_features
from assessment.hosp_agg_processed_features import merge_csvs_in_dir



def run_cohort_preparation_pipeline():
# ------------------------------------------------------
#               HOSP COHORT PREPARATION
# ------------------------------------------------------

    logger.info("-------------------------- Running cohort preparation pipeline...")
    cohort_df = prepare_cohort(FILTER_OVER_AGE_18)

    # Save to interim data for inspection
    OUTPUT_PATH = INTERIM_DATA_DIR / "cohort_df.csv"
    cohort_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Interim data saved to {OUTPUT_PATH}")

# ----------------- ADD TIME TO DEATH ----------------- DONE


    time_to_death_df = filter_time_to_death_dataframe(cohort_df)

    # Save to processed data for inspection
    OUTPUT_PATH = PROCESSED_DATA_DIR / "hosp/time_to_death_df.csv"
    time_to_death_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Time to death processed data saved to {OUTPUT_PATH}")
    logger.info("-------------------------- Cohort preparation pipeline completed.")


    return cohort_df, time_to_death_df


def run_feature_creation_pipeline(cohort_df):

# ------------------------------------------------------
#                 FEATURE CREATION
# ------------------------------------------------------

    logger.info(f"------------------------------------------------------")
    logger.info(f"                FEATURE CREATION                      ")
    logger.info(f"------------------------------------------------------")

    logger.info(f"Creating features for {len(cohort_df)} cohort entries")

    logger.info("----------------- STEP I - DIAGNOSIS FEATURES -----------------")

    logger.info(f"Creating diagnosis features for {len(cohort_df)} cohort entries.")
    diagnosis_df = load_diagnoses_data()
    diagnosis_feat_df = create_diagnosis_features(cohort_df, diagnosis_df)
    logger.info(f"Diagnosis features created for {len(diagnosis_feat_df)} cohort entries.")
    # Save to interim data for inspection
    OUTPUT_PATH = PROCESSED_DATA_DIR / "hosp/diagnosis_feat_df.csv"
    diagnosis_feat_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Diagnosis features interim data saved to {OUTPUT_PATH}")


    logger.info("----------------- STEP II - PROCEDURE FEATURES -----------------")

    logger.info(f"Creating procedure features for {len(cohort_df)} cohort entries.")
    procedures_df = load_procedures_data()
    procedures_feat_df = create_procedures_features(cohort_df, procedures_df)
    logger.info(f"Procedure features created for {len(procedures_feat_df)} cohort entries.")
    # # Save to interim data for inspection
    OUTPUT_PATH = PROCESSED_DATA_DIR / "hosp/procedures_feat_df.csv"
    procedures_feat_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Procedure features interim data saved to {OUTPUT_PATH}")

    logger.info("----------------- STEP III - MEDICATION FEATURES -----------------")
    logger.info(f"Creating medication features for {len(cohort_df)} cohort entries.")
    prescriptions_df = load_prescriptions_data()
    prescriptions_feat_df = create_meds_features(cohort_df, prescriptions_df)
    logger.info(f"Medication features created for {len(prescriptions_feat_df)} cohort entries.")
    # Save to interim data for inspection
    OUTPUT_PATH = PROCESSED_DATA_DIR / "hosp/prescriptions_feat_df.csv"
    prescriptions_feat_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Medication features interim data saved to {OUTPUT_PATH}")


# # ----------------- LAB TESTS FEATURES ----------------- DONE
    logger.info("----------------- STEP IV - LABEVENTS FEATURES -----------------")
    logger.info(f"Creating lab tests features for {len(cohort_df)} cohort entries.")
    labs_feature_df = create_labsevents_features_chunked(cohort_df, LABEVENTS_PATH)
    logger.info(f"Lab tests features created for {len(labs_feature_df)} cohort entries.")
    # # Save to interim data for inspection
    OUTPUT_PATH = PROCESSED_DATA_DIR / "hosp/labs_feature_df.csv"
    labs_feature_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Lab tests features interim data saved to {OUTPUT_PATH}")


# # ------------------- TIME WINDOW LAB TEST FEATURES -----------------
    logger.info("----------------- STEP V - TEMPORAL LABEVENTS FEATURES -----------------")
    logger.info(f"Creating temporal lab tests features for {len(cohort_df)} cohort entries.")
    labs_feature_time_window_df = create_longitudinal_lab_features(cohort_df, LABEVENTS_PATH)
    logger.info(f"Temporal lab tests features created for {len(labs_feature_time_window_df)} cohort entries.")
    # Save to interim data for inspection
    OUTPUT_PATH = PROCESSED_DATA_DIR / "hosp/temporal_labs_feature_df.csv"
    labs_feature_time_window_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Temporal lab tests features interim data saved to {OUTPUT_PATH}")


    # ------------------- MERGE ALL FEATURES -----------------
    # logger.info(f"Merging all features for {len(cohort_df)} patients.")
    # Merge all features
    return merge_csvs_in_dir(PROCESSED_HOSP_DATA_DIR)


if __name__ == "__main__":
    # Run the cohort preparation pipeline
    cohort_df, time_to_death_df = run_cohort_preparation_pipeline()
    

    # Run the feature creation pipeline
    logger.info("-------------------------- Running feature creation pipeline...")
    final_feature_df = run_feature_creation_pipeline(cohort_df)
    logger.info("-------------------------- Feature creation pipeline completed.")

    # Save the final feature dataframe
    OUTPUT_PATH = PROCESSED_DATA_DIR / "hosp/final_feature_df.csv"
    final_feature_df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"-------------------------- Final feature dataframe saved to {OUTPUT_PATH}")