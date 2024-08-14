import requests
import time
import os
from typing import Generator
from zhipuai import ZhipuAI
import jwt
from dialogue_data_types import TextMsg, TextMsgList, MsgList, CharacterMeta


# 智谱开放平台API key，参考 https://open.bigmodel.cn/usercenter/apikeys
API_KEY: str = os.getenv("API_KEY", "1697d74bca9fbf5de3939b8836b52008.gRABWRBZI7HHUBq8")


class ApiKeyNotSet(ValueError):
    pass


def verify_api_key_not_empty():
    if not API_KEY:
        raise ApiKeyNotSet


def get_characterglm_response_via_sdk(messages: TextMsgList, meta: CharacterMeta):
    """ 通过sdk调用CharacterGLM """
    verify_api_key_not_empty()

    print(f"get_characterglm_response_via_sdk - messages passed to function was:  {messages}\n\n\n")
    print(f"get_characterglm_response_via_sdk - meta passed to function was:  {meta}\n\n\n")
    client = ZhipuAI(api_key=API_KEY) # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="charglm-3",  # 填写需要调用的模型名称
        messages=messages,
        meta=meta
    )

    return response.choices[0].message.content
    

def get_chatglm_response_via_sdk(messages):
    """ 通过sdk调用chatglm """
    # reference: https://open.bigmodel.cn/dev/api#glm-3-turbo  `GLM-3-Turbo`相关内容
    # 需要安装新版zhipuai
    # print(f"messages passed to function was:  {messages}")

    verify_api_key_not_empty()
    # print(f"API_KEY passed to function was:  {API_KEY}")
    client = ZhipuAI(api_key=API_KEY) # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型编码
        messages=messages
    )
    return response.choices[0].message.content


def generate_roles(novel_desc: str):
    """ 用chatglm生成两名角色的人设特征 """

    instruction = f"""
请从下列文本中，抽取人物的背景、性格设定和人物关系。要求：
1. 生成两名角色的性格特征和两人的关系，两人关系写在第二个人的描述中，不用单独列出。
2. 描写不能包含敏感词，人物形象需得体。
3. 尽量用短语描写，而不是完整的句子。
4. 每名角色设定描述在20字到50字之间
5. 如果文本中人物超过两个，仅挑选两个人物生成人设，如果描写仅能生成一个人设，另一个人设自行推测
6. 生成一句角色二的对白，用对白开头，分号后跟生成的对白内容，不要用双引号或单引号把对白内容引用起来，生成内容不能含有冒号
生成格式如下，不要出现经推测等字样：
张三:张三是一名侠客。
李四:李四常年游手好闲。张三是李四的好兄弟。
对白:张三你帮帮我，最近手头有点紧。

{novel_desc}
"""
    # print(f"instruction passed to function was:  {instruction}")
    
    res = get_chatglm_response_via_sdk(
        messages=[
            {
                "role": "user",
                "content": instruction.strip()
            }
        ]
    )
    lines = res.splitlines()
    # print(f"lines passed to function was:  {lines}")

    parsed_data = {}

    for line in lines:
        if ':' in line:
            key, value = line.split(":", 1)
            parsed_data[key.strip()] = value.strip()
        if '：' in line:
            key, value = line.split("：", 1)
            parsed_data[key.strip()] = value.strip()

    return parsed_data




