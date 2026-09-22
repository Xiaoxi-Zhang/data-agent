from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime
from app.core.log import logger

from app.agent.llm import llm
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.entities.metric_info import MetricInfo
from app.prompt.prompt_load import load_prompt


async def recall_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("召回指标信息")

    query = state['query']
    keywords = state['keywords']
    embedding_client = runtime.context['embedding_client']
    metric_qdrant_repository = runtime.context['metric_qdrant_repository']

    # 借助 LLM 扩展关键词
    prompt = PromptTemplate(template=load_prompt('extend_keywords_for_metric_recall'), input_variables=['query'])
    output_parsers = JsonOutputParser()
    chain = prompt | llm | output_parsers

    result = await chain.ainvoke({"query": query})

    keywords = set(keywords + result)

    # 从 Qdrant 中检索指标信息
    metric_info_map: dict[str, MetricInfo] = {}
    for keyword in keywords:
        # 对 keyword 进行 embedding
        embedding = await embedding_client.aembed_query(keyword)
        current_metric_infos: list[MetricInfo] = await metric_qdrant_repository.search(embedding)
        for metric_info in current_metric_infos:
            if metric_info.id not in metric_info_map:
                metric_info_map[metric_info.id] = metric_info
    retrieved_metric_infos: list[MetricInfo] = list(metric_info_map.values())

    logger.info(f"检索到的指标信息: {list(metric_info_map.keys())}")
    return {'retrieved_metric_infos': retrieved_metric_infos}
