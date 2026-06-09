# [核心] 智能体组装与执行逻辑
from deepagents import create_deep_agent

from agent.llm import llm
from agent.load_prompt import main_agent_config
from agent.sub_agents.internet_sub_agent import search_sub_agent

print(main_agent_config['system_prompt'])
main_agent = create_deep_agent(
    model=llm,
    system_prompt=main_agent_config['system_prompt'],
    subagents=[search_sub_agent],
    tools=[]
)


if __name__ == '__main__':
    result = main_agent.invoke({
        "messages": [{"role": "user", "content": "今天武汉天气怎么样?"}]
    })
    print(result['messages'][-1].content)