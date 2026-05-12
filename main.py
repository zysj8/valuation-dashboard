import akshare as ak
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

# 确保模板目录存在
if not os.path.exists("templates"):
    os.makedirs("templates")

# ---------------------- 指数列表（补齐所有基金代码） ----------------------
index_list = [
    {"category": "宽基指数", "name": "上证50", "code": "000016", "etf": "510050", "lof": "001051"},
    {"category": "宽基指数", "name": "沪深300", "code": "000300", "etf": "510300", "lof": "160706"},
    {"category": "宽基指数", "name": "中证500", "code": "000905", "etf": "510500", "lof": "160119"},
    {"category": "宽基指数", "name": "中证1000", "code": "000852", "etf": "512100", "lof": "004689"},
    {"category": "宽基指数", "name": "创业板指", "code": "399006", "etf": "159915", "lof": "110026"},
    {"category": "宽基指数", "name": "科创50", "code": "000688", "etf": "588000", "lof": "011614"},

    {"category": "策略指数", "name": "中证红利", "code": "000922", "etf": "515890", "lof": "100032"},
    {"category": "策略指数", "name": "深证红利", "code": "399324", "etf": "159905", "lof": "481012"},
    {"category": "策略指数", "name": "基本面50", "code": "000925", "etf": "160716", "lof": "160716"},

    {"category": "境外指数", "name": "恒生指数", "code": "HSI", "etf": "159920", "lof": "164705"},
    {"category": "境外指数", "name": "恒生科技", "code": "HSI", "etf": "513130", "lof": "014425"},
    {"category": "境外指数", "name": "纳斯达克100", "code": "NDX", "etf": "513100", "lof": "160213"},
    {"category": "境外指数", "name": "标普500", "code": "SPX", "etf": "513500", "lof": "050025"},

    {"category": "行业指数", "name": "证券公司", "code": "399975", "etf": "512000", "lof": "004069"},
    {"category": "行业指数", "name": "中证医疗", "code": "399989", "etf": "512170", "lof": "005056"},
    {"category": "行业指数", "name": "中证消费", "code": "000932", "etf": "159928", "lof": "000248"},
    {"category": "行业指数", "name": "中证新能源", "code": "399808", "etf": "516850", "lof": "012769"},

    {"category": "债券&商品", "name": "国债10年", "code": "000012", "etf": "511260", "lof": "-"},
    {"category": "债券&商品", "name": "黄金", "code": "AU9999", "etf": "518880", "lof": "000216"},
]

# ---------------------- 获取估值 ----------------------
def get_valuation(code):
    try:
        df = ak.stock_zh_index_valuation(symbol=code)
        pe_pct = df["pe_percentile"].iloc[-1] * 100
        pb_pct = df["pb_percentile"].iloc[-1] * 100
        long_temp = (pe_pct + pb_pct) / 2
        return round(long_temp, 1), round(pb_pct, 1)
    except:
        return "-", "-"

# ---------------------- 组装数据 ----------------------
rows = []
for idx in index_list:
    lt, pbt = get_valuation(idx["code"])
    rows.append({
        "c": idx["category"],
        "name": idx["name"],
        "etf": idx["etf"],
        "lof": idx["lof"],
        "lt": lt,
        "pbt": pbt
    })

# ---------------------- 生成HTML ----------------------
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

html = template.render(
    time=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
    rows=rows
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 生成完成")
