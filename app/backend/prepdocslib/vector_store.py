# Set Path Variables
import argparse
import json
import logging
import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from app.backend.prepdocslib.extract_docs import extract_docs
from app.backend.prepdocslib.split_docs import split_docs
from app.backend.utils.file_management import create_folder

# Set up ENV variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMB_MODEL = os.getenv("OPENAI_EMB_MODEL", "text-embedding-3-small")
os.environ["USER_AGENT"] = "DBTT_G5T1_Bot/1.0"

# Set Path Variables and ensure that they exists
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, "docs"))
DATABASE_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, "..", "database"))
FAISS_DIR = os.path.abspath(os.path.join(DATABASE_DIR, "faiss"))
create_folder(paths=[DOCS_DIR, DATABASE_DIR, FAISS_DIR])

REQUIRED_FILES = ["index.faiss", "index.pkl", "../faiss_config.json"]

logger = logging.getLogger(__name__)

# Short Circuit here if there is no OpenAI API Key provided'
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API Key provided, unable to build vector store")


def build_vector_store(
    name: str = "faiss_index",
    urls: bool = True,
    pdfs: bool = True,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
):
    """
    Build vector store using all documents from approved sources

    Args:
        name (str): Name to store the vector store. Default to `faiss_index`.
        urls (bool): Boolean whether to extract URLs. Default to `True`.
        pdfs (bool): Boolean whether to extract PDFs. Default to `True`.
        chunk_size (int): Optional to set the size of each chunk. Defaults to 1000.
        chunk_overlap (int): Optional to set the token overlap between each chunk. Defaults to 200.
    """
    try:
        # Extract and split all documents
        docs, config = extract_docs(urls=urls, pdfs=pdfs)
        chunks = split_docs(
            documents=docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        # Set up embeddings and vector store and return
        embeddings = OpenAIEmbeddings(model=OPENAI_EMB_MODEL)
        vectorstore = FAISS.from_documents(chunks, embeddings)

        # Set up local vector store
        path = os.path.join(FAISS_DIR, name)
        vectorstore.save_local(path)

        # Update metadata and save configuration
        config["metadata"] = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "embedding_model": OPENAI_EMB_MODEL,
        }
        with open(os.path.join(FAISS_DIR, "faiss_config.json"), "w") as f:
            json.dump(config, f, indent=2)

    except Exception as exc:
        logger.warning("Unable to build vector store: %s", exc)


def update_vector_store(
    name: str = "faiss_index", urls: bool = True, pdfs: bool = True
):
    """
    Build vector store using all documents from approved sources

    Args:
        name (str): Name of vector store to update. Default to `faiss_index`.
        urls (bool): Boolean whether to update URLs. Default to `True`.
        pdfs (bool): Boolean whether to update PDFs. Default to `True`.
    """
    vector_store_path = os.path.abspath(os.path.join(FAISS_DIR, name))

    # If vector store does not exist, proceed to build and return instead
    if (
        not os.path.exists(vector_store_path)
        or not os.path.isdir(vector_store_path)
        or any(
            not os.path.exists(os.path.join(vector_store_path, f))
            for f in REQUIRED_FILES
        )
    ):
        build_vector_store(name=name, urls=urls, pdfs=pdfs)
        return

    # Load FAISS config
    with open(os.path.join(FAISS_DIR, "faiss_config.json"), "r") as f:
        config: dict = json.load(f)
        metadata: dict = config.get("metadata", {})
    logger.info("Config: %s", config)

    # Data Extraction
    keys_to_keep = ["urls", "pdfs"]
    docs, config_new = extract_docs(
        urls=urls,
        pdfs=pdfs,
        ignore={k: v for k, v in config.items() if k in keys_to_keep},
    )

    # Short Circuit if no documents
    if len(docs) == 0:
        logger.info("No Documents to update vector DB, returning...")
        return

    # Data Splitting into chunks
    chunks = split_docs(
        documents=docs,
        chunk_size=metadata.get("chunk_size", 1000),
        chunk_overlap=metadata.get("chunk_overlap", 200),
    )

    # Load Vector Store
    embeddings = OpenAIEmbeddings(model=metadata.get("embedding_model", OPENAI_EMB_MODEL))
    vectorstore = FAISS.load_local(
        vector_store_path, embeddings, allow_dangerous_deserialization=True
    )

    # Update Vector Store with new chunks
    vectorstore.add_documents(chunks)

    # Update Config dict, considering that there are no overlaps between them
    for key in ["urls", "pdfs"]:
        config[key] = config_new.get(key, [])

    # Save Vector Store and config json
    vectorstore.save_local(vector_store_path)
    with open(os.path.join(FAISS_DIR, "faiss_config.json"), "w") as f:
        json.dump(config, f, indent=2)


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(description="Build FAISS Vector Store")
    parser.add_argument("--function", type=str, default="build")
    parser.add_argument("--name", type=str, default="faiss_index")
    parser.add_argument("--urls", type=bool, default=True)
    parser.add_argument("--pdfs", type=bool, default=True)
    parser.add_argument("--chunk_size", type=int, default=1000)
    parser.add_argument("--chunk_overlap", type=int, default=200)

    args = parser.parse_args()

    # Handle "Build" Vector Store
    if args.function == "build":
        build_vector_store(
            name=args.name,
            urls=args.urls,
            pdfs=args.pdfs,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )

    # Handle "Update" Vector Store
    elif args.function == "update":
        update_vector_store(
            name=args.name,
            urls=args.urls,
            pdfs=args.pdfs,
        )
