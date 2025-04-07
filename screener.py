import yfinance as yf
import pandas as pd
from rti_scraper import scrape_multiple

def load_saham_list():
    """
    Memuat daftar saham syariah dari file CSV dengan penanganan error yang lebih baik
    """
    try:
        df = pd.read_csv("data/daftar_saham_syariah.csv")
        
        # Debug: Cetak kolom yang tersedia
        print("Kolom yang tersedia:", df.columns.tolist())
        
        # Coba beberapa alternatif nama kolom ticker
        column_names = ['Kode', 'kode', 'Ticker', 'ticker', 'Kode Saham', 'Code', 'Simbol']
        for col in column_names:
            if col in df.columns:
                return df[col].str.upper().tolist()  # Pastikan dalam format uppercase
        
        # Fallback: ambil kolom pertama jika semua gagal
        return df.iloc[:, 0].str.upper().tolist()
        
    except FileNotFoundError:
        print("❌ File daftar saham tidak ditemukan di: data/daftar_saham_syariah.csv")
        return []
    except Exception as e:
        print(f"❌ Gagal memuat daftar saham: {str(e)}")
        return []

def fetch_price_data(ticker, start, end):
    """
    Mengambil data harga saham dari Yahoo Finance
    """
    try:
        df = yf.download(ticker + ".JK", start=start, end=end, progress=False)
        return df if df is not None and not df.empty else None
    except Exception as e:
        print(f"⚠️ Gagal mengambil data harga untuk {ticker}: {str(e)}")
        return None

def fetch_fundamental_data_live(tickers):
    """
    Mengambil data fundamental saham menggunakan RTI Scraper
    """
    try:
        data = scrape_multiple(tickers)
        if not isinstance(data, pd.DataFrame):
            print("❌ Data fundamental bukan DataFrame")
            return pd.DataFrame()
        return data
    except Exception as e:
        print(f"❌ Gagal mengambil data fundamental: {str(e)}")
        return pd.DataFrame()

def screening(tickers, start, end, min_return=2.0, min_volume=500000):
    """
    Melakukan screening saham berdasarkan kriteria teknikal dan fundamental
    """
    # Validasi input
    if not tickers:
        print("⚠️ Daftar ticker kosong")
        return pd.DataFrame()

    print(f"\n🔍 Memproses {len(tickers)} saham...")
    print(f"📅 Periode: {start} sampai {end}")
    print(f"📊 Parameter screening: Return min {min_return}x, Volume min {min_volume:,}")

    # Ambil data fundamental
    fundamental = fetch_fundamental_data_live(tickers)
    
    # Validasi data fundamental
    if not isinstance(fundamental, pd.DataFrame) or fundamental.empty:
        print("❌ Data fundamental tidak valid atau kosong")
        return pd.DataFrame()

    required_columns = ['Kode', 'EPS', 'ROE', 'DER', 'PER', 'PBV', 'PEG', 'NPM', 'RevenueGrowth']
    missing_cols = [col for col in required_columns if col not in fundamental.columns]
    
    if missing_cols:
        print(f"❌ Kolom yang hilang di data fundamental: {missing_cols}")
        return pd.DataFrame()

    results = []
    processed = 0
    
    for kode in tickers:
        try:
            # Ambil data harga
            price_data = fetch_price_data(kode, start, end)
            if price_data is None or price_data.empty or len(price_data) < 100:
                continue

            # Hitung return dan volume
            harga_awal = price_data['Close'].iloc[0]
            harga_akhir = price_data['Close'].iloc[-1]
            ret = (harga_akhir / harga_awal)
            avg_vol = price_data['Volume'].mean()

            # Ambil data fundamental untuk saham ini
            f_row = fundamental[fundamental['Kode'] == kode].iloc[0]
            
            # Konversi ke float dengan penanganan error
            metrics = {
                'EPS': float(f_row['EPS']),
                'ROE': float(f_row['ROE']),
                'DER': float(f_row['DER']),
                'PER': float(f_row['PER']),
                'PBV': float(f_row['PBV']),
                'PEG': float(f_row['PEG']),
                'NPM': float(f_row['NPM']),
                'RevenueGrowth': float(f_row['RevenueGrowth'])
            }

            # Validasi kriteria screening
            if (ret >= min_return and 
                avg_vol >= min_volume and
                metrics['EPS'] > 0 and
                metrics['ROE'] > 10 and
                metrics['DER'] < 1 and
                metrics['PER'] < 15 and
                metrics['PBV'] < 3 and
                metrics['PEG'] < 1 and
                metrics['NPM'] > 10):
                
                result = {
                    'Kode': kode,
                    'Harga Awal': round(harga_awal, 2),
                    'Harga Akhir': round(harga_akhir, 2),
                    'Return (x)': round(ret, 2),
                    'Volume Rata2': f"{avg_vol:,.0f}",
                    **metrics
                }
                results.append(result)
                processed += 1
                
        except IndexError:
            print(f"⚠️ Data fundamental tidak ditemukan untuk {kode}")
            continue
        except ValueError as e:
            print(f"⚠️ Nilai tidak valid untuk {kode}: {str(e)}")
            continue
        except Exception as e:
            print(f"⚠️ Error memproses {kode}: {str(e)}")
            continue

    print(f"✅ Screening selesai. Saham yang memenuhi kriteria: {len(results)} dari {processed} yang diproses")
    return pd.DataFrame(results)

def calculate_score(row):
    """
    Menghitung skor saham berdasarkan bobot tertentu
    """
    try:
        return round(
            row['Return (x)'] * 0.4 +
            row['ROE'] * 0.2 +
            row['RevenueGrowth'] * 0.2 -
            row['DER'] * 0.2, 2
        )
    except Exception as e:
        print(f"⚠️ Gagal menghitung skor untuk {row.get('Kode', 'Unknown')}: {str(e)}")
        return 0

if __name__ == "__main__":
    # Contoh penggunaan untuk testing
    print("Testing screener module...")
    saham_list = load_saham_list()
    print(f"Daftar saham yang dimuat ({len(saham_list)} tickers):", saham_list[:5])
    
    if saham_list:
        test_result = screening(
            tickers=saham_list[:10],  # Test 10 saham pertama saja
            start="2022-01-01",
            end="2023-01-01",
            min_return=1.5,
            min_volume=100000
        )
        print("\nHasil testing:")
        print(test_result)
