import streamlit as st
import requests

# ✅ Set page configuration - must be first!
st.set_page_config(
    page_title="DOGI",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Custom CSS for dark theme
st.markdown(
    """
    <style>
        .main {
            background-color: #1e1e1e;
            color: white;
        }
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #2b2b2b;
        }
        .stTextInput>div>div>input,
        .stTextArea>div>textarea {
            background-color: #333;
            color: white;
        }
        .stChatMessage {
            background-color: #333;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ✅ Groq API setup
GROQ_API_KEY = "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"  # Replace with your actual key
API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ✅ Display image (dog image)
st.image("C:/Users/daksh/Downloads/dogi.jpg", caption="Therapist!", use_container_width=True)

# ✅ Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# ✅ Sidebar chat summary
st.sidebar.title("💬 Chat History Summary")
chat_history = ""
for msg in st.session_state.messages[1:]:  # Skip system message
    chat_history += f"{msg['role'].capitalize()}: {msg['content']}\n\n"
st.sidebar.text_area("Summary", chat_history, height=300)

# ✅ Display past messages
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# ✅ Input box
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Thinking..."):
        payload = {
            "model": "llama3-70b-8192",
            "messages": st.session_state.messages,
            "temperature": 0.7
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        else:
            reply = f"❌ Error: {response.status_code} - {response.text}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

    # ✅ Update sidebar with latest reply
    chat_history += f"Assistant: {reply}\n\n"
    st.sidebar.text_area("Summary", chat_history, height=300)
