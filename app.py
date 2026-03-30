import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="idMe Analysis SKTB", layout="wide", page_icon="🎀")

# 2. PAUTAN LOGO
logo_id = "1XV1CIEWhms8jHqJGOKpSluqr7cxtSWrv"
logo_url = f"https://drive.google.com/thumbnail?id={logo_id}&sz=w500"

# 3. TEMA CSS (Dikemaskini untuk besarkan & bold tajuk kad)
st.markdown("""
    <style>
    .stApp { background-color: #fdf2f5; }
    [data-testid="stHorizontalBlock"] { align-items: center; }
    
    /* Cantikkan Kad Statistik */
    .card-container { display: flex; justify-content: space-around; gap: 10px; margin-bottom: 20px; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border: 2px solid #ffc1d6; text-align: center; flex: 1;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    
    /* --- BAHAGIAN YANG DIUBAH: Tajuk Kad (h4) --- */
    .metric-card h4 { 
        color: #555; 
        font-size: 18px;    /* Saiz asal 14px, sekarang 18px */
        font-weight: bold;  /* Buat jadi Bold */
        margin-bottom: 8px; 
    }
    
    .metric-card h2 { color: #ff4d88; margin: 0; font-size: 30px; font-weight: bold; }
    
    /* Tajuk Portal */
    h1 { color: #ff4d88; text-align: center; font-family: 'Comic Sans MS', cursive; margin-top: -10px; padding-top: 0; }
    
    /* Butang Edit */
    .edit-button {
        background-color: #ff4d88; color: white !important; padding: 12px 25px;
        text-align: center; border-radius: 12px; text-decoration: none;
        display: inline-block; font-weight: bold; margin-bottom: 25px; border: 2px solid #ffb6c1;
    }
    
    section[data-testid="stSidebar"] { background-color: #fff0f5; border-right: 2px solid #ffc1d6; }
    </style>
    """, unsafe_allow_html=True)
# 4. URL DATA
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4K9zTk5to3U37As72duwLP7GRqYMkauaAhjr6ANe8s6bl7Qz85ojUXeSDOYw3-iQkMvKV-gq4ZXf/pub?gid=272260181&single=true&output=csv"
base_edit = "https://docs.google.com/spreadsheets/d/1y8BvpG0NN5wWwhSFWNS2AOI4Qe8O4HYg5M-LPrMmzjk/edit?"

link_setiap_kelas = {
    "D1 IBNU SINA": f"{base_edit}gid=336938430#gid=336938430",
    "D1 IBNU KHALDUN": f"{base_edit}gid=648519110#gid=648519110",
    "D2 IBNU SINA": f"{base_edit}gid=851785168#gid=851785168",
    "D2 IBNU KHALDUN": f"{base_edit}gid=2036307286#gid=2036307286",
    "D3 IBNU SINA": f"{base_edit}gid=1435005895#gid=1435005895",
    "D3 IBNU KHALDUN": f"{base_edit}gid=1308911247#gid=1308911247",
    "D4 IBNU SINA": f"{base_edit}gid=1228814365#gid=1228814365",
    "D4 IBNU KHALDUN": f"{base_edit}gid=749204493#gid=749204493",
    "D5 IBNU SINA": f"{base_edit}gid=1273332386#gid=1273332386",
    "D5 IBNU KHALDUN": f"{base_edit}gid=2136815731#gid=2136815731",
    "D6 IBNU SINA": f"{base_edit}gid=255757977#gid=255757977",
    "D6 IBNU KHALDUN": f"{base_edit}gid=283583087#gid=283583087",
    "PRA AS-SYAFIE": f"{base_edit}gid=1872315757#gid=1872315757",
    "PRA AL-GHAZALI": f"{base_edit}gid=1285559833#gid=1285559833",
    "PRA AL-MALIKI": f"{base_edit}gid=1820910864#gid=1820910864",
    "PPKI AL-BIRUNI": f"{base_edit}gid=646110232#gid=646110232",
    "PPKI AL-FARABI": f"{base_edit}gid=378583943#gid=378583943",
    "PPKI AL-KHAWARIZMI": f"{base_edit}gid=515727477#gid=515727477",
    "KESELURUHAN Sekolah": f"{base_edit}gid=272260181#gid=272260181"
}

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

# 5. LOGIK UTAMA APLIKASI
try:
    df_master, ralat_list = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.image(logo_url, width=90) 
        st.markdown("### 🌸 Menu Carian")
        senarai_kelas = sorted(df_master['KELAS'].unique().tolist())
        pilihan = st.selectbox("Pilih Kelas:", ["KESELURUHAN Sekolah"] + senarai_kelas)
        if st.button('🔄 Refresh'):
            st.cache_data.clear()
            st.rerun()
        st.write(f"Masa: {datetime.now().strftime('%H:%M:%S')}")

    # --- LOGO TENGAH ---
    col1, col_logo, col3 = st.columns([1, 0.3, 1]) 
    with col_logo:
        st.image(logo_url, use_container_width=True)

    st.markdown("<h1 style='text-align: center; color: #ff4d88; font-family: \"Comic Sans MS\", cursive;'>🎀 Portal Analisis Ralat SKTB 🎀</h1>", unsafe_allow_html=True)
    
    # --- ISI KANDUNGAN ---
    link_edit = link_setiap_kelas.get(pilihan, link_setiap_kelas["KESELURUHAN Sekolah"])
    st.markdown(f'<center><a href="{link_edit}" target="_blank" class="edit-button">📝 Klik Untuk Kemaskini Data {pilihan}</a></center>', unsafe_allow_html=True)

    df_display = df_master if pilihan == "KESELURUHAN Sekolah" else df_master[df_master['KELAS'] == pilihan]
    total_r = int(df_display['TOTAL_RALAT'].sum())
    kelas_terbaik = "6 IBNU SINA"

    st.markdown(f"""
    <div class="card-container">
        <div class="metric-card"><h4>Kelas Terbaik 🏆</h4><h2 style="color:#4CAF50;">{kelas_terbaik}</h2></div>
        <div class="metric-card"><h4>Jumlah Ralat</h4><h2 style="color:#ff4d88;">457</h2></div>
        <div class="metric-card"><h4>Ralat Selesai</h4><h2 style="color:#2196F3;">28</h2></div>
        <div class="metric-card"><h4>Belum Selesai</h4><h2 style="color:#FF5252;">429</h2></div>
    </div>
    """, unsafe_allow_html=True)

    if pilihan == "KESELURUHAN Sekolah":
        df_g = df_display.groupby('KELAS')['TOTAL_RALAT'].sum().reset_index()
        fig = px.bar(df_g, x='KELAS', y='TOTAL_RALAT', color='KELAS', color_discrete_sequence=px.colors.qualitative.Pastel)
    else:
        df_cat = df_display[ralat_list].notna().sum().reset_index()
        df_cat.columns = ['Kategori', 'Jumlah']
        fig = px.bar(df_cat, x='Kategori', y='Jumlah', color='Kategori', color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Senarai Murid Perlu Tindakan")
    df_ralat = df_display[df_display['TOTAL_RALAT'] > 0]
    if not df_ralat.empty:
        st.dataframe(df_ralat[['KELAS', 'NAMA_MURID'] + ralat_list].fillna(''), use_container_width=True, hide_index=True)
    else:
        st.success(f"🎉 Tahniah! Kelas {pilihan} sudah tiada ralat.")

except Exception as e:
    st.error(f"Sila Refresh: {e}")
