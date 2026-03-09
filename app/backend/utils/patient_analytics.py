from typing import List

import numpy as np
from pandas import DataFrame, Series
from schemas.patient_analytics import (
    AgeChestPainHeatMapMapping,
    CombinedDistibutionData,
    Comorbidity,
    DistributionData,
    FeatureCorrelations,
    OverviewStats,
    PatientsAnalyticsResponse,
    RiskSegment,
    UrgencyByComorbidities,
    UrgencyFieldGrouping,
)

# Specify numeric columns
NUMERIC_COLS: list[str] = [
    "age",
    "blood pressure",
    "max heart rate",
    "bmi",
    "chest pain type",
    "exercise angina",
    "hypertension",
    "heart_disease",
]


def urgency_rate(series: Series) -> float:
    """
    Helper Function to derive the mean urgency rate from a Series to 4 decimal places.

    Args:
        series (Series): Series of the all urgency rates across the different category.

    Returns:
        float: Float containing the mean urgency rate.
    """
    return round(float(series.mean()), 4)


def get_overall_statistics(df: DataFrame) -> OverviewStats:
    """
    Helper function to extract overview stats from a DataFrame

    Args:
        df (DataFrame): DataFrame to extract the data from

    Returns:
        OverviewStats: Overview Stats in an object
    """
    # Extract overall stats
    total = len(df)
    urgent = int(df["y"].sum())
    non_urgent = total - urgent

    # Construct and return stats
    return OverviewStats(
        total_patients=total,
        urgent_patients=urgent,
        non_urgent_patients=non_urgent,
        overall_urgency_rate=urgency_rate(df["y"]),
        avg_age=round(float(df["age"].mean()), 1),
        avg_bmi=round(float(df["bmi"].mean()), 1),
        avg_blood_pressure=round(float(df["blood pressure"].mean()), 1),
        avg_max_heart_rate=round(float(df["max heart rate"].mean()), 1),
    )


def group_urgency(
    df: DataFrame, col: str, label_col: str | None = None
) -> List[UrgencyFieldGrouping]:
    """
    Helper function to group the urgency based on the col.
    """
    grp_col = label_col if label_col else col
    result = (
        df.groupby(grp_col, observed=True)
        .agg(
            total=("y", "count"),
            urgent=("y", "sum"),
            urgency_rate=("y", "mean"),
        )
        .reset_index()
        .rename(columns={grp_col: "label"})
    )
    result["urgency_rate"] = result["urgency_rate"].round(4)
    result["label"] = result["label"].astype(str)
    return [
        UrgencyFieldGrouping(**grouping)
        for grouping in result.to_dict(orient="records")
    ]


def get_comorbidity_stats(df: DataFrame, flag_col: str) -> Comorbidity:
    """
    Helper Function to extract the comorbidity stats for specified comorbidity.

    Args:
        df (DataFrame): DataFrame to extract the comorbidity stats from.
        flag_col (str): Type of Comorbidity (e.g., hypertension, heart_disease, exercise angina)

    Returns:
        Comorbidity: Comorbidity object containing the statistics for the specified type of Comorbidity
    """
    g = df.groupby(flag_col, observed=True)["y"].agg(["sum", "count", "mean"]).round(4)
    g.index = g.index.map(lambda x: "yes" if x == 1.0 else "no")
    g_dict: dict[str, dict[str, str]] = g.rename(
        columns={"sum": "urgent", "count": "total", "mean": "urgency_rate"}
    ).to_dict(orient="index")

    return Comorbidity(**g_dict)


def get_all_comorbidity_stats(df: DataFrame) -> UrgencyByComorbidities:
    """
    Helper Function to extract comorbidity stats all comorbidities.

    Args:
        df (DataFrame): DataFrame to extract the comorbidity stats from.

    Returns:
        UrgencyByComorbidities: UrgencyByComorbidities object containing the statistics all comorbidities
    """
    return UrgencyByComorbidities(
        hypertension=get_comorbidity_stats(df=df, flag_col="hypertension"),
        heart_disease=get_comorbidity_stats(df=df, flag_col="heart_disease"),
        exercise_angina=get_comorbidity_stats(df=df, flag_col="exercise angina"),
    )


def get_hist_buckets(df: DataFrame, col: str, bins: int = 10) -> DistributionData:
    """
    Helper Function to obtain histogram buckets for the specified col within the dataframe.

    Args:
        df (DataFrame): DataFrame to extract the histogram buckets from.
        col (str): Column title.
        bins (int): Number of bins to use.

    Returns:
        DistributionData: Distribution Data of the histogram with labels and counts
    """
    counts, edges = np.histogram(df[col].dropna(), bins=bins)
    labels = [f"{edges[i]:.0f}-{edges[i+1]:.0f}" for i in range(len(edges) - 1)]
    return DistributionData(
        labels=labels,
        counts=counts.tolist(),
    )


def get_distributions(df: DataFrame) -> CombinedDistibutionData:
    """
    Helper function to get distribution data for all columns within the dataframe

    Args:
        df (DataFrame): DataFrame to extract distributions from.

    Returns:
        CombinedDistibutionData: Distribution Data for all columns
    """
    return CombinedDistibutionData(
        age=get_hist_buckets(df=df, col="age"),
        blood_pressure=get_hist_buckets(df=df, col="blood pressure"),
        max_heart_rate=get_hist_buckets(df=df, col="max heart rate"),
        bmi=get_hist_buckets(df=df, col="bmi"),
    )


def get_feature_correlations(df: DataFrame) -> FeatureCorrelations:
    """
    Helper Function to obtain the feature correlation between each numeric column with the target 'urgency'.

    Args:
        df (DataFrame): DataFrame containing the information required.

    Returns:
        FeatureCorrelations: Object containing all feature correlations.
    """
    corr = df[NUMERIC_COLS + ["y"]].corr()["y"].drop("y").round(4)
    feature_correlations: dict[str, float] = corr.sort_values(ascending=False).to_dict()
    return FeatureCorrelations(**feature_correlations)


def get_age_chest_pain_heatmap(df: DataFrame) -> List[AgeChestPainHeatMapMapping]:
    """
    Helper function to extract the Heatmap for age to chest pain.

    Args:
        df (DataFrame): DataFrame containing the information.

    Returns:
        List[AgeChestPainHeatMapMapping]: List of heatmap cell contents.
    """
    heatmap_list: list[dict[str, str | float]] = (
        df.groupby(["age_group", "chest_pain_label"], observed=True)["y"]
        .mean()
        .round(4)
        .reset_index()
        .rename(
            columns={
                "age_group": "age_group",
                "chest_pain_label": "chest_pain",
                "y": "urgency_rate",
            }
        )
        .assign(age_group=lambda x: x["age_group"].astype(str))
        .to_dict(orient="records")
    )
    return [AgeChestPainHeatMapMapping(**cell) for cell in heatmap_list]


def get_risk_segments(df: DataFrame) -> List[RiskSegment]:
    """
    Helper Function to obtain the risk segments
    """
    # Copy DataFrame
    df_copy = df.copy()

    # Define high-risk = any 2+ of: age≥60, BP≥140, hypertension, heart_disease, chest_pain∈{3,4}
    df_copy["risk_age"] = (df_copy["age"] >= 60).astype(int)
    df_copy["risk_bp"] = (df_copy["blood pressure"] >= 140).astype(int)
    df_copy["risk_hypertension"] = df_copy["hypertension"].astype(int)
    df_copy["risk_heart"] = df_copy["heart_disease"].astype(int)
    df_copy["risk_cp"] = df_copy["chest pain type"].isin([3, 4]).astype(int)
    df_copy["risk_score"] = df_copy[
        ["risk_age", "risk_bp", "risk_hypertension", "risk_heart", "risk_cp"]
    ].sum(axis=1)

    # Find risk segments and return
    risk_segments: list[dict[str, int | float]] = (
        df_copy.groupby("risk_score")
        .agg(total=("y", "count"), urgent=("y", "sum"), urgency_rate=("y", "mean"))
        .reset_index()
        .assign(urgency_rate=lambda x: x["urgency_rate"].round(4))
        .rename(columns={"risk_score": "risk_factor_count"})
        .to_dict(orient="records")
    )
    return [RiskSegment(**segment) for segment in risk_segments]


def get_patient_analytics(df: DataFrame) -> PatientsAnalyticsResponse:
    """
    Function to return all patient analytics data from a DataFrame.

    Args:
        df (DataFrame): DataFrame of patient data.

    Returns:
        PatientsAnalyticsResponse: Response object of all analytics data.
    """

    # ── 1. Overview KPIs ───────────────────────────────────────────────────────
    overview: OverviewStats = get_overall_statistics(df=df)

    # ── 2. Urgency by age group ────────────────────────────────────────────────
    urgency_by_age: List[UrgencyFieldGrouping] = group_urgency(df, "age", "age_group")

    # ── 3. Urgency by chest pain type ─────────────────────────────────────────
    urgency_by_chest_pain: List[UrgencyFieldGrouping] = group_urgency(
        df, "chest pain type", "chest_pain_label"
    )

    # ── 4. Urgency by smoking status ──────────────────────────────────────────
    urgency_by_smoking: List[UrgencyFieldGrouping] = group_urgency(df, "smoking_status")

    # ── 5. Urgency by blood pressure category ─────────────────────────────────
    urgency_by_bp: List[UrgencyFieldGrouping] = group_urgency(
        df, "blood pressure", "bp_category"
    )

    # ── 6. Urgency by BMI category ────────────────────────────────────────────
    urgency_by_bmi: List[UrgencyFieldGrouping] = group_urgency(
        df, "bmi", "bmi_category"
    )

    # ── 7. Comorbidity breakdown ───────────────────────────────────────────────
    comorbidities: UrgencyByComorbidities = get_all_comorbidity_stats(df=df)

    # ── 8. Vital sign distributions (histogram buckets) ───────────────────────
    distributions: CombinedDistibutionData = get_distributions(df=df)

    # ── 9. Correlation of numeric features with urgency ────────────────────────
    feature_correlations: FeatureCorrelations = get_feature_correlations(df=df)

    # ── 10. Age-bucket × Chest Pain Type heatmap data ─────────────────────────
    heatmap: List[AgeChestPainHeatMapMapping] = get_age_chest_pain_heatmap(df=df)

    # ── 11. Risk segments ──────────────────────────────────────────────────────
    risk_segments: List[RiskSegment] = get_risk_segments(df=df)

    return PatientsAnalyticsResponse(
        overview=overview,
        urgency_by_age_group=urgency_by_age,
        urgency_by_chest_pain=urgency_by_chest_pain,
        urgency_by_smoking=urgency_by_smoking,
        urgency_by_bp_category=urgency_by_bp,
        urgency_by_bmi_category=urgency_by_bmi,
        comorbidities=comorbidities,
        distributions=distributions,
        feature_correlations=feature_correlations,
        age_chest_pain_heatmap=heatmap,
        risk_segments=risk_segments,
    )
