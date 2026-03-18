import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="idMe Analysis SKTB", layout="wide")

# --- CSS TEMA CERAH & PINK (PORTAL VIBE) ---
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
    </style>
    """, unsafe_allow_html=True)

# URL yang Cikgu bagi
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4K9zTk5to3U37As72duwLP7GRqYMkauaAhjr6ANe8s6bl7Qz85ojUXeSDOYw3-iQkMvKV-gq4ZXf/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    # Baca CSV
    df = pd.read_csv(url)
    
    # Bersihkan nama kolum
    df.columns = [str(c).strip() for c in df.columns]
    
    # Kategori ralat (Kolum C hingga M dalam sheet Cikgu)
    cols_ralat = ['Alamat', 'Poskod', 'Tiada P1', 'Tiada P2', 'P1=P2', 'Hub P1', 'Hub P2', 'Tanggungan', 'Tiada HP P1', 'Pendapatan', 'Akaun OKU']
    
    # Cari kolum yang betul-betul wujud dalam data
    existing_ralat = [c for c in cols_ralat if c in df.columns]
    
    # Kira 'Total_Ralat' berdasarkan Tick (Sel yang tak kosong)
    if existing_ralat:
        df['Total_Ralat'] = df[existing_ralat].notna().astype(int).sum(axis=1)
    else:
        df['Total_Ralat'] = 0
        
    return df, existing_ralat

try:
    df_master, ralat_list = load_data()
    
    # Semak kalau kolum Kelas wujud
    if 'Kelas' not in df_master.columns:
        st.warning("⚠️ Tips: Pastikan tab 'DATA' adalah tab yang paling kiri sekali dalam Google Sheet Cikgu.")
        st.error(f"Sila semak nama kolum. Sekarang kolum yang ada ialah: {list(df_master.columns)}")
        st.stop()

    # --- SIDEBAR (MENU CARIAN) ---
    with st.sidebar:
        st.markdown("### 🌸 Menu Carian")
        senarai_kelas = sorted(df_master['Kelas'].dropna().unique().tolist())
        pilihan_kelas = st.selectbox("Pilih Kelas:", ["KESELURUHAN"] + senarai_kelas)
        st.write("---")
        if st.button('🔄 Refresh Data'):
            st.cache_data.clear()
            st.rerun()
        st.info("Padam tanda tick (✓) dalam Google Sheet untuk kemaskini dashboard.")

    # Tapis Data
    if pilihan_kelas == "KESELURUHAN":
        df_display = df_master
        title_text = "Keseluruhan Sekolah"
    else:
        df_display = df_master[df_master['Kelas'] == pilihan_kelas]
        title_text = f"Kelas {pilihan_kelas}"

    # --- DASHBOARD UTAMA ---
    st.markdown(f"<h1>🎀 Analisis Ralat: {title_text} 🎀</h1>", unsafe_allow_html=True)
    
    total_kes = int(df_display['Total_Ralat'].sum())
    murid_terlibat = len(df_display[df_display['Total_Ralat'] > 0])
    
    # Paparan Kad Statistik
    st.markdown(f"""
    <div class="card-container">
        <div class="metric-card"><h4>Murid Terlibat</h4><h2>{murid_terlibat}</h2></div>
        <div class="metric-card"><h4>Jumlah Ralat</h4><h2>{total_kes}</h2></div>
        <div class="metric-card"><h4>Ralat Selesai</h4><h2 style="color:#4CAF50;">0</h2></div>
        <div class="metric-card"><h4>Belum Selesai</h4><h2 style="color:#FF5252;">{total_kes}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    # --- GRAF PRESTASI (WARNA PASTEL) ---
    st.write("")
    if pilihan_kelas == "KESELURUHAN":
        st.markdown("<p style='text-align:center; font-weight:bold;'>Statistik Ralat Mengikut Kelas</p>", unsafe_allow_html=True)
        df_graph = df_display.groupby('Kelas')['Total_Ralat'].sum().reset_index()
        fig = px.bar(df_graph, x='Kelas', y='Total_Ralat', color='Kelas', color_discrete_sequence=px.colors.qualitative.Pastel)
    else:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Pecahan Kategori Ralat</p>", unsafe_allow_html=True)
        df_cat = df_display[ralat_list].notna().sum().reset_index()
        df_cat.columns = ['Kategori', 'Jumlah']
        fig = px.bar(df_cat, x='Kategori', y='Jumlah', color='Kategori', color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- JADUAL NAMA MURID (DETAIL) ---
    st.markdown("### 📋 Senarai Murid Perlu Tindakan")
    df_table = df_display[df_display['Total_Ralat'] > 0][['Kelas', 'Nama Murid'] + ralat_list]
    # Tukar NaN jadi kosong supaya nampak bersih
    st.dataframe(df_table.fillna(''), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Sila pastikan link CSV betul dan tab 'DATA' mengandungi kolum 'Kelas': {e}")
