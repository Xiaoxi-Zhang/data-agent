from pathlib import Path

from omegaconf import OmegaConf

from app.conf.meta_config import MetaConfig


class MetaKnowledgeService:
    def __init__(self):
        pass

    async def build(self, config_path: Path):
        # 1.读取配置文件
        context = OmegaConf.load(config_path)
        schema = OmegaConf.structured(MetaConfig)
        meta_config: MetaConfig = OmegaConf.to_object(OmegaConf.merge(schema, context))
        print(meta_config.metrics)

        # 2.根据配置文件同步指定的表信息和指标信息
        if meta_config.tables:
            pass

        if meta_config.metrics:
            pass
