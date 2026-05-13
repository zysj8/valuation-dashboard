import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# 全分类数据（固定兜底，无爬虫，不会报错）
index_list = [
    {"category": "宽基指数", "name": "上证50", "etf": "510050", "lof": "001051", "lt": 63.90},
    {"category": "宽基指数", "name": "创业板指数", "etf": "159915", "lof": "110026", "lt": 66.00},
    {"category": "宽基指数", "name": "沪深300", "etf": "510300", "lof": "160706", "lt": 74.50},
    {"category": "宽基指数", "name": "中证1000", "etf": "512100", "lof": "-", "lt": 80.10},
    {"category": "宽基指数", "name": "中证500", "etf": "510500", "lof": "160119", "lt": 85.00},
    {"category": "宽基指数", "name": "中证全指", "etf": "-", "lof": "-", "lt": 86.50},
    {"category": "策略指数", "name": "基本面50", "etf": "160716", "lof": "160716", "lt": 61.00},
    {"category": "策略指数", "name": "中证红利", "etf": "515890", "lof": "100032", "lt": 61.70},
    {"category": "策略指数", "name": "深证红利", "etf": "159905", "lof": "481012", "lt": 70.80},
    {"category": "策略指数", "name": "500SNLV", "etf": "-", "lof": "003318", "lt": 73.10},
    {"category": "策略指数", "name": "基本面60", "etf": "159916", "lof": "530015", "lt": 73.40},
    {"category": "策略指数", "name": "红利指数", "etf": "510880", "lof": "-", "lt": 76.40},
    {"category": "策略指数", "name": "基本面120", "etf": "159910", "lof": "070023", "lt": 79.80},
    {"category": "境外指数", "name": "标普500", "etf": "513500", "lof": "050025", "lt": 93.00},
    {"category": "境外指数", "name": "纳斯达克100", "etf": "513100", "lof": "160213", "lt": 93.60},
    {"category": "境外指数", "name": "英国富时100", "etf": "-", "lof": "-", "lt": 78.50},
    {"category": "境外指数", "name": "德国DAX", "etf": "513030", "lof": "000614", "lt": 61.00},
    {"category": "境外指数", "name": "法国CAC40", "etf": "-", "lof": "-", "lt": 75.20},
    {"category": "境外指数", "name": "日经225", "etf": "513520", "lof": "000605", "lt": 93.20},
    {"category": "境外指数", "name": "国企指数", "etf": "510900", "lof": "110031", "lt": 76.10},
    {"category": "境外指数", "name": "恒生指数", "etf": "159920", "lof": "164705", "lt": 86.10},
    {"category": "境外指数", "name": "恒生科技", "etf": "513130", "lof": "014425", "lt": 68.50},
    {"category": "行业指数", "name": "中国互联网", "etf": "164906", "lof": "164906", "lt": 6.20},
    {"category": "行业指数", "name": "中国互联网50", "etf": "513050", "lof": "006327", "lt": 7.70},
    {"category": "行业指数", "name": "证券公司", "etf": "512000", "lof": "004069", "lt": 18.60},
    {"category": "商品指数", "name": "AUL9", "etf": "518880", "lof": "000216", "lt": 97.50},
    {"category": "债券指数", "name": "10年国债", "etf": "511260", "lof": "-", "lt": 93.90},
    {"category": "债券指数", "name": "转债ETF", "etf": "511380", "lof": "-", "lt": 99.40},
]

# 生成网页
if not os.path.exists("templates"):
    os.mkdir("templates")

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

html = template.render(
    time=datetime.now().strftime("%Y-%m-%d %H:%M"),
    rows=index_list
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 网页生成成功")
