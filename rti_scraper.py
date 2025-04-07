import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_rti_stock_data(ticker):
    url = f"https://www.rti.co.id/stock/detail/{ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        fundamentals = {"Kode": ticker}

        rows = soup.select(".rt_table tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].text.strip()
                val = cols[1].text.strip().replace(",", "").replace("%", "")
                fundamentals[key] = val

        return {
            "Kode": fundamentals["Kode"],
            "EPS": float(fundamentals.get("EPS", 0)),
            "ROE": float(fundamentals.get("ROE", 0)),
            "DER": float(fundamentals.get("Debt to Equity", 0)),
            "PER": float(fundamentals.get("P/E Ratio", 0)),
            "PBV": float(fundamentals.get("P/BV", 0)),
            "PEG": float(fundamentals.get("PEG Ratio", 0)),
            "NPM": float(fundamentals.get("Net Profit Margin", 0)),
            "RevenueGrowth": float(fundamentals.get("Revenue Growth", 0))
        }
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        return None

def scrape_multiple(tickers):
    results = []
    for ticker in tickers:
        print(f"📡 Scraping {ticker}...")
        data = scrape_rti_stock_data(ticker)
        if data:
            results.append(data)
        time.sleep(1.5)
    return pd.DataFrame(results)
