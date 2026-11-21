#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RETECO Track 2 - EDA Chất lượng dữ liệu (Data Quality)

Vị trí file : <project>/scripts/eda/eda_data_quality.py
Báo cáo     : <project>/reports/eda/data_quality/
Biểu đồ     : <project>/reports/eda/data_quality/figures/

Corpus QUÉT MỘT LẦN (streaming) rồi cache. Các pha dùng chung kết quả.
Pha: integrity, content, conversation, gold, link, retrieval, splits, viz

Chạy:
  python eda_data_quality.py --domain all
  python eda_data_quality.py --domain drones --phases integrity,content,gold
  python eda_data_quality.py --domain all --workers 4 --examples 8
  python eda_data_quality.py --skip-eda
  python eda_data_quality.py --domain all --no-cache

Phụ thuộc: numpy, matplotlib.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html as html_lib
import json
import logging
import math
import os
import pickle
import random
import re
import sys
import time
import zlib
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("RETECO_EDA_DQ")

# ---------------------------------------------------------------------------
# Hằng số
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1] if len(SCRIPT_DIR.parents) >= 2 else SCRIPT_DIR
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "reports" / "eda" / "data_quality"

ALL_PHASES = ["integrity", "content", "conversation", "gold", "link", "retrieval", "splits"]
CACHE_VERSION = "dq3"   # bump khi sửa logic scan/parse

SHORT_CHARS = 50
EMBED_TOKEN_LIMIT_CHARS = 3000
LATE_EVIDENCE_CHARS = 1500
MH_N, MH_BANDS, MH_SHINGLE, MH_MAX_SHINGLES = 64, 16, 5, 1500
MH_P = 2147483647
NEAR_DUP_THRESHOLD = 0.8

SENT_END_CHARS = set(".!?…\"'”’)]»")
TOKEN_RE = re.compile(r"[a-z0-9]+")
URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[\s.\-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s.\-]\d{3,4}[\s.\-]\d{3,4}(?!\d)")
MOJIBAKE_RE = re.compile(r"Ã[\x80-\xbf¡-¿]|â€|Â[\x80-\xbf ]|\ufffd")
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
HTML_RE = re.compile(r"<\s*/?\s*(?:div|span|p|br|a|table|tr|td|ul|li|script|style|img|h[1-6])\b[^>]*>|&(?:[a-z]{2,8}|#\d{2,5});", re.I)
# FIX: bỏ "[edit]" (tiêu đề section Wikipedia, không phải rác)
BOILER_RE = re.compile(r"all rights reserved|cookie|privacy policy|terms of (?:use|service)|click here|"
                       r"subscribe to|sign up for|share this|skip to (?:main )?content|advertisement|"
                       r"related articles|read more", re.I)
SYMBOL_RE = re.compile(r"[^\w\s.,;:!?'\"()\-]")

EN_STOP = frozenset("the of and to in a is that for it as was with be by on not he this are or his from at which "
                    "but have an had they you were their one all we can her has there been if more when will would "
                    "who so no".split())
STOPWORDS = frozenset(
    "a an and are as at be by for from has have i in is it its of on or that the this to was were will with you "
    "your we they he she not but if so do does can could should would about into than then there their what "
    "which who how when where why".split())

PRONOUNS = frozenset({
    "it", "its", "they", "them", "their", "this", "that", "these", "those",
    "he", "him", "his", "she", "her", "there", "former", "latter", "same",
    "such", "one", "ones",
    "it's", "that's", "they're", "there's", "he's", "she's", "we're",
    "we've", "i've", "you've", "those're", "these're",
})

CONNECTOR_RE = re.compile(
    r"^\s*(oh|well|hmm+|and|but|so|also|then|ok(ay)?|right|i see|got it|"
    r"what about|how about|what else|anything else|more|why|or|now)\b",
    re.I)

QTYPE_RULES = [
    ("social", re.compile(r"^\s*(thanks?|thank you|hello|hi|hey|ok(ay)?|great|cool|got it|bye)\b", re.I)),
    ("yes_no", re.compile(r"^\s*(is|are|was|were|do|does|did|can|could|should|will|would|has|have|had|may|might)\b", re.I)),
    ("what", re.compile(r"^\s*what\b", re.I)),
    ("how", re.compile(r"^\s*how\b", re.I)),
    ("why", re.compile(r"^\s*why\b", re.I)),
    ("wh_other", re.compile(r"^\s*(when|where|who|whom|whose|which)\b", re.I)),
    ("imperative", re.compile(r"^\s*(tell|explain|describe|give|list|show|compare|find|suggest|recommend|help|"
                              r"provide|summarize|define)\b", re.I)),
]

FLAGS = ["empty", "too_short", "mojibake", "control_chars", "html_residue", "boilerplate", "url_heavy",
         "symbol_heavy", "repetitive", "non_english", "pii_email", "pii_phone", "possibly_truncated",
         "starts_lower"]
FLAG_MASK = {f: 1 << i for i, f in enumerate(FLAGS)}
FLAG_DESC = {
    "empty": "tài liệu rỗng", "too_short": f"quá ngắn (<{SHORT_CHARS} ký tự)", "mojibake": "lỗi encoding (mojibake)",
    "control_chars": "ký tự điều khiển", "html_residue": "HTML/entity còn sót", "boilerplate": "boilerplate/menu/footer",
    "url_heavy": "URL chiếm >25% nội dung", "symbol_heavy": "ký hiệu lạ >30%", "repetitive": "lặp từ/dòng bất thường",
    "non_english": "nghi không phải tiếng Anh", "pii_email": "chứa email", "pii_phone": "chứa số điện thoại",
    "possibly_truncated": "nghi bị cắt cụt (không dấu câu cuối)", "starts_lower": "bắt đầu bằng chữ thường",
}
SERIOUS_FLAGS = ["empty", "too_short", "mojibake", "control_chars", "html_residue", "boilerplate",
                 "url_heavy", "symbol_heavy", "repetitive", "non_english"]
SERIOUS_MASK = sum(FLAG_MASK[f] for f in SERIOUS_FLAGS)

HEALTH_WEIGHTS = {"integrity": 0.20, "content": 0.25, "conversation": 0.15, "gold": 0.25, "link": 0.15}
HEALTH_GREEN, HEALTH_YELLOW = 85.0, 70.0

PALETTE = {"blue": "#1f77b4", "green": "#2ca02c", "red": "#d62728", "orange": "#ff7f0e", "purple": "#9467bd",
           "teal": "#17becf", "gray": "#7f7f7f", "dark": "#2b2b2b", "yellow": "#e6b800", "neutral": "#b0b0b0"}
STATUS_COLOR = {"green": PALETTE["green"], "yellow": PALETTE["yellow"], "red": PALETTE["red"], "n/a": PALETTE["neutral"]}

plt.rcParams.update({"figure.dpi": 160, "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
                     "axes.grid": True, "grid.alpha": 0.3, "grid.linestyle": "--", "legend.fontsize": 8.5,
                     "savefig.bbox": "tight", "savefig.pad_inches": 0.25})


# ===========================================================================
# Tiện ích chung
# ===========================================================================
def doc_id_of(d: Dict[str, Any], fallback: Any) -> Tuple[str, bool]:
    for k in ("doc_id", "id", "_id", "docid", "document_id"):
        if d.get(k) is not None:
            return str(d[k]), True
    return str(fallback), False


def doc_text_of(d: Dict[str, Any]) -> Tuple[str, bool]:
    for k in ("content", "text", "contents", "body", "passage"):
        if k in d:
            v = d[k]
            return (v, True) if isinstance(v, str) else ("", False)
    return "", False


def norm_apos(s: str) -> str:
    """Chuẩn hóa dấu nháy cong về nháy thẳng (we’re -> we're)."""
    return s.replace("’", "'").replace("‘", "'").replace("`", "'")


def tokenize(text: str) -> List[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


def quantile(sorted_vals, p: float) -> float:
    if len(sorted_vals) == 0:
        return 0
    return float(sorted_vals[min(len(sorted_vals) - 1, int(p * len(sorted_vals)))])


def pct(a: float, b: float, nd: int = 2) -> float:
    return round(a / b * 100, nd) if b else 0.0


def gini(vals: List[float]) -> float:
    v = sorted(vals)
    n, s = len(v), sum(v)
    if n == 0 or s == 0:
        return 0.0
    cum = sum(i * x for i, x in enumerate(v, 1))
    return round((2 * cum) / (n * s) - (n + 1) / n, 4)


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def safe_mean(vals, default: float = float("nan")) -> float:
    v = [x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return float(np.mean(v)) if v else default


def json_default(o: Any):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    if isinstance(o, tuple):
        return list(o)
    return str(o)


def strip_private(d: Any) -> Any:
    """Loại key bắt đầu bằng '_' (example lists) trước khi JSON; ép key không phải str sang str."""
    if isinstance(d, dict):
        out: Dict[str, Any] = {}
        for k, v in d.items():
            if isinstance(k, str) and k.startswith("_"):
                continue
            out[str(k)] = strip_private(v)
        return out
    if isinstance(d, (list, tuple)):
        return [strip_private(x) for x in d]
    return d


def deep_get(d: Dict[str, Any], *path: str, default: Any = float("nan")) -> Any:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur if cur is not None else default


def snippet(text: str, n: int = 220) -> str:
    t = " ".join(str(text).split())
    return t[:n] + ("…" if len(t) > n else "")


def flag_names(mask: int) -> List[str]:
    return [f for f in FLAGS if mask & FLAG_MASK[f]]


# ===========================================================================
# 1. Cờ chất lượng nội dung + MinHash
# ===========================================================================
_rs = np.random.RandomState(20240607)
MH_A = _rs.randint(1, MH_P - 1, size=MH_N).astype(np.int64)
MH_B = _rs.randint(0, MH_P - 1, size=MH_N).astype(np.int64)


def compute_flags(text: str) -> Tuple[int, List[str]]:
    s = text.strip()
    if not s:
        return FLAG_MASK["empty"], []
    n = len(s)
    toks = TOKEN_RE.findall(s.lower())
    m = 0
    if n < SHORT_CHARS:
        m |= FLAG_MASK["too_short"]
    if MOJIBAKE_RE.search(s):
        m |= FLAG_MASK["mojibake"]
    if CTRL_RE.search(s):
        m |= FLAG_MASK["control_chars"]
    if HTML_RE.search(s):
        m |= FLAG_MASK["html_residue"]
    if BOILER_RE.search(s):
        m |= FLAG_MASK["boilerplate"]
    if sum(len(u) for u in URL_RE.findall(s)) / n > 0.25:
        m |= FLAG_MASK["url_heavy"]
    if len(SYMBOL_RE.findall(s)) / n > 0.30:
        m |= FLAG_MASK["symbol_heavy"]
    nt = len(toks)
    if nt >= 20:
        content = [t for t in toks if t not in EN_STOP]
        if content and Counter(content).most_common(1)[0][1] / len(content) > 0.20:
            m |= FLAG_MASK["repetitive"]
        non_ascii = len(re.findall(r"[^\x00-\x7f]", s)) / n
        if (nt - len(content)) / nt < 0.10 or non_ascii > 0.30:
            m |= FLAG_MASK["non_english"]
    lines = [ln.strip() for ln in s.split("\n") if ln.strip()]
    if len(lines) >= 6 and len(set(lines)) / len(lines) < 0.6:
        m |= FLAG_MASK["repetitive"]
    if EMAIL_RE.search(s):
        m |= FLAG_MASK["pii_email"]
    if PHONE_RE.search(s):
        m |= FLAG_MASK["pii_phone"]
    if n > 200 and s[-1] not in SENT_END_CHARS:
        m |= FLAG_MASK["possibly_truncated"]
    if s[0].islower():
        m |= FLAG_MASK["starts_lower"]
    return m, toks


def minhash(tokens: List[str]) -> np.ndarray:
    k = MH_SHINGLE
    if len(tokens) < k:
        sh = {" ".join(tokens)}
    else:
        sh = {" ".join(tokens[i:i + k]) for i in range(min(len(tokens) - k + 1, MH_MAX_SHINGLES))}
    h = np.fromiter((zlib.crc32(x.encode("utf-8")) % MH_P for x in sh), dtype=np.int64, count=len(sh))
    return ((MH_A[:, None] * h[None, :] + MH_B[:, None]) % MH_P).min(axis=1).astype(np.uint32)


def lsh_clusters(sig: np.ndarray, thr: float = NEAR_DUP_THRESHOLD) -> np.ndarray:
    n = sig.shape[0]
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rows = MH_N // MH_BANDS
    for b in range(MH_BANDS):
        block = np.ascontiguousarray(sig[:, b * rows:(b + 1) * rows])
        buckets: Dict[bytes, List[int]] = defaultdict(list)
        for i in range(n):
            buckets[block[i].tobytes()].append(i)
        for grp in buckets.values():
            if len(grp) < 2:
                continue
            grp = grp[:120]
            base = grp[0]
            for j in grp[1:]:
                if find(base) != find(j) and float((sig[base] == sig[j]).mean()) >= thr:
                    parent[find(j)] = find(base)
    return np.array([find(i) for i in range(n)], dtype=np.int64)


# ===========================================================================
# 2. Quét corpus (1 lần, có cache)
# ===========================================================================
def scan_corpus(domain_dir: Path, dom: str, gold_ids: Set[str], args: argparse.Namespace,
                cache_dir: Path) -> Dict[str, Any]:
    doc_file = domain_dir / "documents.jsonl"
    if not doc_file.is_file():
        raise FileNotFoundError(f"Không thấy {doc_file}")
    st = doc_file.stat()
    gh = hashlib.md5(",".join(sorted(gold_ids)).encode()).hexdigest()
    sig = f"{CACHE_VERSION}|{st.st_size}|{st.st_mtime_ns}|{args.sample_size}|{args.retrieval_distractors}|" \
          f"{args.seed}|{args.max_docs}|{args.near_dup_max}|{args.fix_cap}|{args.examples}|{gh}"
    key = hashlib.md5(sig.encode()).hexdigest()[:12]
    cache = cache_dir / f"{dom}_scan_{key}.pkl"
    if not args.no_cache and cache.is_file():
        try:
            with open(cache, "rb") as f:
                res = pickle.load(f)
            logger.info(f"[{dom}] Dùng cache quét corpus: {cache.name}")
            res["from_cache"] = True
            return res
        except Exception as e:
            logger.warning(f"[{dom}] Cache hỏng ({e}) -> quét lại")
    res = _scan(doc_file, dom, gold_ids, args)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        for old in cache_dir.glob(f"{dom}_scan_*.pkl"):
            old.unlink()
        with open(cache, "wb") as f:
            pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        logger.warning(f"[{dom}] Không ghi được cache: {e}")
    res["from_cache"] = False
    return res


def fetch_doc_snippets(doc_file: Path, want: Set[str], n: int = 220) -> Dict[str, str]:
    """Quét lại file 1 lần để lấy snippet cho các doc_id cần làm ví dụ (dừng sớm khi đủ)."""
    out: Dict[str, str] = {}
    if not want:
        return out
    with open(doc_file, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(d, dict):
                continue
            did, _ = doc_id_of(d, lineno)
            if did in want and did not in out:
                out[did] = snippet(doc_text_of(d)[0], n)
                if len(out) == len(want):
                    break
    return out


def _scan(doc_file: Path, dom: str, gold_ids: Set[str], args: argparse.Namespace) -> Dict[str, Any]:
    t0 = time.time()
    rng = random.Random(args.seed)
    logger.info(f"[{dom}] Quét documents.jsonl ...")
    with open(doc_file, "rb") as f:
        est_total = sum(1 for _ in f)
    if args.max_docs > 0:
        est_total = min(est_total, args.max_docs)
    sig_prob = min(1.0, args.near_dup_max / max(1, est_total))
    pool_size = max(args.sample_size if args.sample_size > 0 else 10 ** 9, args.retrieval_distractors)

    ids: List[str] = []
    char_lens: List[int] = []
    word_lens: List[int] = []
    flags: List[int] = []
    md5s: List[int] = []
    sig_idx: List[int] = []
    sig_rows: List[np.ndarray] = []
    flag_ids: Dict[str, List[str]] = defaultdict(list)
    flag_examples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    field_examples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    pool: List[Dict[str, Any]] = []
    gold_docs: Dict[str, Dict[str, Any]] = {}
    seen_ids: Set[str] = set()
    key_counter: Counter = Counter()
    dup_id_examples: List[str] = []
    bad_examples: List[Dict[str, Any]] = []
    bad_json = not_dict = missing_id = missing_text = non_str_text = dup_ids = title_missing = 0
    schema_keys: List[str] = []
    total = 0

    def fex(kind: str, rec: Dict[str, Any]):
        if len(field_examples[kind]) < args.examples:
            field_examples[kind].append(rec)

    with open(doc_file, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            if args.max_docs > 0 and total >= args.max_docs:
                break
            try:
                d = json.loads(line)
            except json.JSONDecodeError as e:
                bad_json += 1
                if len(bad_examples) < args.fix_cap:
                    bad_examples.append({"line": lineno, "error": str(e)[:80], "head": line[:100]})
                continue
            if not isinstance(d, dict):
                not_dict += 1
                if len(bad_examples) < args.fix_cap:
                    bad_examples.append({"line": lineno, "error": "không phải object", "head": line[:100]})
                continue
            if total == 0:
                schema_keys = sorted(d.keys())
            key_counter.update(d.keys())
            did, has_id = doc_id_of(d, total)
            text, text_ok = doc_text_of(d)
            if not has_id:
                missing_id += 1
                fex("missing_id", {"line": lineno, "head": line[:120]})
            if not text_ok:
                if any(k in d for k in ("content", "text", "contents", "body", "passage")):
                    non_str_text += 1
                    fex("non_str_text", {"line": lineno, "doc_id": did, "head": line[:120]})
                else:
                    missing_text += 1
                    fex("missing_text", {"line": lineno, "doc_id": did, "head": line[:120]})
            if "title" in d and not (isinstance(d["title"], str) and d["title"].strip()):
                title_missing += 1
                fex("title_missing", {"line": lineno, "doc_id": did})
            if did in seen_ids:
                dup_ids += 1
                if len(dup_id_examples) < args.fix_cap:
                    dup_id_examples.append(did)
            seen_ids.add(did)

            idx = total
            total += 1
            mask, toks = compute_flags(text)
            s = text.strip()
            ids.append(did)
            char_lens.append(len(text))
            word_lens.append(len(text.split()))
            flags.append(mask)
            md5s.append(int(hashlib.md5(s.encode("utf-8", errors="ignore")).hexdigest()[:15], 16))
            if mask:
                for fl in FLAGS:
                    if mask & FLAG_MASK[fl]:
                        if len(flag_ids[fl]) < args.fix_cap:
                            flag_ids[fl].append(did)
                        if len(flag_examples[fl]) < args.examples:
                            flag_examples[fl].append({"doc_id": did, "chars": len(text), "snippet": snippet(s)})
            if len(toks) >= 8 and (did in gold_ids or rng.random() < sig_prob):
                sig_idx.append(idx)
                sig_rows.append(minhash(toks))
            rec = {"doc_id": did, "text": text,
                   "title": d.get("title", "") if isinstance(d.get("title"), str) else ""}
            if did in gold_ids:
                gold_docs[did] = rec
            if len(pool) < pool_size:
                pool.append(rec)
            else:
                j = rng.randint(0, total - 1)
                if j < pool_size:
                    pool[j] = rec
            if total % 50000 == 0:
                logger.info(f"[{dom}]   ... {total:,} docs ({time.time() - t0:.0f}s)")

    if total == 0:
        raise ValueError("documents.jsonl không có tài liệu hợp lệ nào")
    rng.shuffle(pool)
    cl = np.array(char_lens, dtype=np.int64)
    wl = np.array(word_lens, dtype=np.int64)
    fl_arr = np.array(flags, dtype=np.int64)
    md5_arr = np.array(md5s, dtype=np.int64)
    scl = np.sort(cl)

    q1, q3 = quantile(scl, 0.25), quantile(scl, 0.75)
    long_thr = q3 + 3 * (q3 - q1)
    swl = np.sort(wl)
    char_stats = {"min": int(scl[0]), "p10": quantile(scl, .1), "p25": q1, "median": quantile(scl, .5),
                  "mean": round(float(cl.mean()), 1),
                  "p75": q3, "p90": quantile(scl, .9), "p95": quantile(scl, .95), "p99": quantile(scl, .99),
                  "max": int(scl[-1])}
    word_stats = {"min": int(swl[0]), "median": quantile(swl, .5), "mean": round(float(wl.mean()), 1),
                  "max": int(swl[-1])}
    edges = [100, 300, 650, 800, 1500, 3000, 6000]
    buckets, prev = {}, -1
    for e in edges:
        lo, hi = np.searchsorted(scl, prev, side="right"), np.searchsorted(scl, e, side="right")
        buckets[f"{prev + 1}-{e}" if prev >= 0 else f"0-{e}"] = pct(hi - lo, total)
        prev = e
    buckets[f">{edges[-1]}"] = pct(total - np.searchsorted(scl, edges[-1], side="right"), total)

    flag_counts = {fl: int(((fl_arr & FLAG_MASK[fl]) != 0).sum()) for fl in FLAGS}
    flag_pct = {fl: pct(c, total) for fl, c in flag_counts.items()}
    serious_pct = pct(int(((fl_arr & SERIOUS_MASK) != 0).sum()), total)

    nonempty = (fl_arr & FLAG_MASK["empty"]) == 0
    u, inv, cnt = np.unique(md5_arr[nonempty], return_inverse=True, return_counts=True)
    exact_dup_docs = int((cnt[cnt > 1] - 1).sum())
    exact_groups = int((cnt > 1).sum())
    exact_examples: List[List[str]] = []
    if exact_groups:
        dup_hashes = set(u[cnt > 1][:args.examples].tolist())
        by_hash: Dict[int, List[str]] = defaultdict(list)
        for i in np.nonzero(nonempty)[0]:
            if int(md5_arr[i]) in dup_hashes and len(by_hash[int(md5_arr[i])]) < 6:
                by_hash[int(md5_arr[i])].append(ids[i])
        exact_examples = [v for v in by_hash.values()]
    exact_dup_ids: List[str] = []
    if exact_dup_docs:
        first_seen: Set[int] = set()
        multi = set(u[cnt > 1].tolist())
        for i in np.nonzero(nonempty)[0]:
            h = int(md5_arr[i])
            if h in multi:
                if h in first_seen and len(exact_dup_ids) < args.fix_cap:
                    exact_dup_ids.append(ids[i])
                first_seen.add(h)

    near: Dict[str, Any] = {"docs_with_signature": len(sig_idx), "sampling_prob": round(sig_prob, 4),
                            "clusters": 0, "removable_total": 0, "near_only_removable": 0,
                            "largest_cluster": 0, "examples": []}
    cluster_members: Dict[int, List[int]] = {}
    if len(sig_idx) >= 2:
        sig = np.vstack(sig_rows)
        labels = lsh_clusters(sig)
        groups: Dict[int, List[int]] = defaultdict(list)
        for pos, lab in enumerate(labels):
            groups[int(lab)].append(sig_idx[pos])
        for lab, mem in groups.items():
            if len(mem) < 2:
                continue
            cluster_members[lab] = mem
            d_md5 = len({int(md5_arr[i]) for i in mem})
            near["removable_total"] += len(mem) - 1
            near["near_only_removable"] += d_md5 - 1
            near["largest_cluster"] = max(near["largest_cluster"], len(mem))
        near["clusters"] = len(cluster_members)
        for mem in sorted(cluster_members.values(), key=lambda m: -len(m))[:args.examples * 3]:
            if len(near["examples"]) >= args.examples:
                break
            if len({int(md5_arr[i]) for i in mem}) > 1:
                near["examples"].append({"doc_ids": [ids[i] for i in mem[:5]], "size": len(mem)})
    near["near_only_pct"] = pct(near["near_only_removable"], max(1, len(sig_idx)))
    near["removable_total_pct"] = pct(near["removable_total"], max(1, len(sig_idx)))

    # snippet cho ví dụ trùng (quét lại 1 lần, chỉ các id cần)
    want: Set[str] = set(dup_id_examples[:args.examples])
    for g in exact_examples[:args.examples]:
        want.update(g[:3])
    for e in near["examples"]:
        want.update(e["doc_ids"][:3])
    doc_snippets = fetch_doc_snippets(doc_file, want)

    vocab: Counter = Counter()
    seen_v: Set[str] = set()
    n_vocab_docs = 0
    for rec in list(pool) + list(gold_docs.values()):
        if rec["doc_id"] in seen_v:
            continue
        seen_v.add(rec["doc_id"])
        vocab.update(tokenize(rec["text"]))
        n_vocab_docs += 1

    res = {
        "ids": ids, "char_len": cl, "word_len": wl, "flags": fl_arr, "md5": md5_arr,
        "cluster_members": cluster_members, "pool": pool, "gold_docs": gold_docs, "vocab": vocab,
        "n_vocab_docs": n_vocab_docs, "flag_ids": dict(flag_ids), "flag_examples": dict(flag_examples),
        "field_examples": dict(field_examples), "doc_snippets": doc_snippets,
        "bad_examples": bad_examples, "dup_id_examples": dup_id_examples, "exact_examples": exact_examples,
        "exact_dup_ids": exact_dup_ids, "scan_seconds": round(time.time() - t0, 1),
        "stats": {
            "total_documents": total, "schema_keys": schema_keys,
            "bad_json_lines": bad_json, "not_dict_lines": not_dict, "missing_id": missing_id,
            "missing_text_field": missing_text, "non_str_text": non_str_text,
            "duplicate_doc_ids": dup_ids, "title_missing": title_missing,
            "key_consistency_pct": {k: pct(v, total) for k, v in sorted(key_counter.items())},
            "char_length": char_stats, "word_length": word_stats, "length_buckets_pct": buckets,
            "long_outlier_threshold_chars": round(long_thr, 1),
            "long_outlier_pct": pct(int((cl > long_thr).sum()), total),
            "share_le_chars_pct": {str(x): pct(int(np.searchsorted(scl, x, side="right")), total)
                                   for x in (650, 800, 1500, 3000)},
            "flags_count": flag_counts, "flags_pct": flag_pct, "serious_flag_pct": serious_pct,
            "exact_dup": {"duplicate_docs": exact_dup_docs, "groups": exact_groups,
                          "duplicate_pct": pct(exact_dup_docs, total)},
            "near_dup": near,
        },
    }
    logger.info(f"[{dom}] Quét xong {total:,} docs trong {res['scan_seconds']}s "
                f"(gold tìm thấy {len(gold_docs)}/{len(gold_ids)})")
    return res


def vocab_stats(vocab: Counter) -> Dict[str, Any]:
    if not vocab:
        return {"size": 0}
    freqs = sorted(vocab.values(), reverse=True)
    total = sum(freqs)
    hapax = sum(1 for f in freqs if f == 1)
    top = min(len(freqs), 5000)
    slope = float("nan")
    if top >= 20:
        x = np.log(np.arange(1, top + 1))
        y = np.log(np.array(freqs[:top], dtype=float))
        slope = float(np.polyfit(x, y, 1)[0])
    pts_idx = sorted({int(round(v)) for v in np.logspace(0, math.log10(len(freqs)), 120)})
    return {"size": len(freqs), "tokens": total, "hapax_pct": pct(hapax, len(freqs)),
            "zipf_slope": round(slope, 3) if not math.isnan(slope) else None,
            "top_terms": [(w, c) for w, c in vocab.most_common(30)],
            "top_terms_2000": [w for w, _ in vocab.most_common(2000)],
            "zipf_points": [[i, freqs[i - 1]] for i in pts_idx if i <= len(freqs)]}


# ===========================================================================
# 3. qrels + benchmark
# ===========================================================================
GOLD_KEYS = ("gold_doc_ids", "supporting_doc_ids", "relevant_doc_ids", "gold_docs", "doc_ids",
             "positive_doc_ids", "gold_passages", "relevant_docs")
QUERY_KEYS = ("query", "question", "utterance", "text", "user_query")
ANSWER_KEYS = ("answer", "response", "assistant_answer", "reference_answer")
TURN_ID_KEYS = ("turn_id", "query_id", "qid", "id")


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


def load_qrels(path: Path, cap: int = 10) -> Tuple[Dict[str, Set[str]], Dict[str, Any]]:
    qrels: Dict[str, Set[str]] = defaultdict(set)
    info: Dict[str, Any] = {"exists": path.is_file(), "lines": 0, "malformed": 0, "duplicate_pairs": 0,
                            "relevance_levels": {}, "non_positive": 0, "n_qids": 0, "n_pairs_positive": 0,
                            "_malformed_examples": [], "_dup_examples": [], "_nonpos_examples": []}
    if not path.is_file():
        return qrels, info
    seen: Set[Tuple[str, str]] = set()
    rel_counter: Counter = Counter()
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            info["lines"] += 1
            parts = line.split()
            try:
                if len(parts) >= 4:
                    qid, did, rel = parts[0], parts[2], parts[3]
                elif len(parts) == 3:
                    qid, did, rel = parts
                elif len(parts) == 2:
                    qid, did, rel = parts[0], parts[1], "1"
                else:
                    raise ValueError("ít hơn 2 cột")
                r = int(float(rel))
            except ValueError as e:
                info["malformed"] += 1
                if len(info["_malformed_examples"]) < cap:
                    info["_malformed_examples"].append({"line": lineno, "raw": line.rstrip()[:140], "why": str(e)[:60]})
                continue
            rel_counter[r] += 1
            if (qid, did) in seen:
                info["duplicate_pairs"] += 1
                if len(info["_dup_examples"]) < cap:
                    info["_dup_examples"].append({"line": lineno, "qid": qid, "doc_id": did})
            seen.add((qid, did))
            if r > 0:
                qrels[qid].add(did)
            else:
                info["non_positive"] += 1
                if len(info["_nonpos_examples"]) < cap:
                    info["_nonpos_examples"].append({"line": lineno, "qid": qid, "doc_id": did, "rel": r})
    info["relevance_levels"] = dict(sorted(rel_counter.items()))
    info["n_qids"] = len(qrels)
    info["n_pairs_positive"] = sum(len(v) for v in qrels.values())
    return qrels, info


def _turn_schema(raw: List[Dict[str, Any]]) -> str:
    if not raw:
        return "empty"
    if any("role" in t for t in raw):
        return "message"
    if any(("query" in t or "question" in t) and any(k in t for k in ANSWER_KEYS) for t in raw):
        return "qa_pair"
    return "unknown"


def _qid_candidates(conv_id: str, t: Dict[str, Any], ti: int) -> List[str]:
    """Sinh các dạng qid có thể có trong qrels. Dạng `<conv>_turn_<n>` (format thật) đứng đầu."""
    tid = t.get("turn_id", ti + 1)
    c = [f"{conv_id}_turn_{tid}", f"{conv_id}_turn_{ti + 1}"]
    for sep in ("_", "-", "#", ":", "/"):
        c += [f"{conv_id}{sep}{tid}", f"{conv_id}{sep}{ti + 1}", f"{conv_id}{sep}{ti}"]
    c += [str(t[k]) for k in TURN_ID_KEYS if t.get(k) is not None]
    seen: Set[str] = set()
    out = []
    for x in c:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def parse_benchmark(path: Path, qrels: Dict[str, Set[str]], cap: int = 10) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": False, "turns": [], "meta": {"file": path.name, "schema_type": "unknown"}}
    meta = out["meta"]
    if not path.is_file():
        meta["note"] = f"Không thấy {path.name}"
        return out
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        meta["note"] = f"Không đọc được JSON: {e}"
        return out
    if isinstance(data, dict):
        convs = data.get("conversations") or next((v for v in data.values() if isinstance(v, list)), [])
    else:
        convs = data
    if not convs:
        meta["note"] = "benchmark rỗng hoặc sai cấu trúc"
        return out

    first = convs[0] if isinstance(convs[0], dict) else {}
    meta["schema"] = {"conversation_keys": sorted(first.keys())}
    roles: Counter = Counter()
    conv_ids: Counter = Counter()
    matched_qids: Set[str] = set()
    n_assistant = empty_convs = nonalt = missing_query = 0
    turns_out: List[Dict[str, Any]] = []
    schema_types: Set[str] = set()
    empty_conv_ids: List[str] = []
    nonalt_ids: List[str] = []
    missing_query_qids: List[str] = []
    mismatch: List[Dict[str, Any]] = []
    n_mismatch = 0

    for ci, c in enumerate(convs):
        if not isinstance(c, dict):
            continue
        conv_id = str(c.get("conversation_id") or c.get("conv_id") or c.get("id") or ci)
        conv_ids[conv_id] += 1
        raw = c.get("turns") or c.get("conversation") or c.get("messages") or []
        raw = [t for t in raw if isinstance(t, dict)]
        if not raw:
            empty_convs += 1
            empty_conv_ids.append(conv_id)
            continue
        schema = _turn_schema(raw)
        schema_types.add(schema)

        if schema == "message":
            prev_role = None
            for t in raw:
                r = t.get("role", "user")
                roles[r] += 1
                if prev_role is not None and prev_role == r:
                    nonalt += 1
                    nonalt_ids.append(conv_id)
                    break
                prev_role = r
            users = [t for t in raw if t.get("role", "user") in ("user", "human")]
            n_assistant += len(raw) - len(users)
        else:
            roles["user"] += len(raw)
            roles["assistant"] += len(raw)
            n_assistant += len(raw)
            users = raw

        if ci == 0 and users:
            meta["schema"]["turn_keys"] = sorted(users[0].keys())

        history_parts: List[str] = []
        for ti, t in enumerate(users):
            q = next((t[k] for k in QUERY_KEYS if isinstance(t.get(k), str)), "")
            a = next((t[k] for k in ANSWER_KEYS if isinstance(t.get(k), str)), "")
            tid_raw = next((t[k] for k in ("turn_id", "qid") if t.get(k) is not None), ti + 1)
            qid_str = f"{conv_id}_turn_{tid_raw}"
            if not q.strip():
                missing_query += 1
                missing_query_qids.append(qid_str)

            ch = t.get("conversation_history")
            if isinstance(ch, str) and ch.strip() and not ch.lower().startswith("no previous"):
                history_query = (ch.strip() + "\nQ: " + q).strip()
            else:
                history_query = "\n".join(history_parts + ["Q: " + q])

            gold: List[str] = []
            src = "none"
            for k in GOLD_KEYS:
                if k in t:
                    gold = _norm_ids(t[k])
                    src = "inline" if gold else "none"
                    break

            q_match = None
            for cid in _qid_candidates(conv_id, t, ti):
                if cid in qrels:
                    q_match = cid
                    matched_qids.add(cid)
                    break
            if q_match is not None:
                if not gold:
                    gold, src = sorted(qrels[q_match]), "qrels"
                elif set(gold) != qrels[q_match]:
                    n_mismatch += 1
                    if len(mismatch) < cap:
                        mismatch.append({"qid": qid_str, "inline_only": sorted(set(gold) - qrels[q_match]),
                                         "qrels_only": sorted(qrels[q_match] - set(gold))})

            turns_out.append({
                "qid": qid_str, "conv": conv_id, "ti": ti, "n_turns": len(users),
                "query": q, "gold": gold, "gold_src": src, "qrels_match": q_match,
                "history_query": history_query,
            })
            history_parts.append("Q: " + q)
            if a:
                history_parts.append("A: " + a)

    meta.update({
        "schema_type": "|".join(sorted(schema_types)) if schema_types else "unknown",
        "n_conversations": len(convs), "roles": dict(roles), "assistant_turns": n_assistant,
        "empty_conversations": empty_convs, "non_alternating_roles_convs": nonalt,
        "duplicate_conv_ids": sum(1 for v in conv_ids.values() if v > 1),
        "missing_query_turns": missing_query, "matched_qrels_qids": len(matched_qids),
        "qrels_qids_total": len(qrels),
        "gold_qrels_mismatch_turns": n_mismatch,
        "orphan_qrels_qids": sorted(set(qrels) - matched_qids)[:200],
        "_dup_conv_ids": [k for k, v in conv_ids.items() if v > 1][:cap],
        "_empty_conv_ids": empty_conv_ids[:cap], "_nonalt_conv_ids": nonalt_ids[:cap],
        "_missing_query_qids": missing_query_qids[:cap],
        "_gold_qrels_mismatch": mismatch,
    })
    out["turns"], out["ok"] = turns_out, True
    return out


# ===========================================================================
# 4. Phân tích hội thoại
# ===========================================================================
def classify_context(q: str, ti: int) -> str:
    toks = re.findall(r"[a-z']+", norm_apos(q.lower()))
    if ti == 0:
        return "standalone"
    if CONNECTOR_RE.match(q):
        return "connector"
    if any(t in PRONOUNS for t in toks[:8]):
        return "pronoun"
    if len(toks) <= 4:
        return "short_ellipsis"
    return "standalone"


def classify_qtype(q: str) -> str:
    for name, rx in QTYPE_RULES:
        if rx.match(q):
            return name
    return "statement_other"


def pos_bucket(ti: int) -> str:
    return str(ti + 1) if ti < 4 else "5+"


def analyze_conversations(turns: List[Dict[str, Any]], meta: Dict[str, Any], examples: int) -> Dict[str, Any]:
    if not turns:
        return {"note": meta.get("note", "không có turn")}
    prev_bow: Optional[Counter] = None
    prev_conv = None
    prev_q = ""
    ctx_c, qt_c, shift_c = Counter(), Counter(), Counter()
    dangling0: List[Dict[str, Any]] = []
    conv_shift: Dict[str, List[int]] = defaultdict(list)
    norm_q: Counter = Counter()
    norm_q_qids: Dict[str, List[str]] = defaultdict(list)
    norm_q_conv: Counter = Counter()
    qlens: List[int] = []
    per_pos_gold: Dict[str, List[int]] = defaultdict(list)
    empty_q: List[Dict[str, Any]] = []
    short_ex: List[Dict[str, Any]] = []
    long_ex: List[Dict[str, Any]] = []
    ctx_ex: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    shift_ex: List[Dict[str, Any]] = []
    n_nonfirst = 0
    for t in turns:
        q, ti = t["query"], t["ti"]
        toks = tokenize(q)
        bow = Counter(toks)
        t["ctx"] = classify_context(q, ti)
        t["qtype"] = classify_qtype(q)
        if ti == 0 or t["conv"] != prev_conv:
            t["shift"], t["cos_prev"] = "n/a", None
        else:
            c = cosine(bow, prev_bow or Counter())
            t["cos_prev"] = round(c, 3)
            t["shift"] = "on_topic" if c >= 0.15 else ("weak" if c >= 0.05 else "shift")
            conv_shift[t["conv"]].append(1 if t["shift"] == "shift" else 0)
            shift_c[t["shift"]] += 1
            if t["shift"] == "shift" and len(shift_ex) < examples:
                shift_ex.append({"qid": t["qid"], "cos": t["cos_prev"],
                                 "prev": snippet(prev_q, 120), "query": snippet(q, 120)})
        prev_bow, prev_conv, prev_q = bow, t["conv"], q
        ctx_c[t["ctx"]] += 1
        qt_c[t["qtype"]] += 1
        if ti > 0:
            n_nonfirst += 1
            if t["ctx"] != "standalone" and len(ctx_ex[t["ctx"]]) < examples:
                ctx_ex[t["ctx"]].append({"qid": t["qid"], "query": snippet(q, 140)})
        if ti == 0 and q.strip():
            first6 = re.findall(r"[a-z']+", norm_apos(q.lower()))[:6]
            if any(w in PRONOUNS - {"one", "ones", "there", "same", "such"} for w in first6) \
                    or CONNECTOR_RE.match(q):
                dangling0.append({"qid": t["qid"], "query": snippet(q, 160)})
        if not q.strip():
            empty_q.append({"qid": t["qid"]})
        else:
            nq = " ".join(q.lower().split())
            norm_q[nq] += 1
            norm_q_qids[nq].append(t["qid"])
            norm_q_conv[(t["conv"], nq)] += 1
        nw = len(q.split())
        qlens.append(nw)
        if q.strip() and nw <= 2 and len(short_ex) < examples:
            short_ex.append({"qid": t["qid"], "query": snippet(q, 80)})
        if nw > 60 and len(long_ex) < examples:
            long_ex.append({"qid": t["qid"], "words": nw, "query": snippet(q, 160)})
        per_pos_gold[pos_bucket(ti)].append(1 if t["gold"] else 0)
    n = len(turns)
    sq = sorted(qlens)
    tpc = sorted({t["conv"]: t["n_turns"] for t in turns}.values())
    dup_turns = sum(v - 1 for v in norm_q.values() if v > 1)
    dup_in_conv = sum(v - 1 for v in norm_q_conv.values() if v > 1)
    dup_ex = [{"query": snippet(k, 140), "count": v, "qids": norm_q_qids[k][:5]}
              for k, v in norm_q.most_common() if v > 1][:examples]
    dep = sum(ctx_c[k] for k in ("connector", "pronoun", "short_ellipsis"))
    conv_shift_ratio = [sum(v) / len(v) for v in conv_shift.values() if v]
    return {
        "total_conversations": len(tpc), "total_turns": n,
        "turns_per_conversation": {"min": tpc[0], "median": quantile(tpc, .5),
                                   "mean": round(sum(tpc) / len(tpc), 2), "max": tpc[-1],
                                   "hist": {str(k): v for k, v in sorted(Counter(tpc).items())}},
        "query_word_length": {"min": sq[0], "median": quantile(sq, .5), "mean": round(sum(qlens) / n, 1),
                              "p95": quantile(sq, .95), "max": sq[-1]},
        "very_short_query_pct": pct(sum(1 for x in qlens if x <= 2), n),
        "very_long_query_pct": pct(sum(1 for x in qlens if x > 60), n),
        "empty_query_turns": len(empty_q), "empty_query_pct": pct(len(empty_q), n),
        "duplicate_query_turns": dup_turns, "duplicate_query_pct": pct(dup_turns, n),
        "duplicate_query_in_same_conv": dup_in_conv,
        "context": {"counts": dict(ctx_c), "pct": {k: pct(v, n) for k, v in ctx_c.items()},
                    "dependent_pct_of_nonfirst": pct(dep, n_nonfirst), "dependent_pct_of_all": pct(dep, n),
                    "need_rewrite_estimate_turns": dep},
        "turn0_dangling_ref": {"count": len(dangling0), "pct_of_conversations": pct(len(dangling0), len(tpc)),
                               "examples": dangling0[:examples]},
        "topic_shift": {"counts": dict(shift_c),
                        "pct": {k: pct(v, max(1, sum(shift_c.values()))) for k, v in shift_c.items()},
                        "mean_shift_ratio_per_conv": round(float(np.mean(conv_shift_ratio)), 3) if conv_shift_ratio else 0.0,
                        "convs_mostly_shifting_pct": pct(sum(1 for r in conv_shift_ratio if r >= 0.5),
                                                         max(1, len(conv_shift_ratio)))},
        "question_types": {"counts": dict(qt_c), "pct": {k: pct(v, n) for k, v in qt_c.items()}},
        "gold_rate_by_position_pct": {k: pct(sum(v), len(v)) for k, v in sorted(per_pos_gold.items())},
        "empty_query_list": empty_q[:200],
        "_dup_examples": dup_ex, "_short_examples": short_ex, "_long_examples": long_ex,
        "_ctx_examples": dict(ctx_ex), "_shift_examples": shift_ex,
    }


# ===========================================================================
# 5. Phân tích gold / qrels
# ===========================================================================
def analyze_gold(turns: List[Dict[str, Any]], meta: Dict[str, Any], qinfo: Dict[str, Any],
                 scan: Dict[str, Any], examples: int, fix_cap: int) -> Dict[str, Any]:
    ids: List[str] = scan["ids"]
    id_to_idx = {d: i for i, d in enumerate(ids)}
    cl, fl = scan["char_len"], scan["flags"]
    n_turns = len(turns)
    gold_counts = [len(t["gold"]) for t in turns]
    no_gold = [t for t in turns if not t["gold"]]
    src = Counter(t["gold_src"] for t in turns)
    ref: Counter = Counter()
    orphan_pairs: List[Dict[str, str]] = []
    pairs = 0
    for t in turns:
        for g in set(t["gold"]):
            ref[g] += 1
            pairs += 1
            if g not in id_to_idx:
                orphan_pairs.append({"qid": t["qid"], "doc_id": g})
    orphan_ids = {p["doc_id"] for p in orphan_pairs}
    valid_gold = [g for g in ref if g in id_to_idx]
    n_docs = len(ids)
    g_idx = np.array([id_to_idx[g] for g in valid_gold], dtype=np.int64) if valid_gold else np.array([], dtype=np.int64)
    qrels_used = src.get("qrels", 0) > 0

    len_stats: Dict[str, Any] = {}
    if len(g_idx):
        gl = np.sort(cl[g_idx])
        len_stats = {"gold_median": quantile(gl, .5), "gold_mean": round(float(gl.mean()), 1),
                     "gold_p90": quantile(gl, .9), "corpus_median": float(np.median(cl)),
                     "corpus_mean": round(float(cl.mean()), 1),
                     "median_ratio_gold_over_corpus": round(quantile(gl, .5) / max(1.0, float(np.median(cl))), 2),
                     "gold_gt_3000c_pct": pct(int((gl > 3000).sum()), len(gl)),
                     "corpus_gt_3000c_pct": pct(int((cl > 3000).sum()), n_docs)}
    gold_flag_pct: Dict[str, float] = {}
    gold_serious = 0
    gold_flag_ex: List[Dict[str, Any]] = []
    if len(g_idx):
        gf = fl[g_idx]
        gold_flag_pct = {f: pct(int(((gf & FLAG_MASK[f]) != 0).sum()), len(g_idx)) for f in FLAGS}
        gold_serious = int(((gf & SERIOUS_MASK) != 0).sum())
        gd_docs = scan["gold_docs"]
        for gid, mask in zip(valid_gold, gf):
            if int(mask) & SERIOUS_MASK and len(gold_flag_ex) < examples:
                gold_flag_ex.append({"doc_id": gid, "flags": [f for f in flag_names(int(mask)) if f in SERIOUS_FLAGS],
                                     "snippet": snippet(gd_docs.get(gid, {}).get("text", ""), 200)})

    gold_set_idx = set(g_idx.tolist())
    fn_candidates, redundant_gold = 0, 0
    fn_examples: List[Dict[str, Any]] = []
    fn_ids: List[str] = []
    for lab, mem in scan["cluster_members"].items():
        g_in = [i for i in mem if i in gold_set_idx]
        if not g_in:
            continue
        non_gold = [i for i in mem if i not in gold_set_idx]
        if non_gold:
            fn_candidates += len(g_in)
            for i in non_gold:
                if len(fn_ids) < fix_cap:
                    fn_ids.append(ids[i])
            if len(fn_examples) < examples:
                fn_examples.append({"gold": [ids[i] for i in g_in[:3]],
                                    "non_gold_twins": [ids[i] for i in non_gold[:3]]})
        if len(g_in) > 1:
            redundant_gold += len(g_in) - 1

    by_conv: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for t in turns:
        by_conv[t["conv"]].append(t)
    repeat_turns = later_turns = 0
    for tl in by_conv.values():
        seen: Set[str] = set()
        for t in tl:
            if t["ti"] > 0 and t["gold"]:
                later_turns += 1
                if set(t["gold"]) & seen:
                    repeat_turns += 1
            seen |= set(t["gold"])

    by_pos: Dict[str, List[int]] = defaultdict(list)
    for t in turns:
        by_pos[pos_bucket(t["ti"])].append(len(t["gold"]))
    ref_counts = list(ref.values())
    top_share = 0.0
    if ref_counts:
        k = max(1, int(0.01 * len(ref_counts)))
        top_share = pct(sum(sorted(ref_counts, reverse=True)[:k]), sum(ref_counts))
    orphan_q = meta.get("orphan_qrels_qids", [])

    return {
        "turns": n_turns,
        "gold_source": dict(src),
        "qrels_used_for_eval": qrels_used,
        "matched_qrels_qids": meta.get("matched_qrels_qids", 0),
        "gold_qrels_mismatch_turns": meta.get("gold_qrels_mismatch_turns", 0),
        "gold_qrels_mismatch_pct": pct(meta.get("gold_qrels_mismatch_turns", 0), n_turns),
        "turns_without_gold": len(no_gold), "turns_without_gold_pct": pct(len(no_gold), n_turns),
        "gold_per_turn": {"mean": round(sum(gold_counts) / max(1, n_turns), 2),
                          "max": max(gold_counts) if gold_counts else 0,
                          "hist": {str(k): v for k, v in sorted(Counter(min(c, 10) for c in gold_counts).items())}},
        "gold_pairs": pairs, "gold_unique_docs": len(ref),
        "orphan_gold_pairs": len(orphan_pairs), "orphan_gold_pairs_pct": pct(len(orphan_pairs), pairs),
        "orphan_gold_unique_docs": len(orphan_ids), "orphan_gold_unique_pct": pct(len(orphan_ids), len(ref)),
        "qrels_qids_total": meta.get("qrels_qids_total", 0),
        "orphan_qrels_qids": len(orphan_q),
        "orphan_qrels_qids_pct": pct(len(orphan_q), meta.get("qrels_qids_total", 0)),
        "qrels_file": qinfo,
        "corpus_docs": n_docs, "docs_never_gold": n_docs - len(valid_gold),
        "docs_never_gold_pct": pct(n_docs - len(valid_gold), n_docs),
        "gini_gold_reference": gini(ref_counts), "top1pct_docs_share_of_refs_pct": top_share,
        "most_referenced": [{"doc_id": d, "refs": c} for d, c in ref.most_common(10)],
        "length": len_stats,
        "gold_flag_pct": gold_flag_pct,
        "gold_serious_flag_docs": gold_serious,
        "gold_serious_flag_pct": pct(gold_serious, max(1, len(valid_gold))),
        "false_negative_candidates": fn_candidates,
        "false_negative_candidates_pct": pct(fn_candidates, max(1, len(valid_gold))),
        "false_negative_examples": fn_examples,
        "redundant_gold_dups": redundant_gold,
        "gold_repeat_in_conv_pct": pct(repeat_turns, later_turns),
        "gold_per_turn_by_position": {k: round(sum(v) / len(v), 2) for k, v in sorted(by_pos.items())},
        "_orphan_pairs": orphan_pairs[:fix_cap], "_orphan_qrels": orphan_q[:fix_cap],
        "_no_gold": [{"qid": t["qid"], "query": snippet(t["query"], 150)} for t in no_gold[:fix_cap]],
        "_fn_ids": fn_ids, "_gold_flag_examples": gold_flag_ex,
        "_mismatch": meta.get("_gold_qrels_mismatch", []),
    }


# ===========================================================================
# 6. Liên kết query <-> gold
# ===========================================================================
def sentence_spans(text: str) -> List[Tuple[int, str]]:
    spans: List[Tuple[int, str]] = []
    pos = 0
    for m in re.finditer(r"[.!?…]+[\"'”’)\]]*\s+|\n+", text):
        end = m.end()
        if end > pos:
            sent = text[pos:end]
            if sent.strip():
                spans.append((pos, sent))
            pos = end
    if pos < len(text):
        rest = text[pos:]
        if rest.strip():
            spans.append((pos, rest))
    return spans


def analyze_link(turns: List[Dict[str, Any]], gold_docs: Dict[str, Dict[str, Any]], vocab: Counter,
                 args: argparse.Namespace, rng: random.Random) -> Dict[str, Any]:
    ev = [t for t in turns if t["query"].strip() and any(g in gold_docs for g in t["gold"])]
    if not ev:
        return {"note": "Không có turn nào có gold doc đọc được -> bỏ qua"}
    if len(ev) > args.max_link_turns:
        ev = rng.sample(ev, args.max_link_turns)
    sent_cache: Dict[str, List[Tuple[int, Set[str], str]]] = {}
    doc_tok_cache: Dict[str, Set[str]] = {}

    def doc_tokens(did: str) -> Set[str]:
        if did not in doc_tok_cache:
            doc_tok_cache[did] = set(tokenize(gold_docs[did]["text"]))
        return doc_tok_cache[did]

    def sents(did: str) -> List[Tuple[int, Set[str], str]]:
        if did not in sent_cache:
            sent_cache[did] = [(i, set(tokenize(s)), s) for i, s in sentence_spans(gold_docs[did]["text"])]
        return sent_cache[did]

    best_ov, best_ov_hist, abs_off, rel_pos = [], [], [], []
    zero_examples: List[Dict[str, Any]] = []
    late_examples: List[Dict[str, Any]] = []
    oov_examples: List[Dict[str, Any]] = []
    oov_rates, oov_terms = [], Counter()
    low_by_ctx: Dict[str, List[float]] = defaultdict(list)
    n_vocab_known = len(vocab)
    for t in ev:
        q = set(tokenize(t["query"]))
        qh = set(tokenize(t["history_query"]))
        oov: List[str] = []
        if q and n_vocab_known:
            oov = sorted(w for w in q if w not in vocab)
            oov_rates.append(len(oov) / len(q))
            oov_terms.update(oov)
        gl = [g for g in t["gold"] if g in gold_docs]
        ov = max((len(q & doc_tokens(g)) / len(q) if q else 0.0) for g in gl)
        ovh = max((len(qh & doc_tokens(g)) / len(qh) if qh else 0.0) for g in gl)
        best_ov.append(ov)
        best_ov_hist.append(ovh)
        t["best_gold_overlap"] = round(ov, 3)
        low_by_ctx[t.get("ctx", "standalone")].append(ov)
        if ov == 0 and len(zero_examples) < args.fix_cap:
            zero_examples.append({"qid": t["qid"], "gold": gl[:3],
                                  "query": snippet(t["query"], 140), "ctx": t.get("ctx")})
        qq = qh if (t.get("ctx") not in (None, "standalone") and qh) else q
        best: Tuple[int, Optional[int], Optional[float], str, str] = (0, None, None, "", "")
        for g in gl:
            L = max(1, len(gold_docs[g]["text"]))
            for off, st, stext in sents(g):
                sc = len(qq & st)
                if sc > best[0]:
                    best = (sc, off, off / L, stext, g)
        if best[1] is not None:
            abs_off.append(best[1])
            rel_pos.append(best[2])
            if best[1] > LATE_EVIDENCE_CHARS and len(late_examples) < args.fix_cap:
                late_examples.append({"qid": t["qid"], "offset": best[1], "gold": best[4],
                                      "query": snippet(t["query"], 120), "evidence": snippet(best[3], 160)})
        if oov and len(oov_examples) < args.fix_cap:
            oov_examples.append({"qid": t["qid"], "oov": oov[:8], "query": snippet(t["query"], 140)})
    n = len(ev)
    bins = [0, .2, .4, .6, .8, 1.0001]
    hist_rel = np.histogram(rel_pos, bins=bins)[0] if rel_pos else np.zeros(5)
    ao = np.array(abs_off) if abs_off else np.array([0])
    late_examples.sort(key=lambda x: -x["offset"])
    oov_examples.sort(key=lambda x: -len(x["oov"]))
    return {
        "turns_analyzed": n,
        "best_gold_overlap_mean": round(float(np.mean(best_ov)), 3),
        "best_gold_overlap_hist_mean": round(float(np.mean(best_ov_hist)), 3),
        "zero_overlap_turns": int(sum(1 for x in best_ov if x == 0)),
        "zero_overlap_pct": pct(sum(1 for x in best_ov if x == 0), n),
        "low_overlap_lt20_pct": pct(sum(1 for x in best_ov if x < 0.2), n),
        "zero_overlap_with_history_pct": pct(sum(1 for x in best_ov_hist if x == 0), n),
        "overlap_by_context_mean": {k: round(float(np.mean(v)), 3) for k, v in low_by_ctx.items()},
        "evidence_position": {
            "samples": len(rel_pos),
            "relative_hist_pct": {f"{int(bins[i] * 100)}-{min(100, int(round(bins[i + 1] * 100)))}%":
                                  pct(int(hist_rel[i]), max(1, len(rel_pos))) for i in range(5)},
            "median_abs_offset_chars": float(np.median(ao)),
            "after_650c_pct": pct(int((ao > 650).sum()), len(abs_off)),
            "after_1500c_pct": pct(int((ao > 1500).sum()), len(abs_off)),
            "after_512tok_approx_pct": pct(int((ao > EMBED_TOKEN_LIMIT_CHARS).sum()), len(abs_off)),
        },
        "oov": {"mean_query_oov_pct": round(float(np.mean(oov_rates)) * 100, 2) if oov_rates else 0.0,
                "turns_with_any_oov_pct": pct(sum(1 for r in oov_rates if r > 0), max(1, len(oov_rates))),
                "top_oov_terms": oov_terms.most_common(25),
                "note": f"so với từ vựng của mẫu {n_vocab_known:,} từ (pool + gold)"},
        "_zero_examples": zero_examples, "_late_examples": late_examples, "_oov_examples": oov_examples,
    }


# ===========================================================================
# 7. BM25 baseline
# ===========================================================================
class BM25Index:
    def __init__(self, k1: float = 1.2, b: float = 0.75):
        self.k1, self.b = k1, b
        self.postings: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        self.idf: Dict[str, float] = {}
        self.lens: List[int] = []
        self.owner: List[str] = []
        self.avgdl = 1.0

    def build(self, texts: List[str], owners: List[str]) -> None:
        self.owner = owners
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

    def search(self, query: str, top: int = 10) -> List[str]:
        qt = set(tokenize(query))
        scores: Dict[int, float] = defaultdict(float)
        for t in qt:
            post = self.postings.get(t)
            if not post:
                continue
            idf = self.idf[t]
            for ci, tf in post:
                scores[ci] += idf * tf * (self.k1 + 1) / (
                    tf + self.k1 * (1 - self.b + self.b * self.lens[ci] / self.avgdl))
        return [self.owner[ci] for ci, _ in sorted(scores.items(), key=lambda x: -x[1])[:top]]


def rank_metrics(ranked: List[str], gold: Set[str]) -> Dict[str, float]:
    rel = [1 if d in gold else 0 for d in ranked[:10]]
    dcg = sum(r / math.log2(i + 2) for i, r in enumerate(rel))
    ideal = sum(1 / math.log2(i + 2) for i in range(min(len(gold), 10)))
    mrr = next((1 / (i + 1) for i, d in enumerate(ranked[:10]) if d in gold), 0.0)
    return {"ndcg10": dcg / ideal if ideal else 0.0,
            "recall10": len(set(ranked[:10]) & gold) / len(gold) if gold else 0.0,
            "mrr10": mrr}


def group_stats(rows: List[Dict[str, Any]], keyfn: Callable[[Dict[str, Any]], str]) -> Dict[str, Dict[str, float]]:
    g: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        g[keyfn(r)].append(r)
    out = {}
    for k, rs in sorted(g.items()):
        out[k] = {"n": len(rs)}
        for m in ("ndcg10_single", "ndcg10_history", "recall10_single", "recall10_history"):
            out[k][m] = round(float(np.mean([r[m] for r in rs])), 4)
    return out


def analyze_retrieval(turns: List[Dict[str, Any]], scan: Dict[str, Any], args: argparse.Namespace,
                      rng: random.Random, dom: str) -> Dict[str, Any]:
    gold_docs, pool = scan["gold_docs"], scan["pool"]
    ev = []
    for t in turns:
        g = {x for x in t["gold"] if x in gold_docs}
        if g and t["query"].strip():
            ev.append({**t, "gold_found": g})
    if not ev:
        return {"note": "Không có query có gold hợp lệ -> bỏ qua retrieval"}
    if len(ev) > args.max_queries:
        ev = rng.sample(ev, args.max_queries)
    used: Set[str] = set()
    for t in ev:
        used |= t["gold_found"]
    distract = [d for d in pool if d["doc_id"] not in used][:args.retrieval_distractors]
    corpus = [gold_docs[g] for g in sorted(used)] + distract
    logger.info(f"[{dom}] BM25 whole-doc: {len(ev)} query, corpus con {len(corpus)} docs ...")
    idx = BM25Index()
    idx.build([d["text"] for d in corpus], [d["doc_id"] for d in corpus])
    rows = []
    for t in ev:
        rs = idx.search(t["query"], 10)
        rh = idx.search(t["history_query"], 10)
        ms, mh = rank_metrics(rs, t["gold_found"]), rank_metrics(rh, t["gold_found"])
        q = set(tokenize(t["query"]))
        ov = t.get("best_gold_overlap")
        if ov is None:
            ov = max((len(q & set(tokenize(gold_docs[g]["text"]))) / len(q) if q else 0.0)
                     for g in t["gold_found"])
        rows.append({"qid": t["qid"], "query": t["query"], "history_query": t["history_query"],
                     "ti": t["ti"], "ctx": t.get("ctx", "standalone"), "qtype": t.get("qtype", "?"),
                     "shift": t.get("shift", "n/a"), "gold": sorted(t["gold_found"]),
                     "top3": rs[:3], "overlap": ov,
                     "ndcg10_single": ms["ndcg10"], "recall10_single": ms["recall10"],
                     "mrr10_single": ms["mrr10"],
                     "ndcg10_history": mh["ndcg10"], "recall10_history": mh["recall10"],
                     "mrr10_history": mh["mrr10"]})
    hard = [r for r in rows if r["recall10_single"] == 0 and r["recall10_history"] == 0]
    reasons: Counter = Counter()
    for r in hard:
        if r["overlap"] < 0.2:
            reasons["lexical_gap (overlap<0.2)"] += 1
        elif r["ctx"] != "standalone":
            reasons["context_dependent"] += 1
        else:
            reasons["ranking/distractor"] += 1
    overall = {m: round(float(np.mean([r[m] for r in rows])), 4) for m in
               ("ndcg10_single", "ndcg10_history", "recall10_single", "recall10_history",
                "mrr10_single", "mrr10_history")}
    by_pos = group_stats(rows, lambda r: pos_bucket(r["ti"]))
    for k, v in by_pos.items():
        v["history_gain"] = round(v["ndcg10_history"] - v["ndcg10_single"], 4)
    return {
        "n_queries": len(rows), "n_gold_docs": len(used), "n_distractors": len(distract),
        "retriever": "BM25 (whole-document)",
        "overall": overall, "by_position": by_pos,
        "by_context": group_stats(rows, lambda r: r["ctx"]),
        "by_question_type": group_stats(rows, lambda r: r["qtype"]),
        "by_topic_shift": group_stats(rows, lambda r: r["shift"]),
        "hard_turns": {"count": len(hard), "pct": pct(len(hard), len(rows)), "reasons": dict(reasons)},
        "_hard_examples": [{"qid": r["qid"], "ti": r["ti"], "ctx": r["ctx"],
                            "overlap": round(r["overlap"], 3), "query": snippet(r["query"], 160),
                            "gold": r["gold"][:3], "top3": r["top3"]}
                           for r in sorted(hard, key=lambda x: x["overlap"])[:args.fix_cap]],
        "note": "Số tuyệt đối bị thổi phồng (corpus con); chỉ dùng để so sánh tương đối giữa các nhóm.",
    }


# ===========================================================================
# 8. Rò rỉ giữa các split
# ===========================================================================
def analyze_splits(domain_dir: Path, dev_turns: List[Dict[str, Any]], dev_gold: Set[str],
                   examples: int = 5) -> Dict[str, Any]:
    others = []
    for p in sorted(domain_dir.glob("benchmark_*.json")):
        name = p.stem.replace("benchmark_", "")
        if name != "dev":
            others.append((name, p))
    if not others:
        return {"note": "Không có split nào khác ngoài dev (benchmark_*.json)", "other_splits": [],
                "splits": {}}
    dev_q = {" ".join(t["query"].lower().split()) for t in dev_turns if t["query"].strip()}
    dev_sets = [(set(tokenize(q)), q) for q in dev_q]
    res: Dict[str, Any] = {"other_splits": [], "splits": {}}
    for name, p in others:
        qrels, _ = load_qrels(domain_dir / f"qrels_{name}.txt")
        parsed = parse_benchmark(p, qrels)
        if not parsed["ok"]:
            res["splits"][name] = {"note": parsed["meta"].get("note")}
            continue
        ts = parsed["turns"]
        sq = {" ".join(t["query"].lower().split()) for t in ts if t["query"].strip()}
        exact_set = sq & dev_q
        near = 0
        near_ex: List[Dict[str, str]] = []
        for q in sq - dev_q:
            qs = set(tokenize(q))
            if not qs:
                continue
            for ds, dq in dev_sets:
                if ds and len(qs & ds) / len(qs | ds) >= 0.9:
                    near += 1
                    if len(near_ex) < examples:
                        near_ex.append({"split_query": snippet(q, 120), "dev_query": snippet(dq, 120)})
                    break
        sg: Set[str] = set()
        for t in ts:
            sg |= set(t["gold"])
        shared_set = sg & dev_gold
        res["other_splits"].append(name)
        res["splits"][name] = {"turns": len(ts), "unique_queries": len(sq),
                               "exact_query_overlap": len(exact_set),
                               "exact_query_overlap_pct": pct(len(exact_set), len(sq)),
                               "near_query_overlap": near,
                               "near_query_overlap_pct": pct(near, len(sq)),
                               "gold_docs": len(sg), "shared_gold_with_dev": len(shared_set),
                               "shared_gold_pct": pct(len(shared_set), len(sg)),
                               "_exact_examples": [snippet(q, 140) for q in sorted(exact_set)[:examples]],
                               "_near_examples": near_ex,
                               "_shared_gold_examples": sorted(shared_set)[:examples]}
    return res


# ===========================================================================
# 9. Health score + khuyến nghị
# ===========================================================================
def compute_health(m: Dict[str, Any]) -> Dict[str, Any]:
    pens: List[Dict[str, Any]] = []
    comp_pen: Dict[str, float] = defaultdict(float)

    def pen(comp: str, name: str, value: Any, weight: float, cap: float = 60.0):
        try:
            v = float(value)
        except (TypeError, ValueError):
            return
        if math.isnan(v) or v <= 0:
            return
        p = min(cap, v * weight)
        comp_pen[comp] += p
        pens.append({"component": comp, "name": name, "value": round(v, 3),
                     "weight": weight, "penalty": round(p, 2)})

    present: Dict[str, bool] = {}

    ig = m.get("integrity")
    if ig:
        present["integrity"] = True
        d = ig["documents"]
        pen("integrity", "% dòng JSON lỗi", d["bad_json_pct"], 5)
        pen("integrity", "% doc thiếu doc_id", d["missing_id_pct"], 5)
        pen("integrity", "% doc_id trùng", d["duplicate_id_pct"], 5)
        pen("integrity", "% doc thiếu/sai trường text", d["missing_text_pct"], 5)
        pen("integrity", "% doc có mojibake", ig["encoding"]["mojibake_pct"], 2)
        pen("integrity", "% doc có ký tự điều khiển", ig["encoding"]["control_chars_pct"], 2)
        qrels_used = (m.get("gold") or {}).get("qrels_used_for_eval", False)
        for fname, ok in ig["files"].items():
            if not ok:
                if fname == "qrels_dev.txt":
                    if qrels_used:
                        pen("integrity", f"thiếu file {fname}", 1, 10)
                else:
                    pen("integrity", f"thiếu file {fname}", 1, 25)
        bench = ig.get("benchmark") or {}
        if bench.get("schema_type", "").startswith("message") and bench.get("non_alternating_roles_convs"):
            pen("integrity", "% hội thoại role không xen kẽ",
                pct(bench["non_alternating_roles_convs"], max(1, bench.get("n_conversations", 1))), 1)
        if bench.get("duplicate_conv_ids"):
            pen("integrity", "conversation_id trùng", bench["duplicate_conv_ids"], 2)

    ct = m.get("content")
    if ct:
        present["content"] = True
        fp = ct["flags_pct"]
        pen("content", "% doc rỗng", fp["empty"], 3)
        pen("content", "% doc quá ngắn", fp["too_short"], 0.5)
        pen("content", "% trùng chính xác", ct["exact_dup"]["duplicate_pct"], 1.0)
        pen("content", "% gần trùng (ngoài trùng chính xác)", ct["near_dup"].get("near_only_pct", 0), 0.7)
        pen("content", "% boilerplate", fp["boilerplate"], 0.3)
        pen("content", "% HTML sót", fp["html_residue"], 0.4)
        pen("content", "% nghi không phải tiếng Anh", fp["non_english"], 0.5)
        pen("content", "% lặp bất thường", fp["repetitive"], 0.5)
        pen("content", "% ký hiệu lạ/URL nặng", fp["symbol_heavy"] + fp["url_heavy"], 0.4)
        pen("content", "% chứa PII (email/phone)", fp["pii_email"] + fp["pii_phone"], 0.1, cap=10)

    cv = m.get("conversation")
    if cv and cv.get("total_turns"):
        present["conversation"] = True
        pen("conversation", "% query rỗng", cv["empty_query_pct"], 5)
        pen("conversation", "% query trùng", cv["duplicate_query_pct"], 0.5)
        pen("conversation", "% hội thoại có tham chiếu lơ lửng ở turn đầu",
            cv["turn0_dangling_ref"]["pct_of_conversations"], 1)
        pen("conversation", "% query quá ngắn (<=2 từ)", cv["very_short_query_pct"], 0.3)

    gd = m.get("gold")
    if gd and gd.get("turns"):
        present["gold"] = True
        pen("gold", "% cặp gold mồ côi (doc không có trong corpus)", gd["orphan_gold_pairs_pct"], 3)
        if gd.get("qrels_used_for_eval"):
            pen("gold", "% qrels qid mồ côi (không khớp turn)", gd["orphan_qrels_qids_pct"], 2)
        pen("gold", "% turn gold inline ≠ qrels", gd.get("gold_qrels_mismatch_pct", 0), 2)
        pen("gold", "% turn không có gold", gd["turns_without_gold_pct"], 1)
        pen("gold", "% gold có lỗi nội dung nghiêm trọng", gd["gold_serious_flag_pct"], 0.5)
        pen("gold", "% gold có bản gần trùng không-gold (false-negative)",
            gd["false_negative_candidates_pct"], 0.5)
        pen("gold", "% qrels malformed",
            pct(gd["qrels_file"].get("malformed", 0), max(1, gd["qrels_file"].get("lines", 1))), 3)

    lk = m.get("link")
    if lk and lk.get("turns_analyzed"):
        present["link"] = True
        pen("link", "% turn gold không chia sẻ từ nào với query", lk["zero_overlap_pct"], 1.5)
        pen("link", "% turn overlap=0 (kể cả history)", lk["zero_overlap_with_history_pct"], 0.5)
        pen("link", "% OOV trung bình của query", lk["oov"]["mean_query_oov_pct"], 0.3)

    comps = {c: round(max(0.0, 100.0 - comp_pen.get(c, 0.0)), 1) for c in present}
    if comps:
        wsum = sum(HEALTH_WEIGHTS[c] for c in comps)
        overall = round(sum(HEALTH_WEIGHTS[c] * comps[c] for c in comps) / wsum, 1)
        status = "green" if overall >= HEALTH_GREEN else ("yellow" if overall >= HEALTH_YELLOW else "red")
    else:
        overall, status = float("nan"), "n/a"
    comp_status = {c: ("green" if v >= HEALTH_GREEN else ("yellow" if v >= HEALTH_YELLOW else "red"))
                   for c, v in comps.items()}
    return {"overall": overall, "status": status, "components": comps,
            "component_status": comp_status,
            "penalties": sorted(pens, key=lambda x: -x["penalty"]),
            "weights": {c: HEALTH_WEIGHTS[c] for c in comps}}


def make_recommendations(m: Dict[str, Any]) -> List[Dict[str, str]]:
    rec: List[Dict[str, str]] = []

    def add(sev: str, text: str):
        rec.append({"severity": sev, "text": text})

    ig, ct, cv, gd, lk, rt, sp = (m.get(k) or {} for k in
                                  ("integrity", "content", "conversation", "gold", "link",
                                   "retrieval", "splits"))
    if ig:
        d = ig["documents"]
        if d["bad_json_lines"]:
            add("high", f"{d['bad_json_lines']} dòng JSON lỗi trong documents.jsonl -> sửa/loại.")
        if d["duplicate_doc_ids"]:
            add("high", f"{d['duplicate_doc_ids']} doc_id trùng -> qrels có thể trỏ nhầm.")
        if d["missing_id"]:
            add("high", f"{d['missing_id']} doc không có trường id -> ID bị sinh theo số dòng.")
        if ig["encoding"]["mojibake_pct"] > 0.1:
            add("medium", f"{ig['encoding']['mojibake_pct']}% doc có dấu hiệu lỗi encoding.")
        q = ig.get("qrels") or {}
        if q.get("malformed"):
            add("high", f"qrels có {q['malformed']} dòng sai format.")
        if q.get("duplicate_pairs"):
            add("low", f"qrels có {q['duplicate_pairs']} cặp (qid, doc) trùng.")
    if ct:
        fp = ct["flags_pct"]
        if fp["empty"] > 0 or fp["too_short"] > 1:
            add("medium", f"Rỗng {fp['empty']}% / quá ngắn {fp['too_short']}%.")
        if ct["exact_dup"]["duplicate_pct"] > 0.5:
            add("medium", f"Trùng chính xác {ct['exact_dup']['duplicate_pct']}%.")
        if ct["near_dup"].get("near_only_pct", 0) > 1:
            add("medium", f"Gần trùng {ct['near_dup']['near_only_pct']}% (MinHash).")
        if fp["boilerplate"] > 3 or fp["html_residue"] > 1:
            add("medium", f"Boilerplate {fp['boilerplate']}% / HTML sót {fp['html_residue']}%.")
        if fp["non_english"] > 1:
            add("low", f"{fp['non_english']}% doc nghi không phải tiếng Anh.")
        if fp["pii_email"] + fp["pii_phone"] > 1:
            add("low", "Có email/SĐT trong corpus -> cân nhắc ẩn danh.")
    if cv and cv.get("total_turns"):
        c = cv["context"]
        if c["dependent_pct_of_nonfirst"] > 30:
            add("high", f"{c['dependent_pct_of_nonfirst']}% turn sau turn đầu phụ thuộc ngữ cảnh "
                        f"-> cần query rewriter.")
        if cv["turn0_dangling_ref"]["count"]:
            add("medium", f"{cv['turn0_dangling_ref']['count']} hội thoại có đại từ/liên từ ở turn đầu.")
        if cv["empty_query_turns"]:
            add("high", f"{cv['empty_query_turns']} turn query rỗng -> loại khỏi đánh giá.")
        if cv["duplicate_query_pct"] > 2:
            add("low", f"{cv['duplicate_query_pct']}% query trùng nhau.")
    if gd and gd.get("turns"):
        if gd["orphan_gold_pairs"]:
            add("high", f"{gd['orphan_gold_pairs']} cặp gold trỏ tới doc KHÔNG có trong corpus.")
        if gd.get("qrels_qids_total") and gd.get("matched_qrels_qids", 0) == 0:
            add("medium", "Không khớp được qid qrels nào với turn trong benchmark -> kiểm tra format qid.")
        elif gd.get("orphan_qrels_qids"):
            add("high" if gd.get("qrels_used_for_eval") else "medium",
                f"{gd['orphan_qrels_qids']} qid trong qrels không khớp turn nào (qrels cũ/sai ID).")
        if gd.get("gold_qrels_mismatch_turns"):
            add("high", f"{gd['gold_qrels_mismatch_turns']} turn có gold inline KHÁC qrels.")
        if gd["turns_without_gold"]:
            add("medium", f"{gd['turns_without_gold']} turn không có gold.")
        if gd["false_negative_candidates_pct"] > 1:
            add("medium", f"{gd['false_negative_candidates']} gold có bản gần trùng KHÔNG phải gold.")
        if gd["gini_gold_reference"] > 0.5:
            add("low", f"Gold tập trung (Gini={gd['gini_gold_reference']}).")
        if gd["gold_serious_flag_pct"] > 5:
            add("medium", f"{gd['gold_serious_flag_pct']}% gold doc có lỗi nội dung nghiêm trọng.")
    if lk and lk.get("turns_analyzed"):
        if lk["zero_overlap_pct"] > 5:
            add("medium", f"{lk['zero_overlap_pct']}% turn gold KHÔNG chia sẻ từ nào với query.")
        ep = lk["evidence_position"]
        if ep["samples"] and ep["after_650c_pct"] > 40:
            add("medium", f"Bằng chứng nằm sau 650 ký tự ở {ep['after_650c_pct']}% gold.")
        if ep["samples"] and ep["after_512tok_approx_pct"] > 10:
            add("medium", f"Bằng chứng nằm sau ~512 token ở {ep['after_512tok_approx_pct']}% gold.")
    if rt and rt.get("n_queries"):
        if rt["hard_turns"]["pct"] > 20:
            add("medium", f"{rt['hard_turns']['pct']}% turn khó (recall@10=0).")
    if sp and sp.get("splits"):
        for name, s in sp["splits"].items():
            if s.get("exact_query_overlap_pct", 0) > 0 or s.get("shared_gold_pct", 0) > 50:
                add("high", f"Split '{name}': trùng query {s.get('exact_query_overlap_pct')}%, "
                            f"chia sẻ gold {s.get('shared_gold_pct')}% với dev.")
    if not rec:
        add("info", "Không phát hiện vấn đề vượt ngưỡng.")
    return rec


# ===========================================================================
# 10. Báo cáo Markdown / ví dụ lỗi / log / fix list
# ===========================================================================
def md_table(headers: List[str], rows: List[List[Any]], align: Optional[List[str]] = None) -> List[str]:
    align = align or [":---"] + ["---:"] * (len(headers) - 1)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(align) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "\\|") for x in r) + " |")
    return out


def badge(status: str) -> str:
    return {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(status, "⚪")


def build_report(dom: str, m: Dict[str, Any]) -> str:
    L: List[str] = []
    h = m["health"]
    L.append(f"# Báo cáo chất lượng dữ liệu — domain `{dom}`")
    L.append(f"\n*Tạo lúc {m['generated_at']} | RETECO Track 2 / Data Quality | "
             f"pha: {', '.join(m['phases'])}*\n")
    L.append("## 1. Health score\n")
    L.append(f"**Tổng: {h['overall']} {badge(h['status'])}** "
             f"(xanh ≥{HEALTH_GREEN:.0f}, vàng ≥{HEALTH_YELLOW:.0f}).\n")
    L += md_table(["Nhóm", "Trọng số", "Điểm", "Trạng thái"],
                  [[c, h["weights"][c], v, badge(h["component_status"][c])]
                   for c, v in h["components"].items()])
    L.append("\n**Top điểm trừ:**\n")
    L += md_table(["Nhóm", "Nguyên nhân", "Giá trị", "Hệ số", "Trừ"],
                  [[p["component"], p["name"], p["value"], p["weight"], p["penalty"]]
                   for p in h["penalties"][:12]])
    L.append("\n## 2. Khuyến nghị\n")
    for r in m["recommendations"]:
        L.append(f"- **[{r['severity']}]** {r['text']}")

    ig = m.get("integrity")
    if ig:
        d = ig["documents"]
        L.append("\n## 3. Toàn vẹn cấu trúc\n")
        L.append("- File: " + " | ".join(f"`{k}` {'✅' if v else '❌'}" for k, v in ig["files"].items()))
        L.append(f"- Documents: **{d['total_documents']:,}** | schema `{', '.join(d['schema_keys'])}` | "
                 f"JSON lỗi {d['bad_json_lines']} ({d['bad_json_pct']}%) | "
                 f"không phải object {d['not_dict_lines']} | thiếu id {d['missing_id']} | "
                 f"id trùng {d['duplicate_doc_ids']} | thiếu text {d['missing_text_field']} | "
                 f"text sai kiểu {d['non_str_text']} | title rỗng {d['title_missing']}")
        e = ig["encoding"]
        L.append(f"- Encoding: mojibake {e['mojibake_pct']}% | "
                 f"ký tự điều khiển {e['control_chars_pct']}% | HTML/entity sót {e['html_residue_pct']}%")
        inc = {k: v for k, v in d["key_consistency_pct"].items() if v < 99.9}
        if inc:
            L.append(f"- ⚠ Trường không xuất hiện ở mọi doc: {inc}")
        if ig.get("benchmark"):
            b = ig["benchmark"]
            L.append(f"- Benchmark: {b.get('n_conversations', 0)} hội thoại | "
                     f"schema=`{b.get('schema_type')}` | vai trò {b.get('roles')} | "
                     f"role không xen kẽ {b.get('non_alternating_roles_convs', 0)} | "
                     f"hội thoại rỗng {b.get('empty_conversations', 0)} | "
                     f"conv_id trùng {b.get('duplicate_conv_ids', 0)} | "
                     f"qid qrels khớp {b.get('matched_qrels_qids', 0)}/{b.get('qrels_qids_total', 0)}")
        if ig.get("qrels"):
            q = ig["qrels"]
            L.append(f"- qrels: {q.get('lines', 0)} dòng | malformed {q.get('malformed', 0)} | "
                     f"cặp trùng {q.get('duplicate_pairs', 0)} | "
                     f"mức relevance {q.get('relevance_levels')} | qid {q.get('n_qids', 0)}")
    ct = m.get("content")
    if ct:
        cl = ct["char_length"]
        L.append("\n## 4. Chất lượng nội dung\n")
        L.append(f"- Ký tự: min={cl['min']} p25={cl['p25']} **median={cl['median']}** mean={cl['mean']} "
                 f"p75={cl['p75']} p90={cl['p90']} p99={cl['p99']} max={cl['max']} | "
                 f"outlier dài (>{ct['long_outlier_threshold_chars']}c): {ct['long_outlier_pct']}%")
        L.append("- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: " + " / ".join(f"{v}%" for v in ct["share_le_chars_pct"].values()))
        L.append("\n**Histogram độ dài:**\n")
        L += md_table(["Khoảng (ký tự)", "% doc"], [[k, f"{v}%"] for k, v in ct["length_buckets_pct"].items()])
        L.append("\n**Cờ lỗi:**\n")
        L += md_table(["Cờ", "Mô tả", "Số doc", "%"],
                      [[f, FLAG_DESC[f], ct["flags_count"][f], f"{ct['flags_pct'][f]}%"] for f in FLAGS])
        L.append(f"\n- Doc có ≥1 lỗi NGHIÊM TRỌNG: **{ct['serious_flag_pct']}%**")
        ex, nd = ct["exact_dup"], ct["near_dup"]
        L.append(f"- Trùng chính xác: {ex['duplicate_docs']:,} doc dư ({ex['duplicate_pct']}%), {ex['groups']} nhóm")
        L.append(f"- Gần trùng: {nd['clusters']} cụm | doc dư gần-trùng ngoài trùng chính xác "
                 f"{nd['near_only_removable']} ({nd['near_only_pct']}%) | cụm lớn nhất {nd['largest_cluster']}")
        v = ct["vocab"]
        L.append(f"- Từ vựng (mẫu {v.get('n_docs', 0):,} doc): {v.get('size', 0):,} từ | "
                 f"hapax {v.get('hapax_pct')}% | Zipf {v.get('zipf_slope')} | "
                 + ", ".join(f"{w}({c})" for w, c in v.get("top_terms", [])[:15]))
    cv = m.get("conversation")
    if cv and cv.get("total_turns"):
        L.append("\n## 5. Hội thoại\n")
        t, q = cv["turns_per_conversation"], cv["query_word_length"]
        L.append(f"- **{cv['total_conversations']}** hội thoại, **{cv['total_turns']}** turn | "
                 f"turn/hội thoại: mean {t['mean']} (min {t['min']}, max {t['max']}) | "
                 f"query: mean {q['mean']} từ, median {q['median']}, p95 {q['p95']}")
        L.append(f"- Query rỗng {cv['empty_query_turns']} | trùng {cv['duplicate_query_turns']} "
                 f"({cv['duplicate_query_pct']}%) | ≤2 từ {cv['very_short_query_pct']}%")
        c = cv["context"]
        L.append("\n**Phụ thuộc ngữ cảnh:**\n")
        L += md_table(["Loại", "Số turn", "%"],
                      [[k, c["counts"].get(k, 0), f"{c['pct'].get(k, 0)}%"]
                       for k in ("standalone", "pronoun", "connector", "short_ellipsis")])
        L.append(f"\n→ **{c['dependent_pct_of_nonfirst']}%** turn sau turn đầu cần rewrite.")
        L.append(f"- Turn đầu có đại từ/liên từ lơ lửng: {cv['turn0_dangling_ref']['count']} "
                 f"({cv['turn0_dangling_ref']['pct_of_conversations']}%)")
        ts = cv["topic_shift"]
        L.append(f"- Chuyển chủ đề: {ts['pct']} | hội thoại nhảy chủ đề ≥50% turn: {ts['convs_mostly_shifting_pct']}%")
        L.append("\n**Loại câu hỏi:** " + ", ".join(
            f"{k} {v}%" for k, v in sorted(cv["question_types"]["pct"].items(), key=lambda x: -x[1])))
    gd = m.get("gold")
    if gd and gd.get("turns"):
        L.append("\n## 6. Gold / qrels\n")
        L.append(f"- Nguồn gold: {gd['gold_source']} | qrels được dùng để eval: {gd.get('qrels_used_for_eval', False)}")
        L.append(f"- Gold/turn: mean {gd['gold_per_turn']['mean']}, max {gd['gold_per_turn']['max']}")
        L.append(f"- Turn không gold: **{gd['turns_without_gold']}** ({gd['turns_without_gold_pct']}%)")
        L.append(f"- Gold mồ côi: **{gd['orphan_gold_pairs']}** cặp "
                 f"({gd['orphan_gold_pairs_pct']}%), {gd['orphan_gold_unique_docs']} doc")
        L.append(f"- qrels: khớp {gd.get('matched_qrels_qids', 0)}/{gd['qrels_qids_total']} qid | "
                 f"mồ côi **{gd['orphan_qrels_qids']}** ({gd['orphan_qrels_qids_pct']}%) | "
                 f"gold inline ≠ qrels: **{gd.get('gold_qrels_mismatch_turns', 0)}** turn")
        L.append(f"- Doc chưa từng là gold: {gd['docs_never_gold']:,}/{gd['corpus_docs']:,} "
                 f"({gd['docs_never_gold_pct']}%) | Gini {gd['gini_gold_reference']}")
        ln = gd.get("length") or {}
        if ln:
            L.append(f"- Độ dài gold vs corpus (median): {ln['gold_median']} vs {ln['corpus_median']} "
                     f"(tỷ lệ {ln['median_ratio_gold_over_corpus']}x)")
        L.append(f"- Gold có lỗi nghiêm trọng: {gd['gold_serious_flag_pct']}% | "
                 f"false-negative tiềm năng: {gd['false_negative_candidates']} "
                 f"({gd['false_negative_candidates_pct']}%) | gold trùng nhau: {gd['redundant_gold_dups']}")
    lk = m.get("link")
    if lk and lk.get("turns_analyzed"):
        ep = lk["evidence_position"]
        L.append("\n## 7. Liên kết query ↔ gold\n")
        L.append(f"- Lexical overlap: mean **{lk['best_gold_overlap_mean']}** "
                 f"(có history: {lk['best_gold_overlap_hist_mean']}) | "
                 f"overlap=0: {lk['zero_overlap_pct']}% | <20%: {lk['low_overlap_lt20_pct']}% | "
                 f"overlap=0 dù có history: {lk['zero_overlap_with_history_pct']}%")
        L.append(f"- Overlap theo ngữ cảnh: {lk['overlap_by_context_mean']}")
        L.append(f"- OOV: {lk['oov']['turns_with_any_oov_pct']}% (TB {lk['oov']['mean_query_oov_pct']}%)")
        L.append(f"- **Vị trí bằng chứng** ({ep['samples']} mẫu): {ep['relative_hist_pct']} | "
                 f"median offset {ep['median_abs_offset_chars']:.0f}c | "
                 f"sau 650c: {ep['after_650c_pct']}% | sau 512 token: {ep['after_512tok_approx_pct']}%")
    rt = m.get("retrieval")
    if rt and rt.get("n_queries"):
        L.append("\n## 8. BM25 baseline\n")
        L.append(f"- {rt['n_queries']} query | {rt['n_gold_docs']} gold + {rt['n_distractors']} nhiễu")
        o = rt["overall"]
        L.append(f"- nDCG@10 single/history = {o['ndcg10_single']}/{o['ndcg10_history']} | "
                 f"Recall@10 = {o['recall10_single']}/{o['recall10_history']}")
        for title, key in (("Vị trí turn", "by_position"), ("Ngữ cảnh", "by_context"),
                           ("Loại câu hỏi", "by_question_type"), ("Chuyển chủ đề", "by_topic_shift")):
            L.append(f"\n**{title}:**\n")
            L += md_table(["Nhóm", "n", "nDCG single", "nDCG history", "R@10 single", "R@10 history"],
                          [[k, v["n"], v["ndcg10_single"], v["ndcg10_history"],
                            v["recall10_single"], v["recall10_history"]] for k, v in rt[key].items()])
        L.append(f"\n- Turn khó: **{rt['hard_turns']['count']}** ({rt['hard_turns']['pct']}%) — "
                 f"{rt['hard_turns']['reasons']}")
    sp = m.get("splits")
    if sp:
        L.append("\n## 9. Rò rỉ giữa các split\n")
        if not sp.get("splits"):
            L.append(f"- {sp.get('note')}")
        else:
            L += md_table(["Split", "Turn", "Query trùng dev", "Query gần-trùng dev", "Gold chung dev"],
                          [[n, s.get("turns", "-"),
                            f"{s.get('exact_query_overlap', '-')} ({s.get('exact_query_overlap_pct', '-')}%)",
                            f"{s.get('near_query_overlap', '-')} ({s.get('near_query_overlap_pct', '-')}%)",
                            f"{s.get('shared_gold_with_dev', '-')} ({s.get('shared_gold_pct', '-')}%)"]
                           for n, s in sp["splits"].items()])
    L.append("\n## 10. Giới hạn\n")
    L += ["- Cờ nội dung là HEURISTIC (regex, tỷ lệ stopword) → có dương tính giả.",
          "- Gần trùng: MinHash trên 5-word shingle, tối đa 1500 shingle đầu.",
          "- Phụ thuộc ngữ cảnh / loại câu hỏi dựa trên regex tiếng Anh.",
          "- Vị trí bằng chứng dựa trên trùng từ khóa (không phải đánh giá câu trả lời thật).",
          "- BM25 chạy trên corpus con: chỉ so sánh tương đối.",
          "- Health score là chỉ báo thô; hệ số trừ nằm trong `compute_health()`."]
    return "\n".join(L)


def build_error_examples(dom: str, scan: Optional[Dict[str, Any]], m: Dict[str, Any], n: int) -> str:
    """Ví dụ cụ thể cho TẤT CẢ loại lỗi. Loại không có lỗi vẫn được liệt kê ('✅ Không phát hiện')."""
    L: List[str] = []
    snips: Dict[str, str] = (scan or {}).get("doc_snippets", {})

    def sec(title: str, count: Any, body: List[str], note: str = ""):
        if not count:
            L.append(f"\n### ✅ {title}\n- Không phát hiện.")
            return
        L.append(f"\n### ❌ {title} — {count:,}\n" if isinstance(count, int) else f"\n### ❌ {title} — {count}\n")
        if note:
            L.append(f"*{note}*\n")
        L.extend(body)

    def block(text: str) -> str:
        return f"```text\n{text}\n```"

    def trunc(lst, k=None):
        return list(lst)[: (k or n)]

    # ---------- A. Toàn vẹn ----------
    L.append("\n## A. Toàn vẹn cấu trúc")
    ig = m.get("integrity")
    if ig:
        missing_files = [k for k, v in ig["files"].items() if not v]
        sec("File bị thiếu", len(missing_files), [f"- `{k}`" for k in missing_files])
    if scan:
        st = scan["stats"]
        fe = scan.get("field_examples", {})
        bad = scan["bad_examples"]
        sec("Dòng JSON lỗi / không phải object", st["bad_json_lines"] + st["not_dict_lines"],
            [f"- dòng {b['line']}: {b['error']} — `{b['head']}`" for b in trunc(bad)])
        sec("Doc thiếu trường id", st["missing_id"],
            [f"- dòng {e['line']}: `{e['head']}`" for e in trunc(fe.get("missing_id", []))])
        dups = scan["dup_id_examples"]
        sec("doc_id trùng", st["duplicate_doc_ids"],
            [f"- `{d}`" + (f": {snips[d]}" if d in snips else "") for d in trunc(dups)])
        sec("Doc thiếu trường text", st["missing_text_field"],
            [f"- dòng {e['line']} (`{e['doc_id']}`): `{e['head']}`" for e in trunc(fe.get("missing_text", []))])
        sec("Trường text sai kiểu (không phải string)", st["non_str_text"],
            [f"- dòng {e['line']} (`{e['doc_id']}`): `{e['head']}`" for e in trunc(fe.get("non_str_text", []))])
        sec("Trường title rỗng/sai", st["title_missing"],
            [f"- dòng {e['line']}: `{e['doc_id']}`" for e in trunc(fe.get("title_missing", []))])
    if ig and ig.get("qrels"):
        q = ig["qrels"]
        sec("qrels: dòng sai format", q.get("malformed", 0),
            [f"- dòng {e['line']} ({e['why']}): `{e['raw']}`" for e in trunc(q.get("_malformed_examples", []))])
        sec("qrels: cặp (qid, doc) trùng", q.get("duplicate_pairs", 0),
            [f"- dòng {e['line']}: `{e['qid']}` → `{e['doc_id']}`" for e in trunc(q.get("_dup_examples", []))])
        sec("qrels: relevance ≤ 0", q.get("non_positive", 0),
            [f"- dòng {e['line']}: `{e['qid']}` → `{e['doc_id']}` (rel={e['rel']})"
             for e in trunc(q.get("_nonpos_examples", []))])
    if ig and ig.get("benchmark"):
        b = ig["benchmark"]
        sec("Benchmark: conversation_id trùng", b.get("duplicate_conv_ids", 0),
            [f"- `{x}`" for x in trunc(b.get("_dup_conv_ids", []))])
        sec("Benchmark: hội thoại rỗng", b.get("empty_conversations", 0),
            [f"- `{x}`" for x in trunc(b.get("_empty_conv_ids", []))])
        sec("Benchmark: role không xen kẽ", b.get("non_alternating_roles_convs", 0),
            [f"- `{x}`" for x in trunc(b.get("_nonalt_conv_ids", []))])
        sec("Benchmark: turn thiếu query", b.get("missing_query_turns", 0),
            [f"- `{x}`" for x in trunc(b.get("_missing_query_qids", []))])

    # ---------- B. Nội dung ----------
    L.append("\n## B. Chất lượng nội dung tài liệu")
    if scan:
        st = scan["stats"]
        for fl in FLAGS:
            exs = scan["flag_examples"].get(fl, [])
            body: List[str] = []
            for e in trunc(exs):
                body.append(f"**`{e['doc_id']}`** ({e['chars']} ký tự)\n{block(e['snippet'])}")
            sec(f"`{fl}` — {FLAG_DESC[fl]}", st["flags_count"][fl], body)
        ex = st["exact_dup"]
        body = []
        for g in trunc(scan["exact_examples"]):
            body.append("- nhóm: " + ", ".join(f"`{x}`" for x in g))
            if g and g[0] in snips:
                body.append(block(snips[g[0]]))
        sec("Trùng chính xác", ex["duplicate_docs"], body, f"{ex['groups']} nhóm")
        nd = st["near_dup"]
        body = []
        for e in trunc(nd["examples"]):
            body.append(f"- cụm size {e['size']}: " + ", ".join(f"`{x}`" for x in e["doc_ids"]))
            for did in e["doc_ids"][:2]:
                if did in snips:
                    body.append(f"  - `{did}`:\n{block(snips[did])}")
        sec("Gần trùng (khác nhau chút ít)", nd["near_only_removable"], body,
            "MinHash — doc cùng cụm nhưng nội dung không giống hệt")

    # ---------- C. Hội thoại ----------
    L.append("\n## C. Hội thoại / query")
    cv = m.get("conversation")
    if cv and cv.get("total_turns"):
        sec("Query rỗng", cv["empty_query_turns"], [f"- `{e['qid']}`" for e in trunc(cv["empty_query_list"])])
        sec("Query trùng nhau", cv["duplicate_query_turns"],
            [f"- ×{e['count']} `{e['query']}` — {', '.join('`'+x+'`' for x in e['qids'])}"
             for e in trunc(cv.get("_dup_examples", []))])
        sec("Query quá ngắn (≤ 2 từ)", int(round(cv["very_short_query_pct"] * cv["total_turns"] / 100)),
            [f"- `{e['qid']}`: {e['query']}" for e in trunc(cv.get("_short_examples", []))])
        sec("Query quá dài (> 60 từ)", int(round(cv["very_long_query_pct"] * cv["total_turns"] / 100)),
            [f"- `{e['qid']}` ({e['words']} từ): {e['query']}" for e in trunc(cv.get("_long_examples", []))])
        d0 = cv["turn0_dangling_ref"]
        sec("Turn đầu có đại từ/liên từ lơ lửng", d0["count"],
            [f"- `{e['qid']}`: {e['query']}" for e in trunc(d0["examples"])])
        ce = cv.get("_ctx_examples", {})
        for kind, label in (("pronoun", "đại từ"), ("connector", "liên từ"), ("short_ellipsis", "câu ngắn/tỉnh lược")):
            sec(f"Turn phụ thuộc ngữ cảnh — {label} (cần rewrite)", cv["context"]["counts"].get(kind, 0),
                [f"- `{e['qid']}`: {e['query']}" for e in trunc(ce.get(kind, []))])
        sec("Nhảy chủ đề đột ngột giữa 2 turn liền kề", cv["topic_shift"]["counts"].get("shift", 0),
            [f"- `{e['qid']}` (cos={e['cos']})\n  - trước: {e['prev']}\n  - sau: {e['query']}"
             for e in trunc(cv.get("_shift_examples", []))])

    # ---------- D. Gold / qrels ----------
    L.append("\n## D. Gold / qrels")
    gd = m.get("gold")
    if gd and gd.get("turns"):
        sec("Gold mồ côi (doc không có trong corpus)", gd["orphan_gold_pairs"],
            [f"- `{p['qid']}` → `{p['doc_id']}`" for p in trunc(gd["_orphan_pairs"])])
        sec("qrels qid không khớp turn nào", gd["orphan_qrels_qids"],
            [f"- `{x}`" for x in trunc(gd["_orphan_qrels"])])
        sec("Gold inline (benchmark) ≠ qrels", gd.get("gold_qrels_mismatch_turns", 0),
            [f"- `{e['qid']}`: chỉ có ở inline {e['inline_only']} | chỉ có ở qrels {e['qrels_only']}"
             for e in trunc(gd["_mismatch"])])
        sec("Turn không có gold", gd["turns_without_gold"],
            [f"- `{t['qid']}`: {t['query']}" for t in trunc(gd["_no_gold"])])
        sec("Gold doc có lỗi nội dung nghiêm trọng", gd["gold_serious_flag_docs"],
            [f"- `{e['doc_id']}` {e['flags']}\n{block(e['snippet'])}" for e in trunc(gd["_gold_flag_examples"])])
        sec("Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)", gd["false_negative_candidates"],
            [f"- gold {e['gold']} ↔ bản sao {e['non_gold_twins']}" for e in trunc(gd["false_negative_examples"])])
    else:
        L.append("- (không có dữ liệu gold)")

    # ---------- E. Liên kết ----------
    L.append("\n## E. Liên kết query ↔ gold")
    lk = m.get("link")
    if lk and lk.get("turns_analyzed"):
        sec("Query không chia sẻ từ nào với gold", lk["zero_overlap_turns"],
            [f"- `{e['qid']}` ({e['ctx']}) gold={e['gold']}: {e['query']}" for e in trunc(lk.get("_zero_examples", []))])
        ep = lk["evidence_position"]
        late_n = int(round(ep["after_1500c_pct"] * ep["samples"] / 100)) if ep["samples"] else 0
        sec(f"Bằng chứng nằm muộn (> {LATE_EVIDENCE_CHARS} ký tự)", late_n,
            [f"- `{e['qid']}` offset={e['offset']}c gold=`{e['gold']}`\n  - query: {e['query']}\n  - bằng chứng: {e['evidence']}"
             for e in trunc(lk.get("_late_examples", []))])
        oov_n = int(round(lk["oov"]["turns_with_any_oov_pct"] * lk["turns_analyzed"] / 100))
        sec("Query chứa từ không có trong từ vựng corpus (OOV)", oov_n,
            [f"- `{e['qid']}` OOV={e['oov']}: {e['query']}" for e in trunc(lk.get("_oov_examples", []))])
    else:
        L.append("- (không có dữ liệu link)")

    # ---------- F. Retrieval ----------
    L.append("\n## F. Turn khó với BM25 (recall@10 = 0)")
    rt = m.get("retrieval")
    if rt and rt.get("n_queries"):
        sec("Turn khó", rt["hard_turns"]["count"],
            [f"- `{e['qid']}` ti={e['ti']} ctx={e['ctx']} overlap={e['overlap']}: {e['query']}\n"
             f"  - gold {e['gold']} | top3 {e['top3']}" for e in trunc(rt.get("_hard_examples", []))],
            f"nguyên nhân: {rt['hard_turns']['reasons']}")
    else:
        L.append("- (không có dữ liệu retrieval)")

    # ---------- G. Splits ----------
    L.append("\n## G. Rò rỉ giữa các split")
    sp = m.get("splits")
    if sp and sp.get("splits"):
        for name, s in sp["splits"].items():
            sec(f"Split `{name}`: query trùng hệt với dev", s.get("exact_query_overlap", 0),
                [f"- {q}" for q in trunc(s.get("_exact_examples", []))])
            sec(f"Split `{name}`: query gần trùng dev (Jaccard ≥ 0.9)", s.get("near_query_overlap", 0),
                [f"- {name}: {e['split_query']}\n  - dev: {e['dev_query']}" for e in trunc(s.get("_near_examples", []))])
            sec(f"Split `{name}`: gold doc dùng chung với dev", s.get("shared_gold_with_dev", 0),
                [f"- `{x}`" for x in trunc(s.get("_shared_gold_examples", []))])
    else:
        L.append("- (không có split khác để so sánh)")
    return "\n".join(L)


def build_health_log(dom: str, m: Dict[str, Any]) -> str:
    h = m["health"]
    bar = "=" * 80
    L = [bar, f"LOG HEALTH & CHẤT LƯỢNG DỮ LIỆU — RETECO TRACK 2 — DOMAIN: {dom.upper()}",
         f"Thời điểm: {m['generated_at']} | pha: {', '.join(m['phases'])}", bar, "",
         f"HEALTH TỔNG: {h['overall']}  [{h['status'].upper()}]", "-" * 80]
    for c, v in h["components"].items():
        L.append(f"  {c:<14} {v:>6}  [{h['component_status'][c]}]  (trọng số {h['weights'][c]})")
    L += ["", "CHI TIẾT ĐIỂM TRỪ (value × weight, cap 60/mục):", "-" * 80]
    for p in h["penalties"]:
        L.append(f"  [{p['component']:<12}] {p['name']:<60} value={p['value']:<9} x{p['weight']:<4} = -{p['penalty']}")
    if not h["penalties"]:
        L.append("  (không có điểm trừ)")
    L += ["", "KHUYẾN NGHỊ:", "-" * 80]
    for r in m["recommendations"]:
        L.append(f"  [{r['severity'].upper():<6}] {r['text']}")
    L += ["", bar]
    return "\n".join(L)


def build_inspection(dom: str, scan: Optional[Dict[str, Any]], m: Dict[str, Any], examples: int) -> str:
    head = [f"# Soi bản ghi lỗi — domain `{dom}`\n",
            "*Mẫu để đọc bằng tay (nhiều ví dụ hơn báo cáo chính); danh sách đầy đủ trong `dq_fix_list_*.csv`.*"]
    return "\n".join(head) + build_error_examples(dom, scan, m, examples * 2)


def write_fix_list(path: Path, dom: str, scan: Optional[Dict[str, Any]], m: Dict[str, Any], cap: int) -> int:
    rows: List[List[str]] = []

    def add(kind: str, sev: str, ident: str, detail: str):
        rows.append([dom, kind, sev, ident, detail])

    if scan:
        for b in scan["bad_examples"][:cap]:
            add("bad_json_line", "high", f"line:{b['line']}", b["error"])
        for d in scan["dup_id_examples"][:cap]:
            add("duplicate_doc_id", "high", d, "doc_id xuất hiện nhiều lần")
        sev = {"empty": "high", "mojibake": "medium", "control_chars": "medium", "html_residue": "medium",
               "boilerplate": "low", "too_short": "medium", "url_heavy": "low", "symbol_heavy": "low",
               "repetitive": "low", "non_english": "low", "pii_email": "low", "pii_phone": "low",
               "possibly_truncated": "low"}
        for fl, idl in scan["flag_ids"].items():
            if fl == "starts_lower":
                continue
            for d in idl[:cap]:
                add(f"doc_{fl}", sev.get(fl, "low"), d, FLAG_DESC[fl])
        for d in scan["exact_dup_ids"][:cap]:
            add("doc_exact_duplicate", "medium", d, "bản sao chính xác (giữ 1 bản)")
    q = (m.get("integrity") or {}).get("qrels") or {}
    for e in q.get("_malformed_examples", []):
        add("qrels_malformed", "high", f"line:{e['line']}", e["raw"])
    gd = m.get("gold") or {}
    for p in gd.get("_orphan_pairs", [])[:cap]:
        add("orphan_gold", "high", p["qid"], f"gold doc {p['doc_id']} không có trong corpus")
    if gd.get("qrels_used_for_eval") or gd.get("matched_qrels_qids"):
        for x in gd.get("_orphan_qrels", [])[:cap]:
            add("orphan_qrels_qid", "high", x, "qid trong qrels không khớp turn nào")
    for e in gd.get("_mismatch", []):
        add("gold_qrels_mismatch", "high", e["qid"], f"inline_only={e['inline_only']} qrels_only={e['qrels_only']}")
    for t in gd.get("_no_gold", [])[:cap]:
        add("turn_without_gold", "medium", t["qid"], t["query"])
    for d in gd.get("_fn_ids", [])[:cap]:
        add("possible_false_negative", "medium", d, "gần trùng một gold doc nhưng không phải gold")
    for e in gd.get("_gold_flag_examples", []):
        add("gold_doc_serious_flag", "medium", e["doc_id"], ",".join(e["flags"]))
    cv = m.get("conversation") or {}
    for e in cv.get("empty_query_list", [])[:cap]:
        add("empty_query", "high", e["qid"], "query rỗng")
    for e in cv.get("_dup_examples", []):
        add("duplicate_query", "low", ";".join(e["qids"]), e["query"])
    for e in cv.get("turn0_dangling_ref", {}).get("examples", []):
        add("turn0_dangling_reference", "medium", e["qid"], e["query"])
    lk = m.get("link") or {}
    for e in lk.get("_zero_examples", [])[:cap]:
        add("zero_lexical_overlap", "medium", e["qid"], f"gold {e['gold']} | {e['query']}")
    for e in lk.get("_late_examples", [])[:cap]:
        add("late_evidence", "low", e["qid"], f"offset={e['offset']} gold={e['gold']}")
    for e in (m.get("retrieval") or {}).get("_hard_examples", [])[:cap]:
        add("hard_turn_bm25", "info", e["qid"], f"overlap={e['overlap']} | {e['query']}")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["domain", "issue_type", "severity", "id", "detail"])
        w.writerows(rows)
    return len(rows)


# ===========================================================================
# 11. Viz: hình theo domain + liên corpus + summary + HTML
# ===========================================================================
def _savefig(fig, path: Path, paths: List[Path]):
    fig.savefig(path)
    plt.close(fig)
    paths.append(path)


def make_figures(m: Dict[str, Any], out_dir: Path) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []
    dom = m["domain"]
    ct, cv, gd, lk, rt = (m.get(k) for k in ("content", "conversation", "gold", "link", "retrieval"))

    if ct:
        try:
            fig, ax = plt.subplots(1, 2, figsize=(11, 4))
            cl = ct["char_length"]
            qs = [cl["min"], cl["p10"], cl["p25"], cl["median"], cl["p75"], cl["p90"], cl["p95"], cl["p99"], cl["max"]]
            labels = ["min", "p10", "p25", "p50", "p75", "p90", "p95", "p99", "max"]
            ax[0].bar(range(len(qs)), qs, color=PALETTE["blue"], alpha=0.85)
            ax[0].set_xticks(range(len(qs)))
            ax[0].set_xticklabels(labels, rotation=45)
            ax[0].set_ylabel("chars")
            ax[0].set_title(f"[{dom}] Độ dài tài liệu (quantiles)")
            b = ct["length_buckets_pct"]
            ax[1].barh(list(b.keys()), list(b.values()), color=PALETTE["teal"])
            ax[1].set_xlabel("%")
            ax[1].set_title("Phân bố bucket độ dài")
            fig.tight_layout()
            _savefig(fig, out_dir / f"dq_fig1_length_{dom}.png", paths)
        except Exception as e:
            logger.warning(f"[{dom}] Fig1 lỗi: {e}")
        try:
            fig, ax = plt.subplots(figsize=(10, 5))
            fp = ct["flags_pct"]
            keys = sorted(fp.keys(), key=lambda k: -fp[k])
            ax.barh(keys, [fp[k] for k in keys],
                    color=[PALETTE["red"] if k in SERIOUS_FLAGS else PALETTE["orange"] for k in keys])
            ax.set_xlabel("% doc")
            ax.set_title(f"[{dom}] Tỷ lệ cờ lỗi (đỏ = nghiêm trọng)")
            fig.tight_layout()
            _savefig(fig, out_dir / f"dq_fig2_flags_{dom}.png", paths)
        except Exception as e:
            logger.warning(f"[{dom}] Fig2 lỗi: {e}")
        if ct.get("vocab", {}).get("zipf_points"):
            try:
                fig, ax = plt.subplots(figsize=(7, 5))
                pts = [p for p in ct["vocab"]["zipf_points"] if p[1] > 0]
                ax.loglog([p[0] for p in pts], [p[1] for p in pts], "o-", markersize=2,
                          color=PALETTE["purple"], alpha=0.7)
                ax.set_xlabel("rank")
                ax.set_ylabel("frequency")
                ax.set_title(f"[{dom}] Zipf (slope={ct['vocab'].get('zipf_slope')})")
                fig.tight_layout()
                _savefig(fig, out_dir / f"dq_fig3_zipf_{dom}.png", paths)
            except Exception as e:
                logger.warning(f"[{dom}] Fig3 lỗi: {e}")
        try:
            fig, ax = plt.subplots(figsize=(7, 4))
            vals = [ct["exact_dup"]["duplicate_pct"], ct["near_dup"].get("near_only_pct", 0)]
            ax.bar(["exact dup", "near-only dup"], vals, color=[PALETTE["red"], PALETTE["orange"]])
            for i, v in enumerate(vals):
                ax.text(i, v, f"{v}%", ha="center", va="bottom")
            ax.set_ylabel("% doc")
            ax.set_title(f"[{dom}] Trùng lặp")
            fig.tight_layout()
            _savefig(fig, out_dir / f"dq_fig4_dup_{dom}.png", paths)
        except Exception as e:
            logger.warning(f"[{dom}] Fig4 lỗi: {e}")

    if cv and cv.get("total_turns"):
        try:
            fig, ax = plt.subplots(1, 2, figsize=(11, 4))
            q = cv["query_word_length"]
            ax[0].bar(["min", "median", "p95", "max"], [q["min"], q["median"], q["p95"], q["max"]],
                      color=PALETTE["blue"])
            ax[0].set_ylabel("words")
            ax[0].set_title(f"Query length | mean={q['mean']}")
            ctx = cv["context"]["counts"]
            if ctx:
                cols = [PALETTE[c] for c in ["green", "orange", "red", "blue"][:len(ctx)]]
                ax[1].pie(list(ctx.values()), labels=list(ctx.keys()), autopct="%1.1f%%", colors=cols)
                ax[1].set_title("Loại ngữ cảnh")
            fig.tight_layout()
            _savefig(fig, out_dir / f"dq_fig5_query_{dom}.png", paths)
        except Exception as e:
            logger.warning(f"[{dom}] Fig5 lỗi: {e}")

    if gd and gd.get("turns"):
        try:
            fig, ax = plt.subplots(figsize=(9, 4))
            top = gd.get("most_referenced", [])[:20]
            if top:
                ax.barh([x["doc_id"][-30:] for x in top][::-1], [x["refs"] for x in top][::-1],
                        color=PALETTE["green"])
                ax.set_xlabel("số lượt tham chiếu")
                ax.set_title(f"[{dom}] Top gold docs | Gini={gd['gini_gold_reference']}")
            fig.tight_layout()
            _savefig(fig, out_dir / f"dq_fig6_gold_{dom}.png", paths)
        except Exception as e:
            logger.warning(f"[{dom}] Fig6 lỗi: {e}")

    if rt and rt.get("n_queries"):
        try:
            fig, ax = plt.subplots(figsize=(9, 5))
            bp = rt["by_position"]
            groups = list(bp.keys())
            x = np.arange(len(groups))
            w = 0.35
            ax.bar(x - w / 2, [bp[g]["ndcg10_single"] for g in groups], w, label="single", color=PALETTE["blue"])
            ax.bar(x + w / 2, [bp[g]["ndcg10_history"] for g in groups], w, label="history", color=PALETTE["orange"])
            ax.set_xticks(x)
            ax.set_xticklabels(groups)
            ax.set_ylabel("nDCG@10")
            ax.set_title(f"[{dom}] BM25 nDCG@10 theo vị trí turn")
            ax.legend()
            fig.tight_layout()
            _savefig(fig, out_dir / f"dq_fig7_retrieval_{dom}.png", paths)
        except Exception as e:
            logger.warning(f"[{dom}] Fig7 lỗi: {e}")

    if lk and lk.get("turns_analyzed"):
        try:
            fig, ax = plt.subplots(figsize=(7, 4))
            hist = lk["evidence_position"]["relative_hist_pct"]
            ax.bar(list(hist.keys()), list(hist.values()), color=PALETTE["teal"])
            ax.set_ylabel("% gold")
            ax.set_title(f"[{dom}] Vị trí bằng chứng trong gold (tương đối)")
            fig.tight_layout()
            _savefig(fig, out_dir / f"dq_fig8_evidence_{dom}.png", paths)
        except Exception as e:
            logger.warning(f"[{dom}] Fig8 lỗi: {e}")
    return paths


def _safe_val(m: Dict[str, Any], *path: str, default: Any = 0) -> Any:
    v = deep_get(m, *path, default=default)
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return default
    return v


def make_cross_domain_figures(items: List[Dict[str, Any]], out_dir: Path) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []
    if not items:
        return paths
    doms = [it["domain"] for it in items]
    ms = [it["m"] for it in items]
    safe = _safe_val

    try:
        comps = ["integrity", "content", "conversation", "gold", "link"]
        fig, ax = plt.subplots(figsize=(max(9, len(doms) * 1.0), 5))
        x = np.arange(len(doms))
        w = 0.75 / (len(comps) + 1)
        ax.bar(x - 0.375 + w / 2, [safe(m, "health", "overall") for m in ms], w, label="overall",
               color=PALETTE["dark"], edgecolor="black", linewidth=0.5)
        colors = [PALETTE["blue"], PALETTE["teal"], PALETTE["orange"], PALETTE["green"], PALETTE["purple"]]
        for ci, c in enumerate(comps):
            ax.bar(x - 0.375 + w * (ci + 1.5), [safe(m, "health", "components", c) for m in ms], w,
                   label=c, color=colors[ci], alpha=0.85)
        ax.axhline(HEALTH_GREEN, color="green", ls="--", lw=0.8, alpha=0.6)
        ax.axhline(HEALTH_YELLOW, color="orange", ls="--", lw=0.8, alpha=0.6)
        ax.set_xticks(x)
        ax.set_xticklabels(doms, rotation=30, ha="right")
        ax.set_ylabel("score")
        ax.set_ylim(0, 105)
        ax.set_title("Health score — so sánh liên corpus")
        ax.legend(ncol=3, fontsize=8, loc="lower right")
        fig.tight_layout()
        _savefig(fig, out_dir / "dq_cross_health.png", paths)
    except Exception as e:
        logger.warning(f"Cross health fig lỗi: {e}")

    try:
        fig, ax = plt.subplots(2, 2, figsize=(13, 7))
        spec = [("Số tài liệu", ("content", "total_documents"), "blue"),
                ("Median độ dài (chars)", ("content", "char_length", "median"), "teal"),
                ("Trùng chính xác (%)", ("content", "exact_dup", "duplicate_pct"), "red"),
                ("Doc có lỗi nghiêm trọng (%)", ("content", "serious_flag_pct"), "orange")]
        for a, (title, path, col) in zip(ax.flat, spec):
            a.bar(doms, [safe(m, *path) for m in ms], color=PALETTE[col])
            a.set_title(title)
            a.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        _savefig(fig, out_dir / "dq_cross_content.png", paths)
    except Exception as e:
        logger.warning(f"Cross content fig lỗi: {e}")

    try:
        fnames = ["too_short", "mojibake", "html_residue", "boilerplate", "url_heavy", "symbol_heavy",
                  "repetitive", "non_english", "possibly_truncated", "starts_lower"]
        data = np.zeros((len(doms), len(fnames)))
        for i, m in enumerate(ms):
            fp = safe(m, "content", "flags_pct", default={}) or {}
            for j, f in enumerate(fnames):
                data[i, j] = fp.get(f, 0) or 0
        fig, ax = plt.subplots(figsize=(max(9, len(fnames) * 0.85), max(4, len(doms) * 0.55)))
        im = ax.imshow(data, aspect="auto", cmap="Reds")
        ax.set_xticks(range(len(fnames)))
        ax.set_xticklabels(fnames, rotation=40, ha="right")
        ax.set_yticks(range(len(doms)))
        ax.set_yticklabels(doms)
        vmax = data.max() if data.size else 1
        for i in range(len(doms)):
            for j in range(len(fnames)):
                ax.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", fontsize=8,
                        color="white" if data[i, j] > vmax * 0.5 else "black")
        ax.set_title("Cờ lỗi nội dung — heatmap (% doc)")
        fig.colorbar(im, ax=ax, label="%")
        fig.tight_layout()
        _savefig(fig, out_dir / "dq_cross_flags.png", paths)
    except Exception as e:
        logger.warning(f"Cross flags fig lỗi: {e}")

    try:
        fig, ax = plt.subplots(1, 2, figsize=(13, 5))
        x = np.arange(len(doms))
        ax[0].bar(x - 0.2, [safe(m, "conversation", "turns_per_conversation", "mean") for m in ms], 0.4,
                  label="turns/conv", color=PALETTE["blue"])
        ax[0].bar(x + 0.2, [safe(m, "conversation", "context", "dependent_pct_of_nonfirst") for m in ms], 0.4,
                  label="% phụ thuộc ngữ cảnh", color=PALETTE["orange"])
        ax[0].set_xticks(x)
        ax[0].set_xticklabels(doms, rotation=30, ha="right")
        ax[0].set_title("Hội thoại")
        ax[0].legend()
        ax[1].bar(x - 0.25, [safe(m, "gold", "gold_per_turn", "mean") for m in ms], 0.25, label="gold/turn",
                  color=PALETTE["green"])
        ax[1].bar(x, [safe(m, "gold", "orphan_gold_pairs_pct") for m in ms], 0.25, label="orphan %",
                  color=PALETTE["red"])
        ax[1].bar(x + 0.25, [safe(m, "gold", "turns_without_gold_pct") for m in ms], 0.25, label="no-gold %",
                  color=PALETTE["gray"])
        ax[1].set_xticks(x)
        ax[1].set_xticklabels(doms, rotation=30, ha="right")
        ax[1].set_title("Gold")
        ax[1].legend()
        fig.tight_layout()
        _savefig(fig, out_dir / "dq_cross_conv_gold.png", paths)
    except Exception as e:
        logger.warning(f"Cross conv/gold fig lỗi: {e}")

    try:
        fig, ax = plt.subplots(1, 2, figsize=(13, 5))
        x = np.arange(len(doms))
        ax[0].bar(x - 0.2, [safe(m, "retrieval", "overall", "ndcg10_single") for m in ms], 0.4,
                  label="nDCG@10 single", color=PALETTE["blue"])
        ax[0].bar(x + 0.2, [safe(m, "retrieval", "overall", "ndcg10_history") for m in ms], 0.4,
                  label="nDCG@10 history", color=PALETTE["orange"])
        ax[0].set_xticks(x)
        ax[0].set_xticklabels(doms, rotation=30, ha="right")
        ax[0].set_title("BM25 baseline")
        ax[0].legend()
        ax[1].bar(x - 0.25, [safe(m, "link", "best_gold_overlap_mean") for m in ms], 0.25, label="overlap mean",
                  color=PALETTE["green"])
        ax[1].bar(x, [safe(m, "link", "zero_overlap_pct") for m in ms], 0.25, label="zero overlap %",
                  color=PALETTE["red"])
        ax[1].bar(x + 0.25, [safe(m, "link", "evidence_position", "after_650c_pct") for m in ms], 0.25,
                  label="evidence>650c %", color=PALETTE["purple"])
        ax[1].set_xticks(x)
        ax[1].set_xticklabels(doms, rotation=30, ha="right")
        ax[1].set_title("Query ↔ gold")
        ax[1].legend()
        fig.tight_layout()
        _savefig(fig, out_dir / "dq_cross_retrieval_link.png", paths)
    except Exception as e:
        logger.warning(f"Cross retrieval/link fig lỗi: {e}")
    return paths


def write_cross_summary_csv(items: List[Dict[str, Any]], path: Path) -> None:
    def S(m, *p):
        return _safe_val(m, *p, default="")

    cols = [
        ("domain", lambda m: m["domain"]),
        ("health_overall", lambda m: S(m, "health", "overall")),
        ("health_status", lambda m: S(m, "health", "status")),
        ("docs_total", lambda m: S(m, "content", "total_documents")),
        ("chars_median", lambda m: S(m, "content", "char_length", "median")),
        ("exact_dup_pct", lambda m: S(m, "content", "exact_dup", "duplicate_pct")),
        ("near_dup_pct", lambda m: S(m, "content", "near_dup", "near_only_pct")),
        ("serious_flag_pct", lambda m: S(m, "content", "serious_flag_pct")),
        ("non_english_pct", lambda m: S(m, "content", "flags_pct", "non_english")),
        ("too_short_pct", lambda m: S(m, "content", "flags_pct", "too_short")),
        ("conversations", lambda m: S(m, "conversation", "total_conversations")),
        ("turns", lambda m: S(m, "conversation", "total_turns")),
        ("dep_context_pct", lambda m: S(m, "conversation", "context", "dependent_pct_of_nonfirst")),
        ("gold_per_turn_mean", lambda m: S(m, "gold", "gold_per_turn", "mean")),
        ("orphan_gold_pct", lambda m: S(m, "gold", "orphan_gold_pairs_pct")),
        ("no_gold_pct", lambda m: S(m, "gold", "turns_without_gold_pct")),
        ("gold_qrels_mismatch_turns", lambda m: S(m, "gold", "gold_qrels_mismatch_turns")),
        ("gini_gold", lambda m: S(m, "gold", "gini_gold_reference")),
        ("overlap_mean", lambda m: S(m, "link", "best_gold_overlap_mean")),
        ("zero_overlap_pct", lambda m: S(m, "link", "zero_overlap_pct")),
        ("evidence_after_650_pct", lambda m: S(m, "link", "evidence_position", "after_650c_pct")),
        ("bm25_ndcg_single", lambda m: S(m, "retrieval", "overall", "ndcg10_single")),
        ("bm25_ndcg_history", lambda m: S(m, "retrieval", "overall", "ndcg10_history")),
    ]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([c[0] for c in cols])
        for it in items:
            w.writerow([c[1](it["m"]) for c in cols])


def build_summary_md(items: List[Dict[str, Any]], cross_figs: Optional[List[Path]] = None) -> str:
    L = ["# RETECO Track 2 — Data Quality Summary\n",
         f"*Tạo lúc {datetime.now().isoformat(timespec='seconds')}*", f"*Số domain: {len(items)}*", ""]
    if cross_figs:
        L.append("## 📊 Biểu đồ so sánh liên corpus\n")
        for p in cross_figs:
            L.append(f"![{p.stem}](figures/{p.name})\n")
    L.append("## Health tổng hợp\n")
    comps = ["integrity", "content", "conversation", "gold", "link"]
    rows = []
    for item in items:
        m = item["m"]
        h = m.get("health", {})
        row = [m["domain"], f"{h.get('overall', 'n/a')} {badge(h.get('status', 'n/a'))}"]
        for c in comps:
            v = h.get("components", {}).get(c)
            row.append(f"{v if v is not None else '-'} {badge(h.get('component_status', {}).get(c, 'n/a'))}")
        rows.append(row)
    L += md_table(["Domain", "Overall"] + comps, rows)
    L.append("\n## Metrics chính theo domain\n")
    mrows = []
    for item in items:
        m = item["m"]
        s = lambda *p: _safe_val(m, *p, default="-")
        mrows.append([m["domain"], s("content", "total_documents"), s("content", "char_length", "median"),
                      s("content", "exact_dup", "duplicate_pct"),
                      s("conversation", "context", "dependent_pct_of_nonfirst"),
                      s("gold", "gold_per_turn", "mean"), s("link", "best_gold_overlap_mean"),
                      s("retrieval", "overall", "ndcg10_single"), s("retrieval", "overall", "ndcg10_history")])
    L += md_table(["Domain", "Docs", "Median(c)", "Dup%", "Deps%", "Gold/turn", "Overlap", "nDCG(s)", "nDCG(h)"], mrows)
    L.append("\n## Khuyến nghị chính theo domain\n")
    for item in items:
        m = item["m"]
        L.append(f"### {m['domain']}\n")
        for r in m.get("recommendations", [])[:8]:
            L.append(f"- **[{r['severity']}]** {r['text']}")
        L.append("")
    return "\n".join(L)


def _img_tag(p: Path) -> str:
    try:
        return f'<img src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}" alt="{p.name}">'
    except Exception:
        return f"<p><i>Không nhúng được {p.name}</i></p>"


def build_html_report(items: List[Dict[str, Any]], out_path: Path, cross_figs: Optional[List[Path]] = None):
    cls_of = lambda s: {"green": "green", "yellow": "yellow", "red": "red"}.get(s, "n-a")
    P = ["""<!DOCTYPE html><html><head><meta charset="utf-8"><title>RETECO DQ Report</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:20px;max-width:1500px}
table{border-collapse:collapse;margin:10px 0}
th,td{border:1px solid #ccc;padding:6px 10px;text-align:left;font-size:13px}
th{background:#f0f0f0}
.green{background:#c8e6c9}.yellow{background:#fff9c4}.red{background:#ffcdd2}.n-a{background:#eee}
img{max-width:100%;margin:10px 0;border:1px solid #ddd;border-radius:4px}
h2{border-bottom:2px solid #333;padding-bottom:5px;margin-top:40px}
.rec-high{color:#b71c1c}.rec-medium{color:#e65100}.rec-low{color:#1565c0}.rec-info{color:#555}
.cross-sec{background:#fafafa;padding:15px;border-radius:8px;margin:20px 0}
.toc a{margin-right:15px}
</style></head><body>"""]
    P.append("<h1>RETECO Track 2 — Data Quality Report</h1>")
    P.append(f"<p>Tạo lúc {datetime.now().isoformat(timespec='seconds')}</p>")
    P.append("<p class='toc'><b>Mục lục:</b> <a href='#cross'>📊 So sánh liên corpus</a>"
             + "".join(f"<a href='#dom-{it['domain']}'>{it['domain']}</a>" for it in items) + "</p>")

    comps = ["integrity", "content", "conversation", "gold", "link"]
    P.append("<div class='cross-sec'><h2 id='cross'>📊 So sánh liên corpus</h2><h3>Health tổng hợp</h3>"
             "<table><tr><th>Domain</th><th>Overall</th>" + "".join(f"<th>{c}</th>" for c in comps)
             + "<th>Docs</th><th>Median(c)</th><th>Dup%</th><th>Gold/turn</th><th>nDCG(s)</th><th>nDCG(h)</th></tr>")
    for item in items:
        m = item["m"]
        h = m.get("health", {})
        sv = lambda *p: _safe_val(m, *p, default="-")
        row = f"<tr><td><b>{m['domain']}</b></td><td class='{cls_of(h.get('status', 'n/a'))}'><b>{h.get('overall', 'n/a')}</b></td>"
        for c in comps:
            v = h.get("components", {}).get(c)
            row += f"<td class='{cls_of(h.get('component_status', {}).get(c, 'n/a'))}'>{v if v is not None else '-'}</td>"
        row += (f"<td>{sv('content', 'total_documents')}</td><td>{sv('content', 'char_length', 'median')}</td>"
                f"<td>{sv('content', 'exact_dup', 'duplicate_pct')}</td><td>{sv('gold', 'gold_per_turn', 'mean')}</td>"
                f"<td>{sv('retrieval', 'overall', 'ndcg10_single')}</td><td>{sv('retrieval', 'overall', 'ndcg10_history')}</td></tr>")
        P.append(row)
    P.append("</table>")
    if cross_figs:
        P.append("<h3>Biểu đồ so sánh</h3>")
        P += [_img_tag(p) for p in cross_figs]
    P.append("</div>")

    for item in items:
        m = item["m"]
        dom = m["domain"]
        h = m.get("health", {})
        P.append(f"<h2 id='dom-{dom}'>Domain: {dom}</h2>")
        P.append(f"<p><b>Health:</b> <span class='{cls_of(h.get('status', 'n/a'))}' "
                 f"style='padding:4px 10px;border-radius:4px'>{h.get('overall', 'n/a')} ({h.get('status', 'n/a')})</span></p>")
        P += [_img_tag(p) for p in item.get("figures", [])]
        P.append("<h3>Khuyến nghị</h3><ul>")
        for r in m.get("recommendations", []):
            c2 = {"high": "rec-high", "medium": "rec-medium", "low": "rec-low"}.get(r["severity"], "rec-info")
            P.append(f"<li class='{c2}'><b>[{r['severity']}]</b> {html_lib.escape(r['text'])}</li>")
        P.append("</ul>")
        if h.get("penalties"):
            P.append("<h3>Chi tiết điểm trừ</h3><table><tr><th>Nhóm</th><th>Nguyên nhân</th><th>Giá trị</th>"
                     "<th>Hệ số</th><th>Trừ</th></tr>")
            for p in h["penalties"][:20]:
                P.append(f"<tr><td>{p['component']}</td><td>{html_lib.escape(p['name'])}</td>"
                         f"<td>{p['value']}</td><td>{p['weight']}</td><td>{p['penalty']}</td></tr>")
            P.append("</table>")
        P.append(f"<p>Ví dụ lỗi chi tiết: <code>{dom}/dq_report_{dom}.md</code> (mục 11) và "
                 f"<code>{dom}/dq_inspection_{dom}.md</code></p>")
    P.append("</body></html>")
    out_path.write_text("\n".join(P), encoding="utf-8")


# ===========================================================================
# 12. Orchestrator
# ===========================================================================
def find_domains(data_dir: Optional[str]) -> Tuple[Path, List[str]]:
    candidates: List[Path] = []
    if data_dir:
        candidates.append(Path(data_dir))
    env = os.environ.get("RETECO_DATA_DIR")
    if env:
        candidates.append(Path(env))
    candidates += [PROJECT_ROOT / "reteco_data", PROJECT_ROOT.parent / "reteco_data",
                   Path("reteco_data"), Path("../reteco_data")]
    if os.name == "nt" or sys.platform.startswith("win"):
        candidates.append(Path("D:/reteco/reteco_data"))
    for base in candidates:
        if not base.is_dir():
            continue
        root = base / "track2_recor" if (base / "track2_recor").is_dir() else base
        try:
            doms = [d.name for d in root.iterdir() if d.is_dir() and (d / "documents.jsonl").is_file()]
        except Exception:
            continue
        if doms:
            return root, sorted(doms)
    logger.error(f"Không tìm thấy dữ liệu. Đã thử: {[str(c) for c in candidates]}")
    sys.exit(1)


def run_domain(root_s: str, dom: str, args: argparse.Namespace, reports_s: str) -> Dict[str, Any]:
    t_start = time.time()
    root, reports = Path(root_s), Path(reports_s)
    phases = set(args.phases)
    domain_dir = root / dom
    rng = random.Random(args.seed)
    timing: Dict[str, float] = {}

    def timed(name: str, fn: Callable[[], Any]) -> Any:
        t0 = time.time()
        try:
            out = fn()
        except Exception as exc:
            logger.exception(f"[{dom}] Pha '{name}' lỗi: {exc}")
            out = None
        timing[name] = round(time.time() - t0, 1)
        return out

    bench_path, qrels_path = domain_dir / "benchmark_dev.json", domain_dir / "qrels_dev.txt"
    qrels, qinfo = load_qrels(qrels_path)
    parsed = parse_benchmark(bench_path, qrels)
    turns, bmeta = parsed["turns"], parsed["meta"]
    if bmeta.get("schema"):
        logger.info(f"[{dom}] Schema hội thoại: {bmeta['schema']} | type={bmeta.get('schema_type')} | "
                    f"qid qrels khớp {bmeta.get('matched_qrels_qids', 0)}/{bmeta.get('qrels_qids_total', 0)}")
    gold_ids: Set[str] = set()
    for t in turns:
        gold_ids |= set(t["gold"])

    m: Dict[str, Any] = {
        "domain": dom, "generated_at": datetime.now().isoformat(timespec="seconds"),
        "phases": sorted(phases, key=lambda p: ALL_PHASES.index(p) if p in ALL_PHASES else 99),
        "args": {k: v for k, v in vars(args).items() if k != "phases"},
    }

    scan = None
    if phases & {"integrity", "content", "gold", "link", "retrieval"}:
        scan = timed("scan", lambda: scan_corpus(domain_dir, dom, gold_ids, args, reports / ".cache"))
        if scan is None:
            logger.error(f"[{dom}] Scan thất bại, bỏ qua domain")
            return {}
        st = scan["stats"]
        logger.info(f"[{dom}] Corpus {st['total_documents']:,} docs | median {st['char_length']['median']}c | "
                    f"lỗi nghiêm trọng {st['serious_flag_pct']}% | trùng {st['exact_dup']['duplicate_pct']}% | "
                    f"gần trùng {st['near_dup'].get('near_only_pct')}%")

    if turns and (phases & {"conversation", "gold", "link", "retrieval"}):
        cv = timed("conversation", lambda: analyze_conversations(turns, bmeta, args.examples))
        if cv is not None:
            m["conversation"] = cv

    if scan and "integrity" in phases:
        def _build_integrity():
            sc = scan["stats"]
            total = sc["total_documents"]
            return {
                "files": {"documents.jsonl": (domain_dir / "documents.jsonl").is_file(),
                          "benchmark_dev.json": bench_path.is_file(),
                          "qrels_dev.txt": qrels_path.is_file()},
                "documents": {
                    "total_documents": total, "schema_keys": sc["schema_keys"],
                    "bad_json_lines": sc["bad_json_lines"],
                    "bad_json_pct": pct(sc["bad_json_lines"], total + sc["bad_json_lines"]),
                    "not_dict_lines": sc["not_dict_lines"], "missing_id": sc["missing_id"],
                    "missing_id_pct": pct(sc["missing_id"], total),
                    "duplicate_doc_ids": sc["duplicate_doc_ids"],
                    "duplicate_id_pct": pct(sc["duplicate_doc_ids"], total),
                    "missing_text_field": sc["missing_text_field"],
                    "missing_text_pct": pct(sc["missing_text_field"] + sc["non_str_text"], total),
                    "non_str_text": sc["non_str_text"], "title_missing": sc["title_missing"],
                    "key_consistency_pct": sc["key_consistency_pct"]},
                "encoding": {"mojibake_pct": sc["flags_pct"]["mojibake"],
                             "control_chars_pct": sc["flags_pct"]["control_chars"],
                             "html_residue_pct": sc["flags_pct"]["html_residue"]},
                "benchmark": bmeta, "qrels": qinfo,
            }
        ig = timed("integrity", _build_integrity)
        if ig:
            m["integrity"] = ig

    if scan and "content" in phases:
        def _build_content():
            sc = scan["stats"]
            vs = vocab_stats(scan["vocab"])
            vs["n_docs"] = scan["n_vocab_docs"]
            return {k: sc[k] for k in ("total_documents", "char_length", "word_length", "length_buckets_pct",
                                       "long_outlier_threshold_chars", "long_outlier_pct", "share_le_chars_pct",
                                       "flags_count", "flags_pct", "serious_flag_pct", "exact_dup", "near_dup")} | {"vocab": vs}
        ct = timed("content", _build_content)
        if ct:
            m["content"] = ct

    if scan and turns and "gold" in phases:
        gd = timed("gold", lambda: analyze_gold(turns, bmeta, qinfo, scan, args.examples, args.fix_cap))
        if gd:
            m["gold"] = gd

    if scan and turns and "link" in phases:
        lk = timed("link", lambda: analyze_link(turns, scan["gold_docs"], scan.get("vocab", Counter()), args, rng))
        if lk:
            m["link"] = lk

    if scan and turns and "retrieval" in phases:
        rt = timed("retrieval", lambda: analyze_retrieval(turns, scan, args, rng, dom))
        if rt:
            m["retrieval"] = rt

    if turns and "splits" in phases:
        sp = timed("splits", lambda: analyze_splits(domain_dir, turns, gold_ids, args.examples))
        if sp:
            m["splits"] = sp

    m["health"] = compute_health(m)
    m["recommendations"] = make_recommendations(m)

    out_dir = reports / dom
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"dq_metrics_{dom}.json").write_text(
        json.dumps(strip_private(m), default=json_default, ensure_ascii=False, indent=2), encoding="utf-8")
    report = (build_report(dom, m) + "\n\n## 11. Ví dụ lỗi chi tiết\n\n"
              "*Mỗi loại lỗi liệt kê tối đa `--examples` ví dụ; loại không có lỗi được đánh dấu ✅.*"
              + build_error_examples(dom, scan, m, args.examples))
    (out_dir / f"dq_report_{dom}.md").write_text(report, encoding="utf-8")
    (out_dir / f"dq_health_{dom}.log").write_text(build_health_log(dom, m), encoding="utf-8")
    (out_dir / f"dq_inspection_{dom}.md").write_text(build_inspection(dom, scan, m, args.examples), encoding="utf-8")
    n_fix = write_fix_list(out_dir / f"dq_fix_list_{dom}.csv", dom, scan, m, args.fix_cap)

    logger.info(f"[{dom}] Health: {m['health']['overall']} [{m['health']['status']}] | "
                f"fix_list={n_fix} | {time.time() - t_start:.0f}s")
    m["_timing"] = timing   # (không trả _scan: quá nặng khi pickle qua ProcessPool)
    return m


def main():
    ap = argparse.ArgumentParser(description="RETECO Track 2 — Data Quality EDA")
    ap.add_argument("--domain", default="all")
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--reports-dir", default=str(DEFAULT_REPORTS_DIR))
    ap.add_argument("--phases", default=",".join(ALL_PHASES), help=f"CSV các pha: {','.join(ALL_PHASES)},viz")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--sample-size", type=int, default=10000)
    ap.add_argument("--retrieval-distractors", type=int, default=200)
    ap.add_argument("--max-docs", type=int, default=0, help="0 = không giới hạn")
    ap.add_argument("--near-dup-max", type=int, default=20000)
    ap.add_argument("--fix-cap", type=int, default=500)
    ap.add_argument("--examples", type=int, default=5, help="số ví dụ cho mỗi loại lỗi trong báo cáo")
    ap.add_argument("--max-link-turns", type=int, default=1000)
    ap.add_argument("--max-queries", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--skip-eda", action="store_true", help="Chỉ vẽ lại từ JSON có sẵn")
    args = ap.parse_args()

    phases = [p.strip() for p in args.phases.split(",") if p.strip()]
    for p in phases:
        if p not in ALL_PHASES and p != "viz":
            logger.error(f"Pha không hợp lệ: {p}")
            sys.exit(1)
    args.phases = phases

    reports = Path(args.reports_dir)
    reports.mkdir(parents=True, exist_ok=True)
    root, all_domains = find_domains(args.data_dir)
    domains = all_domains if args.domain == "all" else [args.domain]
    logger.info(f"Root: {root}")
    logger.info(f"Reports: {reports}")
    logger.info(f"Domains ({len(domains)}): {domains}")

    items: List[Dict[str, Any]] = []
    if args.skip_eda:
        for dom in domains:
            p = reports / dom / f"dq_metrics_{dom}.json"
            if not p.is_file():
                logger.warning(f"[{dom}] Không có {p}, bỏ qua")
                continue
            try:
                items.append({"domain": dom, "m": json.loads(p.read_text(encoding="utf-8")), "figures": []})
            except Exception as e:
                logger.exception(f"[{dom}] Đọc JSON lỗi: {e}")
    elif args.workers > 1 and len(domains) > 1:
        with ProcessPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(run_domain, str(root), d, args, str(reports)): d for d in domains}
            for fut in as_completed(futs):
                dom = futs[fut]
                try:
                    m = fut.result()
                    if m:
                        items.append({"domain": dom, "m": m, "figures": []})
                except Exception as e:
                    logger.exception(f"[{dom}] Lỗi: {e}")
    else:
        for dom in domains:
            m = run_domain(str(root), dom, args, str(reports))
            if m:
                items.append({"domain": dom, "m": m, "figures": []})
    items.sort(key=lambda it: it["domain"])

    cross_figs: List[Path] = []
    if items and ("viz" in phases or not args.skip_eda):
        for item in items:
            dom = item["domain"]
            try:
                item["figures"] = make_figures(item["m"], reports / dom / "figures")
            except Exception as e:
                logger.exception(f"[{dom}] Vẽ hình lỗi: {e}")
        try:
            cross_figs = make_cross_domain_figures(items, reports / "figures")
            logger.info(f"Đã vẽ {len(cross_figs)} hình cross-domain vào {reports / 'figures'}")
        except Exception as e:
            logger.exception(f"Lỗi vẽ cross-domain: {e}")
        try:
            write_cross_summary_csv(items, reports / "dq_cross_summary.csv")
        except Exception as e:
            logger.exception(f"Lỗi ghi cross CSV: {e}")
        try:
            (reports / "dq_summary_all.md").write_text(build_summary_md(items, cross_figs), encoding="utf-8")
            build_html_report(items, reports / "dq_report.html", cross_figs)
            logger.info(f"Đã ghi {reports / 'dq_summary_all.md'} và {reports / 'dq_report.html'}")
        except Exception as e:
            logger.exception(f"Lỗi ghi summary/HTML: {e}")
    logger.info(f"Hoàn tất. {len(items)} domain.")


if __name__ == "__main__":
    main()