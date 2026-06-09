# llm初始化
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 加载.env
load_dotenv()

llm = init_chat_model(
    model=os.getenv("LLM_QWEN_PLUS", "qwen-max"),
    model_provider="openai",
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)