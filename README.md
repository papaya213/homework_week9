# AI 大模型应用开发实战营 -- 第九周作业
## 作业一：
### 实现功能：
    改进characterglm_api_demo_streamlit.py的代码，为文生图功能加上风格选项，目前支持二次元风格, 黑白线条风格和写实风格三种，并在页面上增加了可指定图片风格的下拉框。
### 运行方法：
    1. 提前通过pip安装必要依赖包
        pip install -r requirements.txt
    2. 在环境变量或者代码中配置ChatGLM的API_KEY
    3. 在路径homework_1下命令行中运行streamlit环境，在浏览器中进行UI操作
        streamlit run characterglm_api_demo_streamlit_withpicstyle.py
## 作业二：
### 实现功能：
    通过ChatGLM从一段输入文本（可以是小说原文，摘要等）抽取两名角色的人设，再根据生成人设通过CharacterGLM交替回复对方的发言，生成对话可通过文件形式下载。ChatGLM和CharacterGLM调用均通过SDK完成。
### 运行方法：
    1. 提前通过pip安装必要依赖包
        pip install -r requirements.txt
    2. 在环境变量或者代码中配置ChatGLM的API_KEY
    3. 在路径homework_2下命令行中运行streamlit环境，在浏览器中进行UI操作。输入文本后点按钮生成人设，再通过按钮添加回复对话，下载对话文件。
        streamlit run dialogue_gen.py

