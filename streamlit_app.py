import streamlit as st
import pandas as pd
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Dashboard Komoditas", layout="wide")

# --- Muat Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/commodity_prices_clean_model.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()
daftar_komoditas = ['Copper', 'Crude oil, average', 'Gold', 'Platinum', 'Silver']

# --- HEADER & FILTER ---
st.title("Dashboard Analitik Komoditas")

col_f1, col_f2 = st.columns(2)
with col_f1:
    pilih_komoditas = st.selectbox("Pilih Komoditas Utama", daftar_komoditas, index=2) # Default Gold
with col_f2:
    tahun = st.slider("Rentang Tahun", int(df['year'].min()), int(df['year'].max()), (1990, 2024))

# Filter Dataframe berdasarkan rentang tahun
df_filter = df[(df['year'] >= tahun[0]) & (df['year'] <= tahun[1])]

# --- KPI SCORECARDS ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(f"Rata-rata Harga {pilih_komoditas}", f"{df_filter[pilih_komoditas].mean():.2f}")
kpi2.metric(f"Harga Tertinggi", f"{df_filter[pilih_komoditas].max():.2f}")
kpi3.metric(f"Harga Terendah", f"{df_filter[pilih_komoditas].min():.2f}")
st.markdown("---")

# --- BAGIAN TENGAH: TREN (KIRI) & DISTRIBUSI (KANAN) ---
col_utama, col_distribusi = st.columns([2, 1]) # Rasio lebar 2:1

with col_utama:
    st.subheader("Tren Harga Waktu")
    # Plotly Line Chart interaktif
    fig_line = px.line(df_filter, x='date', y=pilih_komoditas)
    st.plotly_chart(fig_line, use_container_width=True)

with col_distribusi:
    st.subheader("Distribusi Data")
    # Boxplot per kuartal
    fig_box = px.box(df_filter, x='quarter', y=pilih_komoditas, title="Variabilitas per Kuartal")
    fig_box.update_layout(margin=dict(t=30, b=0), height=200)
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Histogram
    fig_hist = px.histogram(df_filter, x=pilih_komoditas, nbins=30, title="Frekuensi Harga")
    fig_hist.update_layout(margin=dict(t=30, b=0), height=200)
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# --- BAGIAN BAWAH: KORELASI (KIRI) & SCATTER PLOT (KANAN) ---
col_korelasi, col_scatter = st.columns(2) # Rasio 1:1

with col_korelasi:
    st.subheader("Matriks Korelasi")
    # Hitung matriks korelasi untuk komoditas utama
    corr_matrix = df_filter[daftar_komoditas].corr()
    fig_corr = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', aspect='auto')
    st.plotly_chart(fig_corr, use_container_width=True)

with col_scatter:
    st.subheader("Hubungan Antar Variabel (Scatter Plot)")
    # Dropdown untuk memilih komoditas pembanding
    komoditas_pembanding = st.selectbox("Bandingkan dengan:", [k for k in daftar_komoditas if k != pilih_komoditas])
    
    fig_scatter = px.scatter(df_filter, x=pilih_komoditas, y=komoditas_pembanding, trendline="ols")
    st.plotly_chart(fig_scatter, use_container_width=True)
