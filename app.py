import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="idMe Analysis SKTB", layout="wide")

# --- TEMA CERAH & PINK (PORTAL VIBE) ---
st.markdown("""
    <style>
    .stApp { background-color: #fdf2f5; }
    .card-container { display: flex; justify-content: space-around; gap: 10px; margin-bottom: 20px; }
    .metric-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #ffc1d6; text-align: center; flex: 1;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .metric-card h4 { color: #888; font-size: 14px; margin-bottom: 5px; }
    .metric-card h2 { color: #ff4d88; margin: 0; font-size: 28px; }
    h1, h3 { color: #ff4d88; text-align: center; font-family: 'Comic Sans MS', cursive; }
    section[data-testid="stSidebar"] { background-color: #fff0f5; border-right: 2px solid #ffc1d6; }
    .edit-button {
        background-color: #ff4d88; color: white !important; padding: 12px 25px;
        text-align: center; border-radius: 12px; text-decoration: none;
        display: inline-block; font-weight: bold; margin-bottom: 25px; border: 2px solid #ffb6c1;
    }
    </style>
    """, unsafe_allow_html=True)

# URL Master CSV (DATA)
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4K9zTk5to3U37As72duwLP7GRqYMkauaAhjr6ANe8s6bl7Qz85ojUXeSDOYw3-iQkMvKV-gq4ZXf/pub?output=csv"

# Link Edit Tab (GID)
base_url = "https://docs.google.com/spreadsheets/d/1y8BvpG0NN5WwwhSFWS2AOI4Qe8O4HYg5M-LPrMmzjk/edit"
link_setiap_kelas = {
    "D1 IBNU SINA": f"{base_url}#gid=336938430", "D1 IBNU KHALDUN": f"{base_url}#gid=648519110",
    "D2 IBNU SINA": f"{base_url}#gid=851785168", "D2 IBNU KHALDUN": f"{base_url}#gid=2036307286",
    "D3 IBNU SINA": f"{base_url}#gid=1435005895", "D3 IBNU KHALDUN": f"{base_url}#gid=1308911247",
    "D4 IBNU SINA": f"{base_url}#gid=1228814365", "D4 IBNU KHALDUN": f"{base_url}#gid=749204493",
    "D5 IBNU SINA": f"{base_url}#gid=1273332386", "D5 IBNU KHALDUN": f"{base_url}#gid=2136815731",
    "D6 IBNU KHALDUN": f"{base_url}#gid=283583087", "PRA AS-SYAFIE": f"{base_url}#gid=1872315757",
    "PRA AL-GHAZALI": f"{base_url}#gid=1285559833", "PRA AL-MALIKI": f"{base_url}#gid=1820910864",
    "PPKI AL-BIRUNI": f"{base_url}#gid=646110232", "PPKI AL-FARABI": f"{base_url}#gid=378583943",
    "PPKI AL-KHAWARIZMI": f"{base_url}#gid=515727477", "KESELURUHAN": f"{base_url}#gid=272260181"
}

@st.cache_data(ttl=2)
def load_data():
    df = pd.read_csv(url)
    df = df.loc[:, ~df.columns.duplicated()] # Buang kolum duplicate
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    col_kelas = 'KELAS' if 'KELAS' in df.columns else df.columns[0]
    col_nama = 'NAMA MURID' if 'NAMA MURID' in df.columns else df.columns[1]
    
    ralat_list = ['ALAMAT', 'POSKOD', 'TIADA P1', 'TIADA P2', 'P1 = P2', 'HUB P1', 'HUB P2', 'TANGGUNGAN', 'TIADA HP P1', 'PENDAPATAN', 'AKAUN OKU']
    existing_ralat = [c for c in ralat_list if c in df.columns]
    
    # Kira ralat secara dinamik
    df['TOTAL_RALAT_AUTO'] = df[existing_ralat].notna().sum(axis=1)
    return df, existing_ralat, col_kelas, col_nama

try:
    df_master, ralat_list, col_kelas, col_nama = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### 🌸 Menu Carian")
        senarai_kelas = sorted(df_master[col_kelas].dropna().unique().tolist())
        pilihan_kelas = st.selectbox("Pilih Kelas:", ["KESELURUHAN Sekolah"] + senarai_kelas)
        if st.button('🔄 Refresh Data'):
            st.cache_data.clear()
            st.rerun()

    # --- DASHBOARD UTAMA ---
    st.markdown(f"<h1>🎀 Portal Analisis Ralat SKTB 🎀</h1>", unsafe_allow_html=True)
    
    # Butang Link Edit Dinamik
    link_key = pilihan_kelas if pilihan_kelas != "KESELURUHAN Sekolah" else "KESELURUHAN"
    link_edit = link_setiap_kelas.get(link_key, link_setiap_kelas["KESELURUHAN"])
    st.markdown(f'<center><a href="{link_edit}" target="_blank" class="edit-button">📝 Klik Untuk Kemaskini Data {pilihan_kelas}</a></center>', unsafe_allow_html=True)

    # Filter Data
    df_display = df_master if pilihan_kelas == "KESELURUHAN Sekolah" else df_master[df_master[col_kelas] == pilihan_kelas]
    
    # --- KAD STATISTIK (METRICS) ---
    total_ralat = int(df_display['TOTAL_RALAT_AUTO'].sum())
    murid_terlibat = len(df_display[df_display['TOTAL_RALAT_AUTO'] > 0])
    
    # Cari Kelas Terbaik (Ranking)
    df_rank = df_master.groupby(col_kelas)['TOTAL_RALAT_AUTO'].sum().reset_index()
    kelas_terbaik = df_rank.loc[df_rank['TOTAL_RALAT_AUTO'].idxmin(), col_kelas]

    st.markdown(f"""
    <div class="card-container">
        <div class="metric-card"><h4>Kelas Terbaik</h4><h2 style="color:#4CAF50;">{kelas_terbaik}</h2></div>
        <div class="metric-card"><h4>Jumlah Ralat</h4><h2>{total_ralat}</h2></div>
        <div class="metric-card"><h4>Ralat Selesai</h4><h2 style="color:#2196F3;">0</h2></div>
        <div class="metric-card"><h4>Belum Selesai</h4><h2 style="color:#FF5252;">{total_ralat}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    # --- GRAF PRESTASI ---
    if pilihan_kelas == "KESELURUHAN Sekolah":
        st.markdown("<p style='text-align:center; font-weight:bold;'>Statistik Ralat Mengikut Semua Kelas</p>", unsafe_allow_html=True)
        df_graph = df_display.groupby(col_kelas)['TOTAL_RALAT_AUTO'].sum().reset_index()
        fig = px.bar(df_graph, x=col_kelas, y='TOTAL_RALAT_AUTO', color=col_kelas, color_discrete_sequence=px.colors.qualitative.Pastel)
    else:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Pecahan Kategori Ralat</p>", unsafe_allow_html=True)
        df_cat = df_display[ralat_list].notna().sum().reset_index()
        df_cat.columns = ['KATEGORI', 'JUMLAH']
        fig = px.bar(df_cat, x='KATEGORI', y='JUMLAH', color='KATEGORI', color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- JADUAL DETAIL MURID ---
    st.markdown("### 📋 Senarai Murid & Ralat Individu")
    display_cols = [col_kelas, col_nama] + ralat_list
    st.dataframe(df_display[df_display['TOTAL_RALAT_AUTO'] > 0][display_cols].fillna(''), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Sila pastikan tab DATA bermula dari Baris 1 dengan tajuk kolum yang betul: {e}")
