from typing import TypedDict


class DataAgentState(TypedDict):
    query: str  # 用户输入的SQL查询
    keywords: list[str]  # 提取的关键词
    error: str  # 校验SQL时出现的错误信息
