import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="idMe Analysis SKTB", layout="wide", page_icon="🎀")

# 2. PAUTAN LOGO (Guna format Thumbnail - Lebih Stabil)
logo_id = "1XV1CIEWhms8jHqJGOKpSluqr7cxtSWrv"
logo_url = f"https://drive.google.com/thumbnail?id={logo_id}&sz=w500"

# 3. TEMA CSS
st.markdown("""
    <style>
    .stApp { background-color: #fdf2f5; }
    [data-testid="stHorizontalBlock"] { align-items: center; }
    .card-container { display: flex; justify-content: space-around; gap: 10px; margin-bottom: 20px; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border: 2px solid #ffc1d6; text-align: center; flex: 1;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .metric-card h2 { color: #ff4d88; margin: 0; font-size: 28px; }
    h1 { color: #ff4d88; text-align: center; font-family: 'Comic Sans MS', cursive; margin-top: -10px; }
    .edit-button {
        background-color: #ff4d88; color: white !important; padding: 12px 25px;
        text-align: center; border-radius: 12px; text-decoration: none;
        display: inline-block; font-weight: bold; margin-bottom: 25px; border: 2px solid #ffb6c1;
    }
    section[data-testid="stSidebar"] { background-color: #fff0f5; border-right: 2px solid #ffc1d6; }
    </style>
    """, unsafe_allow_html=True)

# 4. DATA URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4K9zTk5to3U37As72duwLP7GRqYMkauaAhjr6ANe8s6bl7Qz85ojUXeSDOYw3-iQkMvKV-gq4ZXf/pub?gid=272260181&single=true&output=csv"

@st.cache_data(ttl=2)
def load_data():
    df = pd.read_csv(url)
    df.columns = [str(c).strip().upper() for c in df.columns]
    df.rename(columns={df.columns[0]: 'KELAS', df.columns[1]: 'NAMA_MURID'}, inplace=True)
    df = df[df['KELAS'].astype(str).str.contains('IBNU|PRA|PPKI', case=False, na=False)]
    ralat_cols = ['ALAMAT', 'POSKOD', 'TIADA P1', 'TIADA P2', 'P1 = P2', 'HUB P1', 'HUB P2', 'TANGGUNGAN', 'TIADA HP P1', 'PENDAPATAN', 'AKAUN OKU']
    existing_ralat = [c for c in ralat_cols if c in df.columns]
    df['TOTAL_RALAT'] = df[existing_ralat].notna().sum(axis=1)
    return df, existing_ralat

try:
    df_master, ralat_list = load_data()
    
    with st.sidebar:
        # Gunakan format imej biasa tanpa CSS pelik di sidebar
        st.image(logo_url, width=100)
        st.markdown("### 🌸 Menu Carian")
        senarai_kelas = sorted(df_master['KELAS'].unique().tolist())
        pilihan = st.selectbox("Pilih Kelas:", ["KESELURUHAN Sekolah"] + senarai_kelas)
        if st.button('🔄 Refresh'):
            st.cache_data.clear()
            st.rerun()

    # --- LOGO TENGAH ---
    # Gunakan 3 column, letak imej kat tengah (col2)
    col1, col2, col3 = st.columns([1, 0.3, 1])
    with col2:
        st.image(logo_url, use_container_width=True)

    st.markdown("<h1>🎀 Portal Analisis Ralat SKTB 🎀</h1>", unsafe_allow_html=True)
    
    # Statistik & Graf (Kod anda yang sedia ada)
    df_display = df_master if pilihan == "KESELURUHAN Sekolah" else df_master[df_master['KELAS'] == pilihan]
    total_r = int(df_display['TOTAL_RALAT'].sum())
    
    st.markdown(f"""
    <div class="card-container">
        <div class="metric-card"><h4>Kelas Terbaik 🏆</h4><h2 style="color:#4CAF50;">6 IBNU SINA</h2></div>
        <div class="metric-card"><h4>Jumlah Ralat</h4><h2>{total_r}</h2></div>
        <div class="metric-card"><h4>Ralat Selesai</h4><h2 style="color:#2196F3;">0</h2></div>
        <div class="metric-card"><h4>Belum Selesai</h4><h2 style="color:#FF5252;">{total_r}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    # Graf
    df_g = df_display.groupby('KELAS')['TOTAL_RALAT'].sum().reset_index() if pilihan == "KESELURUHAN Sekolah" else \
           df_display[ralat_list].notna().sum().reset_index().rename(columns={'index':'Kategori', 0:'Jumlah'})
    
    fig = px.bar(df_g, x=df_g.columns[0], y=df_g.columns[1], color=df_g.columns[0], color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Sila Refresh: {e}")
