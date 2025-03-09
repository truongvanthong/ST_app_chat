import streamlit as st
import requests
from uuid import uuid4

def init_session_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid4())
    if "student_messages" not in st.session_state:
        st.session_state.student_messages = []
    if "tutor_messages" not in st.session_state:
        st.session_state.tutor_messages = []
    if "api_url" not in st.session_state:
        st.session_state.api_url = ""

def get_endpoints():
    return (
        f"{st.session_state.api_url}/chat-service/student/chat",
        f"{st.session_state.api_url}/chat-service/tutor/chat"
    )

def display_chat_messages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def send_message(endpoint, question, role="student"):
    try:
        with st.spinner('🤔 Đợi tui xíu...'):
            response = requests.post(
                f"{endpoint}/answer",
                json={
                    "question": question,
                    "user_id": st.session_state.user_id,
                    "code": "test123"
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Lỗi: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        st.error(f"Lỗi kết nối: {str(e)}")
        return None

def student_chat():
    st.title("Chat với Trợ lý Tìm Gia sư 🤖")
    
    STUDENT_ENDPOINT, _ = get_endpoints()
    
    # Thêm container cho tin nhắn
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.student_messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👨‍🎓"):  # Icon học sinh
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):  # Icon robot trợ lý
                    st.write(message["content"])

    if question := st.chat_input("Nhập câu hỏi của bạn"):
        st.session_state.student_messages.append({"role": "user", "content": question})
        
        with chat_container:
            with st.chat_message("user", avatar="👨‍🎓"):
                st.write(question)

            with st.chat_message("assistant", avatar="🤖"):
                response = send_message(STUDENT_ENDPOINT, question)
                if response:
                    st.write(response["answer"])
                    st.session_state.student_messages.append({
                        "role": "assistant",
                        "content": response["answer"]
                    })

def tutor_chat():
    st.title("Chat với Trợ lý Tìm Lớp Dạy 🤖")
    
    _, TUTOR_ENDPOINT = get_endpoints()

    # Thêm container cho tin nhắn
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.tutor_messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👨‍🏫"):  # Icon giáo viên
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):  # Icon robot trợ lý
                    st.write(message["content"])

    if question := st.chat_input("Nhập câu hỏi của bạn"):
        st.session_state.tutor_messages.append({"role": "user", "content": question})

        with chat_container:
            with st.chat_message("user", avatar="👨‍🏫"):
                st.write(question)

            with st.chat_message("assistant", avatar="🤖"):
                response = send_message(TUTOR_ENDPOINT, question, role="tutor")
                if response:
                    st.write(response["answer"])
                    st.session_state.tutor_messages.append({
                        "role": "assistant", 
                        "content": response["answer"]
                    })

def main():
    st.set_page_config(
        page_title="TeachMe ChatBot",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_session_state()

    st.sidebar.title("TeachMe ChatBot 📚")
    
    # Thêm trường nhập API URL
    api_url = st.sidebar.text_input("Nhập API URL:", value=st.session_state.api_url)
    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url
        st.rerun()

    page = st.sidebar.radio("Chọn vai trò:", ["Student", "Tutor"])

    if page == "Student":
        student_chat()
    else:
        tutor_chat()

if __name__ == "__main__":
    main()