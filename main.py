import requests
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import time

# ====================== 配置 ======================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 你要监控的指数列表（可自由增删）
INDEX_LIST = [
    {"name": "上证50", "code": "000016"},
    {"name": "沪深300", "code": "000300"},
    {"name": "中证500", "code": "000905"},
    {"name": "中证1000", "code": "000852"},
    {"name": "创业板指", "code": "399006"},
    {"name": "中证红利", "code": "000922"},
    {"name": "证券公司", "code": "399975"},
    {"name": "恒生指数", "code": "HSI"},
    {"name": "恒生科技", "code": "HSTECH"},
    {"name": "标普500", "code": "SPX"},
    {"name": "纳斯达克100", "code": "NDX"},
    {"name": "日经225", "code": "N225"},
    {"name": "德国DAX", "code": "DAX"},
    {"name": "英国富时100", "code": "FTSE"},
    {"name": "法国CAC40", "code": "CAC"},
]

# 基金代码映射（稳定版，爬虫补充不到的用这个兜底）
FUND_MAP = {
    "上证50": {"etf": "510050", "lof": "001051"},
    "沪深300": {"etf": "510300", "lof": "160706"},
    "中证500": {"etf": "510500", "lof": "160119"},
    "中证1000": {"etf": "512100", "lof": "-"},
    "创业板指": {"etf": "159915", "lof": "110026"},
    "中证红利": {"etf": "515890", "lof": "100032"},
    "证券公司": {"etf": "512000", "lof": "004069"},
    "恒生指数": {"etf": "159920", "lof": "164705"},
    "恒生科技": {"etf": "513130", "lof": "014425"},
    "标普500": {"etf": "513500", "lof": "050025"},
    "纳斯达克100": {"etf": "513100", "lof": "160213"},
    "日经225": {"etf": "513520", "lof": "000605"},
    "德国DAX": {"etf": "513030", "lof": "000614"},
}

# ====================== 蛋卷基金爬虫 ======================
def get_index_valuation(index_code):
    try:
        url = f"https://danjuanapp.com/djapi/index_eva/dj/{index_code}"
        res = requests.get(url, headers=HEADERS, timeout=8)
        data = res.json()

        pe = round(float(data["data"]["pe"]), 2)
        pb = round(float(data["data"]["pb"]), 2)
        pe_percent = round(float(data["data"]["pe_percent"]), 2)
        pb_percent = round(float(data["data"]["pb_percent"]), 2)

        # 指数温度公式（(PE百分位 + PB百分位) / 2）
        temp = round((pe_percent + pb_percent) / 2, 2)
        return pe, pb, pe_percent, pb_percent, temp

    except:
        return None, None, None, None, None

# ====================== 主程序 ======================
if __name__ == "__main__":
    index_data = []

    for idx in INDEX_LIST:
        name = idx["name"]
        code = idx["code"]

        print(f"正在爬取：{name}")
        pe, pb, pe_pct, pb_pct, temp = get_index_valuation(code)
        time.sleep(0.5)

        # 基金代码
        etf = FUND_MAP.get(name, {}).get("etf", "-")
        lof = FUND_MAP.get(name, {}).get("lof", "-")

        # 行业指数使用PB温度
        type_ = "pb" if name in ["证券公司", "恒生科技", "中国互联网"] else "long"

        index_data.append({
            "category": "境外指数" if name in ["标普500","纳斯达克100","日经225","德国DAX","英国富时100","法国CAC40","恒生指数","恒生科技"] 
            else "行业指数" if type_ == "pb" 
            else "宽基指数",
            "name": name,
            "etf": etf,
            "lof": lof,
            "lt": temp if temp else 0.00,
            "type": type_
        })

    # ====================== 生成网页 ======================
    if not os.path.exists("templates"):
        os.makedirs("templates")

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")

    html = template.render(
        time=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        rows=index_data
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ 爬取完成！指数温度已自动更新")
