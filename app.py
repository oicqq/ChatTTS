import streamlit as st
import ChatTTS
import torchaudio
import torch
import os
import numpy as np

# Initialize ChatTTS
chat = ChatTTS.Chat()

torch._dynamo.config.cache_size_limit = 64
torch._dynamo.config.suppress_errors = True
torch.set_float32_matmul_precision('high')

# Get the directory of the running script
current_dir = os.path.dirname(os.path.abspath(__file__))
chattts_dir = os.path.join(current_dir, 'local')
files_dir = os.path.join(chattts_dir, 'files')

# Ensure the files directory exists
os.makedirs(files_dir, exist_ok=True)

# Streamlit app title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>ChatTTS @Local</h1>", unsafe_allow_html=True)

# Text input area
st.markdown("<h3>输入要转换的文本：</h3>", unsafe_allow_html=True)
text_input = st.text_area("输入文本", value="你好，世界！", label_visibility='collapsed')

# Sidebar for parameter controls
st.sidebar.header("语音参数")
temperature = st.sidebar.slider("温度", 0.1, 1.0, 0.3)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, 0.7)
top_k = st.sidebar.slider("Top K", 1, 100, 20)

st.sidebar.header("文本细化参数")
oral = st.sidebar.slider("Oral (oral_)", 0, 9, 2)
laugh = st.sidebar.slider("Laugh (laugh_)", 0, 2, 0)
break_ = st.sidebar.slider("Break (break_)", 0, 7, 6)

st.sidebar.header("模型设置")
source = st.sidebar.text_input("Source", value="local")
st.sidebar.markdown(f"Local Path: {chattts_dir}")

# History of generated audios
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to simulate progress
def get_progress():
    # This is a placeholder function. Replace it with the actual progress tracking logic.
    for i in range(101):
        time.sleep(0.1)
        yield i

# Button to trigger speech synthesis
if st.button("生成语音"):
    try:
        with st.spinner('加载模型中...'):
            # Load models with GPU support
            chat.load_models(compile=False, source=source, local_path=chattts_dir)
        
        st.success('模型加载完成！')
        
        # Sample a random speaker
        rand_spk = chat.sample_random_speaker()

        # Inference parameters
        params_infer_code = {
            'spk_emb': rand_spk,
            'temperature': temperature,
            'top_P': top_p,
            'top_K': top_k
        }

        # For sentence level manual control.
        # use oral_(0-9), laugh_(0-2), break_(0-7) 
        # to generate special token in text to synthesize.
        prompt = f'[oral_{oral}][laugh_{laugh}][break_{break_}]'
        params_refine_text = {
            'prompt': prompt
        } 

        with st.spinner('生成语音中...'):
            # Generate speech
            wav = chat.infer([text_input], params_refine_text=params_refine_text, params_infer_code=params_infer_code)
        
        st.success('语音生成完成！')

        # Convert to PyTorch tensor and save
        audio_tensor = torch.tensor(np.array(wav[0]), dtype=torch.float32)
        output_path = "output.wav"
        torchaudio.save(output_path, torch.from_numpy(wav[0]), 24000)

        # Display audio player
        st.audio(output_path)

        # Provide download link
        with open(output_path, "rb") as file:
            btn = st.download_button(
                label="下载生成的音频",
                data=file,
                file_name="output.wav",
                mime="audio/wav"
            )

        # Save to history
        st.session_state.history.append({
            "text": text_input,
            "params": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "oral": oral,
                "laugh": laugh,
                "break": break_,
                "source": source,
                "local_path": chattts_dir
            }
        })

    except Exception as e:
        st.error(f"发生错误: {e}")

# Display history
if st.session_state.history:
    st.markdown("---")
    st.header("生成历史记录")
    for idx, record in enumerate(st.session_state.history):
        with st.expander(f"记录 {idx + 1}"):
            st.write("文本：", record["text"])
            st.write("参数详情：")
            st.json(record["params"])

# Custom CSS for styling
st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stSidebar .css-1d391kg {
            background-color: #f0f0f0;
        }
        .st-expanderHeader {
            font-size: small;
        }
    </style>
""", unsafe_allow_html=True)
