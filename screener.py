def screening(tickers, start, end, min_return=2.0, min_volume=500000):
    fundamental = fetch_fundamental_data_live(tickers)

    # ✅ Validasi: pastikan hasil scraping gak kosong & kolom 'Kode' tersedia
    if not isinstance(fundamental, pd.DataFrame) or 'Kode' not in fundamental.columns:
        print("❌ Data fundamental kosong atau kolom 'Kode' hilang")
        return pd.DataFrame()

    fundamental = fundamental.dropna(subset=['Kode'])
    results = []

    for kode in tickers:
        df = fetch_price_data(kode, start, end)
        if df is None or df.empty or len(df) < 100:
            continue

        harga_awal = df['Close'].iloc[0]
        harga_akhir = df['Close'].iloc[-1]
        ret = harga_akhir / harga_awal
        avg_vol = df['Volume'].mean()

        try:
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
        except KeyError as e:
            print(f"⚠️ KeyError untuk saham {kode}: {e}")
            continue

    return pd.DataFrame(results)
