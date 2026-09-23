from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.entities.value_info import ValueInfo
from app.prompt.prompt_load import load_prompt
from app.core.log import logger


async def recall_value(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("召回字段取值")

    query = state["query"]
    keywords = state["keywords"]
    value_es_repository = runtime.context["value_es_repository"]

    # 借助 LLM 扩展关键词
    prompt = PromptTemplate(template=load_prompt('extend_keywords_for_value_recall'), input_variables=['query'])
    output_parsers = JsonOutputParser()
    chain = prompt | llm | output_parsers

    result = await chain.ainvoke({"query": query})

    keywords = set(keywords + result)

    # 根据关键词召回字段取值
    value_infos_map: dict[str, ValueInfo] = {}
    for keyword in keywords:
        current_value_infos: list[ValueInfo] = await value_es_repository.search(keyword)
        for current_value_info in current_value_infos:
            if current_value_info.id not in value_infos_map:
                value_infos_map[current_value_info.id] = current_value_info

    retrieved_value_infos: list[ValueInfo] = list(value_infos_map.values())
    logger.info(f"检索到的字段取值信息: {list(value_infos_map.keys())}")
    return {'retrieved_value_infos': retrieved_value_infos}
