# Assumptions:

As part of this project, I made several design decisions and assumptions to define the scope, construct the dataset, and guide modeling. These were necessary for practical implementation:

1. **Defining Time-to-Death**:<br>
I chose to model `time to death` as _the duration between hospital admission and in-hospital death during the final hospital stay_. This decision allowed for a clear, timestamp-based outcome variable with a real clinical significence.<br>
2. **Focusing on In-Hospital Deaths**:<br>
I limited the cohort to patients who died during their final hospital admission (i.e., hospital_expire_flag = 1). This excluded patients who were discharged (alive) or died outside the hospital, as their time of death may be uncertain or unavailable.<br>
3. **Choosing Anchor Age as a Proxy for Patient Age**:<br>
In MIMIC-IV, patient age is masked for privacy protection and the exact age at admission isn’t always directly available. To address this, I used the anchor_age field from the patients table as a proxy for patient age throughout the analysis. <br>
4. **Clinical Feature Engineering Based on Best Judgment**<br>
When defining condition flags (e.g., for CHF, diabetes, CKD, cancer) and selecting lab values (e.g., glucose, hemoglobin, sodium), I relied on my clinical intuition and my knowledge from similar mortality prediction studies. However, I am not a clinical expert, and these decisions were made to the best of my judgment based on interpretability and potential clinical relevance. <br>
5. **Referencing External Guidelines for Grouping Categorical Variables**:<br>
For high-cardinality categorical variables like `race` and `admission type`, I referred to best practices published in healthcare analytics communities and academic blogs. Specifically:
    1. I grouped race categories into broader bins based on this reference [Racial Disparities .... MIMIC-IV](https://pmc.ncbi.nlm.nih.gov/articles/PMC10524813/#s1:~:text=of%20Stay%20Criteria.-,Asian,Demographics,-Age%2C%20years%2C%20median) on race grouping best practices to reduce noise and improve model generalizability.

    2. For admission types, I consolidated granular labels (e.g., EU OBSERVATION, DIRECT EMER., OBSERVATION ADMIT) into standardized categories (e.g., Emergency, Elective) based on usage frequency and guidelines like this one [Swiss Physician's mapping approach](https://github.com/MIT-LCP/mimic-code/discussions/1215).<br>

6. **Using Prior Admissions as Patient History**:
To enrich patient context, I incorporated data from previous hospital admissions (before the final admission to avoid leakage). This historical information was used to compute comorbidity scores, flag chronic conditions, and analyze longitudinal lab patterns. <br>
7. **Imputing Missing Values with Flags**:
For features like `"time_since_first_diagnosis_CANCER_ICD_CODES"`, `"time_since_first_diagnosis_STROKE_ICD_CODES`...." I used zero imputation alongside a binary flag `had_cancer`, `had_storke` to indicating whether the value was missing. I assumed that missingness might reflect clinical absence (e.g., never diagnosed) rather than random noise.<br>
8. **Evaluating Regression as Classification**
Although my models predict a continuous time-to-death, I also evaluated them using classification metrics like AUC, precision, recall, and F1 by defining thresholds (e.g., “death within X days”). This made performance easier to interpret in a clinical risk stratification context. <br>
