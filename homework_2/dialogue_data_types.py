"""
相关数据类型的定义
"""
from typing import Literal, TypedDict, List, Union


class BaseMsg(TypedDict):
    pass


class TextMsg(BaseMsg):
    """文本消息"""
    
    # 在类属性标注的下一行用三引号注释，vscode中
    role: Literal["user", "assistant"]
    """消息来源"""
    content: str
    """消息内容"""

class HistoryMsg(BaseMsg):
    """历史文本消息，用于存储不用于API调用"""
    name: str
    """角色名"""
    content: str
    """对白"""
class CharacterMeta(TypedDict):
    """角色扮演设定，它是CharacterGLM API所需的参数"""
    user_info: str
    """用户人设"""
    bot_info: str
    """角色人设"""
    bot_name: str
    """bot扮演的角色的名字"""
    user_name: str
    """用户的名字"""

Msg = Union[TextMsg]
TextMsgList = List[TextMsg]
MsgList = List[Msg]

def filter_text_msg(messages: MsgList) -> TextMsgList:
    return [m for m in messages if m["role"] != "image"]



