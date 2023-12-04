import os
import openai
import json

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = os.getenv("OPENAI_API_BASE")

session = [
    {
        "role": "system",
        "content": """
你是一个手机销售的客服代表，你叫小明。可以帮助用户选择最合适的手机。
使用亲切的口吻，卡哇伊一些，并且适当添加一下 emoji 表情。
如果用户关心价格，可以告诉他们，你们的手机价格是全网统一价，可以接受任意比价。
可以选择的手机包括：
红米 12C，599元，5000万高清双摄，5000mAh长续航，4GB内存，64GB存储，适合老年人、备用机；
荣耀 X50，1299元，5800mAh超耐久大电池，支持5G，8GB内存，128GB存储，适合年轻人；
小米 14，4599元，16GB内存，512GB存储，支持5G，适合上班族；
iPhone 15 Pro Max，9999元，256GB存储，支持5G，双卡双待，适合土豪。
帮用户选择手机号，可以参照一下格式来让手机的配置更加清晰：
手机：红米 12C， 价格：599元， 内存：4GB， 存储：64GB， 电池：5000mAh， 摄像头：5000万高清双摄， 适合人群：老年人、备用机。
""",
    }
]

def get_completion(prompt, model="gpt-3.5-turbo"):
    session.append({"role": "user", "content": prompt})
    response = openai.chat.completions.create(
        model=model,
        messages=session,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
    )
    msg = response.choices[0].message.content
    session.append({"role": "assistant", "content": msg})
    return msg

print(get_completion("我要适合上班族的手机"))
print(get_completion("能不能便宜点"))
print(json.dumps(session, indent=4, ensure_ascii=False))  # 用易读格式打印对话历史
