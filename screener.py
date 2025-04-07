import yfinance as yf
import pandas as pd
from rti_scraper import scrape_multiple

def load_saham_list():
    df = pd.read_csv("data/daftar_saham_syariah.csv")
    return df['Kode'].tolist()

def fetch_price_data(ticker, start, end):
    try:
        df = yf.download(ticker + ".JK", start=start, end=end, progress=False)
        return df
    except:
        return None

def fetch_fundamental_data_live(tickers):
    return scrape_multiple(tickers)

def screening(tickers, start, end, min_return=2.0, min_volume=500000):
    fundamental = fetch_fundamental_data_live(tickers)
    results = []

    for kode in tickers:
        df = fetch_price_data(kode, start, end)
        if df is None or df.empty or len(df) < 100: continue

        harga_awal = df['Close'].iloc[0]
        harga_akhir = df['Close'].iloc[-1]
        ret = harga_akhir / harga_awal
        avg_vol = df['Volume'].mean()

        f_row = fundamental[fundamental['Kode'] == kode]
        if (
            ret >= min_return and avg_vol >= min_volume and
            not f_row.empty and
            float(f_row['EPS']) > 0 and
            float(f_row['ROE']) > 10 and
            float(f_row['DER']) < 1 and
            float(f_row['PER']) < 15 and
            float(f_row['PBV']) < 3 and
            float(f_row['PEG']) < 1 and
            float(f_row['NPM']) > 10
        ):
            results.append({
                'Kode': kode,
                'Harga Awal': round(harga_awal, 2),
                'Harga Akhir': round(harga_akhir, 2),
                'Return (x)': round(ret, 2),
                'EPS': float(f_row['EPS']),
                'ROE': float(f_row['ROE']),
                'DER': float(f_row['DER']),
                'PER': float(f_row['PER']),
                'PBV': float(f_row['PBV']),
                'PEG': float(f_row['PEG']),
                'NPM': float(f_row['NPM']),
                'RevenueGrowth': float(f_row['RevenueGrowth']),
            })

    return pd.DataFrame(results)
