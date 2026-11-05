import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="HR Analytics Dashboard - macOS UI",
    page_icon="💼",
    layout="wide"
)

# 2. CUSTOM CSS: OVERRIDE TOTAL TEKS & KONTRAST MAC OS STYLE
st.markdown("""
    <style>
    /* Font Global SF Pro / Apple Style */
    html, body, [class*="css"], .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        background-color: #1e1e1e !important;
        color: #f5f5f7 !important;
    }
    
    /* ---------------------------------------------------------
       FIX SIDEBAR (CONTROL CENTER)
    --------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #282828 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Paksa semua teks di sidebar berwarna terang */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #f5f5f7 !important;
    }

    /* Chip Multiselect / Tag Filter */
    span[data-baseweb="tag"] {
        background-color: #0a84ff !important;
        border-radius: 6px !important;
    }
    span[data-baseweb="tag"] * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Input Multiselect & Slider Box */
    div[data-baseweb="select"] > div {
        background-color: #1c1c1e !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }

    /* ---------------------------------------------------------
       FIX METRIC CARDS (TOTAL KARYAWAN, GAJI, DLL)
    --------------------------------------------------------- */
    div[data-testid="stMetric"] {
        background-color: #2c2c2e !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #0a84ff !important;
    }

    /* Label Judul Metric (misal: Total Karyawan) */
    div[data-testid="stMetricLabel"] *, 
    div[data-testid="stMetricLabel"] p, 
    div[data-testid="stMetricLabel"] label {
        color: #a1a1a6 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Angka / Value Metric (misal: 311, $69,021) */
    div[data-testid="stMetricValue"] *, 
    div[data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }

    /* ---------------------------------------------------------
       FIX EXPANDER & CHART CONTAINERS
    --------------------------------------------------------- */
    .css-card {
        background-color: #2c2c2e !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }

    .streamlit-expanderHeader {
        background-color: #2c2c2e !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .streamlit-expanderHeader * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    .stExpander p, .stExpander li {
        color: #e5e5ea !important;
    }

    /* Color Slider */
    .stSlider > div > div > div > div {
        background-color: #0a84ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. LOAD DATASET HR
@st.cache_data
def load_data():
    df = pd.read_csv('HRDataset_v14.csv')
    df = df.drop_duplicates()
    return df

df = load_data()

# 4. SIDEBAR (CONTROL CENTER)
st.sidebar.markdown("## 🎛️ Control Center")
st.sidebar.markdown("Filter Dashboard SDM")
st.sidebar.markdown("---")

list_dept = df['Department'].dropna().unique().tolist()
selected_dept = st.sidebar.multiselect(
    "Pilih Departemen:",
    options=list_dept,
    default=list_dept
)

list_marital = df['MaritalDesc'].dropna().unique().tolist()
selected_marital = st.sidebar.multiselect(
    "Status Pernikahan:",
    options=list_marital,
    default=list_marital
)

min_salary, max_salary = int(df['Salary'].min()), int(df['Salary'].max())
selected_salary = st.sidebar.slider(
    "Rentang Gaji ($):",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary)
)

# Filtering Data
df_filtered = df[
    (df['Department'].isin(selected_dept)) &
    (df['MaritalDesc'].isin(selected_marital)) &
    (df['Salary'].between(selected_salary[0], selected_salary[1]))
]

# 5. HEADER WEB & STORYTELLING
st.markdown("""
    <div style="background-color: #2c2c2e; padding: 22px 26px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 25px;">
        <h2 style="margin:0; color: #ffffff; font-weight: 700;">💼 HR Analytics & Employee Performance</h2>
        <p style="margin: 6px 0 0 0; color: #a1a1a6; font-size: 0.95rem;">System Information Data Visualization Dashboard — HRDataset_v14 Analysis</p>
    </div>
""", unsafe_allow_html=True)

with st.expander("📌 Executive Summary & Key Insights", expanded=True):
    st.write("""
    * **Struktur Kompensasi:** Departemen Executive dan IT/IS mencatatkan rata-rata gaji tertinggi dibandingkan unit operasional/produksi.
    * **Sumber Rekrutmen Utama:** Platform digital seperti *Indeed* dan *LinkedIn* menjadi kanal rekrutmen paling efektif.
    * **Kepuasan & Engagement:** Skor keterikatan (Engagement Survey) berbanding lurus dengan hasil penilaian kinerja (Performance Score).
    """)

st.write("")

# 6. KPI METRICS WIDGETS
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

# 7. VISUALISASI DATA (PLOTLY CHARTS)
st.markdown("<h3 style='color:#ffffff;'>📊 Analytics Overview</h3>", unsafe_allow_html=True)

apple_colors = ['#0a84ff', '#30d158', '#ff9f0a', '#bf5af2', '#ff453a', '#64d2ff', '#ffd60a']

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffffff; margin-bottom:15px;'>1. Rata-Rata Gaji per Departemen ($)</h4>", unsafe_allow_html=True)
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
        font=dict(color="#f5f5f7"),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(title="Gaji ($)", showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffffff; margin-bottom:15px;'>2. Proporsi Sumber Rekrutmen</h4>", unsafe_allow_html=True)
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
        font=dict(color="#f5f5f7"),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffffff; margin-bottom:15px;'>3. Distribusi Tingkat Kepuasan Karyawan</h4>", unsafe_allow_html=True)
    fig_hist = px.histogram(
        df_filtered,
        x='EmpSatisfaction',
        nbins=10,
        color_discrete_sequence=['#0a84ff']
    )
    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f5f5f7"),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Tingkat Kepuasan (1-5)", showgrid=False),
        yaxis=dict(title="Jumlah Karyawan", showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffffff; margin-bottom:15px;'>4. Engagement Score vs Gaji</h4>", unsafe_allow_html=True)
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
        font=dict(color="#f5f5f7"),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Skor Engagement", showgrid=False),
        yaxis=dict(title="Gaji ($)", showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
