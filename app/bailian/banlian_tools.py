from app.bailian.common import chat_prompt_template, llm
from langchain_core.tools import  Tool

def add (a, b):
        return a + b

# 转化fn wei langchain 可以使用的对象
add_tools =Tool.from_function(
    func=add,
    name="add",
    description="加法计算"
)


# 将tools 与llm 绑定
llm_with_tools = llm.bind_tools([add_tools])
chain = chat_prompt_template | llm_with_tools

# 调用
resp = chain.invoke(input={
    "role": "高数",
    "domain": "数学计算",
    "question": "请计算 1111+12=?"
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

    print(tool_func(int(args["__arg1"]), int(args["__arg2"])))
# 注意  大模型不一致，请自行测试

