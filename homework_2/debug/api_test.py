from zhipuai import ZhipuAI
client = ZhipuAI(api_key="") # 请填写您自己的APIKey
novel_desc = f""" 张无忌的性格的“复杂”与“软弱”，实际上正是“人性“的复杂与软弱的表现。在小说之中，张无忌的性格的随和而近乎软弱，复杂而近乎无主体的特点，主要地集中表现在以下几个方面。一是他的性格与行为既为环境的产物，而又时时受环境所左右。武功虽强，性格其实颇为优柔寡断，万事之来，往往顺其自然而不愿拂旁人之意，往往宁可舍己从人。他之习乾坤大挪移心法是小昭之请；任明教教主既是迫于形势，亦是殷天正、殷野王等动之以情；与周芷若订婚是奉谢逊之命；不与周芷若拜堂又是为赵敏所迫……。其次，他的这种性格，更突出地表现在他对周芷若、赵敏、殷离、小昭这四位少女的态度上。他周旋其间，常被形势所迫。颇为拖泥带水，若不是最终一“死”（其实并未真死），一走、一叛，他恐怕还会在四位少女之间徘徊无定。不似杨过对小龙女那样一往情深，更不似郭靖对于黄蓉那样除此非他。张无忌的这种形象，对于一个活的个体来说，也许并不大“好”，然而作为一个艺术形象，他的意义却是很大的。这一性格在全篇小说中，以及在武侠小说中都是一种独特的、不多见的成功艺术形象。"""
instruction = f"""
请从下列文本中，抽取人物的背景、性格设定和人物关系。要求：
1. 生成两名角色的性格特征和两人的关系，两人关系写在第二个人的描述中，不用单独列出。
2. 描写不能包含敏感词，人物形象需得体。
3. 尽量用短语描写，而不是完整的句子。
4. 每名角色设定描述在20字到50字之间
5. 如果文本中人物超过两个，仅挑选两个人物生成人设，如果描写仅能生成一个人设，另一个人设自行推测
6. 生成一句角色一的对白，用对白开头，分号后跟生成的对白内容，不要用双引号或单引号把对白内容引用起来，生成内容不能含有冒号
生成格式如下，请将方括号内内容替换为生成内容，不要出现经推测等字样：
张三:张三是一名侠客。
李四:李四常年游手好闲。张三是李四的好兄弟。
对白:你不能再这样下去了，找个正经营生吧。

文本：
{novel_desc}
"""

response = client.chat.completions.create(
    model="glm-4-0520",  # 填写需要调用的模型编码
    messages=[
        {"role": "user", "content": instruction.strip()}
    ]
    # stream=True,
)


lines = response.choices[0].message.content.splitlines()
print(lines)

parsed_data = {}
for line in lines:
    print(line)
    if ':' in line:
        key, value = line.split(":", 1)
        parsed_data[key.strip()] = value.strip()
    if '：' in line:
        key, value = line.split("：", 1)
        parsed_data[key.strip()] = value.strip()
print(parsed_data)
