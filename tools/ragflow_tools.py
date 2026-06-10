# RAG 工具
import os

from dotenv import load_dotenv
from ragflow_sdk import RAGFlow
from scripts.regsetup import description

# 加载.env
load_dotenv()

# 创建ragflow客户端
_ragflow_client = RAGFlow(
    base_url="http://118.195.133.223",
    api_key="ragflow-M2NzZmYzEyNjI4MTExZjE4ODVhOGU1ZD"
)

# 获取所有助手列表
def get_chat_list() -> str:
    """
    获取ragflow服务中所有的聊天助手信息! 用于后续具体提问的筛选!
    :return:
        返回格式:
        助手名称:xxx , 描述: xx , 关联的知识库: x,x,x,x \n
        助手名称:xxx , 描述: xx , 关联的知识库: x,x,x,x \n
    """
    # 获取所有chat列表
    chats = _ragflow_client.list_chats()
    print(chats)
    if not chats:
        return "没有找到任何助手!"
    final_str = ''
    for chat in chats:
        # print(f"chat : {chat}")
        name = chat.name
        description = chat.description
        datasets_str = ",".join([item["name"] for item in chat.datasets])
        final_str += f"助手名称:{name} , 描述: {description} , 关联的知识库: {datasets_str} \n"
        # print(name, description, datasets)
    return final_str
if __name__ == "__main__":
    print(get_chat_list())