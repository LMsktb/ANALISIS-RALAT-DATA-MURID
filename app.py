import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="idMe Analysis SKTB", layout="wide")

# --- TEMA CERAH & PINK ---
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

# URL Master CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4K9zTk5to3U37As72duwLP7GRqYMkauaAhjr6ANe8s6bl7Qz85ojUXeSDOYw3-iQkMvKV-gq4ZXf/pub?output=csv"

# Link Edit Tab (GID Cikgu Moon)
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
    # 💡 KEMASKINI: Skip 2 baris teratas terus untuk elakkan 'Table1' atau ruang kosong
    df = pd.read_csv(url, header=None, skiprows=2)
    
    # Namakan semula kolum secara manual ikut apa Bubu nampak kat screenshot
    new_cols = ['KELAS', 'NAMA_MURID', 'ALAMAT', 'POSKOD', 'TIADA_P1', 'TIADA_P2', 'P1_P2', 'HUB_P1', 'HUB_P2', 'TANGGUNGAN', 'TIADA_HP_P1', 'PENDAPATAN', 'AKAUN_OKU', 'SELESAI']
    df.columns = new_cols[:len(df.columns)]
    
    # Buang baris yang tak ada nama murid
    df = df.dropna(subset=['NAMA_MURID'])
    
    # Kategori ralat (Check tick ✓)
    ralat_list = ['ALAMAT', 'POSKOD', 'TIADA_P1', 'TIADA_P2', 'P1_P2', 'HUB_P1', 'HUB_P2', 'TANGGUNGAN', 'TIADA_HP_P1', 'PENDAPATAN', 'AKAUN_OKU']
    df['TOTAL_RALAT_AUTO'] = df[ralat_list].notna().sum(axis=1)
    
    return df, ralat_list

try:
    df_master, ralat_list = load_data()
    
    # Menu Sidebar
    with st.sidebar:
        st.markdown("### 🌸 Menu Carian")
        senarai_kelas = sorted(df_master['KELAS'].dropna().unique().tolist())
        pilihan_kelas = st.selectbox("Pilih Kelas:", ["KESELURUHAN Sekolah"] + senarai_kelas)
        if st.button('🔄 Refresh'):
            st.cache_data.clear()
            st.rerun()

    # Dashboard Utama
    st.markdown(f"<h1>🎀 Portal Analisis Ralat SKTB 🎀</h1>", unsafe_allow_html=True)
    
    key_link = pilihan_kelas if pilihan_kelas != "KESELURUHAN Sekolah" else "KESELURUHAN"
    link_edit = link_setiap_kelas.get(key_link, link_setiap_kelas["KESELURUHAN"])
    st.markdown(f'<center><a href="{link_edit}" target="_blank" class="edit-button">📝 Klik Untuk Kemaskini Data {pilihan_kelas}</a></center>', unsafe_allow_html=True)

    # Filter Data
    df_display = df_master if pilihan_kelas == "KESELURUHAN Sekolah" else df_master[df_master['KELAS'] == pilihan_kelas]
    
    # Metrics
    total_kes = int(df_display['TOTAL_RALAT_AUTO'].sum())
    murid_terlibat = len(df_display[df_display['TOTAL_RALAT_AUTO'] > 0])
    
    st.markdown(f"""
    <div class="card-container">
        <div class="metric-card"><h4>Murid Terlibat</h4><h2>{murid_terlibat}</h2></div>
        <div class="metric-card"><h4>Jumlah Ralat</h4><h2>{total_kes}</h2></div>
        <div class="metric-card"><h4>Ralat Selesai</h4><h2 style="color:#4CAF50;">0</h2></div>
        <div class="metric-card"><h4>Belum Selesai</h4><h2 style="color:#FF5252;">{total_kes}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    # Graf
    if pilihan_kelas == "KESELURUHAN Sekolah":
        df_graph = df_display.groupby('KELAS')['TOTAL_RALAT_AUTO'].sum().reset_index()
        fig = px.bar(df_graph, x='KELAS', y='TOTAL_RALAT_AUTO', color='KELAS', color_discrete_sequence=px.colors.qualitative.Pastel)
    else:
        df_cat = df_display[ralat_list].notna().sum().reset_index()
        df_cat.columns = ['KATEGORI', 'JUMLAH']
        fig = px.bar(df_cat, x='KATEGORI', y='JUMLAH', color='KATEGORI', color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Jadual
    st.markdown("### 📋 Senarai Murid Perlu Tindakan")
    df_table = df_display[df_display['TOTAL_RALAT_AUTO'] > 0][['KELAS', 'NAMA_MURID'] + ralat_list]
    st.dataframe(df_table.fillna(''), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Sila pastikan data anda bermula dari baris ke-2 atau ke-3 di Google Sheet: {e}")
