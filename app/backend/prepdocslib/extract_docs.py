import json
import logging
import os
import re
from typing import Dict, List, Tuple
from langchain_core.documents import Document

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

# Set Path Variables
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, "docs"))
APPROVED_SOURCES_PATH = os.path.join(DOCS_DIR, "approved_sources.json")

logger = logging.getLogger(__name__)




def clean_text(text: str) -> str:
    """
    Cleans raw text from web pages:
    - Collapses multiple newlines to max 2
    - Removes excessive spaces and tabs
    - Strips leading/trailing whitespace

    Args:
        text (str): Uncleaned text with any of the above issues
    
    Returns:
        str: Cleaned text
    """
    text = re.sub(r"\n{3,}", "\n\n", text)        # Replace 3+ newlines with 2
    text = re.sub(r"[ \t]+", " ", text)           # Replace multiple spaces/tabs with single space
    return text.strip()


def extract_docs_from_urls(ignore: List[str] = []) -> Tuple[List[Document], List[str]]:
    """
    Extract Documents from URLs indicated in the approved sources.json

    Args:
        ignore (List[str]): List of urls to ignore

    Returns:
        List[Document]: List of Documents extracted from the all the approved URLs
        List[str]: List of filenames of documents extracted
    """
    logger.info("Extracting documents from approved URLs")

    # Extract all approved urls from the json
    with open(APPROVED_SOURCES_PATH, "r") as f:
        data: dict = json.load(f)
    urls: List[str] = data.get("urls", [])

    # Filter urls list for anything in urls
    filtered_urls = [url for url in urls if url not in ignore]

    # Short circuit operation to return docs
    if len(filtered_urls) == 0:
        logger.info("No approved URLs found, exiting operation.")
        return [], []
    
    # Load from dedicated websites (Assumes no more than 50 websites, else look into lazy load)
    loader = WebBaseLoader(
        filtered_urls,
        header_template={"User-Agent": "DBTT_G5T1_Bot/1.0"}
    )
    docs = loader.load()

    # Clean each document before returning
    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    logger.info("Successfully extracted from URLs")
    return docs, urls


def extract_docs_from_pdfs(ignore: List[str] = []) -> Tuple[List[Document], List[str]]:
    """
    Extract Documents from PDFs located in docs folder

    Args:
        ignore (List[str]): List of filenames to ignore

    Returns:
        List[Document]: List of Documents extracted from the all the approved PDFs
        List[str]: List of filenames of documents extracted
    """
    logger.info("Extracting documents from approved PDFs")
    all_documents: List[Document] = []
    filenames: List[str] = []

    # Ensures that the path is a directory
    if os.path.isdir(DOCS_DIR):
        # Loops through all files in the directory and finds .pdf files only
        for file in os.listdir(DOCS_DIR):
            if file.lower().endswith(".pdf"):
                # Only create document if file is not to be ignored
                if file not in ignore:
                    pdf_path = os.path.join(DOCS_DIR, file)

                    try:
                        # Initialize a loader for each PDF file
                        loader = PyPDFLoader(pdf_path)
                        # Load the pages/documents and add to the list
                        docs = loader.load()
                        # Clean each document before inserting
                        for doc in docs:
                            doc.page_content = clean_text(doc.page_content)
                        all_documents.extend(docs)
                        filenames.append(file)

                    except Exception as exc:
                        logger.warning(f"Error loading {pdf_path}: {exc}")
                
                # Append filename to config
                else:
                    filenames.append(file)

    logger.info("Successfully extracted from PDFs")
    return all_documents, filenames


def extract_docs(urls: bool = True, pdfs: bool = True, ignore: Dict[str, List[str]] = {}) -> Tuple[List[Document], Dict[str, List[str]]]:
    """
    Extract all documents from approved sources

    Args:
        urls (bool): Boolean whether to extract URLs
        pdfs (bool): Boolean whether to extract PDFs
        ignore (Dict[str, List[str]]): Dictionary containing list of URLs/PDFs to avoid

    Returns:
        List[Document]: List of Documents extracted from the all the approved sources
        Dict[str, List[str]]: Dictionary containing all filenames/urls of approved sources
    """
    logger.info("Extracting all documents")
    documents: List[Document] = []
    filenames: dict[str, list] = {}

    if urls:
        docs, names = extract_docs_from_urls(ignore=ignore.get("urls", []))
        documents.extend(docs)
        filenames["urls"] = names
    if pdfs:
        docs, names = extract_docs_from_pdfs(ignore=ignore.get("pdfs", []))
        documents.extend(docs)
        filenames["pdfs"] = names
    
    logger.info("Successfully extracted all documents")
    return documents, filenames


if __name__ == "__main__":
    docs = extract_docs(urls=True, pdfs=True)

    for doc in docs:
        print(json.dumps(doc.model_dump(), indent=4))
