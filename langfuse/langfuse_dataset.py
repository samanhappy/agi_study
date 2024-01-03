import json

from langfuse import Langfuse
from langfuse.model import CreateDatasetRequest, CreateDatasetItemRequest
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# init
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)

langfuse.create_dataset(CreateDatasetRequest(name="wiki_qa-20"))

print(os.getcwd())
qa_pairs = []
with open("langfuse/example_dataset.jsonl", "r", encoding="utf-8") as fp:
    for line in fp:
        example = json.loads(line.strip())
        qa_pairs.append(example)

for item in qa_pairs[:20]:
    langfuse.create_dataset_item(
        CreateDatasetItemRequest(
            dataset_name="wiki_qa-20",
            # any python object or value
            input=item["question"],
            # any python object or value, optional
            expected_output=item["answer"],
        )
    )
