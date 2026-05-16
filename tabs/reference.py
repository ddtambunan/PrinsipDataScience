import io
from pathlib import Path
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px


def render_reference():
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
        page_title="Dashboard Harga Komoditas",
        page_icon=str(BASE_DIR / "assets"/"icons" / "dashboard.jpg"),
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ==========================================
    # 2. Load Data
    # ==========================================
    @st.cache_data
    def load_data():
        df = pd.read_csv("data/commodity_prices_clean_model.csv")
        return df

    df = load_data()

    # ==========================================
    # 3. Keterangan/Petunjuk Awal Data
    # ==========================================
   # st.title("Data Peramalan Harga Komoditas Emas")
    st.markdown(
        """
        Selamat datang di aplikasi visualisasi data harga komoditas emas. Data ini merupakan hasil EDA dari dataset Kaggle : https://www.kaggle.com/datasets/kanchana1990/world-bank-commodity-price-intelligence-19602026 . Data komoditas yang dipilih untuk visualisasi adalah komoditas Emas, Crude Oil, LNG, Copper, Platinum, dan Silver. Kedepannya akan digunakan pada proses forecasting harga emas. 
        """
    )
    st.info("Klik Tab Summary untuk mulai eksplorasi data.")

    # ==========================================
    # 4. Summary Singkat Data
    # ==========================================
    st.subheader("Informasi Dasar Dataset",divider="blue")


    col1, col2, col3 , col4= st.columns(4)
    with col1:
        st.metric("Jumlah Baris", df.shape[0])

    with col2:
        st.metric("Jumlah Kolom", df.shape[1])

    with col3:
        st.metric("Jumlah Missing Value", int(df.isna().sum().sum()))

    with col4:
        st.metric("Jumlah Duplikasi", int(df.duplicated().sum()))



    # ==========================================
    # 5. Data Dictionary
    # ==========================================

    # Data Anda
    data_dictionary = pd.DataFrame([
        ['date', 'date', 'Tanggal observasi bulanan sebagai penanda waktu utama.'],
        ['year', 'int64', 'Tahun observasi.'],
        ['month', 'int64', 'Bulan observasi dalam angka 1-12.'],
        ['quarter', 'int64', 'Kuartal waktu yang sudah dikodekan ke numerik.'],
        ['category_map', 'int64', 'Kode numerik kategori besar komoditas.'],
        ['price_regime_mom', 'int64', 'Kode numerik regime/pergerakan harga bulanan.'],
        ['era', 'int64', 'Kode numerik periode sejarah ekonomi.'],
        ['Copper', 'float64', 'Harga copper pada bulan observasi.'],
        ['Crude oil, average', 'float64', 'Harga rata-rata crude oil pada bulan observasi.'],
        ['Gold', 'float64', 'Harga emas pada bulan observasi.'],
        ['Platinum', 'float64', 'Harga platinum pada bulan observasi.'],
        ['Silver', 'float64', 'Harga silver pada bulan observasi.'],
        ['gold_target_m1', 'float64', 'Target utama: harga emas bulan berikutnya.'],
        ['gold_lag1', 'float64', 'Harga emas 1 bulan sebelumnya.'],
        ['gold_lag3', 'float64', 'Harga emas 3 bulan sebelumnya.'],
        ['gold_lag12', 'float64', 'Harga emas 12 bulan sebelumnya.'],
        ['crude_oil_average_lag1', 'float64', 'Harga crude oil average 1 bulan sebelumnya.'],
        ['crude_oil_average_lag3', 'float64', 'Harga crude oil average 3 bulan sebelumnya.'],
        ['crude_oil_average_lag12', 'float64', 'Harga crude oil average 12 bulan sebelumnya.'],
        ['platinum_lag1', 'float64', 'Harga platinum 1 bulan sebelumnya.'],
        ['platinum_lag3', 'float64', 'Harga platinum 3 bulan sebelumnya.'],
        ['platinum_lag12', 'float64', 'Harga platinum 12 bulan sebelumnya.'],
        ['silver_lag1', 'float64', 'Harga silver 1 bulan sebelumnya.'],
        ['silver_lag3', 'float64', 'Harga silver 3 bulan sebelumnya.'],
        ['silver_lag12', 'float64', 'Harga silver 12 bulan sebelumnya.'],
        ['copper_lag1', 'float64', 'Harga copper 1 bulan sebelumnya.'],
        ['copper_lag3', 'float64', 'Harga copper 3 bulan sebelumnya.'],
        ['copper_lag12', 'float64', 'Harga copper 12 bulan sebelumnya.'],
        ['gold_roll3_mean', 'float64', 'Rata-rata bergerak 3 bulan harga emas.'],
        ['gold_roll12_mean', 'float64', 'Rata-rata bergerak 12 bulan harga emas.'],
        ['gold_roll12_std', 'float64', 'Standar deviasi 12 bulan harga emas.'],
        ['crude_oil_average_roll3_mean', 'float64', 'Rata-rata bergerak 3 bulan crude oil average.'],
        ['crude_oil_average_roll12_mean', 'float64', 'Rata-rata bergerak 12 bulan crude oil average.'],
        ['crude_oil_average_roll12_std', 'float64', 'Standar deviasi 12 bulan crude oil average.'],
        ['platinum_roll3_mean', 'float64', 'Rata-rata bergerak 3 bulan platinum.'],
        ['platinum_roll12_mean', 'float64', 'Rata-rata bergerak 12 bulan platinum.'],
        ['platinum_roll12_std', 'float64', 'Standar deviasi 12 bulan platinum.'],
        ['silver_roll3_mean', 'float64', 'Rata-rata bergerak 3 bulan silver.'],
        ['silver_roll12_mean', 'float64', 'Rata-rata bergerak 12 bulan silver.'],
        ['silver_roll12_std', 'float64', 'Standar deviasi 12 bulan silver.'],
        ['copper_roll3_mean', 'float64', 'Rata-rata bergerak 3 bulan copper.'],
        ['copper_roll12_mean', 'float64', 'Rata-rata bergerak 12 bulan copper.'],
        ['copper_roll12_std', 'float64', 'Standar deviasi 12 bulan copper.'],
    ], columns=['column_name', 'dtype', 'description'])

    with st.expander("🗂️ Kamus Data Berdasarkan Kategori", expanded=True):
        # Logika Pengelompokan Otomatis
        df_waktu = data_dictionary[data_dictionary['column_name'].isin(['date', 'year', 'month', 'quarter'])]
        df_kat = data_dictionary[data_dictionary['column_name'].isin(['category_map', 'price_regime_mom', 'era'])]
        df_target = data_dictionary[data_dictionary['column_name'] == 'gold_target_m1']
        
        df_lag = data_dictionary[data_dictionary['column_name'].str.contains('lag')]
        df_roll = data_dictionary[data_dictionary['column_name'].str.contains('roll')]
        
        # Ambil sisa harga utama
        exclude_cols = df_waktu['column_name'].tolist() + df_kat['column_name'].tolist() + df_target['column_name'].tolist() + df_lag['column_name'].tolist() + df_roll['column_name'].tolist()
        df_harga = data_dictionary[~data_dictionary['column_name'].isin(exclude_cols)]

        # Membuat Tabs di Streamlit
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Waktu", "Kategori", "Harga", "Target", "Lag", "Rolling"])
        
        with tab1: st.dataframe(df_waktu, use_container_width=True, hide_index=True)
        with tab2: st.dataframe(df_kat, use_container_width=True, hide_index=True)
        with tab3: st.dataframe(df_harga, use_container_width=True, hide_index=True)
        with tab4: st.dataframe(df_target, use_container_width=True, hide_index=True)
        with tab5: st.dataframe(df_lag, use_container_width=True, hide_index=True, height=200)
        with tab6: st.dataframe(df_roll, use_container_width=True, hide_index=True, height=200)


    # ==========================================
    # 6. Display DataFrame
    # ==========================================
    st.subheader("Preview Data")
    #st.dataframe(df, use_container_width=True)
    st.data_editor(
        df, 
        use_container_width=True, 
        disabled=True # 'disabled=True' membuat data tidak bisa diedit, tapi fitur interaksinya aktif
    )



