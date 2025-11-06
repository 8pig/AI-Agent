from pydantic import BaseModel, Field

from app.bailian.common import chat_prompt_template, llm
from langchain_core.tools import  Tool, tool

# @tool
# def add (a, b):
#         return a + b

# 这样参数和方法会被精准的抓取 理解
class AddInputArgs(BaseModel):
    a: int = Field(description="第一个数字")
    b: int = Field(description="第二个数字")

@tool(
    description="加法计算",
    args_schema=AddInputArgs # 定义入参类型 是class类型
)
def add (a, b):
    """add two numbers"""
    return a + b

# 转化fn wei langchain 可以使用的对象
# add =Tool.from_function(
#     func=add,
#     name="add",
#     description="加法计算"
# )

# 将tools 与llm 绑定
llm_with_tools = llm.bind_tools([add])
chain = chat_prompt_template | llm_with_tools

# 调用
resp = chain.invoke(input={
    "role": "高数",
    "domain": "数学计算",
    "question": " 1111+12=?"
})

# 打印响应
print(resp)


tools_dict = {
    "add": add
}



for tool_calls in resp.tool_calls:
    print(tool_calls) # 数组

    args = tool_calls["args"]
    print(args)

    fn_name = tool_calls["name"]
    print(fn_name)

    tool_func = tools_dict[fn_name]

    # 加上注解后 调用方式和参数发生变化
    print(tool_func.invoke(args))

# 注意  大模型不一致，请自行测试
# 有参数打印证明走的是tools 而不是大模型输出


