# JMP JSL 自动报告系统协作说明

如果平台暂时无法上传原始文件（数据、脚本、PPT 模板），可以先按下面方式协作，我可以继续帮你完成开发与排错。

## 1) 先提供最小可复现内容（可直接粘贴到聊天）

- `main.jsl`：主流程脚本（可分多段粘贴）。
- `update_ppt.py`：至少包含 `update_ppt_all(...)`。
- 样例数据：CSV 前 20~50 行（脱敏即可）。
- 报错信息：完整堆栈，不要只截一行。

## 2) 建议的项目结构

```text
project/
  main.jsl
  update_ppt.py
  templates/
    report_template.pptx
  data/
    sample_data.csv
    sample_tolerance.csv
  output/
```

## 3) 数据脱敏建议

- 保留列名与数据类型，数值可做随机扰动（结构不变）。
- 客户名/料号可替换为 `C001`、`P001`。
- 只保留能复现问题的最小数据量。

## 4) 为了实现“标题匹配内容”请补充规则

请给出以下规则之一：

- 页面标题格式（例如：`FAI 1`、`FAI-2`、`FAI_03`）。
- 图片占位符识别方式（shape name / alt text / 固定坐标）。
- 文本占位符格式（例如：`{{cpk}}`、`{{ppk}}`、`{{mean}}`）。

## 5) 你可以直接复制这段模板来发我

```text
【main.jsl 片段】
...

【update_ppt.py 片段】
...

【报错全文】
...

【样例数据（CSV）】
col1,col2,...
...
```

拿到以上内容后，就可以继续做：

1. JSL 自动读取数据并计算 CPK/PPK。
2. JSL 导出图表与统计 JSON。
3. Python 按 PPT 标题（如 FAI 1）匹配并回填图片+数值。
4. 自动输出完整报告 PPT。
