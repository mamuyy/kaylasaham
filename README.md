# 📈 IDX Multibagger Screener (Streamlit Dashboard)

Screener saham IDX berbasis **fundamental dan harga historis** untuk mendeteksi potensi multibagger (naik >200%) 🚀  
✅ Fokus pada saham **syariah**, **likuid**, dan **berkinerja tinggi**  
✅ Menggunakan data fundamental real-time dari [RTI Business](https://www.rti.co.id)

---

## 🧠 Kriteria Screening:
- Return 5 tahun > 200%
- Volume rata-rata harian > 500K
- EPS > 0
- ROE > 10%
- DER < 1
- PER < 15
- PBV < 3
- PEG < 1
- Net Profit Margin > 10%

---

## ⚙️ Cara Jalankan
### 1. Clone Repo
```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

### 2. Install Library
```bash
pip install -r requirements.txt
```

### 3. Jalankan App
```bash
streamlit run app.py
```

---

## 📁 Struktur Folder
```
.
├── app.py              # Streamlit dashboard
├── screener.py         # Logika screening saham
├── rti_scraper.py      # Scraper data fundamental dari RTI
├── requirements.txt    # List dependency
├── data/
│   └── daftar_saham_syariah.csv  # Daftar saham yang akan dianalisis
└── README.md
```

---

## 💡 Next Steps
- Tambahkan grafik teknikal (RSI, MA, breakout)
- Export ke Excel/CSV
- Kirim alert via Telegram

Built with ❤️ by Cody 🤖
