import os
import httpx

from langchain_core.embeddings import Embeddings
from app.core.config import(JINA_EMBEDDING_API_KEY)


class JinaEmbeddings(Embeddings):

    def __init__(
        self,
        model: str = "jina-embeddings-v3"
    ):
        self.api_key = JINA_EMBEDDING_API_KEY
        self.model = model

        if not self.api_key:
            raise ValueError(
                "JINA_EMBEDDING_API_KEY is not configured"
            )

    def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        response = httpx.post(
            "https://api.jina.ai/v1/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "input": texts
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return [
            item["embedding"]
            for item in data["data"]
        ]

    def embed_query(
        self,
        text: str
    ) -> list[float]:

        response = httpx.post(
            "https://api.jina.ai/v1/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "input": [text]
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["data"][0]["embedding"]


def create_embeddings():

    return JinaEmbeddings()