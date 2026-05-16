import io
from pathlib import Path
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def render_summary():

    # ==========================================
    # 0. Set Up & Konfigurasi
    # ==========================================
    BASE_DIR = Path(__file__).resolve().parent

    DARK_THEME = {
        "bg": "#0E1117",
        "card": "#1A1D23",
        "border": "#2E3138",
        "text": "#FAFAFA",
        "text_secondary": "#9CA3AF",
        "accent": "#F7931A",  # gold accent
        "colors": px.colors.qualitative.Plotly,
    }


    # Ini adalah halaman utama, yang pertama sekali diakses. Dimana halaman ini akan berisi :
    # a. Navigasi page awal ke seluruh page yang adalah
    # b. Summary data standard dari file commodity yang sudah bersih
    # c. Data dictionary dari file commodity
   

    # ==========================================
    # 2. Load Data
    # ==========================================
    @st.cache_data
    def load_data():
        df = pd.read_csv("data/commodity_prices_clean_model.csv")
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        return df

    @st.cache_data
    def get_commodity_cols():
        return ["Gold", "Silver", "Platinum", "Copper", "Crude oil, average"]

    @st.cache_data
    def get_color_map():
        return {
            "Gold": "#F7931A",
            "Silver": "#9CA3AF",
            "Platinum": "#D97706",
            "Copper": "#22C55E",
            "Crude oil, average": "#3B82F6",
        }

    def format_number(x):
        return "-" if pd.isna(x) else f"{x:,.2f}"
        

         
    df = load_data()
    daftar_komoditas = get_commodity_cols()
    COLORS=get_color_map()

    # ==========================================
    # 3. Header Atas
    # ==========================================
    #st.title("Dashboard Analitik Komoditas Emas")

    col_f1, col_f2 = st.columns(2, border=True)
    with col_f1:
        pilih_komoditas = st.multiselect(
            "Pilih Komoditas",
            daftar_komoditas,
            default=["Gold","Platinum"]   
        )

    with col_f2:
        tahun = st.slider("Pilih Rentang Tahun", int(df['year'].min()), int(df['year'].max()), (1960, 2024))

    df_filter = df[(df['year'] >= tahun[0]) & (df['year'] <= tahun[1]) ]

    # ==========================================
    # 4. KPI Scorecatds
    # ==========================================
    st.subheader("Statistik per Komoditas")

    if not pilih_komoditas:
        st.warning("Pilih minimal satu komoditas.")
    else:
        tabs = st.tabs(pilih_komoditas,default="Platinum")

        for tab, komoditas in zip(tabs, pilih_komoditas):
            with tab:
                s = df_filter.sort_values("date")
                s = s[komoditas].dropna()
              

                if s.empty: 
                    st.info(f"Tidak ada data untuk {komoditas}.")
                    continue

                kpi1, kpi2, kpi3, kpi4,kpi5 = st.columns(5, border=True)

                kpi1.metric( f"Rata-rata",f"{s.mean():,.2f}")
                kpi2.metric( f"Median ",f"{s.median():,.2f}")
                kpi3.metric( f"Tertinggi ",f"{s.max():,.2f}")
                kpi4.metric( f"Terendah ",f"{s.min():,.2f}")
                kpi5.metric("Skewness", f"{s.skew():.2f}")
                
                
                
    # ====================================================
    # 5. BAGIAN TENGAH: LINE CHART dengan 4 opsi Scalling
    # ====================================================
    col_korelasi, col_line = st.columns([1, 1.4], gap="small", border=True)


    with col_korelasi:
        st.subheader("Matriks Korelasi Pearson")
        corr_matrix = df_filter[pilih_komoditas].corr().round(4)
        fig_corr = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', aspect='auto')
        st.plotly_chart(fig_corr, use_container_width=True)
        
    with col_line:
        st.subheader("Tren Harga terdahap Waktu")

        scale_mode = st.radio(
            "Mode Skala",
            ["Original", "Indexed (Base=100)", "Min-Max Scaling", "Z-Score"],
            horizontal=True
        )

        long_df = (
            df_filter[["date"] + pilih_komoditas]
            .sort_values("date")
            .melt(id_vars="date", var_name="Komoditas", value_name="Harga_Asli")
            .dropna()
        )

        long_df["Nilai_Plot"] = long_df["Harga_Asli"]

        if scale_mode == "Indexed (Base=100)":
            long_df["Nilai_Plot"] = long_df.groupby("Komoditas")["Harga_Asli"].transform(
                lambda s: s / s.iloc[0] * 100 if s.iloc[0] != 0 else np.nan
            )

        elif scale_mode == "Min-Max Scaling":
            scaler = MinMaxScaler()
            long_df["Nilai_Plot"] = (
                long_df.groupby("Komoditas")["Harga_Asli"]
                .transform(lambda s: scaler.fit_transform(s.to_frame()).flatten())
            )

        elif scale_mode == "Z-Score":
            scaler = StandardScaler()
            long_df["Nilai_Plot"] = (
                long_df.groupby("Komoditas")["Harga_Asli"]
                .transform(lambda s: scaler.fit_transform(s.to_frame()).flatten())
            )

        fig_line = px.line(
            long_df,
            x="date",
            y="Nilai_Plot",
            color="Komoditas",
            hover_data={
                "Harga_Asli": ":,.2f",
                "Nilai_Plot": ":.2f"
            }
        )

        fig_line.update_layout(
            height=450,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Year",
            yaxis_title=scale_mode,
            legend_title_text="Komoditas",
            hovermode="x unified"
        )

        st.plotly_chart(fig_line, use_container_width=True)



    # =================================================
    # 6. Bagian Bawah (Diagram Korelasi & Scatter Plot
    # =================================================
  
    if not pilih_komoditas:
        st.warning("Silakan pilih minimal satu komoditas terlebih dahulu.")
    else:
        # Membuat tab secara dinamis berdasarkan list komoditas
        tabs = st.tabs(pilih_komoditas)

        # Looping untuk mengisi konten di setiap tab
        for i, komoditas in enumerate(pilih_komoditas):
            with tabs[i]:
                # Membuat 3 kolom di dalam tab aktif sesuai struktur kode Anda
                col_frekuensi, col_distribusi, col_scatter = st.columns(3, border=True)

                with col_frekuensi:
                    st.subheader(f"Histogram Harga {komoditas}")
                    fig_hist = px.histogram(df_filter, x=komoditas, nbins=30, title=f"Frekuensi Harga {komoditas}")
                    fig_hist.update_layout(margin=dict(t=30, b=0), height=200)
                    st.plotly_chart(fig_hist, use_container_width=True)

                with col_distribusi:
                    st.subheader(f"Distribusi Data {komoditas}")
                    fig_box = px.box(df_filter, x='quarter', y=komoditas, title=f"Variabilitas per Kuartal ({komoditas})")
                    fig_box.update_layout(margin=dict(t=30, b=0), height=200)
                    st.plotly_chart(fig_box, use_container_width=True)
                    
                 
                with col_scatter:
                    st.subheader(f"Scatter {komoditas} vs Gold")

                    if komoditas == "Gold":
                        st.info("Scatter untuk Gold tidak ditampilkan karena Gold adalah variabel acuan.")
                    else:
                        d = df_filter[["date", "Gold", komoditas]].dropna()

                        if d.empty:
                            st.info(f"Tidak ada data Gold vs {komoditas}.")
                        else:
                            fig_scatter = px.scatter(
                                d,
                                x="Gold",
                                y=komoditas,
                                trendline="ols",
                                title=f"Gold vs {komoditas}"
                            )
                            fig_scatter.update_layout(margin=dict(t=30, b=0), height=200)
                            st.plotly_chart(fig_scatter, use_container_width=True)   
                                
                   
