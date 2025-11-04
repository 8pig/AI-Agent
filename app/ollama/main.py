from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

if __name__ == "__main__":
    llm = ChatOllama(
        model="qwen3:1.7b",
        base_url="http://localhost:11434",
        format="json",
        temperature=0
    )
    response = llm.stream([
        SystemMessage(content="""
        你是一个法律 AI 助手，请按以下规则处理问题：
        1. 法律相关问题：提供法律范围内的回答
        2. 非法律范围问题：回复"抱歉，我只能回答法律相关的问题，无法提供其他领域的专业建议"
        3. 模糊问题：先确认是否为法律问题再回答
        """),
        HumanMessage(content="碳元素的同位素有哪些")
    ])
    for chunk in response:
        print(chunk.content, end="", flush=True)

    # # 确保是预期的响应类型
    # if isinstance(response, AIMessage):
    #     answer = response.content
    #     print(f"回答内容: {answer}")
    # else:
    #     print(f"意外的响应类型: {type(response)}")
