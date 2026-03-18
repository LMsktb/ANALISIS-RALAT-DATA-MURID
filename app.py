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
# Kita tukar link sikit supaya dia terus sedut data sebagai CSV (Lagi laju & stabil)
sheet_id = "1y8BvpG0NN5WwwhSFWS2AOI4Qe8O4HYg5M-LPrMmzjk"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1718218161"

try:
    # Kita guna pandas biasa (pd.read_csv) supaya tak perlu 'Secrets' yang pening tu
    # skiprows=7 bermaksud kita lompat 7 baris atas (mula baca dari baris 8)
    df_raw = pd.read_csv(url, skiprows=7)
    
    # Pilih 2 kolum pertama (Kelas & Jumlah Ralat)
    df = df_raw.iloc[:, [0, 1]].copy()
    df.columns = ['Kelas', 'Jumlah Ralat']
    
    # Bersihkan data: Buang row kosong dan row total kat bawah
    df = df.dropna(subset=['Kelas'])
    df = df[df['Kelas'].astype(str).str.contains('IBNU|PRA|PPKI', case=False, na=False)]
    
    # Tukar Jumlah Ralat kepada nombor
    df['Jumlah Ralat'] = pd.to_numeric(df['Jumlah Ralat'], errors='coerce').fillna(0)
    
except Exception as e:
    st.error(f"Alamak! Ada masalah teknikal: {e}")
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
