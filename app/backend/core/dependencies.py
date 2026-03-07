import logging

import numpy as np
import pandas as pd
from config.config import LLM_CLIENT
from fastapi import Depends, Request
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from pandas import DataFrame
from prompts.prompt_manager import JinjaPromptManager
from workflows.components.response_synthesiser import ResponseSynthesiserComponent
from workflows.components.source_retrieval import SourceRetrievalComponent
from workflows.rag_workflow import RAGWorkflow

from utils.file_management import extract_df_from_csv

logger = logging.getLogger(__name__)


def get_llm_client(request: Request) -> ChatOpenAI | ChatGroq:
    """
    Gets the appropriate Langchain AzureChatOpenAI or ChatOpenAI Client.

    Returns:
        ChatOpenAI | ChatGroq: The Langchain ChatOpenAI or ChatGroq instance
    """
    return getattr(request.app.state, LLM_CLIENT)


def get_prompt_manager() -> JinjaPromptManager:
    """Gets the Jinja2 prompt manager."""
    return JinjaPromptManager()


def get_rag_workflow(
    llm_client: ChatOpenAI | ChatGroq = Depends(get_llm_client),
    prompt_manager: JinjaPromptManager = Depends(get_prompt_manager),
) -> RAGWorkflow:
    # Set up components
    source_retrieval = SourceRetrievalComponent(
        name="faiss_index",
        num_sources=4,
    )
    response_synthesiser = ResponseSynthesiserComponent(
        llm_client=llm_client,
        prompt_manager=prompt_manager,
        prompt_filename="response_synthesis.yaml",
    )
    # Set up workflow
    rag_workflow = RAGWorkflow(
        source_retrieval=source_retrieval, response_synthesiser=response_synthesiser
    )
    # Build Graph and return
    rag_workflow.build_graph()
    return rag_workflow


# Chest Pain Mapping between types and name
CHEST_PAIN_MAP: dict[int, str] = {
    0: "Asymptomatic",
    1: "Atypical Angina",
    2: "Non-Anginal",
    3: "Typical Angina",
    4: "Severe Angina",
}


def get_patient_data() -> DataFrame | None:
    # Indicate filename here to not expose to frontend for changes
    filename: str = "patient_priority_modified.csv"

    # Extract DataFrame using utils function
    try:
        df = extract_df_from_csv(filename=filename)
    except Exception as exc:
        logger.exception(exc)
        return None

    # Modifies DataFrame to enhance data
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 30, 40, 50, 60, 70, np.inf],
        labels=["<30", "30-40", "40-50", "50-60", "60-70", "70+"],
        right=False,
    )
    df["bp_category"] = pd.cut(
        df["blood pressure"],
        bins=[0, 120, 130, 140, np.inf],
        labels=[
            "Normal (<120)",
            "Elevated (120-129)",
            "Stage 1 (130-139)",
            "Stage 2 (≥140)",
        ],
        right=False,
    )
    df["bmi_category"] = pd.cut(
        df["bmi"],
        bins=[0, 18.5, 25, 30, np.inf],
        labels=["Underweight", "Normal", "Overweight", "Obese"],
        right=False,
    )
    df["chest_pain_label"] = df["chest pain type"].map(CHEST_PAIN_MAP).fillna("Unknown")

    # Returns DataFrame here
    return df
