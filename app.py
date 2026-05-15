import streamlit as st
from streamlit_jupyter import StreamlitPatcher

StreamlitPatcher().jupyter()

st.title("Dashboard Saya")
st.write("Hello from notebook")
