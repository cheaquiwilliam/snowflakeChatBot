
import streamlit as st
import re

# from utils import *


st.title("Echo Chatbot")
prompt = st.chat_input()

if prompt:
  st.chat_message("user").write(prompt)
  st.chat_message("assistant").write(prompt)
