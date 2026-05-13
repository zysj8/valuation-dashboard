<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>指数估值温度表</title>
<style>
/* 全局美化 */
body {
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    margin: 20px;
    background-color: #f0f2f5;
}
.container {
    max-width: 950px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.title {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
}
.time {
    text-align: center;
    color: #666;
    font-size: 14px;
    margin-bottom: 25px;
}

/* 表格美化 + 所有列居中 */
table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 25px;
}
th, td {
    padding: 14px 10px;
    text-align: center; /* 核心：所有列居中对齐 */
    border-bottom: 1px solid #eee;
    font-size: 16px;
}
/* 指数名称列单独左对齐 */
td:first-child {
    text-align: left;
    padding-left: 15px;
}
/* 表头样式 */
th {
    background-color: #f8f9fa;
    font-weight: bold;
    color: #333;
}
.cate-name {
    text-align: left;
    font-weight: bold;
    color: #333;
}

/* 温度色块（保持之前的统一宽度） */
td.temp-cell {
    width: 140px !important;
    padding: 6px !important;
}
.temp-block {
    display: inline-block;
    width: 130px !important;
    height: 32px !important;
    line-height: 32px;
    text-align: center;
    border-radius: 4px;
    color: white;
    font-weight: 500;
}
.blue { background-color: #007bff; }
.red { background-color: #dc3545; }

/* 基金代码颜色美化 */
td:nth-child(2) {
    color: #0066cc;
    font-weight: 500;
}
td:nth-child(3) {
    color: #333;
}

/* 图例美化 */
.legend {
    display: flex;
    justify-content: center;
    gap: 25px;
    margin-top: 30px;
    font-size: 15px;
    color: #555;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
}
.legend-color {
    width: 20px;
    height: 20px;
    border-radius: 4px;
}
</style>
</head>
<body>
<div class="container">
<div class="title">📈 指数估值温度表</div>
<div class="time">更新时间：{{ time }}</div>

{% set groups = {} %}
{% for r in rows %}
    {% if r.category not in groups %}
        {% set _ = groups.update({r.category: []}) %}
    {% endif %}
    {% set _ = groups[r.category].append(r) %}
{% endfor %}

{% for category, items in groups.items() %}
<table>
  <thead>
    <tr>
      <th class="cate-name">{{ category }}</th>
      <th>场内基金代码</th>
      <th>场外基金代码</th>
      <th>{% if category == '行业指数' %}PB温度{% else %}长投温度{% endif %}</th>
    </tr>
  </thead>
  <tbody>
  {% for item in items %}
    <tr>
      <td>{{ item.name }}</td>
      <td>{{ item.etf }}</td>
      <td>{{ item.lof }}</td>
      <td class="temp-cell">
          {% if item.type == 'pb' %}
              <div class="temp-block blue">{{ item.lt }}</div>
          {% else %}
              <div class="temp-block red">{{ item.lt }}</div>
          {% endif %}
      </td>
    </tr>
  {% endfor %}
  </tbody>
</table>
{% endfor %}

<div class="legend">
    <div class="legend-item"><div class="legend-color" style="background:#007bff;"></div><span>℃ ≤ 30</span></div>
    <div class="legend-item"><div class="legend-color" style="background:#ffc107;"></div><span>30 < ℃ ≤ 40</span></div>
    <div class="legend-item"><div class="legend-color" style="background:#fd7e14;"></div><span>40 < ℃ ≤ 50</span></div>
    <div class="legend-item"><div class="legend-color" style="background:#dc3545;"></div><span>℃ > 50</span></div>
</div>

</div>
</body>
</html>
