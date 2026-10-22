import asyncio

from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.app_config import EmbeddingConfig, app_config


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        # 只需要保留 LangChain 封装的客户端即可，移除原生的 InferenceClient
        self.client: HuggingFaceEndpointEmbeddings | None = None
        self.config: EmbeddingConfig = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        url = self._get_url()
        # 关键修改：使用 LangChain 封装的类，并传入本地 TEI 服务的地址
        self.client = HuggingFaceEndpointEmbeddings(model=url)


embedding_client_manager = EmbeddingClientManager(app_config.embedding)

if __name__ == '__main__':
    embedding_client_manager.init()
    # 获取 LangChain 封装的客户端
    client = embedding_client_manager.client


    async def test():
        # 测试异步批量向量化
        texts = ["This is a test document.", "This is another test document."]
        # 调用 LangChain 标准的异步批量嵌入方法
        query_result = await client.aembed_documents(texts)
        print(query_result[0][:3])


    asyncio.run(test())
