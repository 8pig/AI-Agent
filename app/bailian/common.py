from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import SecretStr, BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()  #
# key = input("请输入 API Key: ")
key = os.getenv("DASHSCOPE_API_KEY")
print(key)
llm = ChatOpenAI(
    # model="qwen-max-latest",
    model="qwen3-235b-a22b",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # api_key=key,
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



class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")



@tool(
    description="add two numbers",
    args_schema=AddInputArgs, # 定义入参类型 是class类型
    return_direct=True
)
def add (a, b):
    """add two numbers"""
    return a + b

def create_calc_tools():
    return [add]

calc_tool = create_calc_tools()