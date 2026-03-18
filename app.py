import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman & Tema Pastel
st.set_page_config(page_title="idMe Error Tracker SKTB", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F8; }
    [data-testid="stMetricValue"] { color: #FF1493; font-family: 'Courier New'; }
    .stHeader { background-color: #FFB6C1; padding: 10px; border-radius: 10px; text-align: center; }
    h1 { color: #C71585; text-shadow: 2px 2px #FFD1DC; }
    </style>
    """, unsafe_allow_html=True)

# Tajuk Dashboard
st.markdown("<div class='stHeader'><h1>🌸 Dashboard Analisis Ralat idMe SKTB 🌸</h1></div>", unsafe_allow_html=True)
st.write("")

# --- SAMBUNGAN GOOGLE SHEETS ---
# Masukkan URL penuh Google Sheet Bubu di bawah
url = "https://docs.google.com/spreadsheets/d/1y8BvpG0NN5WwwhSFWS2AOI4Qe8O4HYg5M-LPrMmzjk/edit#gid=1718218161"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Kita baca tab 'DASHBOARD' yang ada formula =COUNTIF tu
    df = conn.read(spreadsheet=url, worksheet="DASHBOARD", ttl="10s") 
    df = df.dropna(subset=['Kelas', 'Jumlah Ralat']) # Buang row kosong
except Exception as e:
    st.error("Alamak! Tak dapat baca data. Check nama tab 'DASHBOARD' ya.")
    st.stop()

# --- RINGKASAN ATAS ---
total_ralat = df['Jumlah Ralat'].sum()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Ralat Belum Setel", f"{int(total_ralat)} ⚠️")
with col2:
    # Mencari kelas yang paling banyak ralat untuk perhatian
    kelas_max = df.loc[df['Jumlah Ralat'].idxmax(), 'Kelas']
    st.metric("Kelas Paling Tinggi Ralat", kelas_max)
with col3:
    st.metric("Status Data", "LIVE (Auto-Refresh)")

st.divider()

# --- VISUALISASI UTAMA ---
c1, c2 = st.columns([3, 2])

with c1:
    st.subheader("📊 Statistik Ralat Ikut Kelas")
    # Warna pastel mengikut jumlah ralat (merah kalau banyak, hijau kalau sikit)
    fig = px.bar(df, x='Kelas', y='Jumlah Ralat', 
                 text_auto=True,
                 color='Jumlah Ralat',
                 color_continuous_scale='RdYlGn_r') # Red to Green reversed
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("📋 Senarai Semak")
    # Papar jadual ringkas
    st.dataframe(df[['Kelas', 'Jumlah Ralat']].sort_values(by='Jumlah Ralat', ascending=False), 
                 hide_index=True, use_container_width=True)

# Footer & Manual Refresh
st.write("")
if st.button('🔄 Refresh Data Sekarang'):
    st.cache_data.clear()
    st.rerun()

st.caption("Nota Bubu: Dashboard ini akan auto-update setiap kali tanda '✓' dipadam dalam Google Sheets.")
