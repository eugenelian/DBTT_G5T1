import numpy as np
from pandas import DataFrame, Series


def urgency_rate(series: Series) -> float:
    """
    Helper Function to derive the mean urgency rate from a Series to 4 decimal places.

    Args:
        series (Series): Series of the all urgency rates across the different category.

    Returns:
        float: Float containing the mean urgency rate.
    """
    return round(float(series.mean()), 4)


def group_urgency(df: DataFrame, col: str, label_col: str | None = None) -> list[dict]:
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
    return result.to_dict(orient="records")


def get_analytics(df: DataFrame):

    # Overall statistics
    total = len(df)
    urgent = int(df["y"].sum())
    non_urgent = total - urgent

    # ── 1. Overview KPIs ───────────────────────────────────────────────────────
    overview = {
        "total_patients": total,
        "urgent_patients": urgent,
        "non_urgent_patients": non_urgent,
        "overall_urgency_rate": urgency_rate(df["y"]),
        "avg_age": round(float(df["age"].mean()), 1),
        "avg_bmi": round(float(df["bmi"].mean()), 1),
        "avg_blood_pressure": round(float(df["blood pressure"].mean()), 1),
        "avg_max_heart_rate": round(float(df["max heart rate"].mean()), 1),
    }

    # ── 2. Urgency by age group ────────────────────────────────────────────────
    urgency_by_age = group_urgency(df, "age", "age_group")

    # ── 3. Urgency by chest pain type ─────────────────────────────────────────
    urgency_by_chest_pain = group_urgency(df, "chest pain type", "chest_pain_label")

    # ── 4. Urgency by smoking status ──────────────────────────────────────────
    urgency_by_smoking = group_urgency(df, "smoking_status")

    # ── 5. Urgency by blood pressure category ─────────────────────────────────
    urgency_by_bp = group_urgency(df, "blood pressure", "bp_category")

    # ── 6. Urgency by BMI category ────────────────────────────────────────────
    urgency_by_bmi = group_urgency(df, "bmi", "bmi_category")

    # ── 7. Comorbidity breakdown ───────────────────────────────────────────────
    def comorbidity_stats(flag_col: str) -> dict:
        g = (
            df.groupby(flag_col, observed=True)["y"]
            .agg(["sum", "count", "mean"])
            .round(4)
        )
        g.index = g.index.map(lambda x: "yes" if x == 1.0 else "no")
        return g.rename(
            columns={"sum": "urgent", "count": "total", "mean": "urgency_rate"}
        ).to_dict(orient="index")

    comorbidities = {
        "hypertension": comorbidity_stats("hypertension"),
        "heart_disease": comorbidity_stats("heart_disease"),
        "exercise_angina": comorbidity_stats("exercise angina"),
    }

    # ── 8. Vital sign distributions (histogram buckets) ───────────────────────
    def hist_buckets(col: str, bins: int = 10) -> dict:
        counts, edges = np.histogram(df[col].dropna(), bins=bins)
        labels = [f"{edges[i]:.0f}-{edges[i+1]:.0f}" for i in range(len(edges) - 1)]
        return {"labels": labels, "counts": counts.tolist()}

    distributions = {
        "age": hist_buckets("age"),
        "blood_pressure": hist_buckets("blood pressure"),
        "max_heart_rate": hist_buckets("max heart rate"),
        "bmi": hist_buckets("bmi"),
    }

    # ── 9. Correlation of numeric features with urgency ────────────────────────
    numeric_cols = [
        "age",
        "blood pressure",
        "max heart rate",
        "bmi",
        "chest pain type",
        "exercise angina",
        "hypertension",
        "heart_disease",
    ]
    corr = df[numeric_cols + ["y"]].corr()["y"].drop("y").round(4)
    feature_correlations = corr.sort_values(ascending=False).to_dict()

    # ── 10. Age-bucket × Chest Pain Type heatmap data ─────────────────────────
    heatmap = (
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

    # ── 11. Risk segments ──────────────────────────────────────────────────────
    # Define high-risk = any 2+ of: age≥60, BP≥140, hypertension, heart_disease, chest_pain∈{3,4}
    df2 = df.copy()
    df2["risk_age"] = (df2["age"] >= 60).astype(int)
    df2["risk_bp"] = (df2["blood pressure"] >= 140).astype(int)
    df2["risk_hypertension"] = df2["hypertension"].astype(int)
    df2["risk_heart"] = df2["heart_disease"].astype(int)
    df2["risk_cp"] = df2["chest pain type"].isin([3, 4]).astype(int)
    df2["risk_score"] = df2[
        ["risk_age", "risk_bp", "risk_hypertension", "risk_heart", "risk_cp"]
    ].sum(axis=1)

    risk_segments = (
        df2.groupby("risk_score")
        .agg(total=("y", "count"), urgent=("y", "sum"), urgency_rate=("y", "mean"))
        .reset_index()
        .assign(urgency_rate=lambda x: x["urgency_rate"].round(4))
        .rename(columns={"risk_score": "risk_factor_count"})
        .to_dict(orient="records")
    )

    return {
        "overview": overview,
        "urgency_by_age_group": urgency_by_age,
        "urgency_by_chest_pain": urgency_by_chest_pain,
        "urgency_by_smoking": urgency_by_smoking,
        "urgency_by_bp_category": urgency_by_bp,
        "urgency_by_bmi_category": urgency_by_bmi,
        "comorbidities": comorbidities,
        "distributions": distributions,
        "feature_correlations": feature_correlations,
        "age_chest_pain_heatmap": heatmap,
        "risk_segments": risk_segments,
    }
