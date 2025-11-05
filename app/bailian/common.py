from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

llm = ChatOpenAI(
    model="qwen-max-latest",
    # model="qwen3-235b-a22b",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(""),
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