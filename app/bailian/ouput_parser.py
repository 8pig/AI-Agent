from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser

from app.bailian.common import chat_prompt_template, llm

# parser = StrOutputParser ()
parser = CommaSeparatedListOutputParser ()

chain = chat_prompt_template | llm | parser

resp = chain.invoke(input={
    "role": "高数",
    "domain": "数学计算",
    "question": " 1111+12=?"
})

print( resp)

