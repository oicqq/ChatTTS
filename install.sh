
# git clone https://github.com/oicqq/ChatTTS.git
# cd ChatTTS/
# ./install.sh

pip install -r re.txt
git clone https://www.modelscope.cn/pzc163/chatTTS.git local
conda install -c conda-forge pynini=2.1.5 -y && pip install WeTextProcessing -q

streamlit run app.py
