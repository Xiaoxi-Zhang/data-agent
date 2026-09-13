import asyncio

from huggingface_hub import AsyncInferenceClient, InferenceClient
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.app_config import EmbeddingConfig, app_config


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: HuggingFaceEndpointEmbeddings | None = None
        self.async_client: AsyncInferenceClient | None = None
        self.config: EmbeddingConfig = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        url = self._get_url()
        self.client = InferenceClient(model=url)
        self.async_client = AsyncInferenceClient(model=url)


embedding_client_manager = EmbeddingClientManager(app_config.embedding)

if __name__ == '__main__':
    embedding_client_manager.init()
    client = embedding_client_manager.async_client


    async def test():
        query_result = await client.feature_extraction("This is a test document.")
        print(query_result[:3])


    asyncio.run(test())
