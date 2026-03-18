import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="idMe Analysis SKTB", layout="wide")

# --- CSS UNTUK TEMA CERAH & KAD (PASTEL) ---
st.markdown("""
    <style>
    /* Latar belakang putih/pink cair */
    .stApp { background-color: #fdf2f5; }
    
    /* Gaya untuk Kad Statistik */
    .card-container {
        display: flex;
        justify-content: space-around;
        gap: 10px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #ffc1d6;
        text-align: center;
        flex: 1;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .metric-card h4 { color: #888; font-size: 14px; margin-bottom: 5px; }
    .metric-card h2 { color: #ff4d88; margin: 0; font-size: 28px; }
    
    /* Tajuk Pink */
    h1, h3 { color: #ff4d88; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# Tajuk Utama
st.markdown("<h1>🎀 Dashboard Analisis Ralat Murid (idMe) 🎀</h1>", unsafe_allow_html=True)
st.markdown("<h3>SK Telok Berembang</h3>", unsafe_allow_html=True)
st.write("")

# URL Data Bubu (Link Publish)
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4K9zTk5to3U37As72duwLP7GRqYMkauaAhjr6ANe8s6bl7Qz85ojUXeSDOYw3-iQkMvKV-gq4ZXf/pub?output=csv"

@st.cache_data(ttl=10)
def get_data():
    df_raw = pd.read_csv(url, skiprows=7)
    df = df_raw.iloc[:, [0, 1]].copy()
    df.columns = ['Kelas', 'Jumlah Ralat']
    df = df.dropna(subset=['Kelas'])
    df = df[df['Kelas'].astype(str).str.contains('IBNU|PRA|PPKI', case=False, na=False)]
    df['Jumlah Ralat'] = pd.to_numeric(df['Jumlah Ralat'], errors='coerce').fillna(0)
    return df

try:
    df = get_data()
    total_ralat = int(df['Jumlah Ralat'].sum())
    kelas_terbaik = df.loc[df['Jumlah Ralat'].idxmin(), 'Kelas']

    # --- BAHAGIAN KAD (METRICS) ---
    st.markdown(f"""
    <div class="card-container">
        <div class="metric-card"><h4>Kelas Terbaik</h4><h2>{kelas_terbaik}</h2></div>
        <div class="metric-card"><h4>Jumlah Ralat</h4><h2>{total_ralat}</h2></div>
        <div class="metric-card"><h4>Ralat Selesai</h4><h2 style="color:#4CAF50;">0</h2></div>
        <div class="metric-card"><h4>Belum Selesai</h4><h2 style="color:#FF5252;">{total_ralat}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    # --- GRAF PERBANDINGAN (CERAH & WARNA-WARNI) ---
    st.markdown("<p style='text-align:center; color:#ff4d88; font-weight:bold;'>Perbandingan Ralat Mengikut Kelas</p>", unsafe_allow_html=True)
    
    # Warna-warna pastel untuk bar
    pastel_colors = ['#ffb3ba', '#ffdfba', '#ffffba', '#baffc9', '#bae1ff', '#e1baff', '#ffb3e6']
    
    fig = px.bar(df, x='Kelas', y='Jumlah Ralat', 
                 color='Kelas', 
                 color_discrete_sequence=px.colors.qualitative.Pastel)

    # Buang background hitam dan grid gelap
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- JADUAL DI BAWAH (OPSYENAL) ---
    st.dataframe(df.sort_values('Jumlah Ralat', ascending=False), hide_index=True, use_container_width=True)

except Exception as e:
    st.error(f"Data belum sedia atau ada ralat: {e}")

if st.button('🔄 Kemaskini Data'):
    st.cache_data.clear()
    st.rerun()
