@echo off
REM Display prompt message
echo 在之前创建的python虚拟环境中运行。
echo 可以用conda或以下代码（windows下）：
echo .\venv_chattts\Scripts\activate
pause

REM Step 4: Run the Streamlit application
echo Running Streamlit application...
echo 确定在ChatTTS文件夹下

streamlit run app.py

pause
