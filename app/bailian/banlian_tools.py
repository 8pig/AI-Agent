from sys import prefix
from tkinter.scrolledtext import example

from langchain_openai import  ChatOpenAI
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, ChatMessagePromptTemplate, FewShotPromptTemplate
import os


llm = ChatOpenAI(
    model="qwen-max-latest",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr("填写百炼的api key"),
    streaming=True,
)

system_message_template = ChatMessagePromptTemplate.from_template(
    template =  "你是一个{role}专家, 帮助用户解答{domain}领域的问题, 回答内容请遵守法律法规",
    role="system"
)

human_message_template = ChatMessagePromptTemplate.from_template(
    template = "用户的问题: {question}",
    role="user"
)

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message_template,
    human_message_template
])


# 抽象到上面  system 与 user prompt temp
# chat_prompt_template = ChatPromptTemplate.from_messages([
#     ("system", "你是一个{role}专家, 帮助用户解答{domain}领域的问题, 回答内容请遵守法律法规"),
#     ("user", "用户的问题: {question}")
# ])



# prompt = chat_prompt_template.format_messages(
#     role="编程",
#     domain="web开发",
#     question="你擅长什么")


# 提示词模板
example_prompt = "输入:{input}\n输出:{output}"
# 示例
examples = [
    {"input": "将hello 翻译为中文", "output": "你好"},
    {"input": "GoodBye 翻译为中文", "output": "再见"},
    {"input": "pen 翻译为中文", "output": "钢笔"},
]


few_shot_prompt_template = FewShotPromptTemplate(
    examples = examples,
    example_prompt=PromptTemplate.from_template(example_prompt),
    #
    prefix="请将一下英文翻译中文",
    suffix="输入:{text}\n 输出:",
    input_variables=["text"], # text 替换suffix 中的 {text}
)



# # 创建提示词模板
# prompt_template = PromptTemplate.from_template("今天{something}真不错")
# #
# # # 模板+变量 = 提示词
# prompt = prompt_template.format(something="天气")
#
# print(prompt_template)

prompt = few_shot_prompt_template.format(text="what fucking are you doing")
print(prompt)
resp = llm.stream(prompt)

for chunk in resp:
    if hasattr(chunk, 'content'):
        print(chunk.content, end="", flush=True)

# 如果确实需要流式处理
# for chunk in llm.stream(prompt):
#     if hasattr(chunk, 'content'):
#         print(chunk.content, end="", flush=True)
