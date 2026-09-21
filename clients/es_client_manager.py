from elasticsearch import AsyncElasticsearch

from app.conf.app_config import ESConfig, app_config


class ESClientManager:
    def __init__(self, config: ESConfig):
        self.client: AsyncElasticsearch | None = None
        self.config: ESConfig = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = AsyncElasticsearch(hosts=[self._get_url()])

    async def close(self):
        await self.client.close()


es_client_manager = ESClientManager(app_config.es)

if __name__ == '__main__':
    es_client_manager.init()
    client = es_client_manager.client


    def test():
        # 创建数据
        # client.indices.create(
        #     index="books",
        # )

        # 写入数据
        client.index(
            index="books",
            document={
                "name": "Snow Crash",
                "author": "Neal Stephenson",
                "release_date": "1992-06-01",
                "page_count": 470
            },
        )

        # 查询文档
        resp = client.search(
            index="books",
        )
        print(resp)

        es_client_manager.close()


    test()
