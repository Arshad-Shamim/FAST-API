from langchain_text_splitters import CharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.RAG.create_embedding import create_embeddings


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

PERSISTENT_DIRECTORY = "db/chroma_db"

import io
import os
import pandas as pd

from pypdf import PdfReader
from langchain_core.documents import Document


def parse_file(
    file_content: bytes,
    file_title: str,
    user_id: str,
    storage_path: str
):
    """
    Parse uploaded TXT, PDF, CSV and Excel files
    into LangChain Document objects.
    """

    extension = os.path.splitext(file_title)[1].lower()

    metadata = {
        "user_id": user_id,
        "file_title": file_title,
        "storage_path": storage_path
    }

    # TXT

    if extension == ".txt":

        text = file_content.decode("utf-8")

        return [
            Document(
                page_content=text,
                metadata=metadata
            )
        ]

    # PDF

    elif extension == ".pdf":

        pdf_file = io.BytesIO(file_content)

        reader = PdfReader(pdf_file)

        documents = []

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text()

            if text and text.strip():

                page_metadata = {
                    **metadata,
                    "page": page_number + 1
                }

                documents.append(
                    Document(
                        page_content=text,
                        metadata=page_metadata
                    )
                )

        return documents

    # CSV

    elif extension == ".csv":

        csv_file = io.BytesIO(file_content)

        df = pd.read_csv(csv_file)

        # Convert dataframe to text
        text = df.to_string(index=False)

        return [
            Document(
                page_content=text,
                metadata=metadata
            )
        ]

    # Excel

    elif extension in [".xlsx", ".xls"]:

        excel_file = io.BytesIO(file_content)

        excel_data = pd.read_excel(
            excel_file,
            sheet_name=None
        )

        documents = []

        for sheet_name, df in excel_data.items():

            text = df.to_string(index=False)

            if text.strip():

                sheet_metadata = {
                    **metadata,
                    "sheet": sheet_name
                }

                documents.append(
                    Document(
                        page_content=text,
                        metadata=sheet_metadata
                    )
                )

        return documents

    # Unsupported
    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    
# def create_embeddings():

#     return HuggingFaceEmbeddings(
#         model_name=EMBEDDING_MODEL_NAME
#     )


def get_vector_store():

    embedding_model = create_embeddings()

    return Chroma(
        persist_directory=PERSISTENT_DIRECTORY,
        embedding_function=embedding_model,
        collection_metadata={
            "hnsw:space": "cosine"
        }
    )


def inject_file(
    file_content: bytes,
    file_title: str,
    user_id: str,
    storage_path: str
):

    print(f"Starting ingestion: {file_title}")

    # 1. Parse file

    documents = parse_file(
        file_content=file_content,
        file_title=file_title,
        user_id=user_id,
        storage_path=storage_path
    )

    print(
        f"Parsed {len(documents)} document(s)"
    )

    # 2. Split documents

    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    # 3. Load/Create Chroma

    vectorstore = get_vector_store()

    # 4. Add chunks

    vectorstore.add_documents(chunks)

    print(
        f"Added {len(chunks)} chunks to ChromaDB"
    )

    return vectorstore