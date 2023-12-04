from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser


class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, output):
        return output.split(",")


template = """You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more."""
human_template = "{text}"
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("human", human_template),
    ]
)

chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()
print(chain.invoke({"text": "fruit"}))
