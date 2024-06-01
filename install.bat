@echo off
chcp 65001 >nul

REM Display prompt message
echo 建议在创建python虚拟环境后安装运行。
pause

REM Step 1: Download the model files into the local folder
echo Downloading model files...
git clone https://www.modelscope.cn/pzc163/chatTTS.git local

REM Step 2: Create a virtual environment
echo Creating virtual environment...
python -m venv venv_chattts

REM Step 3: Activate the virtual environment
echo Activating virtual environment...
call .\venv_chattts\Scripts\activate

REM Step 4: Install the required Python packages
echo Installing required Python packages...
pip install -r re.txt

echo 安装完成！
echo 运行run.bat或在虚拟环境中运行命令 streamlit run app.py
