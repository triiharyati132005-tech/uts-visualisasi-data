import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN & TEMA UI (macOS Style)
# ---------------------------------------------------------
st.set_page_config(
    page_title="HR Analytics Dashboard - macOS UI",
    page_icon="💼",
    layout="wide"
)

# Custom CSS: Styling ala macOS / Apple Frosted Glass UI
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .stApp {
        background-color: #0f1117;
    }
    
    [data-testid="stSidebar"] {
        background-color: #161922;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .css-card {
        background: #1e2230;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    div[data-testid="stMetric"] {
        background: #1e2230;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 18px 22px;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #0A84FF;
    }

    div[data-testid="stMetricLabel"] {
        color: #8e8e93;
        font-weight: 500;
        font-size: 0.9rem;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.7rem;
    }

    .streamlit-expanderHeader {
        background-color: #1e2230 !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #0A84FF !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LOAD DATASET HR (Membaca file HRDataset_v14.csv)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('HRDataset_v14.csv')
    df = df.drop_duplicates()
    return df

df = load_data()

# ---------------------------------------------------------
# 3. SIDEBAR (FILTER INTERAKTIF / CONTROL CENTER)
# ---------------------------------------------------------
st.sidebar.markdown("### 🎛️ Control Center")
st.sidebar.caption("Filter Dashboard SDM")
st.sidebar.markdown("---")

# Filter 1: Departemen
list_dept = df['Department'].unique().tolist()
selected_dept = st.sidebar.multiselect(
    "Pilih Departemen:",
    options=list_dept,
    default=list_dept
)

# Filter 2: Status Pernikahan
list_marital = df['MaritalDesc'].dropna().unique().tolist()
selected_marital = st.sidebar.multiselect(
    "Status Pernikahan:",
    options=list_marital,
    default=list_marital
)

# Filter 3: Rentang Gaji (Salary Slider)
min_salary, max_salary = int(df['Salary'].min()), int(df['Salary'].max())
selected_salary = st.sidebar.slider(
    "Rentang Gaji ($):",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary)
)

# Filtering Data Sesuai Pilihan Sidebar
df_filtered = df[
    (df['Department'].isin(selected_dept)) &
    (df['MaritalDesc'].isin(selected_marital)) &
    (df['Salary'].between(selected_salary[0], selected_salary[1]))
]

# ---------------------------------------------------------
# 4. HEADER WEB & EXECUTIVE SUMMARY
# ---------------------------------------------------------
st.markdown("""
    <div style="background-color: #161922; padding: 20px 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 25px;">
        <h2 style="margin:0; color: #ffffff; font-weight: 700;">💼 HR Analytics & Employee Performance</h2>
        <p style="margin: 4px 0 0 0; color: #8e8e93; font-size: 0.95rem;">System Information Data Visualization Dashboard — HRDataset_v14 Analysis</p>
    </div>
""", unsafe_allow_html=True)

with st.expander("📌 Executive Summary & Key Insights", expanded=True):
    st.write("""
    * **Struktur Kompensasi:** Departemen Executive dan IT/IS mencatatkan rata-rata gaji tertinggi dibandingkan unit operasional/produksi.
    * **Sumber Rekrutmen Utama:** Platform digital seperti *Indeed* dan *LinkedIn* menjadi kanal rekrutmen yang paling banyak menghasilkan kandidat aktif.
    * **Kepuasan & Engagement:** Skor keterikatan (Engagement Survey) menunjukkan korelasi positif terhadap penilaian kinerja (Performance Score) karyawan.
    """)

st.write("")

# ---------------------------------------------------------
# 5. KPI METRICS WIDGETS (Tampilan Card macOS)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_emp = len(df_filtered)
    st.metric(label="Total Karyawan", value=f"{total_emp:,}")

with col2:
    avg_sal = df_filtered['Salary'].mean() if len(df_filtered) > 0 else 0
    st.metric(label="Rata-Rata Gaji", value=f"${avg_sal:,.0f}")

with col3:
    avg_sat = df_filtered['EmpSatisfaction'].mean() if len(df_filtered) > 0 else 0
    st.metric(label="Kepuasan Karyawan", value=f"⭐ {avg_sat:.2f} / 5")

with col4:
    avg_eng = df_filtered['EngagementSurvey'].mean() if len(df_filtered) > 0 else 0
    st.metric(label="Skor Engagement", value=f"📊 {avg_eng:.2f}")

st.write("")

# ---------------------------------------------------------
# 6. VISUALISASI DATA INTERAKTIF (Plotly Charts)
# ---------------------------------------------------------
st.markdown("### 📊 Analytics Overview")

apple_colors = ['#0A84FF', '#30D158', '#FF9F0A', '#BF5AF2', '#FF453A', '#64D2FF', '#FFD60A']

# Row 1 Grafik
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**1. Rata-Rata Gaji per Departemen ($)**")
    dept_salary = df_filtered.groupby('Department')['Salary'].mean().reset_index()
    fig_bar = px.bar(
        dept_salary,
        x='Department',
        y='Salary',
        color='Department',
        text_auto='.2s',
        color_discrete_sequence=apple_colors
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(title="Gaji ($)", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**2. Proporsi Sumber Rekrutmen (Recruitment Source)**")
    rec_counts = df_filtered['RecruitmentSource'].value_counts().reset_index()
    rec_counts.columns = ['RecruitmentSource', 'Count']
    fig_pie = px.pie(
        rec_counts,
        names='RecruitmentSource',
        values='Count',
        hole=0.55,
        color_discrete_sequence=apple_colors
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2 Grafik
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**3. Distribusi Tingkat Kepuasan Karyawan**")
    fig_hist = px.histogram(
        df_filtered,
        x='EmpSatisfaction',
        nbins=10,
        color_discrete_sequence=['#0A84FF']
    )
    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title="Tingkat Kepuasan (1-5)", showgrid=False),
        yaxis=dict(title="Jumlah Karyawan", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**4. Engagement Score vs Gaji per Performance Score**")
    fig_scatter = px.scatter(
        df_filtered,
        x='EngagementSurvey',
        y='Salary',
        color='PerformanceScore',
        color_discrete_sequence=apple_colors,
        hover_data=['Employee_Name', 'Position']
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title="Skor Engagement", showgrid=False),
        yaxis=dict(title="Gaji ($)", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)