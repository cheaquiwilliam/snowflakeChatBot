
import streamlit as st
import re

# from utils import *


st.title("Echo Chatbot")

if "messages" not in st.session_state:
  st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
  

prompt = st.chat_input()

if prompt:
  st.session_state.messages.append({"role": "user", "content": prompt})
  st.session_state.messages.append({"role": "assistant", "content": prompt})
for msg in st.session_state.messages:
  if msg.get("role") == "user":
    st.chat_message("user").write(msg.get("content"))
  elif msg.get("role") == "assistant":
    st.chat_message("assistant").write(msg.get("content"))
