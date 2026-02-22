import json
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_docs(
    documents=List[Document], chunk_size: int = 1000, chunk_overlap: int = 200
):
    """
    Recursively Split Documents based on indicated chunk size and chunk overlap

    Args:
        documents (List[Document]): List of Documents that should be split
        chunk_size (int): Optional to set the size of each chunk. Defaults to 1000
        chunk_overlap (int): Optional to set the token overlap between each chunk. Defaults to 200

    Returns:
        List[Document]: List of split documents
    """
    # Initialise recursive splitter based on preset parameters
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    # Return split documents
    return splitter.split_documents(documents)


if __name__ == "__main__":
    docs = [Document(page_content="Hello, I am John")]
    docs = split_docs(documents=docs)

    for doc in docs:
        print(json.dumps(doc.model_dump(), indent=4))
