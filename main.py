import requests
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

INDEX_LIST = [
    # 宽基指数
    {"name": "上证50", "code": "000016", "category": "宽基指数"},
    {"name": "沪深300", "code": "000300", "category": "宽基指数"},
    {"name": "中证500", "code": "000905", "category": "宽基指数"},
    {"name": "中证1000", "code": "000852", "category": "宽基指数"},
    {"name": "创业板指数", "code": "399006", "category": "宽基指数"},
    {"name": "中证全指", "code": "000985", "category": "宽基指数"},

    # 策略指数
    {"name": "基本面50", "code": "000025", "category": "策略指数"},
    {"name": "中证红利", "code": "000922", "category": "策略指数"},
    {"name": "深证红利", "code": "399324", "category": "策略指数"},
    {"name": "红利指数", "code": "000015", "category": "策略指数"},
    {"name": "基本面60", "code": "399701", "category": "策略指数"},
    {"name": "基本面120", "code": "399702", "category": "策略指数"},

    # 行业指数
    {"name": "中国互联网", "code": "HSIII", "category": "行业指数"},
    {"name": "中国互联网50", "code": "H30533", "category": "行业指数"},
    {"name": "证券公司", "code": "399975", "category": "行业指数"},

    # 境外指数
    {"name": "标普500", "code": "SPX", "category": "境外指数"},
    {"name": "纳斯达克100", "code": "NDX", "category": "境外指数"},
    {"name": "英国富时100", "code": "FTSE", "category": "境外指数"},
    {"name": "德国DAX", "code": "DAX", "category": "境外指数"},
    {"name": "法国CAC40", "code": "CAC", "category": "境外指数"},
    {"name": "日经225", "code": "N225", "category": "境外指数"},
    {"name": "国企指数", "code": "HSCEI", "category": "境外指数"},
    {"name": "恒生指数", "code": "HSI", "category": "境外指数"},
    {"name": "恒生科技", "code": "HSTECH", "category": "境外指数"},

    # 商品指数
    {"name": "AUL9", "code": "AU9999", "category": "商品指数"},

    # 债券指数
    {"name": "10年国债", "code": "000012", "category": "债券指数"},
    {"name": "转债ETF", "code": "399596", "category": "债券指数"},
]

FUND_MAP = {
    "上证50": {"etf": "510050", "lof": "001051"},
    "沪深300": {"etf": "510300", "lof": "160706"},
    "中证500": {"etf": "510500", "lof": "160119"},
    "中证1000": {"etf": "512100", "lof": "-"},
    "创业板指数": {"etf": "159915", "lof": "110026"},
    "中证全指": {"etf": "-", "lof": "-"},
    "基本面50": {"etf": "160716", "lof": "160716"},
    "中证红利": {"etf": "515890", "lof": "100032"},
    "深证红利": {"etf": "159905", "lof": "481012"},
    "红利指数": {"etf": "510880", "lof": "-"},
    "基本面60": {"etf": "159916", "lof": "530015"},
    "基本面120": {"etf": "159910", "lof": "070023"},
    "中国互联网": {"etf": "164906", "lof": "164906"},
    "中国互联网50": {"etf": "513050", "lof": "006327"},
    "证券公司": {"etf": "512000", "lof": "004069"},
    "标普500": {"etf": "513500", "lof": "050025"},
    "纳斯达克100": {"etf": "513100", "lof": "160213"},
    "英国富时100": {"etf": "-", "lof": "-"},
    "德国DAX": {"etf": "513030", "lof": "000614"},
    "法国CAC40": {"etf": "-", "lof": "-"},
    "日经225": {"etf": "513520", "lof": "000605"},
    "国企指数": {"etf": "510900", "lof": "110031"},
    "恒生指数": {"etf": "159920", "lof": "164705"},
    "恒生科技": {"etf": "513130", "lof": "014425"},
    "AUL9": {"etf": "518880", "lof": "000216"},
    "10年国债": {"etf": "511260", "lof": "-"},
    "转债ETF": {"etf": "511380", "lof": "-"},
}

def get_valuation(code):
    try:
        url = f"https://danjuanapp.com/djapi/index_eva/dj/{code}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        data = res.json()["data"]
        pe_pct = float(data["pe_percent"])
        pb_pct = float(data["pb_percent"])
        return round((pe_pct + pb_pct) / 2, 2)
    except:
        return None

if __name__ == "__main__":
    rows = []
    for idx in INDEX_LIST:
        name = idx["name"]
        cate = idx["category"]
        temp = get_valuation(idx["code"])
        time.sleep(0.5)

        if temp is None:
            fallback = {
                "中国互联网": 6.2, "中国互联网50": 7.7, "证券公司": 18.6,
                "标普500": 93.0, "纳斯达克100": 93.6, "德国DAX": 61.0,
                "日经225": 93.2, "恒生指数": 86.1, "恒生科技": 68.5, "国企指数": 76.1,
                "AUL9": 97.5, "10年国债": 93.9, "转债ETF": 99.4
            }
            temp = fallback.get(name, 50.0)

        rows.append({
            "category": cate,
            "name": name,
            "etf": FUND_MAP[name]["etf"],
            "lof": FUND_MAP[name]["lof"],
            "lt": temp,
            "type": "pb" if cate == "行业指数" else "long"
        })

    env = Environment(loader=FileSystemLoader("templates"))
    html = env.get_template("index.html").render(
        time=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        rows=rows
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
