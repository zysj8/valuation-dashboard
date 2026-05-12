<details> <summary>import json
import os
import subprocess

def generate_html():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = ["宽基指数", "策略指数", "境外指数", "行业指数", "商品指数", "债券指数"]
    grouped = {cat: [] for cat in categories}
    for item in data:
        grouped[item["category"]].append(item)

    def temp_color(temp):
        if temp is None:
            return "#6c757d"
        if temp <= 30:
            return "#28a745"
        elif temp <= 50:
            return "#ffc107"
        else:
            return "#dc3545"

    rows_html = ""
    for cat in categories:
        if not grouped[cat]:
            continue
        rows_html += f'<tr class="category-header"><td colspan="4"><strong>{cat}</strong></td></tr>'
        for item in grouped[cat]:
            temp = item["temperature"]
            pb = item.get("pb_temp")
            temp_display = f"{temp}%" if temp is not None else "N/A"
            pb_display = f" (PB {pb}%)" if pb is not None else ""
            color = temp_color(temp)
            rows_html += f"""
            <tr>
                <td>{item["name"]}</td>
                <td>{item["etf_code"] or "-"}</td>
                <td>{item["off_code"] or "-"}</td>
                <td style="background-color: {color}; color: white; font-weight: bold; text-align: center;">{temp_display}{pb_display}</td>
            </tr>
            """

    try:
        update_time = subprocess.check_output('date "+%Y-%m-%d %H:%M:%S"', shell=True).decode().strip()
    except:
        update_time = "刚刚"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>指数长投温度估值表 - 每日自动更新</title>
    <style>
        body {{ font-family: 'Segoe UI', Roboto, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: auto; background: white; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); overflow-x: auto; }}
        h1 {{ text-align: center; color: #1e2a3e; padding: 24px 0 8px; margin: 0; font-size: 1.8rem; }}
        .sub {{ text-align: center; color: #5a6e7c; font-size: 0.85rem; margin-bottom: 20px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th, td {{ padding: 12px 10px; text-align: left; border-bottom: 1px solid #e9ecef; }}
        th {{ background-color: #eef2f5; font-weight: 600; color: #1e466e; }}
        .category-header td {{ background-color: #d9e2ec; font-weight: bold; color: #0f2b3d; border-bottom: 2px solid #bdd4e2; padding: 8px 10px; }}
        tr:hover {{ background-color: #f8fafc; }}
        footer {{ text-align: center; font-size: 12px; color: #7f8c8d; padding: 20px; border-top: 1px solid #e2e8f0; }}
    </style>
</head>
<body>
<div class="container">
    <h1>📊 指数长投温度估值表</h1>
    <div class="sub">
        计算公式：长投温度 = (PE历史百分位 + PB历史百分位)/2 &nbsp;|&nbsp;
        绿色≤30℃ 黄色30~50℃ 红色≥50℃<br>
        数据每日自动更新 · 仅供参考
    </div>
    <table>
        <thead>
            <tr><th>指数名称</th><th>场内基金代码</th><th>场外基金代码</th><th>长投温度</th></tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    <footer>
        数据来源：AKShare 公开接口 & 沪深交易所ETF行情<br>
        最后更新: {update_time} (北京时间)
    </footer>
</div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML 生成成功: index.html")

if __name__ == "__main__":
    generate_html()</summary></details>
