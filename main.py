import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

if not os.path.exists("templates"):
    os.makedirs("templates")

index_list = [
    # 宽基指数
    {"category":"宽基指数","name":"上证50","etf":"510050","lof":"001051","lt":28.5},
    {"category":"宽基指数","name":"沪深300","etf":"510300","lof":"160706","lt":35.2},
    {"category":"宽基指数","name":"中证500","etf":"510500","lof":"160119","lt":42.8},
    {"category":"宽基指数","name":"中证1000","etf":"512100","lof":"004689","lt":55.6},
    {"category":"宽基指数","name":"创业板指","etf":"159915","lof":"110026","lt":48.3},
    {"category":"宽基指数","name":"中证全指","etf":"-","lof":"-","lt":39.7},
    {"category":"宽基指数","name":"科创50","etf":"588000","lof":"011614","lt":52.1},

    # 策略指数
    {"category":"策略指数","name":"中证红利","etf":"515890","lof":"100032","lt":22.4},
    {"category":"策略指数","name":"深证红利","etf":"159905","lof":"481012","lt":25.8},
    {"category":"策略指数","name":"基本面50","etf":"160716","lof":"160716","lt":31.6},
    {"category":"策略指数","name":"基本面60","etf":"159916","lof":"530015","lt":33.9},
    {"category":"策略指数","name":"基本面120","etf":"159910","lof":"070023","lt":36.5},
    {"category":"策略指数","name":"500低波","etf":"-","lof":"003318","lt":29.2},

    # 境外指数
    {"category":"境外指数","name":"恒生指数","etf":"159920","lof":"164705","lt":62.3},
    {"category":"境外指数","name":"恒生国企","etf":"510900","lof":"110031","lt":58.7},
    {"category":"境外指数","name":"恒生科技","etf":"513130","lof":"014425","lt":68.5},
    {"category":"境外指数","name":"标普500","etf":"513500","lof":"050025","lt":72.1},
    {"category":"境外指数","name":"纳斯达克100","etf":"513100","lof":"160213","lt":75.4},
    {"category":"境外指数","name":"日经225","etf":"513520","lof":"000605","lt":45.6},
    {"category":"境外指数","name":"德国DAX","etf":"513030","lof":"000614","lt":41.2},

    # 行业指数
    {"category":"行业指数","name":"证券公司","etf":"512000","lof":"004069","lt":19.8},
    {"category":"行业指数","name":"中证消费","etf":"159928","lof":"000248","lt":66.7},
    {"category":"行业指数","name":"中证医疗","etf":"512170","lof":"005056","lt":26.3},
    {"category":"行业指数","name":"中证新能源","etf":"516850","lof":"012769","lt":49.5},
    {"category":"行业指数","name":"中国互联网","etf":"164906","lof":"164906","lt":59.4},
    {"category":"行业指数","name":"互联网50","etf":"513050","lof":"006327","lt":61.8},

    # 商品&债券
    {"category":"商品&债券","name":"黄金","etf":"518880","lof":"000216","lt":44.2},
    {"category":"商品&债券","name":"10年国债","etf":"511260","lof":"-","lt":30.1},
    {"category":"商品&债券","name":"可转债","etf":"511380","lof":"-","lt":38.6},
]

rows = index_list

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

html = template.render(
    time=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
    rows=rows
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 完整指数估值表生成完毕")
