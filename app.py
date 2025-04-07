import streamlit as st
import datetime
from screener import load_saham_list, screening, calculate_score
from export_to_gsheet import export_to_gsheet
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import json

st.set_page_config(page_title="IDX Multibagger Screener", layout="wide")

st.title("🚀 IDX Multibagger Screener (Sektor + Skor + Watchlist)")
st.markdown("Saring saham syariah potensial multibagger berdasarkan data fundamental dan historis 📊")

start = datetime.datetime.now() - datetime.timedelta(days=5*365)
end = datetime.datetime.now()

# Load data saham syariah dan sektor
df_syariah = pd.read_csv("data/daftar_saham_syariah.csv")
sektors = sorted(df_syariah["Sektor"].unique())
selected_sektor = st.selectbox("🎯 Pilih Sektor", ["Semua"] + sektors)

if selected_sektor == "Semua":
    tickers = df_syariah["Kode"].tolist()
else:
    tickers = df_syariah[df_syariah["Sektor"] == selected_sektor]["Kode"].tolist()

if st.button("🔍 Jalankan Screener"):
    with st.spinner("⏳ Memproses data..."):
        df = screening(tickers, start, end)

    if not df.empty:
        df["Skor"] = df.apply(calculate_score, axis=1)
        df = df.sort_values(by="Skor", ascending=False).reset_index(drop=True)
        st.success(f"{len(df)} saham ditemukan di sektor {selected_sektor}")
        st.dataframe(df)

        selected = st.selectbox("📈 Pilih saham untuk candlestick chart", df["Kode"])
        if selected:
            df_chart = yf.download(selected + ".JK", start=start, end=end)
            fig = go.Figure(data=[go.Candlestick(
                x=df_chart.index,
                open=df_chart["Open"],
                high=df_chart["High"],
                low=df_chart["Low"],
                close=df_chart["Close"]
            )])
            fig.update_layout(title=f"Candlestick {selected}", xaxis_title="Tanggal", yaxis_title="Harga")
            st.plotly_chart(fig, use_container_width=True)

            if st.button("⭐ Tambahkan ke Watchlist"):
                try:
                    with open("watchlist.json", "r") as f:
                        watchlist = json.load(f)
                except:
                    watchlist = []
                if selected not in watchlist:
                    watchlist.append(selected)
                    with open("watchlist.json", "w") as f:
                        json.dump(watchlist, f)
                    st.success(f"{selected} ditambahkan ke Watchlist!")
                else:
                    st.info(f"{selected} sudah ada di Watchlist.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Export ke Excel"):
                df.to_excel("multibagger_result.xlsx", index=False)
                st.success("✅ Hasil disimpan sebagai multibagger_result.xlsx")

        with col2:
            if st.button("📤 Export ke Google Sheet"):
                with st.spinner("📤 Mengirim ke Google Sheet..."):
                    export_to_gsheet(df, "multibagger_test_sheet", worksheet_name="Portofolio Saham IDX")
                    st.success("✅ Data berhasil dikirim ke Google Sheet!")

    else:
        st.warning("⚠️ Tidak ada saham yang memenuhi kriteria.")

st.markdown("---")
st.subheader("⭐ Watchlist Saya")
try:
    with open("watchlist.json", "r") as f:
        watchlist = json.load(f)
    st.write(watchlist)
except:
    st.info("Watchlist masih kosong.")
