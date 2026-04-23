# JMP JSL + Python 自动报告系统

本仓库提供一个可落地的自动报告流程，用于：

1. 从数据源读取测量数据；
2. 使用 JMP（JSL）完成统计分析（均值、标准差、CPK、PPK 等）；
3. 自动导出图表和分析结果；
4. 通过 JSL 调用 Python，将结果回填到 PPT 模板（图片与数值）；
5. 根据 PPT 页面标题中的标识（例如 `FAI 1`）自动匹配对应分析内容；
6. 生成最终报告 `final_report.pptx`。

---

## 目录结构

- `jsl/auto_report.jsl`：JSL 主流程（数据读取、统计、导出、调用 Python）
- `python/ppt_updater.py`：PPT 更新脚本（按页面标识匹配并替换）
- `templates/mapping_example.json`：页面标识与变量映射示例
- `output/`：默认输出目录（图表、CSV、最终 PPT）

---

## 前置环境

### JMP

- JMP 16+（推荐）
- 支持运行 JSL

### Python

建议 Python 3.10+，安装依赖：

```bash
pip install python-pptx pandas pillow
```

---

## 数据格式建议

输入数据（CSV）至少包含以下列：

- `fai_id`：分析标识（如 `FAI 1`）
- `part_no`：零件/项目编号
- `measure_value`：测量值
- `lsl`：规格下限
- `usl`：规格上限

示例：

```csv
fai_id,part_no,measure_value,lsl,usl
FAI 1,A1001,10.02,9.8,10.2
FAI 1,A1001,10.11,9.8,10.2
FAI 2,B2001,5.03,4.9,5.1
```

---

## 使用步骤

1. 准备数据文件（例如 `data/source_data.csv`）。
2. 准备 PPT 模板（例如 `templates/report_template.pptx`），并在每页标题包含类似 `FAI 1` 的标识。
3. 打开并运行 `jsl/auto_report.jsl`，按实际路径修改顶部参数。
4. JSL 会输出：
   - `output/metrics.csv`（统计结果，含 CPK/PPK）
   - `output/charts/<FAI_ID>.png`（每个分析项图表）
   - `output/final_report.pptx`（最终报告）

---

## 匹配规则说明

`ppt_updater.py` 会读取每页标题文本：

- 若检测到标题包含 `FAI 1`，就从 `metrics.csv` 中提取 `fai_id == FAI 1` 的结果；
- 将 `{{CPK}}`、`{{PPK}}` 等占位符替换为实际数值；
- 将标题对应图表（如 `output/charts/FAI_1.png`）插入到页内。

> 建议在模板中统一使用占位符：`{{CPK}}`、`{{PPK}}`、`{{MEAN}}`、`{{STD}}`。

---

## 可扩展方向

- 接入数据库（Oracle/SQL Server/PostgreSQL）替代 CSV；
- 增加 Western Electric 规则、控制图自动判异；
- 通过配置文件控制每页图表布局与替换区域；
- 结合 CI 定时生成日报/周报。

