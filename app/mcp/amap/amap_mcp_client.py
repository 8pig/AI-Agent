from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

from app.bailian.common import llm, file_tools


async def create_amap_client():
    mcp_config = {
        "amap": {
            "url": "https://mcp.amap.com/sse?key=ca4d9b4b851b694faced0fe50079a24d",
            "transport": "sse"

        }
    }

    client = MultiServerMCPClient(mcp_config)
    print( client)
    tools = await client.get_tools()
    print(tools)
    return client, tools

async def create_and_run_agent():
    client, tools = await create_amap_client()

    agent = initialize_agent(
        llm=llm,
        tools=tools + file_tools,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    print(file_tools)

    prompt_template =PromptTemplate.from_template("你是一个智能助手，可以使用高德mcp 工具，问题: {input}")

    prompt = prompt_template.format(input="""
        目标： 
        - 明天我要从三街坊到北京西站
        - 线路选择,地铁或者公交
        - 考虑出行时间和路线以及天气情况
        
        要求:
        - 制作网页展示出线路和位置, 输出一个html页面, 路径\\.temp 目录下travel.html,
        - 网页使用简约美观风格, 以及卡片展示
        - 行程规划的结果要在APP展示, 并集成到H5页面中
    """)

    print(prompt)
    resp = await agent.ainvoke(prompt)
    print(resp)
    return resp

asyncio.run(create_and_run_agent())