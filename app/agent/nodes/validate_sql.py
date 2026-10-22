from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.core.log import logger


async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "校验SQL"
    writer({"type": "progress", "step": step, "status": "running"})

    try:
        sql = state['sql']
        dw_mysql_repository: DWMySQLRepository = runtime.context['dw_mysql_repository']
        try:
            await dw_mysql_repository.validate(sql)
            logger.info("SQL语法正确")
            writer({"type": "progress", "step": step, "status": "success"})
            return {'error': None}
        except Exception as e:
            logger.error(f"SQL语法错误: {str(e)}")
            writer({"type": "progress", "step": step, "status": "success"})
            return {'error': str(e)}
    except Exception as e:
        logger.error(f"{step} 错误: {e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
