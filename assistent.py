from openai import OpenAI
from anyio import sleep
from dotenv import load_dotenv, find_dotenv
import json
import math
import os

_ = load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

assistant = client.beta.assistants.create(
    name="平方根计算器",
    instructions="你是一个专业的平方根计算器，用户输入任何一个数字，你通过调用对应的函数来得到结果",
    model="gpt-3.5-turbo",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "sqrt",
                "description": "计算平方根",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "数字",
                        }
                    },
                    "required": ["x"],
                },
            },
        }
    ],
)
print(assistant)

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "计算256的平方根",
        }
    ]
)
print(thread)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
print(run)

while True:
    print(run.status)
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages.data[0].content[0].text.value)
        break
    elif run.status == "failed":
        break
    elif run.status == "queued":
        sleep(1000)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id)
        continue
    elif run.status == "requires_action":
        require_action = run.required_action
        print(require_action)
        output = []
        for submit_tool in require_action.submit_tool_outputs.tool_calls:
            if submit_tool.function.name == "sqrt":
                args = json.loads(submit_tool.function.arguments)
                result = math.sqrt(args.get("x"))
                output.append(
                    {"output": result, "tool_call_id": submit_tool.id})

            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id, run_id=run.id, tool_outputs=output
            )
    elif run.status == "in_progress":
        sleep(1000)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id)
        continue
    else:
        print("unknown status")
        break
