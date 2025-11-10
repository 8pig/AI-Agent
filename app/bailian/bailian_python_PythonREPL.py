import json

from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from langchain_experimental.tools.python.tool import PythonREPLTool

from app.bailian.common import llm

# 定义工具
tools = [PythonREPLTool()]
#创建智能体
tool_names = ["PythonREPLTool"]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# 创建提示词
prompt_template = PromptTemplate.from_template(
    template="""
    尽你所能回答问题或执行用户的命令, 你可以使用{tool_names}工具
    --
    请按照一下格式思考:
    # 思考的过程
        - 问题: 你必须回答的输入问题
        - 思考: 你考虑应该怎么做
        - 行动: 应该选择一个{tool_names}中的一个
        - 行动输入: 行动的输入
        - 观察: 观察你选择的行动所返回的结果
        > (思考/行动/行动输入/观察 可以重复多次)
    --
    # 最终答案
        - 对原始输入问题的最终答案
        
    **注意**
    - PythonREPLTool入参是python代码, 不允许添加```py 等标记
    
    问题:  {input}
    """
)

# 创建提示词
prompt = prompt_template.format(
    tool_names=",".join(tool_names),
    input="""
        1. 向D:\\code\\ai-agent-test\\.temp 写一个文件, index.html,
        2. 写一个企业官网
        3. 要求有3个tabs, 首页, 加入我们, 关于我们, 并且可以点击切换内容
        3. 使用React
    """,
)

print( prompt)

resp = agent.invoke(prompt)
print(resp)