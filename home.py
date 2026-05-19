import io
from pathlib import Path
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from tabs.reference import render_reference
from tabs.summary import render_summary

# ==========================================
# 0. Set Up & Konfigurasi
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

# Ini adalah halaman utama, yang pertama sekali diakses. Dimana halaman ini akan berisi :
# a. Navigasi page awal ke seluruh page yang adalah
# b. Summary data standard dari file commodity yang sudah bersih
# c. Data dictionary dari file commodity


# ==========================================
# 1. Konfigurasi awal halaman dashboard
# ==========================================
st.set_page_config(
    page_title="Dashboard Harga Komoditas Emas",
    page_icon=str(BASE_DIR / "assets"/"icons" / "dashboard.jpg"),
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard Analitik Komoditas Emas")

# ============================================================
# 2. Penambahan tab untuk mengakses file summary dan reference
# ============================================================

tab_reference, tab_summary = st.tabs(["Reference", "Summary"])

with tab_reference:
    render_reference()

with tab_summary:
    render_summary()
    
with tab_project:
    render_project()
