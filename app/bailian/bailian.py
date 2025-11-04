

from pydantic import SecretStr

from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY")).get_secret_value(),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [
    {"role": "user", "content": "碳元素的同位素是什么? "},
    {"role": "system", "content": "你是一个法律助手, 帮助用户解答相关文档, 如果不是法律范围问题, 请回答 无法回答, 回答内容请遵守法律法规"},
]
completion = client.chat.completions.create(
    model="qwen3-235b-a22b",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)