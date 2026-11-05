# 📊 HR Analytics & Employee Performance Dashboard

Aplikasi web dashboard interaktif berbasis **Streamlit** dan **Plotly** dengan desain antarmuka modern ala **macOS UI** untuk menganalisis data SDM/Karyawan (`HRDataset_v14.csv`).

## 🛠️ Fitur & Komponen Utama
- **Control Center (Filter Interaktif):** Filter berdasarkan Departemen, Status Pernikahan, dan Rentang Gaji.
- **KPI Metrics Widget:** Mengukur Total Karyawan, Rata-rata Gaji, Kepuasan Karyawan, dan Skor Engagment.
- **Visualisasi Interactive (Plotly):**
  1. *Bar Chart:* Rata-rata Gaji per Departemen.
  2. *Donut Chart:* Proporsi Sumber Rekrutmen (Recruitment Source).
  3. *Histogram:* Distribusi Tingkat Kepuasan Karyawan (EmpSatisfaction).
  4. *Scatter Plot:* Hubungan Skor Engagement vs Gaji berdasarkan Kategori Performance Score.
- **Data Storytelling / Executive Summary:** Ringkasan temuan kunci untuk analisis manajemen.

## 🚀 Cara Menjalankan Secara Lokal
```bash
pip install -r requirements.txt
streamlit run app.py