#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RETECO Track 2 - Visualization Suite (v3)

Đọc eda_metrics_<domain>.json, sinh 6 biểu đồ PNG + 1 báo cáo Markdown.

Output: <reports-dir>/figures/*.png và <reports-dir>/visualization_report.md

Chạy:
    python 02_visualize_eda.py
    python 02_visualize_eda.py --include-sweep
    python 02_visualize_eda.py --reports-dir ../../reports/eda

Tham số:
    --reports-dir     Thư mục chứa eda_metrics_*.json (tự dò nếu bỏ trống)
    --output-dir      Thư mục xuất PNG (mặc định <reports-dir>/figures)
    --include-sweep   Hiện tất cả biến thể sweep trong heatmap

Changelog v3:
    - Thêm tên hiển thị cho 4d_Recursive_250, 5e_Adaptive_Hybrid
    - fig3 mở rộng 2x2: thêm Semantic Gain + Length-Bias check
    - Report Section 5 chuyển từ hard-code sang data-driven
    - [FIX-viz] Pie chart dùng palette động (không trùng màu khi >6 slice)
    - [FIX-viz] Panel D: legend không bị cột đè
    - [FIX-viz] Panel C: chấm scatter rõ hơn
    - [FIX-viz] Heatmap: colorbar + label không bị cắt (bbox_inches="tight")
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ép backend Agg để chạy headless an toàn trên mọi môi trường server/CLI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("RETECO_VISUALIZE")

# ---------------------------------------------------------------------------
# Cấu hình thẩm mỹ Matplotlib
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "figure.dpi": 200,
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 13,
    "font.family": "sans-serif",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--"
})

# ---- Danh sách 9 chiến lược chính (dùng cho bar chart, không có sweep) ----
PRIMARY_STRATEGIES = [
    "1_Fixed_Char",
    "2_Fixed_Word",
    "3_Sentence_Boundary",
    "4_Recursive_Markdown",
    "5_Semantic_Context_Injected",
    "6_Whole_Document",
    "7_Parent_Child",
    "8_Sentence_Window",
    "9_TextTiling_Semantic"
]

# ---- Tên hiển thị thân thiện ----
STRATEGY_DISPLAY_NAMES = {
    "1_Fixed_Char": "1. Fixed-Char",
    "2_Fixed_Word": "2. Fixed-Word",
    "3_Sentence_Boundary": "3. Sentence-Boundary",
    "4_Recursive_Markdown": "4. Recursive-Markdown",
    "5_Semantic_Context_Injected": "5. Semantic-Context",
    "6_Whole_Document": "6. Whole-Document",
    "7_Parent_Child": "7. Parent-Child",
    "8_Sentence_Window": "8. Sentence-Window",
    "9_TextTiling_Semantic": "9. TextTiling",
    # Sweep variants
    "1b_Fixed_Char_300": "1b. Char-300",
    "1c_Fixed_Char_900": "1c. Char-900",
    "3b_Sentence_80w": "3b. Sent-80w",
    "3c_Sentence_220w": "3c. Sent-220w",
    "4b_Recursive_450": "4b. Rec-450",
    "4c_Recursive_1000": "4c. Rec-1000",
    "4d_Recursive_250": "4d. Rec-250",
    "5b_Semantic_thr1200_max900": "5b. Sem-1200",
    "5c_Semantic_thr500_max400": "5c. Sem-500",
    "5d_Semantic_prefix_all": "5d. Sem-PrefAll",
    "5e_Adaptive_Hybrid": "5e. Adaptive-Hybrid",
    "8b_Sentence_Window_6_3": "8b. Window-6-3",
}

PALETTE = {
    "blue": "#1f77b4",
    "green": "#2ca02c",
    "red": "#d62728",
    "orange": "#ff7f0e",
    "purple": "#9467bd",
    "teal": "#17becf",
    "gray": "#7f7f7f",
    "dark": "#2b2b2b",
    "missing": "#e5e5e5",
    "neutral": "#b0b0b0",
}


# ===========================================================================
# 1. Tiện ích tính toán an toàn
# ===========================================================================
def safe_mean(values: List[float], default: float = 0.0) -> float:
    """Tính trung bình an toàn, tránh RuntimeWarning khi list rỗng."""
    valid = [v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    return float(np.mean(valid)) if valid else default


def safe_median(values: List[float], default: float = 0.0) -> float:
    valid = [v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    return float(np.median(valid)) if valid else default


def default_reports_dir() -> Path:
    """Tự động tìm thư mục reports/eda phù hợp theo layout dự án."""
    here = Path(__file__).resolve().parent
    cands = [
        here.parent / "reports" / "eda",
        here.parents[1] / "reports" / "eda" if len(here.parents) >= 2 else None,
        Path("reports/eda"),
        Path("../reports/eda")
    ]
    for c in cands:
        if c and c.is_dir() and list(c.glob("eda_metrics_*.json")):
            return c
    return here.parent / "reports" / "eda"


# ===========================================================================
# 2. Data Loader
# ===========================================================================
def load_all_metrics(reports_dir: Path) -> Dict[str, Dict[str, Any]]:
    metrics_by_domain = {}
    for f in sorted(reports_dir.glob("eda_metrics_*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            domain = data.get("domain")
            if domain:
                metrics_by_domain[domain] = data
        except Exception as e:
            logger.warning(f"Lỗi đọc file {f.name}: {e}")
    logger.info(f"Đã nạp thành công metrics của {len(metrics_by_domain)} domains từ {reports_dir}")
    return metrics_by_domain


# ===========================================================================
# 3. Plotting Functions
# ===========================================================================

def plot_corpus_profile(data: Dict[str, Dict[str, Any]], out_path: Path):
    """Fig 1: Quy mô & Phân bố độ dài tài liệu theo từng domain."""
    domains = sorted(data.keys())
    n_dom = len(domains)
    if n_dom == 0:
        return

    doc_counts = [data[d].get("document_statistics", {}).get("total_documents", 0) for d in domains]
    char_lens = [data[d].get("document_statistics", {}).get("char_length", {}) for d in domains]
    medians = [cl.get("median", 0) for cl in char_lens]
    p75s = [cl.get("p75", 0) for cl in char_lens]
    p90s = [cl.get("p90", 0) for cl in char_lens]

    fig, axes = plt.subplots(1, 2, figsize=(14, max(5.5, n_dom * 0.45)))

    y_pos = np.arange(n_dom)
    max_docs = max(doc_counts) if doc_counts else 1
    offset = max(100.0, max_docs * 0.02)

    # Panel A
    axes[0].barh(y_pos, doc_counts, color=PALETTE["blue"], alpha=0.85, edgecolor=PALETTE["dark"])
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels(domains, fontweight="bold")
    axes[0].invert_yaxis()
    axes[0].set_xlabel("Số lượng tài liệu (Documents)")
    axes[0].set_title(f"A. Quy mô Corpus ({n_dom} Domains)", fontweight="bold")
    for i, v in enumerate(doc_counts):
        axes[0].text(v + offset, i, f"{v:,}", va="center", fontsize=8.5, color=PALETTE["dark"])
    axes[0].set_xlim(0, max_docs * 1.18)

    # Panel B
    width = 0.25
    axes[1].barh(y_pos - width, medians, height=width, label="Median Length", color=PALETTE["teal"], alpha=0.85)
    axes[1].barh(y_pos, p75s, height=width, label="75th Percentile", color=PALETTE["orange"], alpha=0.85)
    axes[1].barh(y_pos + width, p90s, height=width, label="90th Percentile", color=PALETTE["red"], alpha=0.85)
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels(domains, fontweight="bold")
    axes[1].invert_yaxis()
    axes[1].set_xlabel("Độ dài ký tự (Characters)")
    axes[1].set_title("B. Phân bố độ dài tài liệu (Ký tự)", fontweight="bold")
    axes[1].legend(loc="lower right")

    plt.suptitle(f"RETECO Track 2 — Đặc trưng Corpus & Phân bố độ dài trên {n_dom} Domains",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Đã lưu biểu đồ: {out_path.name}")


def plot_chunking_integrity(data: Dict[str, Dict[str, Any]], out_path: Path):
    """Fig 2: Tỷ lệ lỗi ngữ nghĩa phá vỡ RAG giữa các chiến lược chính."""
    stats = {k: {"quality": [], "starts_mid": [], "ends_mid": [], "dangling": [], "heading": [], "expansion": []}
             for k in PRIMARY_STRATEGIES}

    for d, ddata in data.items():
        comp = ddata.get("chunking_comparison", {})
        for k in PRIMARY_STRATEGIES:
            if k in comp:
                c = comp[k]
                stats[k]["quality"].append(c.get("avg_quality_score"))
                stats[k]["starts_mid"].append(c.get("starts_mid_pct"))
                stats[k]["ends_mid"].append(c.get("ends_mid_pct"))
                stats[k]["dangling"].append(c.get("dangling_unresolved_pct"))
                stats[k]["heading"].append(c.get("trailing_heading_pct"))
                stats[k]["expansion"].append(c.get("expansion_ratio"))

    labels = [STRATEGY_DISPLAY_NAMES[k] for k in PRIMARY_STRATEGIES]
    avg_quality = [safe_mean(stats[k]["quality"]) for k in PRIMARY_STRATEGIES]
    avg_starts = [safe_mean(stats[k]["starts_mid"]) for k in PRIMARY_STRATEGIES]
    avg_ends = [safe_mean(stats[k]["ends_mid"]) for k in PRIMARY_STRATEGIES]
    avg_dangling = [safe_mean(stats[k]["dangling"]) for k in PRIMARY_STRATEGIES]
    avg_heading = [safe_mean(stats[k]["heading"]) for k in PRIMARY_STRATEGIES]
    avg_expansion = [safe_mean(stats[k]["expansion"], default=1.0) for k in PRIMARY_STRATEGIES]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    x = np.arange(len(labels))
    w = 0.2
    axes[0].bar(x - 1.5 * w, avg_starts, width=w, label="Đứt đầu câu (%)", color=PALETTE["red"], alpha=0.85)
    axes[0].bar(x - 0.5 * w, avg_ends, width=w, label="Đứt đuôi câu (%)", color=PALETTE["orange"], alpha=0.85)
    axes[0].bar(x + 0.5 * w, avg_dangling, width=w, label="Đại từ mồ côi unresolved (%)", color=PALETTE["purple"], alpha=0.85)
    axes[0].bar(x + 1.5 * w, avg_heading, width=w, label="Tiêu đề mồ côi (%)", color=PALETTE["teal"], alpha=0.85)

    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=35, ha="right", fontweight="bold")
    axes[0].set_ylabel("Tỷ lệ chunk mắc lỗi (%)")
    axes[0].set_title("A. Tỷ lệ lỗi ngữ nghĩa phá vỡ ngữ cảnh RAG (Thấp hơn là tốt hơn)", fontweight="bold")
    axes[0].legend(loc="upper right")

    ax2 = axes[1]
    ax2_twin = ax2.twinx()
    ax2.bar(x - 0.15, avg_quality, width=0.3, label="Điểm chất lượng (0-100)", color=PALETTE["green"], alpha=0.85)
    ax2_twin.plot(x + 0.15, avg_expansion, color=PALETTE["blue"], marker="o", linewidth=2.5,
                  label="Tỷ lệ nở Chunk (x lần)")

    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=35, ha="right", fontweight="bold")
    ax2.set_ylabel("Điểm chất lượng ngữ nghĩa (0 - 100)", color=PALETTE["green"], fontweight="bold")
    ax2_twin.set_ylabel("Hệ số nở tài liệu (Expansion Ratio)", color=PALETTE["blue"], fontweight="bold")
    ax2.set_title("B. Điểm chất lượng tổng thể vs Hệ số nở Index", fontweight="bold")
    ax2.set_ylim(max(0, min(avg_quality) - 10) if avg_quality else 50, 105)

    lines, l_labels = ax2.get_legend_handles_labels()
    lines2, l_labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines + lines2, l_labels + l_labels2, loc="lower left")

    plt.suptitle(f"Độ toàn vẹn ngữ nghĩa của 9 Chiến lược Chunking (Macro-Average {len(data)} Domains)",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Đã lưu biểu đồ: {out_path.name}")


def plot_retrieval_impact(data: Dict[str, Dict[str, Any]], out_path: Path):
    """Fig 3: Đo tác động retrieval với kiểm soát length bias (4 panel)."""
    labels = [STRATEGY_DISPLAY_NAMES[k] for k in PRIMARY_STRATEGIES]
    x = np.arange(len(labels))
    w = 0.35

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))

    # ---------- Panel [0,0]: nDCG@10 ----------
    ndcg_single = [safe_mean([data[d]["retrieval"][k]["ndcg10_single"]
                              for d in data if k in data[d].get("retrieval", {})]) for k in PRIMARY_STRATEGIES]
    ndcg_hist = [safe_mean([data[d]["retrieval"][k]["ndcg10_history"]
                            for d in data if k in data[d].get("retrieval", {})]) for k in PRIMARY_STRATEGIES]

    ax = axes[0, 0]
    ax.bar(x - w / 2, ndcg_single, width=w, label="Turn hiện tại (Single Query)", color=PALETTE["blue"], alpha=0.85)
    ax.bar(x + w / 2, ndcg_hist, width=w, label="+ Lịch sử hội thoại (+History)", color=PALETTE["green"], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontweight="bold")
    ax.set_ylabel("nDCG@10")
    ax.set_title("A. nDCG@10 — Single vs +History", fontweight="bold")
    ax.legend(loc="upper left")
    max_ndcg = max(ndcg_hist + ndcg_single) if (ndcg_hist + ndcg_single) else 0.5
    ax.set_ylim(0, max(0.1, max_ndcg * 1.25))
    for i in range(len(x)):
        if ndcg_single[i] > 0.001:
            gain = ((ndcg_hist[i] - ndcg_single[i]) / ndcg_single[i]) * 100
            ax.text(x[i], max(ndcg_single[i], ndcg_hist[i]) + 0.015, f"{gain:+.1f}%",
                    ha="center", fontsize=8, fontweight="bold",
                    color=PALETTE["green"] if gain >= 0 else PALETTE["red"])

    # ---------- Panel [0,1]: Recall@10 ----------
    rec_single = [safe_mean([data[d]["retrieval"][k]["recall10_single"]
                             for d in data if k in data[d].get("retrieval", {})]) for k in PRIMARY_STRATEGIES]
    rec_hist = [safe_mean([data[d]["retrieval"][k]["recall10_history"]
                           for d in data if k in data[d].get("retrieval", {})]) for k in PRIMARY_STRATEGIES]

    ax = axes[0, 1]
    ax.bar(x - w / 2, rec_single, width=w, label="Turn hiện tại (Single Query)", color=PALETTE["orange"], alpha=0.85)
    ax.bar(x + w / 2, rec_hist, width=w, label="+ Lịch sử hội thoại (+History)", color=PALETTE["teal"], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontweight="bold")
    ax.set_ylabel("Recall@10")
    ax.set_title("B. Recall@10 — Single vs +History", fontweight="bold")
    ax.legend(loc="upper left")
    ax.set_ylim(0, 1.05)

    # ---------- Panel [1,0]: Semantic Gain ----------
    sem_gain = [safe_mean([data[d]["retrieval"][k].get("ndcg10_semantic_gain", 0.0)
                           for d in data if k in data[d].get("retrieval", {})]) for k in PRIMARY_STRATEGIES]

    ax = axes[1, 0]
    colors = [PALETTE["green"] if g > 0.01 else (PALETTE["red"] if g < -0.01 else PALETTE["neutral"])
              for g in sem_gain]
    ax.bar(x, sem_gain, width=0.6, color=colors, alpha=0.85, edgecolor=PALETTE["dark"])
    ax.axhline(0, color=PALETTE["dark"], linewidth=1)
    ax.axhline(0.01, color=PALETTE["green"], linestyle="--", alpha=0.5, label="Ngưỡng có ý nghĩa (+0.01)")
    ax.axhline(-0.01, color=PALETTE["red"], linestyle="--", alpha=0.5, label="Ngưỡng có hại (-0.01)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontweight="bold")
    ax.set_ylabel("Δ nDCG@10  (history − random_padded)")
    ax.set_title("C. Semantic Gain — Lợi ích ngữ nghĩa thực của History\n"
                 "(≈0 ⇒ history chỉ là length bias, không phải ngữ nghĩa)",
                 fontweight="bold")
    ax.legend(loc="upper right", fontsize=8)
    for i, g in enumerate(sem_gain):
        if abs(g) > 0.001:
            ax.text(x[i], g + (0.005 if g >= 0 else -0.005), f"{g:+.3f}",
                    ha="center", va="bottom" if g >= 0 else "top",
                    fontsize=8, fontweight="bold")

    # ---------- Panel [1,1]: Length-bias check ----------
    rand_pad = [safe_mean([data[d]["retrieval"][k].get("ndcg10_random_padded", 0.0)
                           for d in data if k in data[d].get("retrieval", {})]) for k in PRIMARY_STRATEGIES]

    ax = axes[1, 1]
    ax.bar(x - w / 2, ndcg_hist, width=w, label="+History (nối lịch sử thật)",
           color=PALETTE["green"], alpha=0.85)
    ax.bar(x + w / 2, rand_pad, width=w, label="+Random-Pad (baseline cùng độ dài)",
           color=PALETTE["gray"], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontweight="bold")
    ax.set_ylabel("nDCG@10")
    ax.set_title("D. Length-bias check — History vs Random-Pad\n"
                 "(nếu 2 cột ≈ nhau ⇒ history KHÔNG hơn gì nối từ ngẫu nhiên)",
                 fontweight="bold")
    ax.legend(loc="upper left")

    plt.suptitle(f"Tác động Retrieval có Kiểm soát Length Bias (Macro-Average {len(data)} Domains)",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Đã lưu biểu đồ: {out_path.name}")


def plot_domain_strategy_heatmap(data: Dict[str, Dict[str, Any]], out_path: Path, include_sweep: bool = False):
    """Fig 4: Heatmap Composite Score giữa Domains và Chiến lược.

    Sử dụng GridSpec tách biệt Heatmap và Colorbar để không bị cắt chữ.
    """
    domains = sorted(data.keys())
    if not domains:
        return

    # Rút gọn tên domain dài để tiết kiệm diện tích bên trái
    DOMAIN_DISPLAY_NAMES = {
        "earth_science": "earth_sci",
        "medicalsciences": "med_sci",
        "sustainable_living": "sust_living",
    }
    domain_labels = [DOMAIN_DISPLAY_NAMES.get(d, d) for d in domains]

    winning_sweeps = set()
    for d in domains:
        ranking = data[d].get("ranking", [])
        if ranking:
            top_key = ranking[0].get("key")
            if top_key and top_key not in PRIMARY_STRATEGIES:
                winning_sweeps.add(top_key)

    if include_sweep:
        all_keys = sorted({r["key"] for d in domains for r in data[d].get("ranking", [])})
        strategies_to_show = all_keys
    else:
        strategies_to_show = list(PRIMARY_STRATEGIES) + sorted(winning_sweeps)

    matrix = np.full((len(domains), len(strategies_to_show)), np.nan)
    for i, d in enumerate(domains):
        ranking_map = {r["key"]: r["composite"] for r in data[d].get("ranking", [])}
        for j, s in enumerate(strategies_to_show):
            if s in ranking_map:
                matrix[i, j] = ranking_map[s]

    # 1. Tạo figure với GridSpec (tách heatmap và colorbar)
    fig_w = max(16, len(strategies_to_show) * 0.85)
    fig_h = max(6, len(domains) * 0.5)
    fig = plt.figure(figsize=(fig_w, fig_h))
    
    # Tỉ lệ: Heatmap chiếm 100 phần, Colorbar chiếm 2.5 phần
    gs = fig.add_gridspec(1, 2, width_ratios=[100, 2.5], wspace=0.02)
    ax = fig.add_subplot(gs[0, 0])
    cax = fig.add_subplot(gs[0, 1])
    ax.grid(False)

    # 2. Vẽ Heatmap
    cmap = plt.cm.YlGnBu.copy()
    cmap.set_bad(color=PALETTE["missing"])
    masked_data = np.ma.masked_invalid(matrix)
    vmin_val = np.nanmin(matrix) if not np.isnan(matrix).all() else 0.5
    vmax_val = np.nanmax(matrix) if not np.isnan(matrix).all() else 0.85
    im = ax.imshow(masked_data, cmap=cmap, aspect="auto", vmin=vmin_val, vmax=vmax_val)

    ax.set_xticks(np.arange(len(strategies_to_show)))
    ax.set_yticks(np.arange(len(domains)))
    
    display_labels = []
    for s in strategies_to_show:
        name = STRATEGY_DISPLAY_NAMES.get(s, s)
        if s in winning_sweeps:
            name += " (*win)"
        display_labels.append(name)
        
    ax.set_xticklabels(display_labels, rotation=35, ha="right", fontweight="bold")
    ax.set_yticklabels(domain_labels, fontweight="bold")

    # Ghi số lên từng ô
    for i in range(len(domains)):
        for j in range(len(strategies_to_show)):
            val = matrix[i, j]
            if np.isnan(val):
                ax.text(j, i, "N/A", ha="center", va="center", color=PALETTE["gray"], fontsize=7.5)
            else:
                threshold = (vmin_val + vmax_val) / 2
                color = "white" if val > threshold else "black"
                ax.text(j, i, f"{val:.3f}", ha="center", va="center", color=color, fontsize=8.5)

    # 3. Vẽ Colorbar
    cbar = fig.colorbar(im, cax=cax)
    # Rút gọn label để không bị tràn lề (chi tiết công thức đưa lên Title)
    cbar.set_label("Composite Score", fontweight="bold", fontsize=10)

    # 4. Title (đưa chú thích công thức lên đây thay vì nhét vào colorbar)
    ax.set_title(
        f"Ma Trận Composite Score ({len(domains)} Domains × {len(strategies_to_show)} Chiến Lược)\n"
        f"Composite = 0.45·nDCG_eff + 0.20·Recall + 0.25·Quality + 0.10·Cost (min-max NỘI domain)\n"
        f"⚠ KHÔNG so sánh liên domain",
        fontweight="bold", pad=12, fontsize=11
    )

    # 5. Chỉnh lề thủ công (KHÔNG dùng bbox_inches="tight" vì sẽ cắt colorbar)
    # left=0.08 (chừa chỗ tên domain), right=0.95 (chừa chỗ colorbar), bottom=0.25 (chừa chỗ x-labels xoay 35 độ)
    fig.subplots_adjust(left=0.08, right=0.95, top=0.88, bottom=0.25)

    plt.savefig(out_path, dpi=200)
    plt.close()
    logger.info(f"Đã lưu biểu đồ: {out_path.name}")


def plot_conversational_dynamics(data: Dict[str, Dict[str, Any]], out_path: Path):
    """Fig 5: Đặc trưng hội thoại Track 2 (Turns, Query length, Gold docs)."""
    domains = sorted(data.keys())
    n_dom = len(domains)
    if n_dom == 0:
        return

    conv_stats = [data[d].get("conversation_statistics", {}) for d in domains]
    total_convs = [cs.get("total_conversations", 0) for cs in conv_stats]
    total_turns = [cs.get("total_turns", 0) for cs in conv_stats]
    mean_turns = [cs.get("turns_per_conversation", {}).get("mean", 0) for cs in conv_stats]
    mean_qlens = [cs.get("query_word_length", {}).get("mean", 0) for cs in conv_stats]
    median_qlens = [cs.get("query_word_length", {}).get("median", 0) for cs in conv_stats]
    mean_golds = [cs.get("gold_docs_per_turn", {}).get("mean", 0) for cs in conv_stats]

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    x = np.arange(n_dom)
    w = 0.35

    # Panel A
    axes[0, 0].bar(x - w / 2, total_convs, width=w, label="Số cuộc hội thoại", color=PALETTE["blue"], alpha=0.85)
    axes[0, 0].bar(x + w / 2, total_turns, width=w, label="Tổng số lượt (Turns)", color=PALETTE["teal"], alpha=0.85)
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(domains, rotation=35, ha="right", fontweight="bold")
    axes[0, 0].set_ylabel("Số lượng")
    axes[0, 0].set_title("A. Quy mô hội thoại theo Domain", fontweight="bold")
    axes[0, 0].legend(loc="upper right")

    # Panel B
    axes[0, 1].bar(x, mean_turns, width=0.5, color=PALETTE["orange"], alpha=0.85, edgecolor=PALETTE["dark"])
    axes[0, 1].axhline(safe_mean(mean_turns), color=PALETTE["red"], linestyle="--",
                       label=f"Mean chung ({safe_mean(mean_turns):.1f})")
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(domains, rotation=35, ha="right", fontweight="bold")
    axes[0, 1].set_ylabel("Số lượt trung bình (Turns / Conv)")
    axes[0, 1].set_title("B. Độ dài hội thoại trung bình", fontweight="bold")
    axes[0, 1].legend(loc="upper right")

    # Panel C
    axes[1, 0].bar(x - w / 2, mean_qlens, width=w, label="Mean Word Count", color=PALETTE["purple"], alpha=0.85)
    axes[1, 0].bar(x + w / 2, median_qlens, width=w, label="Median Word Count", color=PALETTE["teal"], alpha=0.85)
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(domains, rotation=35, ha="right", fontweight="bold")
    axes[1, 0].set_ylabel("Số từ / Query")
    axes[1, 0].set_title("C. Độ dài câu hỏi từng lượt (Query Words)", fontweight="bold")
    axes[1, 0].legend(loc="upper right")

    # Panel D
    axes[1, 1].bar(x, mean_golds, width=0.5, color=PALETTE["green"], alpha=0.85, edgecolor=PALETTE["dark"])
    axes[1, 1].axhline(safe_mean(mean_golds), color=PALETTE["blue"], linestyle="--",
                       label=f"Mean chung ({safe_mean(mean_golds):.1f})")
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(domains, rotation=35, ha="right", fontweight="bold")
    axes[1, 1].set_ylabel("Gold docs / Turn")
    axes[1, 1].set_title("D. Mật độ tài liệu liên quan mỗi lượt", fontweight="bold")
    axes[1, 1].legend(loc="upper right")

    plt.suptitle(f"RETECO Track 2 — Đặc trưng Động thái Hội thoại (Conversational Dynamics) trên {n_dom} Domains",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Đã lưu biểu đồ: {out_path.name}")


def plot_master_dashboard(data: Dict[str, Dict[str, Any]], out_path: Path):
    """Fig 6: Master Overview Dashboard."""
    domains = sorted(data.keys())
    n_dom = len(domains)
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))

    # Panel A: % tài liệu ngắn
    pct_800 = [data[d].get("document_statistics", {}).get("share_le_chars_pct", {}).get("800", 0) for d in domains]
    y_pos = np.arange(n_dom)
    axes[0, 0].barh(y_pos, pct_800, color=PALETTE["teal"], alpha=0.85, edgecolor=PALETTE["dark"])
    axes[0, 0].axvline(50, color=PALETTE["red"], linestyle="--", alpha=0.7, label="Ngưỡng 50%")
    axes[0, 0].set_yticks(y_pos)
    axes[0, 0].set_yticklabels(domains, fontweight="bold")
    axes[0, 0].invert_yaxis()
    axes[0, 0].set_xlabel("% tài liệu <= 800 ký tự")
    axes[0, 0].set_title(f"A. Tỷ lệ tài liệu ngắn theo từng Domain ({n_dom} Domains)", fontweight="bold")
    axes[0, 0].legend(loc="lower right")

    # ========== Panel B: Winner pie — FIX trùng màu ==========
    winner_counts = Counter()
    for d in domains:
        ranking = data[d].get("ranking", [])
        if ranking:
            winner_counts[ranking[0]["key"]] += 1

    w_labels, w_vals = [], []
    for k, cnt in winner_counts.most_common():
        name = STRATEGY_DISPLAY_NAMES.get(k, k)
        if k not in PRIMARY_STRATEGIES:
            name += " (sweep)"
        w_labels.append(f"{name} ({cnt})")
        w_vals.append(cnt)

    # Sinh đủ màu động từ colormap — không giới hạn 6 màu
    n_slices = len(w_vals)
    if n_slices <= 10:
        pie_colors = plt.cm.tab10(np.linspace(0, 1, n_slices))
    else:
        pie_colors = plt.cm.tab20(np.linspace(0, 1, n_slices))

    axes[0, 1].pie(
        w_vals,
        labels=w_labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=pie_colors,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 9},
    )
    axes[0, 1].set_title(f"B. Phân bố Chiến lược Thắng Cuộc (#1 trên {n_dom} Domains)", fontweight="bold")

    # ========== Panel C: Trade-off — FIX chấm nhỏ ==========
    stats = {k: {"quality": [], "expansion": []} for k in PRIMARY_STRATEGIES}
    for d, ddata in data.items():
        comp = ddata.get("chunking_comparison", {})
        for k in PRIMARY_STRATEGIES:
            if k in comp:
                stats[k]["quality"].append(comp[k].get("avg_quality_score"))
                stats[k]["expansion"].append(comp[k].get("expansion_ratio"))

    for k in PRIMARY_STRATEGIES:
        q = safe_mean(stats[k]["quality"])
        exp = safe_mean(stats[k]["expansion"], default=1.0)
        axes[1, 0].scatter(exp, q, s=180, label=STRATEGY_DISPLAY_NAMES[k],
                           edgecolors="black", linewidths=1.5, alpha=0.9)

    axes[1, 0].set_xlabel("Hệ số nở tài liệu (Expansion Ratio) — Càng thấp càng tiết kiệm")
    axes[1, 0].set_ylabel("Điểm chất lượng ngữ nghĩa (0-100) — Càng cao càng tốt")
    axes[1, 0].set_title("C. Trade-off: Chất lượng vs Chi phí Index", fontweight="bold")
    axes[1, 0].legend(loc="lower left", fontsize=8)
    axes[1, 0].grid(True, alpha=0.3)

    # ========== Panel D: nDCG_eff — FIX legend bị đè ==========
    ndcg_eff, ndcg_single = [], []
    for k in PRIMARY_STRATEGIES:
        eff_vals = [data[d]["retrieval"][k].get("ndcg10_eff", 0.0)
                    for d in domains if k in data[d].get("retrieval", {})]
        s_vals = [data[d]["retrieval"][k].get("ndcg10_single", 0.0)
                  for d in domains if k in data[d].get("retrieval", {})]
        ndcg_eff.append(safe_mean(eff_vals))
        ndcg_single.append(safe_mean(s_vals))

    x = np.arange(len(PRIMARY_STRATEGIES))
    w = 0.35
    axes[1, 1].bar(x - w / 2, ndcg_single, width=w, label="Single Query",
                   color=PALETTE["blue"], alpha=0.85)
    axes[1, 1].bar(x + w / 2, ndcg_eff, width=w,
                   label="nDCG_eff (= single + max(0, semantic_gain))",
                   color=PALETTE["green"], alpha=0.85)
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels([STRATEGY_DISPLAY_NAMES[k] for k in PRIMARY_STRATEGIES],
                                rotation=35, ha="right", fontweight="bold")
    axes[1, 1].set_ylabel("nDCG@10")
    axes[1, 1].set_title("D. nDCG@10 — Single vs Effective (đã trừ length bias)", fontweight="bold")
    # Chừa 35% phía trên cho legend 2 cột, tránh cột đè
    max_ndcg = max(ndcg_eff + ndcg_single) if (ndcg_eff + ndcg_single) else 0.5
    axes[1, 1].set_ylim(0, max_ndcg * 1.35)
    axes[1, 1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.0),
                      ncol=2, fontsize=8, framealpha=0.9)

    plt.suptitle(f"MASTER DASHBOARD: TỔNG HỢP PHÂN TÍCH EDA & CHUNKING — {n_dom} DOMAINS (v3)",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Đã lưu biểu đồ: {out_path.name}")


# ===========================================================================
# 4. Báo cáo Markdown động
# ===========================================================================
def generate_dynamic_markdown_report(data: Dict[str, Dict[str, Any]], out_file: Path) -> None:
    """Sinh báo cáo Markdown từ số liệu tính toán, không hard-code kết luận."""
    domains = sorted(data.keys())
    n_dom = len(domains)
    total_docs = sum(data[d].get("document_statistics", {}).get("total_documents", 0) for d in domains)

    medians = [data[d].get("document_statistics", {}).get("char_length", {}).get("median", 0) for d in domains]
    mean_median = safe_mean(medians)

    winner_counts = Counter()
    domain_winners = {}
    for d in domains:
        ranking = data[d].get("ranking", [])
        if ranking:
            top = ranking[0].get("key")
            winner_counts[top] += 1
            domain_winners[d] = (top, ranking[0].get("composite", 0.0))

    all_s_ndcg, all_h_ndcg, all_rand_ndcg, all_sem_gain, all_eff_ndcg = [], [], [], [], []
    for d in domains:
        ret = data[d].get("retrieval", {})
        for s in PRIMARY_STRATEGIES:
            if s in ret:
                all_s_ndcg.append(ret[s].get("ndcg10_single", 0))
                all_h_ndcg.append(ret[s].get("ndcg10_history", 0))
                all_rand_ndcg.append(ret[s].get("ndcg10_random_padded", 0))
                all_sem_gain.append(ret[s].get("ndcg10_semantic_gain", 0))
                all_eff_ndcg.append(ret[s].get("ndcg10_eff", 0))

    mean_s = safe_mean(all_s_ndcg)
    mean_h = safe_mean(all_h_ndcg)
    mean_rand = safe_mean(all_rand_ndcg)
    mean_sem = safe_mean(all_sem_gain)
    mean_eff = safe_mean(all_eff_ndcg)

    sorted_by_med = sorted(domains,
                            key=lambda d: data[d].get("document_statistics", {}).get("char_length", {}).get("median", 0))
    shortest_dom = sorted_by_med[0] if sorted_by_med else "N/A"
    longest_dom = sorted_by_med[-1] if sorted_by_med else "N/A"

    md = []
    md.append("# Báo Cáo Phân Tích Thực Nghiệm & Trực Quan Hóa Chunking — RETECO Track 2 (v3)\n")
    md.append(f"- **Thời điểm khởi tạo:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    md.append(f"- **Số domains:** `{n_dom}` (`{', '.join(domains)}`)")
    md.append(f"- **Tổng tài liệu:** `{total_docs:,}`\n")

    md.append("## 1. Master Overview Dashboard\n")
    md.append("![Master Dashboard](figures/dashboard_master_overview.png)\n")

    md.append("### Tóm lược phát hiện (dựa trên số liệu):\n")
    md.append(f"1. **Phân bố độ dài:** Median trung bình = `{mean_median:.1f}` ký tự. "
              f"Ngắn nhất: `{shortest_dom}` (median={data[shortest_dom]['document_statistics']['char_length']['median']}); "
              f"dài nhất: `{longest_dom}` (median={data[longest_dom]['document_statistics']['char_length']['median']}).")

    win_summary_str = ", ".join([f"`{STRATEGY_DISPLAY_NAMES.get(k, k)}`: {v}/{n_dom} ({v/n_dom*100:.1f}%)"
                                 for k, v in winner_counts.most_common()])
    md.append(f"2. **Phân bố chiến lược thắng:** {win_summary_str}.")

    md.append(f"3. **Length-bias analysis:** nDCG@10 trung bình: "
              f"single=`{mean_s:.4f}`, +History=`{mean_h:.4f}`, +Random-Pad=`{mean_rand:.4f}`. "
              f"→ **Δ Semantic (history − random-pad) = `{mean_sem:+.4f}`**. "
              f"nDCG_eff dùng trong composite = `{mean_eff:.4f}`.")
    if abs(mean_sem) < 0.01:
        md.append(f"   > ⚠️ **Δ Semantic ≈ 0** — phần lớn gain của history đến từ **length bias** "
                  f"(query dài hơn → BM25 match dễ hơn), KHÔNG phải ngữ nghĩa. Composite đã trung hòa yếu tố này.")
    elif mean_sem > 0:
        md.append(f"   > ✅ **Δ Semantic > 0** — history thực sự mang lại lợi ích ngữ nghĩa "
                  f"vượt qua baseline random-pad cùng độ dài.")
    else:
        md.append(f"   > 🔴 **Δ Semantic < 0** — history có hại: nối cả hội thoại đưa thêm nhiễu "
                  f"khiến BM25 match kém hơn nối từ ngẫu nhiên cùng độ dài.")
    md.append("")

    md.append("## 2. Bảng Tổng Hợp Chiến Lược #1 Theo Domain\n")
    md.append("| Domain | Docs | Median (c) | % ≤ 800c | Chiến lược #1 | Composite |")
    md.append("| :--- | ---: | ---: | ---: | :--- | ---: |")
    for d in domains:
        ds = data[d].get("document_statistics", {})
        cl = ds.get("char_length", {})
        pct_800 = ds.get("share_le_chars_pct", {}).get("800", 0)
        win_strat, win_comp = domain_winners.get(d, ("N/A", 0.0))
        win_display = STRATEGY_DISPLAY_NAMES.get(win_strat, win_strat)
        md.append(f"| **{d}** | {ds.get('total_documents', 0):,} | {cl.get('median', 0)} | "
                  f"{pct_800}% | `{win_display}` | **{win_comp:.4f}** |")
    md.append("\n> ⚠️ **Lưu ý thang điểm:** Composite được chuẩn hóa min-max **trong từng domain**. "
              "Composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — "
              "chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**.\n")
    md.append("---\n")

    md.append("## 3. Khảo Sát Đặc Trưng Corpus\n")
    md.append("![Corpus Profile](figures/fig1_corpus_profile_by_domain.png)\n")
    long_tail_doms = [d for d in domains
                       if data[d].get("document_statistics", {}).get("char_length", {}).get("p90", 0) > 1500]
    short_tail_doms = [d for d in domains if d not in long_tail_doms]
    md.append(f"- **Domain có đuôi dài** (P90 > 1,500c, nguy cơ truncation cao nếu Whole_Document): "
              f"`{', '.join(long_tail_doms) if long_tail_doms else 'Không có'}`.")
    md.append(f"- **Domain ngắn gọn** (P90 ≤ 1,500c): "
              f"`{', '.join(short_tail_doms) if short_tail_doms else 'Tất cả'}`.\n")

    md.append("## 4. Đo Lường Lỗi Ngữ Nghĩa của Chunking\n")
    md.append("![Semantic Integrity](figures/fig2_chunking_semantic_integrity.png)\n")
    md.append("### Phân tích nguyên nhân lỗi kỹ thuật:")
    md.append("- **`1_Fixed_Char` & `2_Fixed_Word`:** Đứt câu cao nhất do cắt chuỗi theo độ dài cơ học.")
    md.append("- **`4_Recursive_Markdown`:** Phân rã phân cấp + cơ chế hoãn tiêu đề mồ côi (`carry = cur.pop()`).")
    md.append("- **`5_Semantic_Context_Injected`:** Tiêm prefix `[Document Topic: ...]` để giảm đại từ mồ côi.")
    md.append("- **`6_Whole_Document`:** Không đứt câu nhân tạo, nhưng `over_token_limit_pct` cao ở domain dài.\n")

    md.append("## 5. Hiệu Năng Truy Hồi (BM25 + Length-Bias Control)\n")
    md.append("![Retrieval Performance](figures/fig3_retrieval_performance.png)\n")

    def _mean_metric(strategy_key: str, metric: str) -> float:
        vals = [data[d]["retrieval"][strategy_key].get(metric, 0.0)
                for d in domains if strategy_key in data[d].get("retrieval", {})]
        return safe_mean(vals)

    md.append("**So sánh data-driven giữa các chiến lược chính:**\n")
    md.append("| Chiến lược | nDCG single | nDCG +Hist | Δ Semantic | nDCG_eff |")
    md.append("| :--- | ---: | ---: | ---: | ---: |")
    for k in ["3_Sentence_Boundary", "4_Recursive_Markdown", "6_Whole_Document",
              "7_Parent_Child", "5_Semantic_Context_Injected"]:
        if any(k in data[d].get("retrieval", {}) for d in domains):
            md.append(f"| {STRATEGY_DISPLAY_NAMES.get(k, k)} | "
                      f"{_mean_metric(k, 'ndcg10_single'):.4f} | "
                      f"{_mean_metric(k, 'ndcg10_history'):.4f} | "
                      f"{_mean_metric(k, 'ndcg10_semantic_gain'):+.4f} | "
                      f"{_mean_metric(k, 'ndcg10_eff'):.4f} |")
    md.append("")
    md.append("> Δ Semantic ≈ 0 (không có mũi tên) ⇒ history chỉ là length bias; nếu Δ Semantic > 0 ⇒ "
              "history thực sự giúp. `nDCG_eff = single + max(0, Δ Semantic)` là metric dùng trong composite.\n")

    md.append("## 6. Ma Trận Composite (Domain × Strategy)\n")
    md.append("![Domain Strategy Heatmap](figures/fig4_domain_strategy_heatmap.png)\n")
    md.append("> Ô xám `N/A` = chiến lược không được chạy trong domain đó. "
              "Composite NỘI domain (min-max) — không so sánh liên domain.\n")

    md.append("## 7. Đặc Tính Hội Thoại\n")
    md.append("![Conversational Dynamics](figures/fig5_conversational_dynamics.png)\n")
    md.append("- Số turns/conv, độ dài query, gold docs/turn — đầu vào cho bước thiết kế Query Rewriter.\n")

    out_file.write_text("\n".join(md), encoding="utf-8")
    logger.info(f"Đã lưu báo cáo Markdown động tại: {out_file}")


# ===========================================================================
# 5. CLI & Main Orchestrator
# ===========================================================================
def main():
    parser = argparse.ArgumentParser(
        description="RETECO Track 2: Comprehensive EDA & Chunking Visualization Suite (v3)"
    )
    parser.add_argument(
        "--reports-dir", default=str(default_reports_dir()),
        help="Thư mục chứa eda_metrics_*.json (mặc định: tự động tìm)"
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Thư mục xuất figures (mặc định: <reports-dir>/figures)"
    )
    parser.add_argument(
        "--include-sweep", action="store_true",
        help="Hiện tất cả biến thể sweep trong heatmap (mặc định: chỉ sweep nào thắng #1)"
    )
    args = parser.parse_args()

    reports_path = Path(args.reports_dir).resolve()
    if not reports_path.is_dir():
        logger.error(f"Thư mục reports không tồn tại: {reports_path}")
        sys.exit(1)

    figures_path = Path(args.output_dir).resolve() if args.output_dir else (reports_path / "figures")
    figures_path.mkdir(parents=True, exist_ok=True)

    data = load_all_metrics(reports_path)
    if not data:
        logger.error(f"Không tìm thấy eda_metrics_*.json nào trong {reports_path}")
        sys.exit(1)

    logger.info(f"Bắt đầu sinh 6 bộ biểu đồ trực quan hóa vào: {figures_path}")

    fig1 = figures_path / "fig1_corpus_profile_by_domain.png"
    fig2 = figures_path / "fig2_chunking_semantic_integrity.png"
    fig3 = figures_path / "fig3_retrieval_performance.png"
    fig4 = figures_path / "fig4_domain_strategy_heatmap.png"
    fig5 = figures_path / "fig5_conversational_dynamics.png"
    fig6 = figures_path / "dashboard_master_overview.png"

    plot_corpus_profile(data, fig1)
    plot_chunking_integrity(data, fig2)
    plot_retrieval_impact(data, fig3)
    plot_domain_strategy_heatmap(data, fig4, include_sweep=args.include_sweep)
    plot_conversational_dynamics(data, fig5)
    plot_master_dashboard(data, fig6)

    report_md_file = reports_path / "visualization_report.md"
    generate_dynamic_markdown_report(data, report_md_file)

    logger.info(">>> HOÀN THÀNH TẤT CẢ BIỂU ĐỒ & BÁO CÁO TRỰC QUAN HÓA (v3)! <<<")


if __name__ == "__main__":
    main()