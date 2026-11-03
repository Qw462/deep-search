# 搜索工具
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient
from typing import Literal

# 加载.env环境配置，如果在环境变量中配置了，就不会加载.env文件
load_dotenv()

# 创建TavilyClient对象
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 定义一个联网搜索工具函数
@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """使用  Tavily 进行联网搜索"""
    print(f"正在搜索: {query}")
    return tavily_client.search(
        query=query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

if __name__ == "__main__":
    print(type(internet_search))
    internet_search.invoke({"query": "如何使用langchain"})