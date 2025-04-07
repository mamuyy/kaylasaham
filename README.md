# 🚀 IDX Multibagger Screener

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.10-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Screener saham syariah Indonesia berbasis performa harga & data fundamental. Fokus deteksi **potensi multibagger (>200% return)** dalam 5 tahun ke depan 📈

---

## 🔍 Fitur Utama
- ✅ **Filter saham syariah & likuid**
- ✅ **Candlestick chart interaktif**
- ✅ **Export hasil ke Excel**
- ✅ **Watchlist saham favorit**
- ✅ **Skor Multibagger (return, growth, ROE, DER)**
- ✅ **Filter berdasarkan sektor**

---

## 🧠 Formula Skor Multibagger

```text
Skor = Return (x) * 0.4 + ROE * 0.2 + Revenue Growth * 0.2 - DER * 0.2
