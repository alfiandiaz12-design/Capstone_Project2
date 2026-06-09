# 🛒 Customer Personality Analysis
### Analisis Perilaku Konsumen Berdasarkan Segmentasi Pelanggan

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 📌 Project Overview

Proyek ini merupakan **Capstone Project 2** dari program Data Analytics di **Purwadhika Digital Technology School**. Analisis dilakukan menggunakan dataset **Customer Personality Analysis** dari Kaggle untuk memahami bagaimana pendapatan dan tanggungan keluarga memengaruhi preferensi pembelian pelanggan.

---

## 🗃️ Dataset

- **Sumber:** [Kaggle — Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)
- **Ukuran awal:** 2.240 rows, 30 columns
- **Ukuran setelah preprocessing:** 2.233 rows, 28 columns

---

## 📋 Data Understanding

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| `Income` | Float64 | Pendapatan tahunan pelanggan |
| `Kidhome` | Integer64 | Jumlah anak kecil dalam rumah tangga |
| `Teenhome` | Integer64 | Jumlah remaja dalam rumah tangga |
| `MntWines` | Integer64 | Pengeluaran untuk wines (2 tahun terakhir) |
| `MntMeat` | Integer64 | Pengeluaran untuk daging (2 tahun terakhir) |
| `MntFruits` | Integer64 | Pengeluaran untuk buah-buahan (2 tahun terakhir) |
| `MntFish` | Integer64 | Pengeluaran untuk ikan (2 tahun terakhir) |
| `MntSweet` | Integer64 | Pengeluaran untuk makanan manis (2 tahun terakhir) |
| `MntGold` | Integer64 | Pengeluaran untuk emas (2 tahun terakhir) |
| `NumWebPurchases` | Integer64 | Jumlah pembelian via website |
| `NumCatalogPurchases` | Integer64 | Jumlah pembelian via katalog |
| `NumStorePurchases` | Integer64 | Jumlah pembelian langsung di toko |
| `NumWebVisitsMonth` | Integer64 | Kunjungan website per bulan |
| `Income_Segment` | Category | Segmentasi income: Low / Mid / High |
| `Child_Segment` | String | Segmentasi tanggungan anak |

---

## 🔧 Data Preprocessing

### 1. Marital Status
Hapus klasifikasi yang tidak valid:
- `Absurd`
- `YOLO`
- `Alone`

### 2. Education
Mapping ulang kategori pendidikan:
- `Basic` → Bachelor
- `2n Cycle` → Magister
- `Master` → Magister
- Gabungkan `Together` dengan `Married`

### 3. Missing Values
- Kolom `Income` memiliki **24 baris missing**
- Ditangani menggunakan **imputasi median dua tahap**

---

## 🏷️ Segmentasi

### Income Segment
Dibagi menjadi 3 kelompok menggunakan metode persentil (P33 & P67):

| Segmen | Rata-rata Pendapatan |
|--------|----------------------|
| Low | ~282.283 |
| Mid | ~515.324 |
| High | ~769.155 |

### Child Segment
Kombinasi Kidhome dan Teenhome menjadi 4 kelompok:

| Segmen | Definisi |
|--------|----------|
| No Child | 0 Kidhome & 0 Teenhome |
| Balance Mixed | 1 Kidhome & 1 Teenhome |
| Kid Dominant | 2 Kidhome & 1 Teenhome |
| Teen Dominant | 2 Teenhome & 1 Kidhome |

> **Catatan:** Kid Dominant (n=31) dan Teen Dominant (n=22) memiliki sampel kecil — dipertahankan untuk kelengkapan komparasi, namun tidak cukup representatif untuk generalisasi.

---

## 🛠️ Tools & Libraries

| Tool | Kegunaan |
|------|----------|
| Python | EDA & preprocessing |
| Pandas | Data manipulation |
| Matplotlib & Seaborn | Visualisasi data |

---

