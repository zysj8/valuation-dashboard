import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

if not os.path.exists("templates"):
    os.makedirs("templates")

# 测试用固定数据，直接写死温度，保证页面能显示
index_list = [
    {"category": "宽基指数", "name": "上证50", "etf": "510050", "lof": "001051", "lt": 63.9},
    {"category": "宽基指数", "name": "沪深300", "etf": "510300", "lof": "160706", "lt": 74.5},
    {"category": "宽基指数", "name": "中证500", "etf": "510500", "lof": "160119", "lt": 85.0},
    {"category": "宽基指数", "name": "中证1000", "etf": "512100", "lof": "004689", "lt": 80.1},
    {"category": "宽基指数", "name": "创业板指", "etf": "159915", "lof": "110026", "lt": 66.0},
    {"category": "宽基指数", "name": "科创50", "etf": "588000", "lof": "011614", "lt": 70.0},

    {"category": "策略指数", "name": "中证红利", "etf": "515890", "lof": "100032", "lt": 61.7},
    {"category": "策略指数", "name": "深证红利", "etf": "159905", "lof": "481012", "lt": 70.8},
    {"category": "策略指数", "name": "基本面50", "etf": "160716", "lof": "160716", "lt": 61.0},

    {"category": "行业指数", "name": "证券公司", "etf": "512000", "lof": "004069", "lt": 18.6},
    {"category": "行业指数", "name": "中证医疗", "etf": "512170", "lof": "005056", "lt": 45.0},
    {"category": "行业指数", "name": "中证消费", "etf": "159928", "lof": "000248", "lt": 75.0},
    {"category": "行业指数", "name": "中证新能源", "etf": "516850", "lof": "012769", "lt": 60.0},
]

# 直接用固定数据，不用akshare接口
rows = index_list

# 生成HTML
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

html = template.render(
    time=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
    rows=rows
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 测试数据生成完成，温度会正常显示！")
