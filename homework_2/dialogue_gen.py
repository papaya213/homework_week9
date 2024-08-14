"""
实现 role-play 对话数据生成工具，要求包含下列功能：

基于一段文本（自己找一段文本，复制到提示词就可以了，比如你可以从小说中选取一部分文本，注意文本要用 markdown 格式）生成角色人设，可借助 ChatGLM 实现。
给定两个角色的人设，调用 CharacterGLM 交替生成他们的回复。
将生成的对话数据保存到文件中。
（可选）设计图形界面，通过点击图形界面上的按钮执行对话数据生成，并展示对话数据。


依赖：
pyjwt
requests
streamlit
zhipuai
python-dotenv

运行方式：
```bash
streamlit run dialogue_gen.py
```
"""
import os
import itertools
from typing import Iterator, Optional

import streamlit as st
from dotenv import load_dotenv
# 通过.env文件设置环境变量
# reference: https://github.com/theskumar/python-dotenv
load_dotenv()

import dialogue_api
from dialogue_api import generate_roles, get_characterglm_response_via_sdk
from dialogue_data_types import TextMsg, TextMsgList, MsgList, HistoryMsg


st.set_page_config(page_title="CharacterGLM 角色对话生成器", page_icon="🤖", layout="wide")
debug = os.getenv("DEBUG", "").lower() in ("1", "yes", "y", "true", "t", "on")


def update_api_key(key: Optional[str] = None):
    if debug:
        print(f'update_api_key. st.session_state["API_KEY"] = {st.session_state["API_KEY"]}, key = {key}')
    key = key or st.session_state["API_KEY"]
    if key:
        dialogue_api.API_KEY = key

# 设置API KEY
api_key = st.sidebar.text_input("API_KEY", value=os.getenv("API_KEY", ""), key="API_KEY", type="password", on_change=update_api_key)
update_api_key(api_key)

# 交替对话用meta信息
if "meta" not in st.session_state:
    st.session_state["meta"] = [{
            "user_info": "",
            "bot_info": "",
            "bot_name": "",
            "user_name": ""
        },{
            "user_info": "",
            "bot_info": "",
            "bot_name": "",
            "user_name": ""
        }]


# 初始化
if "history" not in st.session_state:
    st.session_state["history"] = []
if "api_message" not in st.session_state: 
    st.session_state["api_message"] = []
if "novel" not in st.session_state:
    st.session_state["novel"] = ""
if "characters" not in st.session_state:
    st.session_state["characters"] = "待生成"
if "user_content" not in st.session_state:
    st.session_state["user_content"] = ""
if "assistant_content" not in st.session_state:
    st.session_state["assistant_content"] = ""
if "user_info" not in st.session_state:
    st.session_state["user_info"] = ""
if "bot_info" not in st.session_state:
    st.session_state["bot_info"] = ""
if "bot_name" not in st.session_state:
    st.session_state["bot_name"] = ""
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "char_gen_button_disabled" not in st.session_state:
    st.session_state["char_gen_button_disabled"] = False
if "diag_gen_button_disabled" not in st.session_state:
    st.session_state["diag_gen_button_disabled"] = True


button_labels = {
    "gen_dialogue": "继续对话",
    "gen_characters": "生成人设"
}


# 小说段落输入框
novel = st.text_area("请输入一段小说文字用于生成两个角色人设", height=200)

# 生成人设按钮
if st.button(button_labels["gen_characters"], key="gen_characters", disabled=st.session_state["char_gen_button_disabled"]):
    print("gen_characters clicked")
    if novel:
        characters = generate_roles(novel)
        if len(characters) != 3:
            st.warning("人设生成解析失败")
        else:
            iterator = iter(characters)
            bot_name = next(iterator)
            bot_info = characters[bot_name]
            st.session_state.update(bot_name=bot_name)
            st.session_state.update(bot_info=bot_info)
            st.session_state["meta"][1].update(bot_name=bot_name)
            st.session_state["meta"][1].update(bot_info=bot_info)
            st.session_state["meta"][0].update(user_name=bot_name)
            st.session_state["meta"][0].update(user_info=bot_info)
            user_name = next(iterator)
            user_info = characters[user_name]
            st.session_state["meta"][0].update(bot_name= user_name)
            st.session_state["meta"][0].update(bot_info= user_info)
            st.session_state["meta"][1].update(user_name= user_name)
            st.session_state["meta"][1].update(user_info= user_info)
            st.session_state.update(user_name=user_name)
            st.session_state.update(user_info=user_info)
            st.session_state.update(char_gen_button_disabled=True)
            st.session_state.update(diag_gen_button_disabled=False)
            user_content = next(iterator)
            st.session_state.update(user_content=characters[user_content])
            st.session_state["api_message"].append(TextMsg({"role": "user", "content": st.session_state["user_content"]}))
            st.session_state["history"].append(HistoryMsg({"name": st.session_state["meta"][0]["bot_name"], "content": st.session_state["user_content"] + '\n'}))

            print(f"meta: {st.session_state["meta"]}")
    else:
        st.warning("请输入一段小说文字用于生成两个角色人设")



# 4个输入框，设置meta的4个字段
meta_labels = {
    "bot_name": "角色A",
    "user_name": "角色B", 
    "bot_info": "角色A人设",
    "user_info": "角色B人设"
}

# 2x2 layout
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(label="角色A", key="bot_name")
        st.text_area(label="角色A人设", key="bot_info")
    with col2:
        st.text_input(label="角色B", key="user_name")
        st.text_area(label="角色B人设", key="user_info")


def verify_meta() -> bool:
    # 检查`角色名`和`角色人设`是否空，若为空，则弹出提醒
    if st.session_state["bot_name"] == "" or st.session_state["bot_info"] == "" or st.session_state["user_name"] == "" or st.session_state["user_info"] == "" :
        st.error("两位角色名和角色人设不能为空")
        return False
    else:
        return True

# 对话内容显示
st.markdown("对话内容：")
st.markdown('\n'.join(f"[{d['name']}] {d['content']}" for d in st.session_state["history"]))

def update_history():
    # 如果是偶数条历史，就要assistant role开头，反之user开头
    roles = []
    if len(st.session_state["api_message"]) % 2 == 0:
        roles = ["assistant", "user"]
    else:
        roles = ["user", "assistant"]
    for i, msg in enumerate(st.session_state["api_message"]):
        # print(f"api_message msg :  {msg}")
        # print(f"api_message i :  {i}")
        st.session_state["api_message"][i].update(role= roles[i % 2])



def start_chat():
    global meta

    if not verify_meta():
        return
    
    print(f"meta in start_chat: {st.session_state["meta"]}")

    response_stream = get_characterglm_response_via_sdk(st.session_state["api_message"], meta=st.session_state["meta"][len(st.session_state["history"]) % 2])

    if not response_stream:
        st.warning("生成对话出错")
        print(f"error response_stream: {response_stream}")
        st.session_state["api_message"].pop()
        st.session_state["history"].pop()
    else:
        st.session_state["api_message"].append(TextMsg({"role": "assistant", "content": response_stream}))
        print(f"current botname in start_chat :  {st.session_state["meta"][len(st.session_state["history"]) % 2]["bot_name"]}")
        st.session_state["history"].append(HistoryMsg({"name": st.session_state["meta"][len(st.session_state["history"]) % 2]["bot_name"], "content": response_stream}))    
    
    update_history()
    st.rerun()

            
if st.button(button_labels["gen_dialogue"], key="gen_dialogue", disabled=st.session_state["diag_gen_button_disabled"]):
    start_chat()

# if st.button("调试信息"):
#     print(f"st.session_state[history]: {st.session_state["history"]}")
#     print(f"st.session_state[api_message]: {st.session_state["api_message"]}")
#     print(f"meta: {st.session_state["meta"]}")
#     print(f"current botname :  {st.session_state["meta"][len(st.session_state["history"]) % 2]["bot_name"]}")
    
if st.download_button(
    label="下载对话",
    data='\n'.join(f"[{d['name']}] {d['content']}" for d in st.session_state["history"]).encode("utf-8"),
    disabled=False,
    file_name="character_dialogue.txt",
    mime="text/plain"
):
    print("File downloaded.")