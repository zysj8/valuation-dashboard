<details> <summary>import akshare as ak
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime

# ---------- 1. 指数配置 ----------
INDEX_LIST = [
    # 宽基指数
    ("上证50", "000016", "510050", "001051", "pepb", False),
    ("创业板指数", "399006", "159915", "110026", "pepb", False),
    ("沪深300", "000300", "510300", "160706", "pepb", False),
    ("中证1000", "000852", "512100", "003646", "pepb", False),
    ("中证500", "000905", "510500", "160119", "pepb", False),
    ("中证全指", "000985", "159633", "", "pepb", False),

    # 策略指数
    ("基本面50", "000925", "160716", "160716", "pepb", False),
    ("中证红利", "000922", "515890", "100032", "pepb", False),
    ("深证红利", "399324", "159905", "481012", "pepb", False),
    ("500SNLV", "930782", "", "003318", "pepb", False),
    ("基本面60", "000968", "159916", "530015", "pepb", False),
    ("红利指数", "000015", "510880", "100032", "pepb", False),
    ("基本面120", "000970", "159910", "070023", "pepb", False),

    # 境外指数
    ("德国DAX", "GDAXI", "513030", "000614", "price_only", False),
    ("国企指数", "HSCEI", "510900", "110031", "price_only", False),
    ("恒生指数", "HSI", "159920", "164705", "price_only", False),
    ("标普500", "SPX", "513500", "050025", "price_only", False),
    ("日经225", "N225", "513520", "513520", "price_only", False),
    ("纳斯达克100", "NDX", "513300", "160213", "price_only", False),

    # 行业指数
    ("中国互联网", "H11136", "164906", "164906", "price_only", False),
    ("中国互联网50", "H30533", "513050", "006327", "price_only", False),
    ("证券公司", "399975", "512000", "004069", "pb_only", True),

    # 商品指数
    ("AUL9", "AU9999", "518880", "000216", "price_only", False),

    # 债券指数
    ("10年国债", "CGB10Y", "511260", "003358", "price_only", False),
    ("转债ETF", "CB_INDEX", "511380", "", "price_only", False),
]

def get_csindex_history(symbol, start_date="20150101"):
    try:
        df = ak.stock_zh_index_value_csindex(symbol=symbol, start_date=start_date, end_date=datetime.now().strftime("%Y%m%d"))
        if df.empty:
            return None
        df['日期'] = pd.to_datetime(df['日期'])
        df = df.sort_values('日期')
        df.rename(columns={'市盈率': 'pe', '市净率': 'pb'}, inplace=True)
        return df[['日期', 'pe', 'pb']]
    except Exception as e:
        print(f"获取指数 {symbol} 历史失败: {e}")
        return None

def get_latest_pepb_from_history(df):
    if df is None or len(df) < 30:
        return None, None, None, None
    latest = df.iloc[-1]
    pe = latest['pe']
    pb = latest['pb']
    pe_percentile = (df['pe'] <= pe).sum() / df['pe'].count() if pd.notna(pe) else None
    pb_percentile = (df['pb'] <= pb).sum() / df['pb'].count() if pd.notna(pb) else None
    return pe, pb, pe_percentile, pb_percentile

def get_etf_price_percentile(fund_code, start_date="20180101"):
    try:
        df = ak.fund_etf_hist_em(symbol=fund_code, period="daily", start_date=start_date, end_date=datetime.now().strftime("%Y%m%d"))
        if df.empty:
            return None, None
        df['日期'] = pd.to_datetime(df['日期'])
        df = df.sort_values('日期')
        close_prices = df['收盘']
        latest_price = close_prices.iloc[-1]
        percentile = (close_prices <= latest_price).sum() / len(close_prices)
        return latest_price, percentile
    except Exception as e:
        print(f"获取ETF {fund_code} 价格历史失败: {e}")
        return None, None

def get_pb_temp_for_399975():
    df = get_csindex_history("399975")
    if df is None:
        return None
    latest_pb = df['pb'].iloc[-1]
    pb_percentile = (df['pb'] <= latest_pb).sum() / df['pb'].count()
    return pb_percentile * 100

def main():
    results = []
    for name, idx_code, etf_code, off_code, data_type, is_pb_only in INDEX_LIST:
        print(f"处理 {name} ...")
        temp_value = None
        pb_temp_for_display = None

        if data_type == "pepb":
            hist = get_csindex_history(idx_code)
            if hist is not None:
                pe, pb, pe_per, pb_per = get_latest_pepb_from_history(hist)
                if pe_per is not None and pb_per is not None:
                    temp_value = (pe_per + pb_per) / 2 * 100
                    if is_pb_only:
                        pb_temp_for_display = pb_per * 100
        elif data_type == "pb_only":
            pb_temp = get_pb_temp_for_399975()
            if pb_temp is not None:
                temp_value = pb_temp
                pb_temp_for_display = pb_temp
        elif data_type == "price_only":
            fund_code = etf_code if etf_code else off_code
            if fund_code:
                price, percentile = get_etf_price_percentile(fund_code)
                if percentile is not None:
                    temp_value = percentile * 100

        results.append({
            "name": name,
            "etf_code": etf_code,
            "off_code": off_code,
            "temperature": round(temp_value, 1) if temp_value is not None else None,
            "pb_temp": round(pb_temp_for_display, 1) if pb_temp_for_display is not None else None,
            "category": get_category(name)
        })
        time.sleep(0.5)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("数据采集完成，已保存至 data.json")

def get_category(name):
    if name in ["上证50","创业板指数","沪深300","中证1000","中证500","中证全指"]:
        return "宽基指数"
    elif name in ["基本面50","中证红利","深证红利","500SNLV","基本面60","红利指数","基本面120"]:
        return "策略指数"
    elif name in ["德国DAX","国企指数","恒生指数","标普500","日经225","纳斯达克100"]:
        return "境外指数"
    elif name in ["中国互联网","中国互联网50","证券公司"]:
        return "行业指数"
    elif name == "AUL9":
        return "商品指数"
    elif name in ["10年国债","转债ETF"]:
        return "债券指数"
    else:
        return "其他"

if __name__ == "__main__":
    main()</summary></details>
