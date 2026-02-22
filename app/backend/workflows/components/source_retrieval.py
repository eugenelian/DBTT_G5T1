import json
import logging
import os

from core.settings import Settings, get_settings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from schemas.state import State

logger = logging.getLogger(__name__)


class SourceRetrievalComponent:
    """
    The source retrieval component obtains relevant chunks from the local vector store
    """

    SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
    FAISS_DIR = os.path.abspath(
        os.path.join(SCRIPT_PATH, "..", "..", "database", "faiss")
    )

    def __init__(self, name: str):
        # Obtain settings
        s: Settings = get_settings()

        # Instantiate vector store path
        vector_store_path = os.path.join(type(self).FAISS_DIR, name)

        # Load FAISS config
        with open(os.path.join(type(self).FAISS_DIR, "faiss_config.json"), "r") as f:
            config: dict = json.load(f)
            self.metadata: dict = config.get("metadata", {})

        # Set up embedding model
        embeddings = OpenAIEmbeddings(
            model=self.metadata.get("embedding_model", s.OPENAI_EMB_MODEL)
        )

        # Security risk as it involves unpickling data from the index.pkl file, ensure that .pkl is not tampered with
        self.vectorstore = FAISS.load_local(
            vector_store_path, embeddings, allow_dangerous_deserialization=True
        )

    async def retrieve(self, state: State):
        """
        Retrieve sources based on the user query

        Args:
            state: State that contains information about "user_query"

        Returns:
            state: Updated state containing the "sources"
        """
        try:
            sources = self.vectorstore.similarity_search(state.user_query, k=4)
            return {"sources": [source.model_dump() for source in sources]}

        except Exception as exc:
            logger.warning("Exception occurred: %s", exc)
            return {}
