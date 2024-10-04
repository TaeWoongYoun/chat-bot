from openai import OpenAI
import streamlit as st

st.title("Chat-Bot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

system_message = '''
너의 이름은 하츄핑이야.
너는 항상 나한테 절대 반말을 해서는 안돼
항상 친근하게 대답해줘
영어로 질문을 받아도 항상 한글로 답변해줘
한글이 아닌 답변일 때는 다시 생각해서 한글로 만들어줘
모든 답변 끝에 알맞는 이모티콘을 추가해줘
'''

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_message})

# 시스템 메시지를 제외하고 사용자와 어시스턴트의 메시지만 출력
for message in st.session_state.messages:
    if message["role"] != "system":  # 시스템 메시지는 출력하지 않음
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
