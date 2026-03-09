from typing import List, Literal

from pydantic import BaseModel, Field

# Default types
AgeGroup = Literal["<30", "30-40", "40-50", "50-60", "60-70", "70+"]

ChestPainType = Literal[
    "Asymptomatic", "Atypical Angina", "Non-Anginal", "Severe Angina", "Typical Angina"
]


class OverviewStats(BaseModel):
    total_patients: int = Field(
        default=0, description="Total number of patients handled"
    )
    urgent_patients: int = Field(
        default=0, description="Total number of urgent patients handled"
    )
    non_urgent_patients: int = Field(
        default=0, description="Total number of urgent patients handled"
    )
    overall_urgency_rate: float = Field(
        default=0.0, description="Proportion of total patients that are urgent cases"
    )
    avg_age: float = Field(default=0.0, description="Average age of all patients")
    avg_bmi: float = Field(default=0.0, description="Average BMI of all patients")
    avg_blood_pressure: float = Field(
        default=0.0, description="Average Blood Pressure of all patients"
    )
    avg_max_heart_rate: float = Field(
        default=0.0, description="Average Max Heart Rate of all patients"
    )


class UrgencyStats(BaseModel):
    total: int = Field(default=0, description="Total number of patients")
    urgent: int = Field(default=0, description="Total number of urgent patients")
    urgency_rate: float = Field(
        default=0.0, description="Proportion of total patients that are urgent"
    )


class UrgencyFieldGrouping(UrgencyStats):
    label: str = Field(
        default="", description="Label of field grouping to categorise urgency by"
    )


class Comorbidity(BaseModel):
    no: UrgencyStats = Field(
        default_factory=UrgencyStats,
        description="Urgency Stats that do not have the comorbiditity",
    )
    yes: UrgencyStats = Field(
        default_factory=UrgencyStats,
        description="Urgency Stats that have the comorbiditity",
    )


class UrgencyByComorbidities(BaseModel):
    hypertension: Comorbidity = Field(
        default_factory=Comorbidity, description="Urgency cases by hypertension"
    )
    heart_disease: Comorbidity = Field(
        default_factory=Comorbidity, description="Urgency cases by heart_disease"
    )
    exercise_angina: Comorbidity = Field(
        default_factory=Comorbidity, description="Urgency cases by exercise_angina"
    )


class DistributionData(BaseModel):
    labels: list[str] = Field(
        default_factory=list, description="Labels for Distribution"
    )
    counts: list[int] = Field(
        default_factory=list, description="Counts for each label in distribution"
    )


class CombinedDistibutionData(BaseModel):
    age: DistributionData = Field(
        default_factory=DistributionData, description="Distribution Data for age"
    )
    blood_pressure: DistributionData = Field(
        default_factory=DistributionData,
        description="Distribution Data for blood_pressure",
    )
    max_heart_rate: DistributionData = Field(
        default_factory=DistributionData,
        description="Distribution Data for max_heart_rate",
    )
    bmi: DistributionData = Field(
        default_factory=DistributionData, description="Distribution Data for BMI"
    )


class FeatureCorrelations(BaseModel):
    chest_pain_type: float = Field(
        default=0.0,
        description="Correlation between urgency and chest pain type",
        alias="chest pain type",
    )
    exercise_angina: float = Field(
        default=0.0,
        description="Correlation between urgency and exercise angina",
        alias="exercise angina",
    )
    blood_pressure: float = Field(
        default=0.0,
        description="Correlation between urgency and blood pressure",
        alias="blood pressure",
    )
    max_heart_rate: float = Field(
        default=0.0,
        description="Correlation between urgency and max heart rate",
        alias="max heart rate",
    )
    heart_disease: float = Field(
        default=0.0, description="Correlation between urgency and heart_disease"
    )
    hypertension: float = Field(
        default=0.0, description="Correlation between urgency and hypertension"
    )
    bmi: float = Field(default=0.0, description="Correlation between urgency and BMI")
    age: float = Field(default=0.0, description="Correlation between urgency and age")


class AgeChestPainHeatMapMapping(BaseModel):
    age_group: AgeGroup = Field(default="<30", description="Age Group of Heatmap cell")
    chest_pain: ChestPainType = Field(
        default="Asymptomatic", description="Chest Pain Type of Heatmap cell"
    )
    urgency_rate: float = Field(
        default=0.0,
        description="Urgency rate of group given age group and chest pain level",
    )


class RiskSegment(BaseModel):
    risk_factor_count: int = Field(
        default=0, description="Number of risk factors present in patient group"
    )
    total: int = Field(
        default=0, description="Count of patients with specified number of risk factors"
    )
    urgent: int = Field(
        default=0,
        description="Count of urgent patients with specified number of risk factors",
    )
    urgency_rate: float = Field(
        default=0.0,
        description="Proportion of total patients with specified number of risk factors who are urgent",
    )


class PatientsAnalyticsResponse(BaseModel):
    # Overall-level statistics
    overview: OverviewStats = Field(
        default_factory=OverviewStats, description="Overall level statistics of Clinic"
    )

    # Urgency
    urgency_by_age_group: List[UrgencyFieldGrouping] = Field(
        default_factory=list, description="List of urgency grouping by age group"
    )
    urgency_by_chest_pain: List[UrgencyFieldGrouping] = Field(
        default_factory=list, description="List of urgency grouping by chest pain type"
    )
    urgency_by_smoking: List[UrgencyFieldGrouping] = Field(
        default_factory=list,
        description="List of urgency grouping by smoking intensity",
    )
    urgency_by_bp_category: List[UrgencyFieldGrouping] = Field(
        default_factory=list,
        description="List of urgency grouping by blood pressure category",
    )
    urgency_by_bmi_category: List[UrgencyFieldGrouping] = Field(
        default_factory=list, description="List of urgency grouping by BMI category"
    )
    urgency_by_age_group: List[UrgencyFieldGrouping] = Field(
        default_factory=list, description="List of urgency grouping by age group"
    )

    # Urgency by comorbidities (Hypertension, Heart Disease, Exercise Angina)
    comorbidities: UrgencyByComorbidities = Field(
        default_factory=UrgencyByComorbidities,
        description="Urgency Statistics based on different comorbidities",
    )

    # Distribution
    distributions: CombinedDistibutionData = Field(
        default_factory=CombinedDistibutionData,
        description="All distribution data for different fields",
    )

    # Correlation
    feature_correlations: FeatureCorrelations = Field(
        default_factory=FeatureCorrelations,
        description="Feature Correlation of urgency against different fields",
    )

    # Heat Map
    age_chest_pain_heatmap: List[AgeChestPainHeatMapMapping] = Field(
        default_factory=list, description="List of Heat Map Cells for representation"
    )

    # Risk Segments for patients with age >= 60
    risk_segments: List[RiskSegment] = Field(
        default_factory=list,
        description="List of risk segments for patients >= 60 years old",
    )
