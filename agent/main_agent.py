# [核心] 智能体组装与执行逻辑
import shutil
from pathlib import Path

from deepagents import create_deep_agent

from agent.llm import llm
from agent.load_prompt import main_agent_config
from agent.sub_agents.rag_sub_agent import rag_sub_agent
from agent.sub_agents.db_sub_agent import db_sub_agent
from agent.sub_agents.internet_sub_agent import search_sub_agent
from api.context import set_thread_context, set_session_context
from api.monitor import monitor
from tools.markdown_tools import generate_markdown
from tools.pdf_tools import convert_md_to_pdf
from tools.upload_file_read_tool import read_file_content

print(main_agent_config['system_prompt'])
main_agent = create_deep_agent(
    model=llm,
    system_prompt=main_agent_config['system_prompt'],
    subagents=[rag_sub_agent, db_sub_agent, search_sub_agent],
    tools=[read_file_content, generate_markdown, convert_md_to_pdf]
)

def _report_agent_process(chunk):
    for key, value in chunk.items():
        # print(f"=={key}==")
        # print(value)
        if not value or "messages" not in value: continue
        message = value["messages"][-1]
        if key == "model":
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    # 区分子智能体和工具
                    if tool_call["name"] == "task":
                        # print( f"--准备调用子智能体{tool_call['args']['subagent_type']}, 参数：{tool_call['args']['description']}")
                        monitor.report_assistant(tool_call['args']['subagent_type'], tool_call['args']['description'])
                    else:
                        # print(f"--智能体准备调用工具{tool_call['name']}, 参数：{tool_call['args']}")
                        monitor.report_tool(tool_call['name'], tool_call['args'])
            elif message.content:
                # print(f"--智能体返回最终结果: {message.content}")
                monitor.report_task_result(message.content)
        # elif key == "tools":
        #     if message.name == "task":
        #         print(f"--调用子智能体返回的结果为：{message.content}")
        #     else:
        #         print(f"--调用工具{message.name}返回的结果为：{message.content}")

async def run_deep_agent(query: str, thread_id: str):

    # 在调用agent之前，保存thread_id, session_dir_str
    # 保存thread_id
    set_thread_context(thread_id)
    # 生成session_dir_str， 再保存session_dir_str，, 并向前端发送session_dir_str
    project_dir = Path(__file__).parents[1].resolve()  # 项目根目录
    session_dir = project_dir / "output" / f"session_{thread_id}"  # 拼接生成sesion目录path对象
    session_dir.mkdir(parents=True, exist_ok=True)  # 确保输出目录存在
    session_dir_str = str(session_dir).replace("\\", "/") # 生成完整路径字符串
    set_session_context(session_dir_str) # 保存session_dir_str
    monitor.report_session_dir(session_dir_str) # 告诉前端，当前会话的输出目录, 浏览器才能在右侧显示会话文件列表

    # 将upload中的文件拷贝到session目录中
    upload_dir = project_dir / "upload" / f"session_{thread_id}"
    if upload_dir.exists():
        # 得到所有文件的列表
        file_names = [ item.name for item in upload_dir.iterdir() if item.is_file()]
        for name in file_names:
            shutil.copy2(upload_dir/name, session_dir/name)

    # 执行agent,遍历过程数据，并将特定数据信息发送给前端
    result = main_agent.astream({
        "messages": [{
            "role": "user",
            "content": query
        }]
    })
    async for chunk in result:
        # 遍历每个chunk,向前端发送当前状态及数据
        _report_agent_process(chunk)
