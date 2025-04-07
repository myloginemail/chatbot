import streamlit as st
from openai import OpenAI

# 시스템 프롬프트: 역할 설정
SYSTEM_PROMPT = "너는 일본 여행 전문가야. 사용자가 일본 여행과 관련된 질문을 하면 친절하고 자세하게 안내해줘."

# 세션 초기화
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 메시지 출력
def display_messages():
    for message in st.session_state.messages:
        if message["role"] != "system":  # system 메시지는 표시하지 않음
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# 응답 생성
def get_response(prompt, client):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

# Streamlit UI
def main():
    st.title("💬 나의 일본 여행 Chatbot 가이드")
    st.write("일본 여행을 도와주는 챗봇 가이드입니다. 궁금한 것을 물어보세요!")

    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.info("OpenAI API 키를 입력해주세요.", icon="🗝️")
        return

    client = OpenAI(api_key=openai_api_key)
    init_session()
    display_messages()

    if prompt := st.chat_input("일본 여행에 대해 궁금한 점을 물어보세요!"):
        get_response(prompt, client)

if __name__ == "__main__":
    main()
