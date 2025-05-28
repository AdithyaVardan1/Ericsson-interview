import streamlit as st
from langgraph.graph import END
from langchain_core.messages import HumanMessage
from main import ecommerce_system 

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="🛒 E-Commerce Assistant", layout="wide")
st.title("🛍️ E-Commerce AI Assistant")
st.caption("Ask about orders, products, preferences, or even the weather for deliveries!")

with st.chat_message("user"):
    user_input = st.text_input("Type your message:", key="user_input")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    messages = [("user", user_input)]
    for step in ecommerce_system.stream({"messages": messages}, subgraphs=True):
        if isinstance(step, tuple) and len(step) == 2:
            thread_id, data = step
            if thread_id == ():
                for key, value in data.items():
                    if key != "supervisor" and value is not None:
                        if "messages" in value and value["messages"]:
                            bot_reply = value["messages"][0].content

                            with st.chat_message("assistant"):
                                st.markdown(f"**{key.replace('_', ' ').title()} Agent**: {bot_reply}")

                            st.session_state.chat_history.append((f"{key}_agent", bot_reply))

    if step[1] == END:
        with st.chat_message("assistant"):
            st.markdown("✅ Conversation complete!")
        st.session_state.chat_history.append(("system", "Conversation complete!"))

if st.session_state.chat_history:
    st.sidebar.markdown("### 📜 Chat History")
    for role, content in st.session_state.chat_history:
        role_label = "🧑 User" if role == "user" else ("🤖 System" if role == "system" else f"🔧 {role.title()}")
        st.sidebar.markdown(f"**{role_label}:** {content}")
