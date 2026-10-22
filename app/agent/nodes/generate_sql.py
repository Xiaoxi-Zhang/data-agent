import yaml
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.prompt.prompt_load import load_prompt
from app.core.log import logger


async def generate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "生成SQL"
    writer({"type": "progress", "step": step, "status": "running"})

    try:
        query = state['query']
        db_info = state['db_info']
        date_info = state['date_info']
        metric_infos = state['metric_infos']
        table_infos = state['table_infos']

        prompt = PromptTemplate(template=load_prompt('generate_sql'),
                                input_variables=['db_info', 'date_info', 'metric_infos', 'table_infos', 'query'])
        output_parsers = StrOutputParser()
        chain = prompt | llm | output_parsers

        result = await chain.ainvoke({"db_info": yaml.dump(db_info, allows_unicode=True, sort_keys=False),
                                    "date_info": yaml.dump(date_info, allows_unicode=True, sort_keys=False),
                                    "metric_infos": yaml.dump(metric_infos, allow_unicode=True, sort_keys=False),
                                    "table_infos": yaml.dump(table_infos, allow_unicode=True, sort_keys=False),
                                    "query": query})
        logger.info(f"生成的SQL: {result}")
        writer({"type": "progress", "step": step, "status": "success"})
        return {'sql': result}
    except Exception as e:
        logger.error(f"{step} 失败: {e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
