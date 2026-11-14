#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
RETECO Track 2 - EDA & Chunking Diagnostic Suite (v3)
===============================================================================
Vị trí file : <project>/scripts/eda/01_eda.py
Báo cáo     : <project>/reports/eda/   (tự tạo)

Changelog v3 (so với v2):
  [FIX-1.2] Baseline random_padded dùng seed deterministic theo (strategy, qid)
            thay vì Random(42) share toàn cục -> A/B test ổn định giữa các lần chạy.
  [FIX-1.3] ndcg10_semantic_gain (history - random_padded) được đưa vào:
            - ADR log (Section 3 & 4)
            - eda_report_<domain>.md (Section 4)
            - JSON output (eda_metrics_<domain>.json)
  [FIX-2.1] Truncation penalty đổi từ bậc thang tại ot=5% sang tuyến tính liên tục
            (0% tại ot<=5%, 40% tại ot>=25%) -> composite không nhảy loạn.
  [FIX-2.2] Composite dùng ndcg10_eff = single + max(0, semantic_gain)
            thay vì ndcg10_avg = (single+history)/2 -> loại thiên lệch độ dài query.
            ndcg10_avg vẫn được báo cáo để minh bạch, nhưng KHÔNG dùng xếp hạng.
  [FIX-2.4] Guard vocab >= MIN_VOCAB_FOR_PAD trước khi bật random_padded
            (tránh baseline "mạnh giả tạo" khi vocab nhỏ).
===============================================================================
Bảng tham số CLI chính:
  --domain              Tên domain (hoặc 'all')
  --sample-size         Số tài liệu mẫu để đo chunk quality       (default: 2000)
  --retrieval-distractors Số distractors trong corpus retrieval    (default: 10000)
  --max-queries         Số query tối đa dùng đo retrieval          (default: 300)
  --seed                Seed cho reservoir sampling và ranking     (default: 42)
  --max-docs            Giới hạn đọc documents.jsonl (0 = hết)     (default: 0)
  --no-retrieval        Bỏ qua bước đo retrieval BM25
  --no-sweep            Bỏ qua các biến thể tham số (sweep)
  --worst-n             Số chunk tệ nhất mỗi chiến lược trong file soi (default: 25)

Hằng số cấu hình scoring:
  W_WITH_RETRIEVAL      Trọng số composite khi CÓ retrieval
  W_NO_RETRIEVAL        Trọng số composite khi KHÔNG có retrieval
  EMBED_TOKEN_LIMIT     Ngưỡng token embedding (512 = BGE/E5/Contriever)
  TOKEN_PER_WORD        Hệ số ước lượng token/từ (1.35 cho văn bản kỹ thuật)
  TRUNC_PENALTY_START   Ngưỡng % chunk vượt 512 token bắt đầu bị phạt (5%)
  TRUNC_PENALTY_MAX     Mức phạt tối đa (40% composite)
  TRUNC_PENALTY_RANGE   Khoảng % vượt để đạt mức phạt tối đa (20%)
===============================================================================
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import logging
import math
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# Windows console (cp1252) không in được tiếng Việt -> ép UTF-8
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("RETECO_EDA")

# ---------------------------------------------------------------------------
# Hằng số
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1] if len(SCRIPT_DIR.parents) >= 2 else SCRIPT_DIR

# ---- Ngưỡng embedding ----
EMBED_TOKEN_LIMIT = 512      # giới hạn thường gặp của BGE/E5/Contriever
TOKEN_PER_WORD = 1.35        # ước lượng thô số token / từ (văn bản kỹ thuật tiếng Anh)

# ---- Ngưỡng kích thước chunk ----
UNDERSIZED_CHARS = 80        # dưới ngưỡng này -> chunk quá ngắn
OVERSIZED_CHARS = 1500       # trên ngưỡng này -> chunk quá dài (dù chưa vượt token)

# ---- Marker định vị ----
PARA_MARK = "¶"              # ký hiệu thay cho xuống dòng khi định vị chunk
SENT_END_CHARS = set(".!?…\"'”’)]»")

# ---- Regex ----
SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[“])")
MARKDOWN_HEADER_REGEX = re.compile(r"^(#{1,6}\s+.+|.+\[edit\]|\*\*([^*]+)\*\*)$", re.MULTILINE)
BULLET_REGEX = re.compile(r"^\s*([*\-+]|\d+\.)\s+", re.MULTILINE)
URL_REGEX = re.compile(r"https?://\S+|www\.\S+")
CODE_BLOCK_REGEX = re.compile(r"```[\s\S]*?```|`[^`]+`")
TOKEN_REGEX = re.compile(r"[a-z0-9]+")

# ---- Từ điển heuristic ----
PRONOUN_ORPHANS = {
    "it", "its", "they", "them", "their", "theirs", "this", "these", "that",
    "those", "he", "him", "his", "she", "her", "hers", "such",
}
PHRASE_ORPHANS = {"the above", "the latter", "the former", "the same", "the aforementioned"}
CONTINUATION_STARTERS = {
    "and", "but", "so", "then", "thus", "therefore", "however", "also",
    "which", "because", "while", "whereas", "moreover", "furthermore",
}
STOPWORDS = frozenset(
    "a an and are as at be by for from has have i in is it its of on or that the this to was "
    "were will with you your we they he she not but if so do does can could should would about "
    "into than then there their what which who how when where why".split()
)

# ---- Trọng số xếp hạng tổng hợp ----
# (ndcg + recall + quality + cost = 1.0; truncation_penalty là hệ số nhân)
W_WITH_RETRIEVAL = {"ndcg": 0.45, "recall": 0.20, "quality": 0.25, "cost": 0.10}
W_NO_RETRIEVAL = {"quality": 0.80, "cost": 0.20}

# ---- Truncation penalty (mượt, FIX-2.1) ----
TRUNC_PENALTY_START = 5.0    # % chunk vượt 512 token bắt đầu bị phạt
TRUNC_PENALTY_RANGE = 20.0   # khoảng % vượt để đạt mức phạt tối đa (ot=25% -> 40%)
TRUNC_PENALTY_MAX = 0.40     # mức phạt tối đa (giảm 40% composite)

# ---- Guard cho random_padded baseline (FIX-2.4) ----
MIN_VOCAB_FOR_PAD = 500      # vocab dưới ngưỡng này -> bỏ random_padded mode
MAX_PAD_WORDS = 200          # giới hạn số từ padding tối đa mỗi query

THEORY_NOTES = {
    "1_Fixed_Char": "Cắt theo ký tự thô: có thể chẻ đôi một từ (vd 'quadcopter' -> 'quad'+'copter'), "
                    "BM25 mất từ khóa, tokenizer sinh sub-token rác, mệnh đề kỹ thuật bị tách đôi.",
    "2_Fixed_Word": "Không chẻ từ nhưng cắt ngang câu; reranker/cross-encoder mất ngữ cảnh cú pháp.",
    "3_Sentence_Boundary": "Giữ nguyên câu nhưng vẫn chia nhỏ cả tài liệu vốn đã ngắn và không xử lý đại từ mồ côi.",
    "4_Recursive_Markdown": "Tôn trọng đoạn/dòng/bullet, nhưng chunk sau của tài liệu dài mất tên thực thể "
                            "(bắt đầu bằng 'It', 'This drone'...).",
    "5_Semantic_Context_Injected": "Giữ nguyên tài liệu ngắn, chia tài liệu dài theo cấu trúc và gắn chủ đề/tiêu đề "
                                   "vào chunk sau. Rủi ro: prefix lặp lại làm các chunk cùng tài liệu giống nhau "
                                   "(near-duplicate) và tăng độ dài.",
    "6_Whole_Document": "Không chia: tốt cho tài liệu ngắn, nhưng tài liệu dài bị embedding cắt cụt (truncation) "
                        "và BM25 bị loãng do độ dài.",
    "7_Parent_Child": "Chunk con nhỏ (~60 từ) giúp truy hồi chính xác, nhưng nếu không trả về chunk cha thì "
                      "câu trả lời thiếu ngữ cảnh; chunk con thường quá ngắn và đầy đại từ mồ côi.",
    "8_Sentence_Window": "Cửa sổ N câu cố định, dễ cài đặt, nhưng bỏ qua ranh giới đoạn/chủ đề.",
    "9_TextTiling_Semantic": "Cắt tại điểm đổi chủ đề (độ tương đồng từ vựng giữa hai khối câu giảm). "
                             "Nhạy với nhiễu ở văn bản ngắn; cần ngưỡng min câu/đoạn.",
}


# ===========================================================================
# Tiện ích chung
# ===========================================================================
def doc_id_of(d: Dict[str, Any], fallback: Any) -> str:
    for k in ("doc_id", "id", "_id", "docid", "document_id"):
        if d.get(k) is not None:
            return str(d[k])
    return str(fallback)


def doc_text_of(d: Dict[str, Any]) -> str:
    for k in ("content", "text", "contents", "body", "passage"):
        v = d.get(k)
        if isinstance(v, str):
            return v
    return ""


def doc_title_of(d: Dict[str, Any]) -> str:
    v = d.get("title")
    return " ".join(v.split()) if isinstance(v, str) else ""


def tokenize(text: str) -> List[str]:
    return [t for t in TOKEN_REGEX.findall(text.lower()) if t not in STOPWORDS]


def est_tokens(text: str) -> int:
    return int(len(text.split()) * TOKEN_PER_WORD) + 1


def quantile(sorted_vals: List[float], p: float) -> float:
    if not sorted_vals:
        return 0
    return sorted_vals[min(len(sorted_vals) - 1, int(p * len(sorted_vals)))]


def normalize_with_marks(text: str) -> str:
    """Thay mọi xuống dòng bằng PARA_MARK rồi gộp khoảng trắng -> dùng để định vị chunk."""
    t = re.sub(r"[ \t\r\f\v]*\n[ \t\r\f\v\n]*", " " + PARA_MARK + " ", text)
    return " ".join(t.split())


def normalize_flat(text: str) -> str:
    return " ".join(text.split())


def split_sentences(text: str) -> Tuple[List[str], List[bool]]:
    """Tách câu, đồng thời nhớ câu nào mở đầu đoạn mới (để nối lại không mất xuống dòng)."""
    sents: List[str] = []
    brk: List[bool] = []
    for para in re.split(r"\n+", text):
        para = para.strip()
        if not para:
            continue
        parts = [s.strip() for s in SENTENCE_SPLIT_REGEX.split(para) if s.strip()]
        for j, s in enumerate(parts):
            sents.append(s)
            brk.append(j == 0)
    return sents, brk


def join_range(sents: List[str], brk: List[bool], a: int, b: int) -> str:
    out = sents[a]
    for i in range(a + 1, b):
        out += ("\n" if brk[i] else " ") + sents[i]
    return out


def looks_like_heading(u: str) -> bool:
    u = u.strip()
    return 0 < len(u) < 80 and "\n" not in u and u[-1] not in SENT_END_CHARS


def extract_lead(text: str, title: str = "") -> str:
    """Chủ đề của tài liệu: ưu tiên title thật, sau đó dòng đầu, sau đó câu đầu."""
    if title:
        return title[:150]
    first_line = next((ln.strip() for ln in text.split("\n") if ln.strip()), "")
    first_sentence = SENTENCE_SPLIT_REGEX.split(text.strip(), 1)[0].strip()
    lead = first_line if 15 < len(first_line) < 150 else first_sentence
    lead = " ".join(lead.split())
    if len(lead) > 120:
        lead = lead[:120].rsplit(" ", 1)[0] + "…"
    return lead


def make_chunk(idx: int, name: str, body: str, prefix: str = "", **extra: Any) -> Dict[str, Any]:
    content = prefix + body
    d = {
        "chunk_id": idx,
        "strategy": name,
        "content": content,        # phần được đưa vào index (có thể có prefix)
        "body": body,              # phần văn bản gốc (không có prefix) - dùng để định vị
        "prefix": prefix,
        "char_len": len(content),
        "word_count": len(content.split()),
    }
    d.update(extra)
    return d


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def _seed_for_pair(strategy_key: str, qid: str) -> int:
    """
    [FIX-1.2] Sinh seed xác định (deterministic) cho cặp (chiến lược, query).
    Mục đích: baseline random_padded phải giống nhau mỗi lần chạy cùng seed
    -> tránh dao động metric ±0.01 giữa các lần chạy, cho phép A/B test đáng tin.
    """
    h = hashlib.md5(f"{strategy_key}||{qid}".encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def truncation_penalty(ot_pct: float) -> float:
    """
    [FIX-2.1] Phạt mượt cho tỷ lệ chunk vượt 512 token.

    Công thức: TRUNC_PENALTY_MAX * clip((ot_pct - TRUNC_PENALTY_START) / TRUNC_PENALTY_RANGE, 0, 1)
      - ot_pct <= 5%  : penalty = 0 (không phạt)
      - ot_pct = 10%  : penalty = 0.10 (giảm 10% composite)
      - ot_pct = 15%  : penalty = 0.20 (giảm 20%)
      - ot_pct = 25%  : penalty = 0.40 (giảm 40% - sàn)

    Khác bản cũ: dùng tuyến tính liên tục thay vì bậc thang tại ngưỡng 5%,
    tránh composite nhảy loạn giữa các lần chạy khi ot_pct dao động ~5%.
    """
    excess = max(0.0, ot_pct - TRUNC_PENALTY_START)
    frac = min(1.0, excess / TRUNC_PENALTY_RANGE)
    return TRUNC_PENALTY_MAX * frac


# ===========================================================================
# 1. Các chiến lược chunking
# ===========================================================================
class ChunkingStrategies:
    """Mọi hàm trả về list chunk dict (xem make_chunk).

    Tham số mặc định đã được chọn theo sweep (xem build_strategy_registry).
    """

    # ---- 1. Fixed char ------------------------------------------------------
    @staticmethod
    def fixed_char(text: str, chunk_size: int = 500, overlap: int = 50, name: str = "1_Fixed_Char"):
        """Tham số: chunk_size=500 ký tự, overlap=50 ký tự giữa các chunk liền kề."""
        text = text.strip()
        if not text:
            return []
        chunks, start, idx = [], 0, 0
        step = max(1, chunk_size - overlap)
        while start < len(text):
            end = min(len(text), start + chunk_size)
            body = text[start:end].strip()
            if body:
                chunks.append(make_chunk(idx, name, body))
                idx += 1
            if end >= len(text):
                break
            start += step
        return chunks

    # ---- 2. Fixed word ------------------------------------------------------
    @staticmethod
    def fixed_word(text: str, chunk_words: int = 120, overlap_words: int = 20, name: str = "2_Fixed_Word"):
        """Tham số: chunk_words=120 từ, overlap_words=20 từ giữa các chunk."""
        words = text.strip().split()
        if not words:
            return []
        chunks, start, idx = [], 0, 0
        step = max(1, chunk_words - overlap_words)
        while start < len(words):
            end = min(len(words), start + chunk_words)
            chunks.append(make_chunk(idx, name, " ".join(words[start:end])))
            idx += 1
            if end >= len(words):
                break
            start += step
        return chunks

    # ---- 3. Sentence boundary ----------------------------------------------
    @staticmethod
    def sentence_boundary(text: str, max_chunk_words: int = 150, overlap_sentences: int = 1,
                          name: str = "3_Sentence_Boundary"):
        """Tham số: max_chunk_words=150 từ/chunk, overlap_sentences=1 câu chồng lấn."""
        text = text.strip()
        if not text:
            return []
        sents, brk = split_sentences(text)
        n = len(sents)
        if n == 0:
            return [make_chunk(0, name, text)]
        wc = [len(s.split()) for s in sents]
        chunks, a, idx = [], 0, 0
        while a < n:
            b, words = a, 0
            while b < n and (b == a or words + wc[b] <= max_chunk_words):
                words += wc[b]
                b += 1
            chunks.append(make_chunk(idx, name, join_range(sents, brk, a, b)))
            idx += 1
            if b >= n:
                break
            nxt = b - overlap_sentences
            a = nxt if nxt > a else b
        return chunks

    # ---- 4. Recursive structure-aware --------------------------------------
    @staticmethod
    def _merge_units(units: List[str], joiner: str, max_chars: int, min_chars: int) -> List[str]:
        """Gộp các unit liên tiếp sao cho không vượt max_chars; gộp đuôi < min_chars vào chunk trước."""
        chunks: List[str] = []
        cur: List[str] = []

        def cur_len(items: List[str]) -> int:
            return sum(len(x) for x in items) + len(joiner) * max(0, len(items) - 1)

        for u in units:
            add = len(u) + (len(joiner) if cur else 0)
            if cur and cur_len(cur) + add > max_chars:
                carry = None
                # không để tiêu đề mồ côi ở cuối chunk: chuyển nó sang chunk kế tiếp
                if len(cur) > 1 and looks_like_heading(cur[-1]):
                    carry = cur.pop()
                chunks.append(joiner.join(cur))
                cur = [carry] if carry else []
            cur.append(u)
        if cur:
            chunks.append(joiner.join(cur))
        # gộp đuôi quá ngắn vào chunk trước nếu không vượt quá 1.3x giới hạn
        merged: List[str] = []
        for c in chunks:
            if merged and len(c) < min_chars and len(merged[-1]) + len(joiner) + len(c) <= max_chars * 1.3:
                merged[-1] += joiner + c
            else:
                merged.append(c)
        return merged

    @staticmethod
    def _split_units(text: str, max_chars: int, min_chars: int, level: int = 0) -> List[str]:
        """Đệ quy phân rã: đoạn -> dòng -> câu -> từ (dừng ở level 3)."""
        text = text.strip()
        if len(text) <= max_chars:
            return [text] if text else []
        if level == 0:
            parts, joiner = re.split(r"\n\s*\n", text), "\n\n"
        elif level == 1:
            parts, joiner = text.split("\n"), "\n"
        elif level == 2:
            parts, joiner = SENTENCE_SPLIT_REGEX.split(text), " "
        else:
            parts, joiner = text.split(), " "
        parts = [p.strip() for p in parts if p.strip()]
        if not parts:
            return []
        if len(parts) == 1:
            if level >= 3:
                return [parts[0]]
            return ChunkingStrategies._split_units(parts[0], max_chars, min_chars, level + 1)
        units: List[str] = []
        for p in parts:
            if len(p) > max_chars and level < 3:
                units.extend(ChunkingStrategies._split_units(p, max_chars, min_chars, level + 1))
            else:
                units.append(p)
        return ChunkingStrategies._merge_units(units, joiner, max_chars, min_chars)

    @staticmethod
    def recursive_structure(text: str, max_chunk_chars: int = 650, min_chunk_chars: int = 150,
                            name: str = "4_Recursive_Markdown"):
        """Tham số: max_chunk_chars=650, min_chunk_chars=150 (gộp đuôi ngắn)."""
        text = text.strip()
        if not text:
            return []
        pieces = ChunkingStrategies._split_units(text, max_chunk_chars, min_chunk_chars)
        return [make_chunk(i, name, p) for i, p in enumerate(pieces)]

    # ---- 5. Semantic hierarchical + context injection ----------------------
    @staticmethod
    def semantic_context(text: str, title: str = "", threshold_no_chunk: int = 800,
                         max_chunk_chars: int = 650, prefix_all: bool = False,
                         name: str = "5_Semantic_Context_Injected"):
        """Tham số:
        - threshold_no_chunk: tài liệu <= ngưỡng này thì giữ nguyên 1 chunk (800 ký tự)
        - max_chunk_chars: kích thước tối đa chunk con (650 ký tự)
        - prefix_all: nếu True, thêm prefix "[Document Topic: ...]" cho MỌI chunk
                       (mặc định chỉ thêm cho chunk 2+, vì chunk 1 đã chứa lead)
        """
        text = text.strip()
        if not text:
            return []
        if len(text) <= threshold_no_chunk:
            return [make_chunk(0, name, text, is_whole_doc=True)]
        lead = extract_lead(text, title)
        base = ChunkingStrategies.recursive_structure(text, max_chunk_chars, name=name)
        out = []
        for idx, c in enumerate(base):
            body = c["body"]
            prefix = ""
            if lead and (idx > 0 or prefix_all) and lead.lower().rstrip("…") not in body.lower():
                prefix = f"[Document Topic: {lead}]\n"
            out.append(make_chunk(idx, name, body, prefix=prefix))
        return out

    # ---- 6. Whole document --------------------------------------------------
    @staticmethod
    def whole_document(text: str, name: str = "6_Whole_Document"):
        """Không chia - mỗi tài liệu = 1 chunk."""
        text = text.strip()
        return [make_chunk(0, name, text, is_whole_doc=True)] if text else []

    # ---- 7. Parent-child (chunk con nhỏ dùng để truy hồi) -------------------
    @staticmethod
    def parent_child(text: str, child_words: int = 60, name: str = "7_Parent_Child"):
        """Tham số: child_words=60 từ/chunk con."""
        return ChunkingStrategies.sentence_boundary(text, child_words, 0, name)

    # ---- 8. Sentence window -------------------------------------------------
    @staticmethod
    def sentence_window(text: str, window: int = 4, stride: int = 2, name: str = "8_Sentence_Window"):
        """Tham số: window=4 câu/cửa sổ, stride=2 câu bước nhảy (overlap = window-stride)."""
        text = text.strip()
        if not text:
            return []
        sents, brk = split_sentences(text)
        n = len(sents)
        if n == 0:
            return [make_chunk(0, name, text)]
        chunks, a, idx = [], 0, 0
        while a < n:
            b = min(n, a + window)
            chunks.append(make_chunk(idx, name, join_range(sents, brk, a, b)))
            idx += 1
            if b >= n:
                break
            a += max(1, stride)
        return chunks

    # ---- 9. TextTiling (cắt theo đổi chủ đề, thuần từ vựng) -----------------
    @staticmethod
    def texttiling(text: str, block: int = 3, max_chunk_chars: int = 900, min_sents: int = 6,
                   min_seg_sents: int = 2, k: float = 0.5, name: str = "9_TextTiling_Semantic"):
        """Tham số:
        - block=3 câu mỗi bên để tính cosine similarity
        - k=0.5: ngưỡng cắt = mean - k*std (càng nhỏ càng nhiều điểm cắt)
        - min_sents=6: tài liệu ít hơn ngưỡng này thì bỏ qua TextTiling
        - min_seg_sents=2: mỗi segment phải có ít nhất 2 câu
        - max_chunk_chars=900: fallback sentence_boundary nếu segment vượt
        """
        text = text.strip()
        if not text:
            return []
        sents, brk = split_sentences(text)
        n = len(sents)
        if n < min_sents:
            if len(text) <= max_chunk_chars:
                return [make_chunk(0, name, text, is_whole_doc=True)]
            return ChunkingStrategies.sentence_boundary(text, 120, 1, name)
        bows = [Counter(tokenize(s)) for s in sents]
        sims: List[float] = []
        for i in range(1, n):
            left, right = Counter(), Counter()
            for b in bows[max(0, i - block):i]:
                left.update(b)
            for b in bows[i:i + block]:
                right.update(b)
            sims.append(cosine(left, right))
        mean = sum(sims) / len(sims)
        std = math.sqrt(sum((x - mean) ** 2 for x in sims) / len(sims))
        cutoff = mean - k * std
        cuts = []
        for g in range(len(sims)):
            ls = sims[g - 1] if g > 0 else float("inf")
            rs = sims[g + 1] if g + 1 < len(sims) else float("inf")
            if sims[g] < cutoff and sims[g] <= ls and sims[g] <= rs:
                cuts.append(g + 1)
        bounds = [0]
        for c in cuts:
            if c - bounds[-1] >= min_seg_sents and n - c >= min_seg_sents:
                bounds.append(c)
        bounds.append(n)
        chunks, idx = [], 0
        for a, b in zip(bounds[:-1], bounds[1:]):
            body = join_range(sents, brk, a, b)
            if len(body) > max_chunk_chars:
                for sc in ChunkingStrategies.sentence_boundary(body, 120, 0, name):
                    chunks.append(make_chunk(idx, name, sc["body"]))
                    idx += 1
            else:
                chunks.append(make_chunk(idx, name, body))
                idx += 1
        return chunks


def build_strategy_registry(include_sweep: bool = True) -> List[Dict[str, Any]]:
    """Danh sách chiến lược: 9 chiến lược chính + các biến thể tham số (sweep).

    Tham số `include_sweep`:
      True  -> thêm 12 biến thể (dùng để tìm hyperparameter tốt nhất)
      False -> chỉ chạy 9 chiến lược chính (nhanh hơn khi test)
    """
    S = ChunkingStrategies
    reg: List[Dict[str, Any]] = []

    def add(key: str, fn: Callable[[str, str], List[Dict[str, Any]]], params: str, primary: bool):
        reg.append({"key": key, "fn": fn, "params": params, "primary": primary})

    # ---- 9 chiến lược chính ----
    add("1_Fixed_Char", lambda t, ti: S.fixed_char(t, 500, 50, "1_Fixed_Char"), "size=500 overlap=50", True)
    add("2_Fixed_Word", lambda t, ti: S.fixed_word(t, 120, 20, "2_Fixed_Word"), "words=120 overlap=20", True)
    add("3_Sentence_Boundary", lambda t, ti: S.sentence_boundary(t, 140, 1, "3_Sentence_Boundary"),
        "max_words=140 overlap=1 câu", True)
    add("4_Recursive_Markdown", lambda t, ti: S.recursive_structure(t, 650, 150, "4_Recursive_Markdown"),
        "max_chars=650 min_chars=150", True)
    add("5_Semantic_Context_Injected",
        lambda t, ti: S.semantic_context(t, ti, 800, 650, False, "5_Semantic_Context_Injected"),
        "no_chunk<=800 max_chars=650 prefix từ chunk 2", True)
    add("6_Whole_Document", lambda t, ti: S.whole_document(t, "6_Whole_Document"), "không chia", True)
    add("7_Parent_Child", lambda t, ti: S.parent_child(t, 60, "7_Parent_Child"), "child=60 từ", True)
    add("8_Sentence_Window", lambda t, ti: S.sentence_window(t, 4, 2, "8_Sentence_Window"),
        "window=4 stride=2", True)
    add("9_TextTiling_Semantic", lambda t, ti: S.texttiling(t, name="9_TextTiling_Semantic"),
        "block=3 k=0.5 max=900", True)

    # ---- Biến thể sweep (dùng để tìm hyperparameter) ----
    if include_sweep:
        add("1b_Fixed_Char_300", lambda t, ti: S.fixed_char(t, 300, 30, "1b_Fixed_Char_300"), "size=300", False)
        add("1c_Fixed_Char_900", lambda t, ti: S.fixed_char(t, 900, 90, "1c_Fixed_Char_900"), "size=900", False)
        add("3b_Sentence_80w", lambda t, ti: S.sentence_boundary(t, 80, 1, "3b_Sentence_80w"), "max_words=80", False)
        add("3c_Sentence_220w", lambda t, ti: S.sentence_boundary(t, 220, 1, "3c_Sentence_220w"), "max_words=220", False)
        add("4b_Recursive_450", lambda t, ti: S.recursive_structure(t, 450, 100, "4b_Recursive_450"), "max_chars=450", False)
        add("4c_Recursive_1000", lambda t, ti: S.recursive_structure(t, 1000, 200, "4c_Recursive_1000"), "max_chars=1000", False)
        add("4d_Recursive_250", lambda t, ti: S.recursive_structure(t, 250, 60, "4d_Recursive_250"),
            "max_chars=250 min_chars=60 (cho domain ngắn)", False)
        add("5b_Semantic_thr1200_max900",
            lambda t, ti: S.semantic_context(t, ti, 1200, 900, False, "5b_Semantic_thr1200_max900"),
            "no_chunk<=1200 max=900", False)
        add("5c_Semantic_thr500_max400",
            lambda t, ti: S.semantic_context(t, ti, 500, 400, False, "5c_Semantic_thr500_max400"),
            "no_chunk<=500 max=400", False)
        add("5d_Semantic_prefix_all",
            lambda t, ti: S.semantic_context(t, ti, 800, 650, True, "5d_Semantic_prefix_all"),
            "prefix cho mọi chunk (kể cả chunk 1)", False)
        add("5e_Adaptive_Hybrid",
            lambda t, ti: S.semantic_context(t, ti, 1000, 750, False, "5e_Adaptive_Hybrid"),
            "no_chunk<=1000 max=750", False)
        add("8b_Sentence_Window_6_3", lambda t, ti: S.sentence_window(t, 6, 3, "8b_Sentence_Window_6_3"),
            "window=6 stride=3", False)
    return reg


# ===========================================================================
# 2. Đánh giá chất lượng từng chunk (dựa trên vị trí thật trong tài liệu gốc)
# ===========================================================================
def _starts_clean(T: str, s: int) -> bool:
    i = s - 1
    while i >= 0 and T[i] == " ":
        i -= 1
    return i < 0 or T[i] in SENT_END_CHARS or T[i] == PARA_MARK


def _ends_clean(T: str, e: int) -> bool:
    if e <= 0:
        return True
    if T[e - 1] in SENT_END_CHARS:
        return True
    j = e
    while j < len(T) and T[j] == " ":
        j += 1
    return j >= len(T) or T[j] == PARA_MARK


class ChunkQualityEvaluator:
    @staticmethod
    def analyze_chunk(chunk: Dict[str, Any], doc_marked: str, doc_flat: str, idx: int) -> Dict[str, Any]:
        body = chunk.get("body", chunk["content"]).strip()
        prefix = chunk.get("prefix", "")
        content = chunk["content"]
        res: Dict[str, Any] = {
            "char_len": len(content), "word_count": len(content.split()),
            "est_tokens": est_tokens(content), "located": False, "is_whole_doc": False,
            "starts_mid": False, "ends_mid": False, "dangling_raw": False,
            "dangling_unresolved": False, "dangling_connector": False, "trailing_heading": False,
            "undersized": False, "oversized_chars": False, "over_token_limit": False,
            "issues": [], "quality_score": 0.0,
        }
        if not body:
            res["issues"].append("empty_chunk")
            return res

        # --- định vị chunk trong tài liệu gốc ---
        nb = normalize_with_marks(body)
        loc: Optional[Tuple[str, int, int]] = None
        p = doc_marked.find(nb)
        if p >= 0:
            loc = (doc_marked, p, p + len(nb))
        else:
            nf = normalize_flat(body)
            p = doc_flat.find(nf)
            if p >= 0:
                loc = (doc_flat, p, p + len(nf))

        if loc is not None:
            T, s, e = loc
            res["located"] = True
            res["start"], res["end"] = s, e
            res["is_whole_doc"] = (s == 0 and e >= len(T))
            res["starts_mid"] = not _starts_clean(T, s)
            res["ends_mid"] = not _ends_clean(T, e)
            is_continuation = s > 0
            if T is doc_marked and PARA_MARK in nb and e < len(T):
                j = e
                while j < len(T) and T[j] == " ":
                    j += 1
                last_seg = nb.rsplit(PARA_MARK, 1)[-1].strip()
                if j < len(T) and T[j] == PARA_MARK and looks_like_heading(last_seg):
                    res["trailing_heading"] = True
        else:
            res["starts_mid"] = body[0].islower() or body[0] in ",;:!?)]./\\"
            res["ends_mid"] = body[-1] not in SENT_END_CHARS
            is_continuation = idx > 0

        # --- đại từ / liên từ mồ côi ---
        if is_continuation:
            toks = [w.lower().strip(".,;:\"'([{)]}") for w in body.split()[:2]]
            t0 = toks[0] if toks else ""
            t01 = " ".join(toks)
            orphan = t0 in PRONOUN_ORPHANS or t01 in PHRASE_ORPHANS
            res["dangling_raw"] = orphan
            resolved = bool(prefix) and len(prefix.split()) >= 3
            res["dangling_unresolved"] = orphan and not resolved
            res["dangling_connector"] = t0 in CONTINUATION_STARTERS

        # --- kích thước ---
        res["undersized"] = len(body) < UNDERSIZED_CHARS and not res["is_whole_doc"]
        res["oversized_chars"] = len(content) > OVERSIZED_CHARS
        res["over_token_limit"] = res["est_tokens"] > EMBED_TOKEN_LIMIT

        issues = res["issues"]
        score = 100.0
        if res["starts_mid"]:
            score -= 25; issues.append("starts_mid_sentence")
        if res["ends_mid"]:
            score -= 20; issues.append("ends_mid_sentence")
        if res["dangling_unresolved"]:
            score -= 30; issues.append("dangling_pronoun")
        elif res["dangling_raw"]:
            score -= 8; issues.append("dangling_pronoun_mitigated_by_prefix")
        if res["dangling_connector"]:
            score -= 10; issues.append("starts_with_connector")
        if res["trailing_heading"]:
            score -= 15; issues.append("trailing_heading_orphan")
        if res["undersized"]:
            score -= 25; issues.append("undersized")
        if res["over_token_limit"]:
            score -= 20; issues.append("over_embedding_token_limit")
        elif res["oversized_chars"]:
            score -= 10; issues.append("oversized_chars")
        if not res["located"]:
            issues.append("unlocated(heuristic)")
        res["quality_score"] = max(0.0, score)
        return res


FLAG_KEYS = [
    "starts_mid", "ends_mid", "dangling_raw", "dangling_unresolved", "dangling_connector",
    "trailing_heading", "undersized", "oversized_chars", "over_token_limit",
]


def evaluate_strategy(fn: Callable[[str, str], List[Dict[str, Any]]], docs: List[Dict[str, Any]],
                      worst_cap: int = 6000) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Đánh giá chất lượng chunk trên mẫu tài liệu.

    Tham số:
      worst_cap: số chunk tệ nhất tối đa giữ lại để xuất file soi (6000)
    """
    counts: Counter = Counter()
    lens: List[int] = []
    scores: List[float] = []
    n_chunks = n_docs = docs_split = unlocated = 0
    body_chars = prefix_chars = doc_chars = 0
    worst: List[Dict[str, Any]] = []

    for d in docs:
        text = d["text"].strip()
        if not text:
            continue
        doc_marked, doc_flat = normalize_with_marks(text), normalize_flat(text)
        chunks = fn(text, d.get("title", ""))
        if not chunks:
            continue
        n_docs += 1
        doc_chars += len(doc_flat)
        if len(chunks) > 1:
            docs_split += 1
        for idx, c in enumerate(chunks):
            q = ChunkQualityEvaluator.analyze_chunk(c, doc_marked, doc_flat, idx)
            n_chunks += 1
            lens.append(q["char_len"])
            scores.append(q["quality_score"])
            body_chars += len(c.get("body", ""))
            prefix_chars += len(c.get("prefix", ""))
            for k in FLAG_KEYS:
                if q[k]:
                    counts[k] += 1
            if not q["located"]:
                unlocated += 1
            if q["quality_score"] < 80 and len(worst) < worst_cap:
                worst.append({
                    "doc_id": d["doc_id"], "chunk_id": idx, "n_chunks_in_doc": len(chunks),
                    "score": q["quality_score"], "issues": q["issues"], "char_len": q["char_len"],
                    "head": c["content"][:350], "tail": c["content"][-160:],
                })

    n = max(1, n_chunks)
    sl = sorted(lens)
    metrics: Dict[str, Any] = {
        "docs_evaluated": n_docs,
        "total_chunks": n_chunks,
        "expansion_ratio": round(n_chunks / max(1, n_docs), 2),
        "docs_split_pct": round(docs_split / max(1, n_docs) * 100, 2),
        "duplication_ratio": round(body_chars / max(1, doc_chars), 2),
        "prefix_overhead_pct": round(prefix_chars / max(1, body_chars + prefix_chars) * 100, 2),
        "avg_chunk_char_len": round(sum(lens) / n, 1),
        "median_chunk_char_len": quantile(sl, 0.5),
        "p95_chunk_char_len": quantile(sl, 0.95),
        "avg_quality_score": round(sum(scores) / n, 2),
        "unlocated_pct": round(unlocated / n * 100, 2),
    }
    for k in FLAG_KEYS:
        metrics[f"{k}_pct"] = round(counts[k] / n * 100, 2)
    return metrics, worst


# ===========================================================================
# 3. BM25 thuần Python + đo retrieval
# ===========================================================================
class BM25Index:
    """BM25 thuần Python (không cần thư viện ngoài).

    Tham số:
      k1=1.2  : điều khiển độ bão hòa term frequency
      b=0.75  : điều khiển chuẩn hóa theo độ dài document
    """

    def __init__(self, k1: float = 1.2, b: float = 0.75):
        self.k1, self.b = k1, b
        self.postings: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        self.idf: Dict[str, float] = {}
        self.lens: List[int] = []
        self.chunk_doc: List[str] = []
        self.avgdl = 1.0

    def build(self, texts: List[str], doc_ids: List[str]) -> None:
        self.chunk_doc = doc_ids
        for ci, t in enumerate(texts):
            toks = tokenize(t)
            self.lens.append(len(toks))
            for term, tf in Counter(toks).items():
                self.postings[term].append((ci, tf))
        n = max(1, len(texts))
        self.avgdl = max(1.0, sum(self.lens) / n)
        for term, post in self.postings.items():
            df = len(post)
            self.idf[term] = math.log(1 + (n - df + 0.5) / (df + 0.5))

    def search_docs(self, query: str, top_docs: int = 10) -> List[str]:
        """Trả về top-K doc_id (sau khi gộp chunk theo doc, lấy max score)."""
        qt = set(tokenize(query))
        if not qt:
            return []
        scores: Dict[int, float] = defaultdict(float)
        for t in qt:
            post = self.postings.get(t)
            if not post:
                continue
            idf = self.idf[t]
            for ci, tf in post:
                dl = self.lens[ci]
                scores[ci] += idf * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
        doc_scores: Dict[str, float] = {}
        for ci, s in scores.items():
            d = self.chunk_doc[ci]
            if s > doc_scores.get(d, -1.0):
                doc_scores[d] = s
        return [d for d, _ in sorted(doc_scores.items(), key=lambda x: -x[1])[:top_docs]]


def rank_metrics(ranked: List[str], gold: Set[str]) -> Dict[str, float]:
    """Tính nDCG@10, Recall@5, Recall@10, MRR@10 cho một query."""
    rel = [1 if d in gold else 0 for d in ranked[:10]]
    dcg = sum(r / math.log2(i + 2) for i, r in enumerate(rel))
    ideal = sum(1 / math.log2(i + 2) for i in range(min(len(gold), 10)))
    mrr = next((1 / (i + 1) for i, d in enumerate(ranked[:10]) if d in gold), 0.0)
    return {
        "ndcg10": dcg / ideal if ideal else 0.0,
        "recall5": len(set(ranked[:5]) & gold) / len(gold),
        "recall10": len(set(ranked[:10]) & gold) / len(gold),
        "mrr10": mrr,
    }


def evaluate_retrieval(registry: List[Dict[str, Any]], corpus: List[Dict[str, Any]],
                       queries: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    Đo retrieval cho TỪNG chiến lược với 3 mode query:
      - single        : chỉ query hiện tại
      - history       : query + lịch sử hội thoại (nối đầy đủ)
      - random_padded : query + N từ ngẫu nhiên (N = len(history) - len(query))
                        -> baseline để TÁCH lợi ích ngữ nghĩa khỏi thiên lệch độ dài

    Đầu ra cho mỗi chiến lược:
      ndcg10_single/history/random_padded : nDCG@10 từng mode
      ndcg10_semantic_gain = history - random_padded
                          -> nếu ~0 : history chỉ là length bias
                          -> nếu >0 : history thực sự hữu ích
      ndcg10_eff = single + max(0, semantic_gain)
                -> metric dùng trong composite (đã trừ thiên lệch độ dài)
      ndcg10_avg = (single + history)/2 -> chỉ để báo cáo, KHÔNG dùng composite
      n_vocab, vocab_ok_for_pad -> debug baseline
    """
    results: Dict[str, Dict[str, float]] = {}

    for entry in registry:
        t0 = time.time()
        texts: List[str] = []
        owners: List[str] = []
        for d in corpus:
            for c in entry["fn"](d["text"].strip(), d.get("title", "")):
                texts.append(c["content"])
                owners.append(d["doc_id"])
        idx = BM25Index()
        idx.build(texts, owners)
        vocab = list(idx.postings.keys())
        vocab_ok = len(vocab) >= MIN_VOCAB_FOR_PAD

        agg: Dict[str, List[float]] = defaultdict(list)
        for q in queries:
            q_base = q["query"]
            q_hist = q["history_query"]

            # [FIX-2.4] Guard vocab nhỏ -> bỏ random_padded mode
            base_len = len(tokenize(q_base))
            hist_len = len(tokenize(q_hist))
            pad_len = max(0, hist_len - base_len)
            if pad_len > 0 and vocab_ok:
                # [FIX-1.2] Seed theo cặp (strategy_key, qid) -> deterministic
                rng_q = random.Random(_seed_for_pair(entry["key"], q["qid"]))
                pad_words = " ".join(rng_q.choices(vocab, k=min(pad_len, MAX_PAD_WORDS)))
                q_rand = f"{q_base} {pad_words}"
            else:
                q_rand = q_base  # fallback khi vocab nhỏ hoặc không cần pad

            for mode, qtext in (("single", q_base), ("history", q_hist), ("random_padded", q_rand)):
                m = rank_metrics(idx.search_docs(qtext, 10), q["gold"])
                for k, v in m.items():
                    agg[f"{k}_{mode}"].append(v)

        res = {k: round(sum(v) / max(1, len(v)), 4) for k, v in agg.items()}

        # [FIX-1.3] Tách biệt lợi ích ngữ nghĩa khỏi thiên lệch độ dài query
        res["ndcg10_semantic_gain"] = round(
            res["ndcg10_history"] - res["ndcg10_random_padded"], 4
        )

        # [FIX-2.2] Composite dùng nDCG hiệu dụng (đã trừ length bias)
        res["ndcg10_eff"] = round(
            res["ndcg10_single"] + max(0.0, res["ndcg10_semantic_gain"]), 4
        )

        # Giữ avg để minh bạch, nhưng KHÔNG dùng composite
        res["ndcg10_avg"] = round((res["ndcg10_single"] + res["ndcg10_history"]) / 2, 4)
        res["recall10_avg"] = round((res["recall10_single"] + res["recall10_history"]) / 2, 4)

        res["n_vocab"] = len(vocab)
        res["vocab_ok_for_pad"] = vocab_ok
        res["n_queries"] = len(queries)
        res["n_chunks_indexed"] = len(texts)
        results[entry["key"]] = res

        logger.info(
            f"   [retrieval] {entry['key']:<30} "
            f"nDCG(single/hist/rand)={res['ndcg10_single']:.4f}/{res['ndcg10_history']:.4f}/{res['ndcg10_random_padded']:.4f} "
            f"sem_gain={res['ndcg10_semantic_gain']:+.4f} eff={res['ndcg10_eff']:.4f} "
            f"chunks={len(texts)} vocab={len(vocab)} ({time.time() - t0:.1f}s)"
        )
    return results


# ===========================================================================
# 4. Profiler corpus + hội thoại
# ===========================================================================
GOLD_KEYS = ("gold_doc_ids", "supporting_doc_ids", "relevant_doc_ids", "gold_docs", "doc_ids",
             "positive_doc_ids", "gold_passages", "relevant_docs")
QUERY_KEYS = ("query", "question", "utterance", "text", "user_query")
TURN_ID_KEYS = ("query_id", "qid", "turn_id", "id")


def _norm_ids(v: Any) -> List[str]:
    out: List[str] = []
    if isinstance(v, (str, int)):
        return [str(v)]
    if isinstance(v, list):
        for it in v:
            if isinstance(it, dict):
                x = it.get("doc_id") or it.get("id")
                if x is not None:
                    out.append(str(x))
            elif it is not None:
                out.append(str(it))
    return out


class RETECOCorpusProfiler:
    def __init__(self, domain_dir: Path, domain_name: str):
        self.domain_dir = domain_dir
        self.domain_name = domain_name
        self.doc_file = domain_dir / "documents.jsonl"
        self.bench_dev_file = domain_dir / "benchmark_dev.json"
        self.qrels_dev_file = domain_dir / "qrels_dev.txt"

    def load_qrels(self) -> Dict[str, Set[str]]:
        qrels: Dict[str, Set[str]] = defaultdict(set)
        if not self.qrels_dev_file.is_file():
            return qrels
        with open(self.qrels_dev_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                try:
                    if len(parts) >= 4:
                        qid, did, rel = parts[0], parts[2], parts[3]
                    elif len(parts) == 3:
                        qid, did, rel = parts
                    elif len(parts) == 2:
                        qid, did, rel = parts[0], parts[1], "1"
                    else:
                        continue
                    if int(float(rel)) > 0:
                        qrels[qid].add(did)
                except ValueError:
                    continue
        return qrels

    def profile_conversations(self) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Trả về (thống kê, danh sách turn đã chuẩn hóa: query, history_query, gold)."""
        if not self.bench_dev_file.is_file():
            return {"note": "Không tìm thấy benchmark_dev.json"}, []
        with open(self.bench_dev_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            convs = data.get("conversations") or next((v for v in data.values() if isinstance(v, list)), [])
        else:
            convs = data
        if not convs:
            return {"note": "benchmark_dev.json rỗng hoặc sai cấu trúc"}, []

        first = convs[0] if isinstance(convs[0], dict) else {}
        schema = {"conversation_keys": sorted(first.keys())}
        qrels = self.load_qrels()

        turn_counts: List[int] = []
        qlens: List[int] = []
        gold_counts: List[int] = []
        eval_turns: List[Dict[str, Any]] = []
        turns_with_gold_from_qrels = 0

        for ci, c in enumerate(convs):
            if not isinstance(c, dict):
                continue
            conv_id = c.get("conversation_id") or c.get("conv_id") or c.get("id") or ci
            turns = c.get("turns") or c.get("conversation") or c.get("messages") or []
            turns = [t for t in turns if isinstance(t, dict) and t.get("role", "user") in ("user", "human")]
            if ci == 0 and turns:
                schema["turn_keys"] = sorted(turns[0].keys())
            turn_counts.append(len(turns))
            history: List[str] = []
            for ti, t in enumerate(turns):
                q = next((t[k] for k in QUERY_KEYS if isinstance(t.get(k), str)), "")
                qlens.append(len(q.split()))
                gold: List[str] = []
                for k in GOLD_KEYS:
                    if k in t:
                        gold = _norm_ids(t[k])
                        break
                if not gold and qrels:
                    cands = [str(t[k]) for k in TURN_ID_KEYS if t.get(k) is not None]
                    cands += [f"{conv_id}_{ti}", f"{conv_id}_{ti + 1}", f"{conv_id}-{ti}", f"{conv_id}-{ti + 1}"]
                    for cid in cands:
                        if cid in qrels:
                            gold = sorted(qrels[cid])
                            turns_with_gold_from_qrels += 1
                            break
                gold_counts.append(len(gold))
                if q and gold:
                    eval_turns.append({
                        "qid": f"{conv_id}#{ti}", "query": q,
                        "history_query": " ".join(history + [q]), "gold": set(gold),
                    })
                history.append(q)

        n_turns = len(qlens)
        sq = sorted(qlens)
        stats = {
            "schema_detected": schema,
            "total_conversations": len(convs),
            "total_turns": n_turns,
            "turns_with_gold": sum(1 for g in gold_counts if g > 0),
            "turns_gold_from_qrels": turns_with_gold_from_qrels,
            "turns_per_conversation": {
                "min": min(turn_counts) if turn_counts else 0,
                "mean": round(sum(turn_counts) / max(1, len(turn_counts)), 2),
                "max": max(turn_counts) if turn_counts else 0,
            },
            "query_word_length": {
                "min": sq[0] if sq else 0, "median": quantile(sq, 0.5),
                "mean": round(sum(qlens) / max(1, n_turns), 1), "max": sq[-1] if sq else 0,
            },
            "gold_docs_per_turn": {
                "mean": round(sum(gold_counts) / max(1, n_turns), 2),
                "max": max(gold_counts) if gold_counts else 0,
            },
        }
        return stats, eval_turns

    def scan_corpus(self, pool_size: int, gold_ids: Set[str], max_docs: int,
                    rng: random.Random) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Any]]:
        """Đọc streaming toàn bộ corpus (thống kê trên TẤT CẢ tài liệu), đồng thời
        lấy mẫu reservoir ngẫu nhiên và giữ lại các gold docs.

        Tham số:
          pool_size: kích thước pool reservoir (số tài liệu giữ lại để đánh giá chunk)
          max_docs: nếu > 0 thì chỉ đọc tối đa ngần này dòng (dùng để debug nhanh)
        """
        if not self.doc_file.is_file():
            raise FileNotFoundError(f"Không tìm thấy file tài liệu: {self.doc_file}")
        logger.info(f"Đang quét documents.jsonl của domain '{self.domain_name}' ...")

        char_lens: List[int] = []
        word_lens: List[int] = []
        feat = Counter()
        seen_hashes: Set[str] = set()
        pool: List[Dict[str, Any]] = []
        gold_docs: Dict[str, Dict[str, Any]] = {}
        bad_json = empty = dup = 0
        schema_keys: List[str] = []
        total = 0

        with open(self.doc_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if max_docs > 0 and total >= max_docs:
                    break
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    bad_json += 1
                    continue
                if not isinstance(d, dict):
                    bad_json += 1
                    continue
                if total == 0:
                    schema_keys = sorted(d.keys())
                did = doc_id_of(d, total)
                text = doc_text_of(d)
                total += 1
                stripped = text.strip()
                if not stripped:
                    empty += 1
                char_lens.append(len(text))
                words = text.split()
                word_lens.append(len(words))
                h = hashlib.md5(stripped.encode("utf-8", errors="ignore")).hexdigest()
                if h in seen_hashes:
                    dup += 1
                else:
                    seen_hashes.add(h)
                if MARKDOWN_HEADER_REGEX.search(text):
                    feat["headers"] += 1
                if BULLET_REGEX.search(text):
                    feat["bullets"] += 1
                if CODE_BLOCK_REGEX.search(text):
                    feat["code"] += 1
                if URL_REGEX.search(text):
                    feat["urls"] += 1
                if "\n" in stripped:
                    feat["multiline"] += 1
                if stripped:
                    if stripped[0].islower():
                        feat["starts_lower"] += 1
                    if stripped[-1] not in SENT_END_CHARS:
                        feat["no_terminal_punct"] += 1
                    if words and words[0].lower().strip(".,;:\"'") in PRONOUN_ORPHANS:
                        feat["starts_pronoun"] += 1
                if est_tokens(text) > EMBED_TOKEN_LIMIT:
                    feat["over_512_tokens"] += 1

                rec = {"doc_id": did, "text": text, "title": doc_title_of(d)}
                if did in gold_ids:
                    gold_docs[did] = rec
                if len(pool) < pool_size:
                    pool.append(rec)
                else:
                    j = rng.randint(0, total - 1)
                    if j < pool_size:
                        pool[j] = rec

        if total == 0:
            return [], gold_docs, {}
        rng.shuffle(pool)
        sc = sorted(char_lens)
        sw = sorted(word_lens)

        def share_le(x: int) -> float:
            return round(bisect.bisect_right(sc, x) / total * 100, 2)

        edges = [100, 300, 650, 800, 1500, 3000, 6000]
        buckets: Dict[str, float] = {}
        prev = -1
        for e in edges:
            lo = bisect.bisect_right(sc, prev)
            hi = bisect.bisect_right(sc, e)
            buckets[f"{prev + 1}-{e}" if prev >= 0 else f"0-{e}"] = round((hi - lo) / total * 100, 2)
            prev = e
        buckets[f">{edges[-1]}"] = round((total - bisect.bisect_right(sc, edges[-1])) / total * 100, 2)

        stats = {
            "schema_keys": schema_keys,
            "total_documents": total,
            "char_length": {
                "min": sc[0], "p10": quantile(sc, 0.10), "p25": quantile(sc, 0.25),
                "median": quantile(sc, 0.50), "mean": round(sum(sc) / total, 1),
                "p75": quantile(sc, 0.75), "p90": quantile(sc, 0.90), "p95": quantile(sc, 0.95),
                "p99": quantile(sc, 0.99), "max": sc[-1],
            },
            "word_length": {"min": sw[0], "median": quantile(sw, 0.5),
                            "mean": round(sum(sw) / total, 1), "max": sw[-1]},
            "length_buckets_pct": buckets,
            "share_le_chars_pct": {"650": share_le(650), "800": share_le(800),
                                   "1500": share_le(1500), "3000": share_le(3000)},
            "est_tokens_over_512_pct": round(feat["over_512_tokens"] / total * 100, 2),
            "structural_features": {
                "markdown_headers_pct": round(feat["headers"] / total * 100, 2),
                "bullet_lists_pct": round(feat["bullets"] / total * 100, 2),
                "code_snippets_pct": round(feat["code"] / total * 100, 2),
                "contains_urls_pct": round(feat["urls"] / total * 100, 2),
                "multiline_pct": round(feat["multiline"] / total * 100, 2),
            },
            "data_quality": {
                "bad_json_lines": bad_json,
                "empty_docs": empty,
                "duplicate_docs": dup,
                "duplicate_pct": round(dup / total * 100, 2),
                "starts_lowercase_pct": round(feat["starts_lower"] / total * 100, 2),
                "no_terminal_punct_pct": round(feat["no_terminal_punct"] / total * 100, 2),
                "starts_with_pronoun_pct": round(feat["starts_pronoun"] / total * 100, 2),
            },
        }
        return pool, gold_docs, stats


# ===========================================================================
# 5. Xếp hạng & Log quyết định (sinh từ số liệu)
# ===========================================================================
def min_max_norm(vals: List[float]) -> List[float]:
    """Chuẩn hóa min-max; nếu biên độ ~0 thì trả về 1.0 cho tất cả (không phân biệt)."""
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-6:
        return [1.0] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def rank_strategies(comparison: Dict[str, Dict[str, Any]],
                    retrieval: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
    """
    Xếp hạng composite cho từng chiến lược.

    Công thức (CÓ retrieval):
      base_comp = 0.45*nDCG_eff(norm) + 0.20*Recall(norm) + 0.25*Quality(norm) + 0.10*Cost(log_norm)
      final_comp = base_comp * (1 - truncation_penalty)

    Trong đó:
      nDCG_eff = single + max(0, semantic_gain)   -> đã trừ length bias [FIX-2.2]
      Cost     = 1 / (1 + ln(expansion_ratio))    -> thang log
      Penalty  = hàm mượt tại ot=5% → 25%         -> [FIX-2.1]

    Chuẩn hóa min-max: quality/cost/nDCG/recall đều được chuẩn hóa TRONG từng domain,
    nên composite chỉ có ý nghĩa so sánh nội domain (không so sánh liên domain).
    """
    keys = list(comparison.keys())
    if not keys:
        return []

    qualities = [comparison[k]["avg_quality_score"] for k in keys]
    expansions = [comparison[k]["expansion_ratio"] for k in keys]
    over_tokens = [comparison[k].get("over_token_limit_pct", 0.0) for k in keys]

    # Cost: 1/(1+ln(exp)). exp=1 -> 1.0; exp=2 -> 0.59; exp=4 -> 0.42
    costs = [1.0 / (1.0 + math.log(max(1.0, exp))) for exp in expansions]
    q_norm = min_max_norm(qualities)
    c_norm = min_max_norm(costs)

    rows = []
    if retrieval:
        # [FIX-2.2] Dùng nDCG_eff (đã trừ length bias); fallback ndcg10_avg cho backward compat
        ndcgs = [retrieval.get(k, {}).get("ndcg10_eff",
                  retrieval.get(k, {}).get("ndcg10_avg", 0.0)) for k in keys]
        recalls = [retrieval.get(k, {}).get("recall10_avg", 0.0) for k in keys]
        n_norm = min_max_norm(ndcgs)
        r_norm = min_max_norm(recalls)

        w = W_WITH_RETRIEVAL
        for i, k in enumerate(keys):
            base_comp = (w["ndcg"] * n_norm[i]
                         + w["recall"] * r_norm[i]
                         + w["quality"] * q_norm[i]
                         + w["cost"] * c_norm[i])
            tp = truncation_penalty(over_tokens[i])
            comp = base_comp * (1.0 - tp)
            rows.append({
                "key": k,
                "composite": round(comp, 4),
                "base_composite": round(base_comp, 4),
                "trunc_penalty": round(tp, 4),
            })
    else:
        w = W_NO_RETRIEVAL
        for i, k in enumerate(keys):
            base_comp = w["quality"] * q_norm[i] + w["cost"] * c_norm[i]
            tp = truncation_penalty(over_tokens[i])
            comp = base_comp * (1.0 - tp)
            rows.append({
                "key": k,
                "composite": round(comp, 4),
                "base_composite": round(base_comp, 4),
                "trunc_penalty": round(tp, 4),
            })

    rows.sort(key=lambda x: -x["composite"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


DIFF_METRICS = [
    ("tỷ lệ đứt đầu câu", "starts_mid_pct", False, 3.0, "%"),
    ("tỷ lệ đứt đuôi câu", "ends_mid_pct", False, 3.0, "%"),
    ("đại từ mồ côi chưa được giải quyết", "dangling_unresolved_pct", False, 3.0, "%"),
    ("tiêu đề mồ côi cuối chunk", "trailing_heading_pct", False, 2.0, "%"),
    ("chunk quá ngắn (<80 ký tự)", "undersized_pct", False, 5.0, "%"),
    ("chunk vượt giới hạn token embedding", "over_token_limit_pct", False, 2.0, "%"),
    ("điểm chất lượng ngữ nghĩa TB", "avg_quality_score", True, 3.0, ""),
]


def diff_lines(m: Dict[str, Any], w: Dict[str, Any], r: Optional[Dict[str, float]],
               rw: Optional[Dict[str, float]]) -> Tuple[List[str], List[str]]:
    worse, better = [], []
    for label, key, hib, thr, unit in DIFF_METRICS:
        delta = m[key] - w[key]
        bad = (delta < -thr) if hib else (delta > thr)
        good = (delta > thr) if hib else (delta < -thr)
        txt = f"{label}: {m[key]}{unit} (chiến lược chọn: {w[key]}{unit})"
        if bad:
            worse.append(txt)
        elif good:
            better.append(txt)
    if m["expansion_ratio"] >= w["expansion_ratio"] * 1.5 and m["expansion_ratio"] - w["expansion_ratio"] >= 0.3:
        worse.append(f"chi phí index: nở {m['expansion_ratio']}x chunk/tài liệu (chiến lược chọn: {w['expansion_ratio']}x)")
    if r and rw:
        for label, key in (("nDCG_eff", "ndcg10_eff"), ("Recall@10", "recall10_avg")):
            delta = r[key] - rw[key]
            txt = f"{label}: {r[key]:.4f} (chiến lược chọn: {rw[key]:.4f})"
            if delta < -0.01:
                worse.append(txt)
            elif delta > 0.01:
                better.append(txt)
    return worse, better


def generate_decision_rationale_log(domain: str, doc_stats: Dict[str, Any], comparison: Dict[str, Dict[str, Any]],
                                    retrieval: Dict[str, Dict[str, float]], ranking: List[Dict[str, Any]],
                                    registry: List[Dict[str, Any]], retrieval_meta: Dict[str, Any]) -> str:
    L: List[str] = []
    bar = "=" * 80
    sub = "-" * 80
    cl = doc_stats["char_length"]
    primary_keys = [e["key"] for e in registry if e["primary"]]
    params = {e["key"]: e["params"] for e in registry}
    winner = ranking[0]
    wk = winner["key"]
    wm, wr = comparison[wk], retrieval.get(wk) if retrieval else None
    comp_of = {r["key"]: r["composite"] for r in ranking}

    L += [bar, "LOG QUYẾT ĐỊNH KIẾN TRÚC CHUNKING (ADR) - RETECO TRACK 2 (v3)",
          f"DOMAIN: {domain.upper()}   |   Thời điểm: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", bar, ""]

    L += ["1. BỐI CẢNH DỮ LIỆU (đo trên TOÀN BỘ corpus)", sub,
          f"- Số tài liệu: {doc_stats['total_documents']:,} | trùng lặp: {doc_stats['data_quality']['duplicate_pct']}% "
          f"| rỗng: {doc_stats['data_quality']['empty_docs']}",
          f"- Độ dài ký tự: min={cl['min']} p25={cl['p25']} median={cl['median']} mean={cl['mean']} "
          f"p75={cl['p75']} p90={cl['p90']} p95={cl['p95']} p99={cl['p99']} max={cl['max']}",
          f"- Tỷ lệ tài liệu <= 650 / 800 / 1500 / 3000 ký tự: "
          f"{doc_stats['share_le_chars_pct']['650']}% / {doc_stats['share_le_chars_pct']['800']}% / "
          f"{doc_stats['share_le_chars_pct']['1500']}% / {doc_stats['share_le_chars_pct']['3000']}%",
          f"- Tài liệu ước tính vượt {EMBED_TOKEN_LIMIT} token (sẽ bị embedding cắt cụt nếu không chia): "
          f"{doc_stats['est_tokens_over_512_pct']}%",
          f"- Cấu trúc: bullet {doc_stats['structural_features']['bullet_lists_pct']}% | "
          f"nhiều dòng {doc_stats['structural_features']['multiline_pct']}% | "
          f"header {doc_stats['structural_features']['markdown_headers_pct']}%",
          f"- Chất lượng thô: bắt đầu bằng chữ thường {doc_stats['data_quality']['starts_lowercase_pct']}% | "
          f"thiếu dấu câu cuối {doc_stats['data_quality']['no_terminal_punct_pct']}% | "
          f"mở đầu bằng đại từ {doc_stats['data_quality']['starts_with_pronoun_pct']}%", ""]

    L += ["2. PHƯƠNG PHÁP & GIỚI HẠN (đọc trước khi tin kết luận)", sub,
          "- Chất lượng chunk: định vị từng chunk trong tài liệu gốc rồi xét ký tự liền trước/sau để biết "
          "chunk có cắt giữa câu không (không đoán theo chữ hoa/thường).",
          "- Đại từ mồ côi được báo cáo 2 mức: 'raw' (nhìn phần văn bản gốc) và 'unresolved' (sau khi trừ các chunk "
          "có prefix chủ đề >= 3 từ). Việc prefix thật sự giải quyết tham chiếu chỉ là HEURISTIC.",
          f"- Điểm tổng hợp (CÓ retrieval) = "
          "0.45*nDCG_eff(norm) + 0.20*Recall(norm) + 0.25*Quality(norm) + 0.10*Cost(log_norm); "
          "sau đó NHÂN với (1 - truncation_penalty).",
          f"- Điểm tổng hợp (KHÔNG retrieval) = "
          "0.80*Quality(norm) + 0.20*Cost(log_norm); sau đó NHÂN với (1 - truncation_penalty).",
          "- nDCG_eff = nDCG_single + max(0, nDCG_history - nDCG_random_padded): "
          "đã trừ thiên lệch độ dài query (baseline random_padded cùng độ dài).",
          "- Truncation penalty: mượt tuyến tính, 0% tại ot<=5%, 40% tại ot>=25%.",
          "- Cost = 1 / (1 + ln(expansion_ratio)).",
          "- Chuẩn hóa min-max TRONG từng domain: composite chỉ có nghĩa so sánh nội domain, "
          "KHÔNG so sánh liên domain.",
          "- Số token là ƯỚC LƯỢNG (từ x 1.35), không phải token thật của model embedding."]
    if retrieval:
        L += [f"- Retrieval: BM25 (từ vựng) trên corpus con = {retrieval_meta['n_gold_docs']} gold docs + "
              f"{retrieval_meta['n_distractors']} tài liệu nhiễu; {retrieval_meta['n_queries']} query. "
              "Số tuyệt đối bị thổi phồng so với corpus đầy đủ; chỉ nên so SÁNH TƯƠNG ĐỐI giữa các chiến lược. "
              "Chưa đo dense retriever / reranker / chất lượng sinh câu trả lời của LLM."]
    else:
        L += ["- CHƯA có đo retrieval thật (thiếu benchmark/gold hoặc chạy --no-retrieval): xếp hạng chỉ dựa trên "
              "heuristic chất lượng chunk -> độ tin cậy thấp hơn."]
    L += [""]

    L += ["3. BẢNG XẾP HẠNG TỔNG HỢP", sub]
    for r in ranking:
        m = comparison[r["key"]]
        rr = retrieval.get(r["key"]) if retrieval else None
        if rr:
            ret_txt = (f" | nDCG_eff={rr['ndcg10_eff']:.4f} "
                       f"(single={rr['ndcg10_single']:.4f} hist={rr['ndcg10_history']:.4f} "
                       f"rand={rr['ndcg10_random_padded']:.4f} sem_gain={rr['ndcg10_semantic_gain']:+.4f})")
        else:
            ret_txt = ""
        L.append(f"#{r['rank']:<2} {r['key']:<30} composite={r['composite']:.4f} "
                 f"| base={r['base_composite']:.4f} | trunc_pen={r['trunc_penalty']:.3f} "
                 f"| quality={m['avg_quality_score']} | nở={m['expansion_ratio']}x{ret_txt}")
    L += [""]

    L += ["4. PHÂN TÍCH TỪNG CHIẾN LƯỢC CHÍNH "
          "(so với chiến lược được chọn; nếu người thắng là biến thể sweep thì được thêm vào cuối)", sub]
    for key in primary_keys + ([wk] if wk not in primary_keys else []):
        m = comparison[key]
        r = retrieval.get(key) if retrieval else None
        worse, better = diff_lines(m, wm, r, wr)
        gap = winner["composite"] - comp_of[key]
        if key == wk:
            verdict = "ĐƯỢC CHỌN (composite cao nhất)"
        elif gap < 0.01:
            verdict = f"NGANG HÀNG (chênh {gap:.4f}) - có thể dùng làm phương án dự phòng"
        else:
            verdict = f"KHÔNG CHỌN (kém {gap:.4f} điểm composite)"
        L += [f"[{key}]  params: {params[key]}", f"  KẾT LUẬN: {verdict}",
              f"  Đo được: quality={m['avg_quality_score']} | đứt đầu={m['starts_mid_pct']}% | đứt đuôi={m['ends_mid_pct']}% "
              f"| đại từ mồ côi raw/unresolved={m['dangling_raw_pct']}%/{m['dangling_unresolved_pct']}% "
              f"| tiêu đề mồ côi={m['trailing_heading_pct']}% | quá ngắn={m['undersized_pct']}% "
              f"| >512 token={m['over_token_limit_pct']}% | nở={m['expansion_ratio']}x "
              f"| tài liệu bị chia={m['docs_split_pct']}%"]
        if r:
            L.append(f"  Retrieval: nDCG_eff={r['ndcg10_eff']:.4f} "
                     f"(single={r['ndcg10_single']:.4f} hist={r['ndcg10_history']:.4f} rand={r['ndcg10_random_padded']:.4f}) "
                     f"| semantic_gain={r['ndcg10_semantic_gain']:+.4f}")
            L.append(f"           : Recall@10 single/history={r['recall10_single']:.4f}/{r['recall10_history']:.4f} "
                     f"| MRR@10 single/history={r['mrr10_single']:.4f}/{r['mrr10_history']:.4f} "
                     f"| vocab_ok={r['vocab_ok_for_pad']}")
        if key != wk:
            if worse:
                L.append("  Điểm yếu đo được so với chiến lược chọn:")
                L += [f"    - {x}" for x in worse]
            if better:
                L.append("  Điểm mạnh đo được so với chiến lược chọn:")
                L += [f"    + {x}" for x in better]
            if not worse and not better:
                L.append("  Không có khác biệt đáng kể theo các ngưỡng đã đặt.")
        L.append(f"  Lý thuyết (không phải số đo): {THEORY_NOTES.get(key, '')}")
        L.append("")

    L += ["5. QUYẾT ĐỊNH", sub, f"-> Chiến lược được chọn cho domain '{domain}': {wk} ({params[wk]})"]
    runner = ranking[1] if len(ranking) > 1 else None
    if runner:
        L.append(f"-> Á quân: {runner['key']} (composite {runner['composite']:.4f}, "
                 f"kém {winner['composite'] - runner['composite']:.4f})")
        if winner["composite"] - runner["composite"] < 0.01:
            L.append("   !! Chênh lệch < 0.01: coi như HÒA, nên kiểm chứng thêm bằng "
                     "dense retriever / LLM judge trước khi chốt.")
    hypo = "5_Semantic_Context_Injected"
    if wk != hypo and hypo in comp_of:
        L.append(f"-> Lưu ý: giả thuyết ban đầu ({hypo}) xếp hạng "
                 f"#{[r['key'] for r in ranking].index(hypo) + 1}, "
                 "dữ liệu KHÔNG ủng hộ nó là tối ưu cho domain này.")
    L += ["", "Gợi ý hành động dựa trên số đo:"]
    if doc_stats["share_le_chars_pct"]["800"] >= 70:
        L.append(f"- {doc_stats['share_le_chars_pct']['800']}% tài liệu <= 800 ký tự: "
                 "nên giữ nguyên tài liệu ngắn (không chia).")
    if doc_stats["est_tokens_over_512_pct"] > 1:
        L.append(f"- {doc_stats['est_tokens_over_512_pct']}% tài liệu vượt ~512 token: "
                 "bắt buộc chia hoặc dùng model embedding context dài.")
    if doc_stats["data_quality"]["duplicate_pct"] > 1:
        L.append("- Có tài liệu trùng lặp: cân nhắc khử trùng trước khi index.")
    if doc_stats["data_quality"]["starts_with_pronoun_pct"] > 2:
        L.append("- Nhiều tài liệu tự thân mở đầu bằng đại từ: cần context/tiêu đề ngay cả khi không chia.")
    L.append("- Mở file chunk_inspection_<domain>.md để đọc trực tiếp các chunk tệ nhất của từng chiến lược trước khi chốt.")
    L += ["", bar]
    return "\n".join(L)


# ===========================================================================
# 6. Báo cáo Markdown + file soi chunk
# ===========================================================================
def flag_str(q: Dict[str, Any]) -> str:
    return "✅" if not q["issues"] else "⚠ " + ", ".join(q["issues"])


def build_markdown_report(domain: str, doc_stats: Dict[str, Any], conv_stats: Dict[str, Any],
                          comparison: Dict[str, Dict[str, Any]], retrieval: Dict[str, Dict[str, float]],
                          ranking: List[Dict[str, Any]], registry: List[Dict[str, Any]],
                          case_studies: List[Dict[str, Any]], retrieval_meta: Dict[str, Any]) -> str:
    md: List[str] = []
    cl = doc_stats["char_length"]
    md.append(f"# Báo cáo EDA & đánh giá Chunking — domain `{domain}`")
    md.append(f"\n*Tạo lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | RETECO Track 2 (v3)*\n")

    md.append("## 1. Corpus\n")
    md.append(f"- Tổng tài liệu: **{doc_stats['total_documents']:,}** | schema: `{', '.join(doc_stats['schema_keys'])}`")
    md.append(f"- Ký tự: min={cl['min']}, p25={cl['p25']}, **median={cl['median']}**, mean={cl['mean']}, "
              f"p75={cl['p75']}, p90={cl['p90']}, p95={cl['p95']}, p99={cl['p99']}, max={cl['max']}")
    md.append(f"- Từ: median={doc_stats['word_length']['median']}, mean={doc_stats['word_length']['mean']}, "
              f"max={doc_stats['word_length']['max']}")
    md.append(f"- Ước tính vượt {EMBED_TOKEN_LIMIT} token: **{doc_stats['est_tokens_over_512_pct']}%**")
    md.append("\n**Histogram độ dài (ký tự):**\n")
    md.append("| Khoảng | % tài liệu |\n| :--- | ---: |")
    for k, v in doc_stats["length_buckets_pct"].items():
        md.append(f"| {k} | {v}% |")
    sf, dq = doc_stats["structural_features"], doc_stats["data_quality"]
    md.append(f"\n- Cấu trúc: header {sf['markdown_headers_pct']}% | bullet {sf['bullet_lists_pct']}% | "
              f"code {sf['code_snippets_pct']}% | URL {sf['contains_urls_pct']}% | nhiều dòng {sf['multiline_pct']}%")
    md.append(f"- Chất lượng dữ liệu: trùng {dq['duplicate_pct']}% | rỗng {dq['empty_docs']} | JSON lỗi {dq['bad_json_lines']} | "
              f"bắt đầu chữ thường {dq['starts_lowercase_pct']}% | thiếu dấu câu cuối {dq['no_terminal_punct_pct']}% | "
              f"mở đầu bằng đại từ {dq['starts_with_pronoun_pct']}%\n")

    md.append("## 2. Hội thoại Track 2\n")
    if conv_stats.get("total_conversations"):
        md.append(f"- Hội thoại: **{conv_stats['total_conversations']}** | lượt: **{conv_stats['total_turns']}** | "
                  f"lượt có gold: {conv_stats['turns_with_gold']}")
        t = conv_stats["turns_per_conversation"]
        md.append(f"- Lượt/hội thoại: mean={t['mean']} (min {t['min']}, max {t['max']})")
        q = conv_stats["query_word_length"]
        md.append(f"- Độ dài query: mean={q['mean']} từ, median={q['median']}, max={q['max']}")
        g = conv_stats["gold_docs_per_turn"]
        md.append(f"- Gold docs/lượt: mean={g['mean']}, max={g['max']}")
        md.append(f"- Schema dò được: `{json.dumps(conv_stats['schema_detected'], ensure_ascii=False)}`\n")
    else:
        md.append(f"- {conv_stats.get('note', 'Không có dữ liệu hội thoại')}\n")

    md.append("## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)\n")
    md.append("| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | "
              "Tiêu đề mồ côi | <80c | >512tok | Quality |")
    md.append("| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for e in registry:
        m = comparison[e["key"]]
        tag = "**" if e["primary"] else ""
        md.append(f"| {tag}{e['key']}{tag} | {m['expansion_ratio']}x | {m['avg_chunk_char_len']} | "
                  f"{m['starts_mid_pct']}% | {m['ends_mid_pct']}% | {m['dangling_raw_pct']}% | "
                  f"{m['dangling_unresolved_pct']}% | {m['trailing_heading_pct']}% | {m['undersized_pct']}% | "
                  f"{m['over_token_limit_pct']}% | **{m['avg_quality_score']}** |")
    md.append("\n> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. "
              "'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.\n")

    md.append("## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)\n")
    if retrieval:
        md.append(f"Corpus con: {retrieval_meta['n_gold_docs']} gold + {retrieval_meta['n_distractors']} nhiễu | "
                  f"{retrieval_meta['n_queries']} query. **Chỉ so sánh tương đối.**\n")
        md.append("**Định nghĩa các cột:**")
        md.append("- `nDCG single` : chỉ query hiện tại")
        md.append("- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại")
        md.append("- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)")
        md.append("- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)")
        md.append("- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite\n")
        md.append("| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |")
        md.append("| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for e in registry:
            r = retrieval.get(e["key"])
            if r:
                sem = r["ndcg10_semantic_gain"]
                sem_marker = "" if abs(sem) < 0.01 else (" 🔼" if sem > 0 else " 🔽")
                md.append(f"| {e['key']} | {r['ndcg10_single']:.4f} | {r['ndcg10_history']:.4f} | "
                          f"{r['ndcg10_random_padded']:.4f} | {sem:+.4f}{sem_marker} | "
                          f"**{r['ndcg10_eff']:.4f}** | "
                          f"{r['recall5_history']:.4f} | {r['recall10_single']:.4f} | {r['recall10_history']:.4f} | "
                          f"{r['mrr10_history']:.4f} | {r['n_chunks_indexed']} |")
        md.append("\n> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại "
                  "KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, "
                  "không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.\n")
    else:
        md.append("_Không chạy được đo retrieval (thiếu gold/benchmark hoặc dùng --no-retrieval)._\n")

    md.append("## 5. Xếp hạng tổng hợp\n")
    md.append("**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` "
              "→ nhân `(1 - trunc_penalty)`\n")
    md.append("| Hạng | Chiến lược | Composite | Base | Trunc penalty |\n| ---: | :--- | ---: | ---: | ---: |")
    for r in ranking[:15]:
        md.append(f"| {r['rank']} | {r['key']} | **{r['composite']:.4f}** | {r['base_composite']:.4f} | "
                  f"{r['trunc_penalty']:.3f} |")
    md.append(f"\n**Chiến lược được chọn: `{ranking[0]['key']}`** "
              f"(xem log ADR để biết lý do chi tiết, sinh từ số đo).\n")

    md.append("> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** "
              "(vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở "
              "`earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó "
              "vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.\n")

    md.append("## 6. Case studies (từng chunk có gắn cờ lỗi)\n")
    for cs in case_studies:
        md.append(f"### `{cs['doc_id']}` — {cs['char_len']} ký tự\n")
        md.append(f"```text\n{cs['original_snippet']}\n```\n")
        for s_name, items in cs["strategy_slices"].items():
            md.append(f"- **{s_name}** ({len(items)} chunks)")
            for c, q in items[:3]:
                prev = c["content"].replace("\n", " ")
                prev = prev[:140] + ("..." if len(prev) > 140 else "")
                md.append(f"  - `[{c['chunk_id']}]` {c['char_len']}c {flag_str(q)} — *\"{prev}\"*")
            if len(items) > 3:
                md.append(f"  - *(... {len(items) - 3} chunk nữa — xem chunk_inspection)*")
        md.append("\n---\n")

    md.append("## 7. Giới hạn của phân tích\n")
    md.append("- Heuristic không thay được đánh giá của người: hãy đọc `chunk_inspection_*.md`.")
    md.append("- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.")
    md.append("- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.")
    md.append("- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.")
    return "\n".join(md)


def build_inspection_report(domain: str, worst: Dict[str, List[Dict[str, Any]]],
                            case_studies: List[Dict[str, Any]], registry: List[Dict[str, Any]],
                            worst_n: int, rng: random.Random) -> str:
    md = [f"# Soi chi tiết từng chunk — domain `{domain}`\n",
          f"*Mỗi chiến lược chính: {worst_n} chunk tệ nhất (điểm thấp nhất, lấy mẫu ngẫu nhiên khi hòa).*\n"]
    for e in registry:
        if not e["primary"]:
            continue
        items = worst.get(e["key"], [])
        rng.shuffle(items)
        items = sorted(items, key=lambda x: x["score"])[:worst_n]
        md.append(f"## {e['key']}  ({e['params']})\n")
        if not items:
            md.append("_Không có chunk nào điểm < 80._\n")
            continue
        for it in items:
            md.append(f"**doc `{it['doc_id']}` chunk {it['chunk_id']}/{it['n_chunks_in_doc'] - 1}** — "
                      f"score {it['score']} — {it['char_len']}c — `{', '.join(it['issues'])}`")
            md.append(f"```text\n{it['head']}\n ...\n{it['tail']}\n```")
    md.append("\n# Case studies (toàn văn từng chunk)\n")
    for cs in case_studies:
        md.append(f"## Tài liệu `{cs['doc_id']}` ({cs['char_len']} ký tự)\n")
        md.append(f"```text\n{cs['full_text'][:6000]}\n```\n")
        for s_name, items in cs["strategy_slices"].items():
            md.append(f"### {s_name} — {len(items)} chunks\n")
            for c, q in items:
                md.append(f"**[{c['chunk_id']}]** {c['char_len']}c | quality {q['quality_score']} | {flag_str(q)}")
                md.append(f"```text\n{c['content']}\n```")
    return "\n".join(md)


# ===========================================================================
# 7. Orchestrator
# ===========================================================================
def default_data_dir() -> str:
    cands = [os.environ.get("RETECO_DATA_DIR"), "D:/reteco/reteco_data", str(PROJECT_ROOT / "reteco_data"),
             str(PROJECT_ROOT.parent / "reteco_data"), "reteco_data", "../reteco_data"]
    for c in cands:
        if c and os.path.isdir(c):
            return c
    return "D:/reteco/reteco_data"


def find_domains(data_dir: str) -> Tuple[Path, List[str]]:
    base = Path(data_dir)
    root = base / "track2_recor" if (base / "track2_recor").is_dir() else base
    if not root.is_dir():
        logger.error(f"Thư mục dữ liệu không tồn tại: {root}")
        sys.exit(1)
    doms = sorted(d.name for d in root.iterdir() if d.is_dir() and (d / "documents.jsonl").is_file())
    return root, doms


def run_domain(root: Path, dom: str, args: argparse.Namespace, reports_path: Path) -> Dict[str, Any]:
    rng = random.Random(args.seed)
    profiler = RETECOCorpusProfiler(root / dom, dom)

    # 1) hội thoại (cần trước để biết gold ids)
    conv_stats, eval_turns = profiler.profile_conversations()
    if conv_stats.get("schema_detected"):
        logger.info(f"Schema hội thoại dò được: {conv_stats['schema_detected']}")
    gold_ids: Set[str] = set()
    for t in eval_turns:
        gold_ids |= t["gold"]

    # 2) corpus
    registry = build_strategy_registry(include_sweep=not args.no_sweep)
    pool_size = max(args.sample_size if args.sample_size > 0 else 10 ** 9, args.retrieval_distractors)
    pool, gold_docs, doc_stats = profiler.scan_corpus(pool_size, gold_ids, args.max_docs, rng)
    if not pool:
        logger.warning(f"Bỏ qua domain {dom}: không có tài liệu.")
        return {}
    logger.info(f"Corpus: {doc_stats['total_documents']:,} docs | median {doc_stats['char_length']['median']} ký tự | "
                f"<=800c: {doc_stats['share_le_chars_pct']['800']}% | gold docs tìm thấy: {len(gold_docs)}/{len(gold_ids)}")

    # 3) chất lượng chunk trên mẫu
    sample = pool if args.sample_size <= 0 else pool[:args.sample_size]
    comparison: Dict[str, Dict[str, Any]] = {}
    worst: Dict[str, List[Dict[str, Any]]] = {}
    logger.info(f"Đánh giá chất lượng chunk: {len(registry)} chiến lược x {len(sample)} tài liệu ...")
    for e in registry:
        t0 = time.time()
        m, w = evaluate_strategy(e["fn"], sample)
        comparison[e["key"]] = m
        worst[e["key"]] = w
        logger.info(f"   [quality] {e['key']:<30} quality={m['avg_quality_score']:<6} chunks={m['total_chunks']:<6} "
                    f"({time.time() - t0:.1f}s)")

    # 4) retrieval
    retrieval: Dict[str, Dict[str, float]] = {}
    retrieval_meta: Dict[str, Any] = {}
    if not args.no_retrieval:
        queries = []
        for t in eval_turns:
            g = {x for x in t["gold"] if x in gold_docs}
            if g:
                queries.append({**t, "gold": g})
        if len(queries) > args.max_queries:
            queries = rng.sample(queries, args.max_queries)
        if queries:
            used_gold: Set[str] = set()
            for q in queries:
                used_gold |= q["gold"]
            corpus = [gold_docs[g] for g in sorted(used_gold)]
            distractors = [d for d in pool if d["doc_id"] not in used_gold][:args.retrieval_distractors]
            corpus += distractors
            retrieval_meta = {"n_gold_docs": len(used_gold), "n_distractors": len(distractors),
                              "n_queries": len(queries)}
            logger.info(f"Đo retrieval BM25: {len(queries)} query, corpus con {len(corpus)} docs ...")
            retrieval = evaluate_retrieval(registry, corpus, queries)
        else:
            logger.warning("Không tìm được query có gold docs hợp lệ -> bỏ qua đo retrieval. "
                           "Kiểm tra 'schema_detected' ở trên và tên trường gold trong benchmark_dev.json.")

    # 5) xếp hạng
    ranking = rank_strategies(comparison, retrieval)
    logger.info(f"=> Chiến lược xếp #1 cho '{dom}': {ranking[0]['key']} (composite {ranking[0]['composite']})")

    # 6) case studies
    sorted_docs = sorted(sample, key=lambda x: len(x["text"]))
    n = len(sorted_docs)
    picks, seen_ids = [], set()
    for i in (n // 10, n // 2, int(0.95 * n), n - 1):
        d = sorted_docs[min(max(i, 0), n - 1)]
        if d["doc_id"] not in seen_ids:
            seen_ids.add(d["doc_id"])
            picks.append(d)
    case_studies = []
    for d in picks:
        text = d["text"].strip()
        doc_marked, doc_flat = normalize_with_marks(text), normalize_flat(text)
        slices: Dict[str, List[Tuple[Dict[str, Any], Dict[str, Any]]]] = {}
        for e in registry:
            if not e["primary"]:
                continue
            chunks = e["fn"](text, d.get("title", ""))
            slices[e["key"]] = [(c, ChunkQualityEvaluator.analyze_chunk(c, doc_marked, doc_flat, i))
                                for i, c in enumerate(chunks)]
        case_studies.append({
            "doc_id": d["doc_id"], "char_len": len(text),
            "original_snippet": text[:500] + ("..." if len(text) > 500 else ""),
            "full_text": text, "strategy_slices": slices,
        })

    # 7) xuất file
    log_text = generate_decision_rationale_log(dom, doc_stats, comparison, retrieval, ranking, registry, retrieval_meta)
    (reports_path / f"chunking_decision_rationale_{dom}.log").write_text(log_text, encoding="utf-8")
    md = build_markdown_report(dom, doc_stats, conv_stats, comparison, retrieval, ranking, registry,
                               case_studies, retrieval_meta)
    (reports_path / f"eda_report_{dom}.md").write_text(md, encoding="utf-8")
    insp = build_inspection_report(dom, worst, case_studies, registry, args.worst_n, rng)
    (reports_path / f"chunk_inspection_{dom}.md").write_text(insp, encoding="utf-8")
    payload = {
        "domain": dom, "generated_at": datetime.now().isoformat(timespec="seconds"),
        "args": {k: v for k, v in vars(args).items()},
        "document_statistics": doc_stats, "conversation_statistics": conv_stats,
        "chunking_comparison": comparison, "retrieval": retrieval, "retrieval_meta": retrieval_meta,
        "ranking": ranking,
    }
    (reports_path / f"eda_metrics_{dom}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"Đã ghi 4 file báo cáo cho '{dom}' vào {reports_path}")
    return {"domain": dom, "winner": ranking[0]["key"], "composite": ranking[0]["composite"],
            "median_chars": doc_stats["char_length"]["median"], "docs": doc_stats["total_documents"]}


def run_eda(args: argparse.Namespace) -> None:
    reports_path = Path(args.reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)
    root, available = find_domains(args.data_dir)
    if not available:
        logger.error(f"Không có domain nào chứa documents.jsonl trong {root}")
        sys.exit(1)
    if args.domain.lower() == "all":
        targets = available
    elif args.domain in available:
        targets = [args.domain]
    else:
        logger.error(f"Domain '{args.domain}' không có. Các domain hiện có: {available}")
        sys.exit(1)

    logger.info(f"Data root: {root} | domains: {targets} | báo cáo: {reports_path.resolve()}")
    summary = []
    for dom in targets:
        logger.info("=" * 60)
        logger.info(f">>> DOMAIN: {dom}")
        logger.info("=" * 60)
        try:
            res = run_domain(root, dom, args, reports_path)
            if res:
                summary.append(res)
        except Exception as exc:  # không để 1 domain lỗi làm hỏng cả lượt chạy 'all'
            logger.exception(f"Domain '{dom}' lỗi: {exc}")
    if len(summary) > 1:
        lines = ["# Tổng hợp các domain (v3 - composite đã chuẩn hóa min-max NỘI DOMAIN)\n",
                 "> ⚠️ Composite chỉ so sánh được giữa các chiến lược **trong cùng domain**, "
                 "KHÔNG so sánh liên domain.\n",
                 "| Domain | Docs | Median (c) | Chiến lược #1 | Composite |",
                 "| :--- | ---: | ---: | :--- | ---: |"]
        for s in summary:
            lines.append(f"| {s['domain']} | {s['docs']:,} | {s['median_chars']} | {s['winner']} | {s['composite']} |")
        (reports_path / "eda_summary_all.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info(">>> HOÀN THÀNH EDA & PHÂN TÍCH CHUNKING (v3) <<<")


def main() -> None:
    p = argparse.ArgumentParser(description="RETECO Track 2: EDA & Chunking Diagnostic Suite (v3)")
    # ---- Tham số đường dẫn ----
    p.add_argument("--data-dir", default=default_data_dir(), help="Thư mục reteco_data")
    p.add_argument("--reports-dir", default=str(PROJECT_ROOT / "reports" / "eda"), help="Thư mục xuất báo cáo")
    # ---- Tham số domain ----
    p.add_argument("--domain", default="drones", help="Tên domain hoặc 'all'")
    # ---- Tham số chất lượng chunk ----
    p.add_argument("--sample-size", type=int, default=2000,
                   help="Số tài liệu mẫu để đo chunk quality (0 = toàn bộ pool)")
    p.add_argument("--worst-n", type=int, default=25,
                   help="Số chunk tệ nhất mỗi chiến lược trong file soi chunk")
    # ---- Tham số retrieval ----
    p.add_argument("--retrieval-distractors", type=int, default=10000,
                   help="Số distractors trong corpus retrieval (default: 10000)")
    p.add_argument("--max-queries", type=int, default=300,
                   help="Số query tối đa dùng đo retrieval")
    # ---- Tham số corpus scan ----
    p.add_argument("--seed", type=int, default=42, help="Seed cho reservoir sampling và ranking")
    p.add_argument("--max-docs", type=int, default=0,
                   help="Giới hạn đọc documents.jsonl (0 = hết)")
    # ---- Công tắc bật/tắt ----
    p.add_argument("--no-retrieval", action="store_true", help="Bỏ đo retrieval BM25")
    p.add_argument("--no-sweep", action="store_true", help="Bỏ các biến thể tham số (sweep)")
    run_eda(p.parse_args())


if __name__ == "__main__":
    main()