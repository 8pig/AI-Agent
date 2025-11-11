from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

from app.bailian.common import llm


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
        tools=tools,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template =PromptTemplate.from_template("你是一个智能助手，可以使用高德mcp 工具，问题: {input}")

    prompt = prompt_template.format(input="提供北京南站到望京soho的路线")

    print(prompt)
    resp = await agent.ainvoke(prompt)
    print(resp)
    return resp

asyncio.run(create_and_run_agent())