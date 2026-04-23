#!/usr/bin/env python3
"""根据 PPT 页面标题中的 FAI 标识替换指标文本并插入图表。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
from pptx import Presentation
from pptx.util import Inches


FAI_PATTERN = re.compile(r"\bFAI\s*\d+\b", re.IGNORECASE)


PLACEHOLDER_MAP = {
    "{{CPK}}": "cpk",
    "{{PPK}}": "ppk",
    "{{MEAN}}": "mean",
    "{{STD}}": "std",
    "{{N}}": "n",
    "{{PART_NO}}": "part_no",
}


def normalize_fai(fai_text: str) -> str:
    m = FAI_PATTERN.search(fai_text or "")
    if not m:
        return ""
    # 统一格式: FAI 1
    raw = m.group(0).upper().replace("  ", " ").strip()
    raw = re.sub(r"\s+", " ", raw)
    if raw.startswith("FAI") and len(raw.split()) == 1:
        return raw
    parts = raw.split()
    return f"FAI {parts[-1]}"


def load_metrics(metrics_path: Path) -> dict[str, dict]:
    df = pd.read_csv(metrics_path)
    if "fai_id" not in df.columns:
        raise ValueError("metrics.csv 缺少 fai_id 列")

    bucket: dict[str, dict] = {}
    for _, row in df.iterrows():
        fai_id = normalize_fai(str(row["fai_id"]))
        if not fai_id:
            continue
        bucket[fai_id] = row.to_dict()
    return bucket


def extract_slide_title_text(slide) -> str:
    # 优先使用 title 占位符
    if slide.shapes.title and hasattr(slide.shapes.title, "text"):
        return slide.shapes.title.text or ""

    # 兜底：取最上方文本框
    text_shapes = [
        s for s in slide.shapes if getattr(s, "has_text_frame", False) and s.text.strip()
    ]
    if not text_shapes:
        return ""

    top_shape = sorted(text_shapes, key=lambda s: s.top)[0]
    return top_shape.text


def replace_text_placeholders(slide, data: dict) -> None:
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue

        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                original = run.text
                new_text = original
                for placeholder, key in PLACEHOLDER_MAP.items():
                    if placeholder in new_text:
                        value = data.get(key, "")
                        if isinstance(value, float):
                            value = f"{value:.4f}"
                        new_text = new_text.replace(placeholder, str(value))
                run.text = new_text


def add_chart_image(slide, charts_dir: Path, fai_id: str) -> None:
    image_name = fai_id.replace(" ", "_") + ".png"
    image_path = charts_dir / image_name
    if not image_path.exists():
        return

    # 简单默认布局：右侧区域插图
    left = Inches(6.0)
    top = Inches(1.4)
    width = Inches(6.8)
    height = Inches(4.5)
    slide.shapes.add_picture(str(image_path), left, top, width=width, height=height)


def update_ppt(template: Path, metrics: Path, charts_dir: Path, output: Path) -> None:
    metric_map = load_metrics(metrics)
    prs = Presentation(str(template))

    for slide in prs.slides:
        title_text = extract_slide_title_text(slide)
        fai_id = normalize_fai(title_text)
        if not fai_id:
            continue

        row = metric_map.get(fai_id)
        if not row:
            continue

        replace_text_placeholders(slide, row)
        add_chart_image(slide, charts_dir, fai_id)

    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update PPT from JMP metrics and charts")
    parser.add_argument("--template", required=True, type=Path, help="PPT 模板路径")
    parser.add_argument("--metrics", required=True, type=Path, help="metrics.csv 路径")
    parser.add_argument("--charts", required=True, type=Path, help="图表目录")
    parser.add_argument("--output", required=True, type=Path, help="输出 PPT 路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    update_ppt(args.template, args.metrics, args.charts, args.output)
    print(f"PPT generated: {args.output}")


if __name__ == "__main__":
    main()
