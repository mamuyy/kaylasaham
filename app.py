import streamlit as st
import datetime
from screener import load_saham_list, screening

st.set_page_config(page_title="IDX Multibagger Screener", layout="wide")

st.title("🚀 IDX Multibagger Screener (Syariah & Likuid)")
st.markdown("Filter saham dengan potensi multibagger berdasarkan performa harga dan data fundamental 📊")

start = datetime.datetime.now() - datetime.timedelta(days=5*365)
end = datetime.datetime.now()

tickers = load_saham_list()

if st.button("🔍 Jalankan Screener"):
    with st.spinner("Memproses data..."):
        df = screening(tickers, start, end)
    if not df.empty:
        st.success(f"{len(df)} saham ditemukan!")
        st.dataframe(df)

        selected = st.selectbox("📈 Pilih saham untuk grafik", df['Kode'])
        if selected:
            import yfinance as yf
            df_chart = yf.download(selected + ".JK", start=start, end=end)
            st.line_chart(df_chart['Close'])
    else:
        st.warning("Tidak ada saham yang memenuhi kriteria.")
