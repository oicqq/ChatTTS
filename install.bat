@echo off
REM Display prompt message
echo 建议在创建python虚拟环境后安装运行。
echo 可以用conda或以下代码（windows下）：
echo python -m venv venv_chattts
echo .\venv_chattts\Scripts\activate
pause

REM Step 1: Clone the ChatTTS repository
echo Cloning ChatTTS repository...
git clone https://github.com/oicqq/ChatTTS

cd ChatTTS

REM Step 2: Download the model files
echo Downloading model files...
git clone https://www.modelscope.cn/pzc163/chatTTS.git

REM Step 3: Install the required Python packages
echo Installing required Python packages...
pip install -r re.txt

echo 安装完成！
echo 运行run.bat或在虚拟环境中运行命令 streamlit run app.py
pause
