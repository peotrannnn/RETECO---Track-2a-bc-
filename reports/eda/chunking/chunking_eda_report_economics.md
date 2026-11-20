# Báo cáo EDA & đánh giá Chunking — domain `economics`

*Tạo lúc 2026-11-20 23:29:06 | RETECO Track 2 (v4)*

## 1. Corpus

- Tổng tài liệu: **50,220** | schema: `content, doc_id`
- Ký tự: min=3, p25=35, **median=120**, mean=394.5, p75=346, p90=909, p95=1866, p99=3822, max=39672
- Từ: median=12, mean=51.5, max=5529
- Ước tính vượt 512 token: **2.81%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 45.85% |
| 101-300 | 26.05% |
| 301-650 | 13.9% |
| 651-800 | 2.76% |
| 801-1500 | 5.26% |
| 1501-3000 | 3.93% |
| 3001-6000 | 1.96% |
| >6000 | 0.28% |

- Cấu trúc: header 11.05% | bullet 19.43% | code 0.51% | URL 18.41% | nhiều dòng 55.04%
- Chất lượng dữ liệu: trùng 19.17% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 4.49% | thiếu dấu câu cuối 43.15% | mở đầu bằng đại từ 1.11%

## 2. Hội thoại Track 2

- Hội thoại: **22** | lượt: **92** | lượt có gold: 92
- Lượt/hội thoại: mean=4.18 (min 3, max 6)
- Độ dài query: mean=18.0 từ, median=18, max=28
- Gold docs/lượt: mean=1.73, max=6
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 1.45x | 254.1 | 28.93% | 28.93% | 0.62% | 0.62% | 0.41% | 1.17% | 0.0% | **86.42** |
| **2_Fixed_Word** | 1.2x | 311.0 | 14.73% | 15.19% | 0.38% | 0.38% | 0.0% | 0.13% | 0.0% | **92.97** |
| **3_Sentence_Boundary** | 1.15x | 309.5 | 0.0% | 0.0% | 0.44% | 0.44% | 3.92% | 0.13% | 0.0% | **99.05** |
| **4_Recursive_Markdown** | 1.31x | 264.0 | 0.08% | 0.08% | 0.53% | 0.53% | 6.84% | 0.15% | 0.0% | **98.68** |
| **5_Semantic_Context_Injected** | 1.29x | 284.1 | 0.04% | 0.04% | 0.5% | 0.04% | 6.22% | 0.12% | 0.0% | **98.92** |
| **6_Whole_Document** | 1.0x | 345.8 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.1% | **99.28** |
| **7_Parent_Child** | 1.51x | 227.9 | 0.03% | 0.0% | 1.39% | 1.39% | 14.04% | 2.01% | 0.0% | **96.86** |
| **8_Sentence_Window** | 3.24x | 175.4 | 0.03% | 0.0% | 1.62% | 1.62% | 34.21% | 13.83% | 0.0% | **90.78** |
| **9_TextTiling_Semantic** | 1.92x | 179.7 | 0.16% | 0.08% | 1.28% | 1.28% | 22.28% | 17.2% | 0.0% | **91.8** |
| 1b_Fixed_Char_300 | 1.9x | 195.8 | 44.39% | 44.55% | 0.6% | 0.6% | 0.89% | 3.68% | 0.0% | **78.72** |
| 1c_Fixed_Char_900 | 1.19x | 305.4 | 14.7% | 14.95% | 0.25% | 0.25% | 0.13% | 0.0% | 0.0% | **93.24** |
| 3b_Sentence_80w | 1.37x | 270.4 | 0.0% | 0.0% | 1.13% | 1.13% | 10.23% | 0.29% | 0.0% | **97.96** |
| 3c_Sentence_220w | 1.07x | 327.9 | 0.0% | 0.0% | 0.23% | 0.23% | 2.25% | 0.05% | 0.0% | **99.16** |
| 4b_Recursive_450 | 1.55x | 222.2 | 0.16% | 0.16% | 0.45% | 0.45% | 11.85% | 0.19% | 0.0% | **97.9** |
| 4c_Recursive_1000 | 1.16x | 298.8 | 0.04% | 0.04% | 0.26% | 0.26% | 3.2% | 0.09% | 0.0% | **99.39** |
| 4d_Recursive_250 | 2.34x | 147.3 | 0.96% | 0.94% | 1.33% | 1.33% | 21.67% | 1.52% | 0.0% | **95.42** |
| 5b_Semantic_thr1200_max900 | 1.18x | 304.4 | 0.04% | 0.04% | 0.34% | 0.0% | 3.19% | 0.0% | 0.0% | **99.45** |
| 5c_Semantic_thr500_max400 | 1.6x | 245.6 | 0.19% | 0.19% | 0.66% | 0.0% | 11.93% | 0.22% | 0.0% | **97.95** |
| 5d_Semantic_prefix_all | 1.29x | 285.9 | 0.04% | 0.04% | 0.5% | 0.04% | 6.22% | 0.12% | 0.0% | **98.92** |
| 5e_Adaptive_Hybrid | 1.23x | 295.1 | 0.04% | 0.04% | 0.37% | 0.0% | 4.48% | 0.2% | 0.0% | **99.2** |
| 8b_Sentence_Window_6_3 | 2.35x | 231.7 | 0.0% | 0.0% | 1.32% | 1.32% | 28.01% | 8.34% | 0.0% | **93.19** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 70 gold + 9991 nhiễu | 92 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.2420 | 0.3480 | 0.2090 | +0.1390 🔼 | **0.3810** | 0.4221 | 0.3587 | 0.5100 | 0.3118 | 15724 |
| 2_Fixed_Word | 0.2482 | 0.3772 | 0.2071 | +0.1701 🔼 | **0.4183** | 0.4755 | 0.3705 | 0.5607 | 0.3358 | 12659 |
| 3_Sentence_Boundary | 0.2484 | 0.3628 | 0.2033 | +0.1595 🔼 | **0.4079** | 0.4402 | 0.3678 | 0.5716 | 0.3190 | 12059 |
| 4_Recursive_Markdown | 0.2570 | 0.3570 | 0.2274 | +0.1296 🔼 | **0.3866** | 0.4043 | 0.3754 | 0.5212 | 0.3313 | 13967 |
| 5_Semantic_Context_Injected | 0.2717 | 0.3663 | 0.2562 | +0.1101 🔼 | **0.3818** | 0.4130 | 0.3808 | 0.5493 | 0.3308 | 13774 |
| 6_Whole_Document | 0.2306 | 0.3715 | 0.2072 | +0.1643 🔼 | **0.3949** | 0.4837 | 0.3351 | 0.5815 | 0.3220 | 10061 |
| 7_Parent_Child | 0.2383 | 0.3700 | 0.2427 | +0.1273 🔼 | **0.3656** | 0.4312 | 0.3279 | 0.5290 | 0.3494 | 16526 |
| 8_Sentence_Window | 0.2502 | 0.3603 | 0.2271 | +0.1332 🔼 | **0.3834** | 0.4384 | 0.3596 | 0.5154 | 0.3349 | 35802 |
| 9_TextTiling_Semantic | 0.2383 | 0.3408 | 0.2084 | +0.1324 🔼 | **0.3707** | 0.3877 | 0.3678 | 0.5480 | 0.2938 | 20650 |
| 1b_Fixed_Char_300 | 0.2271 | 0.3350 | 0.2031 | +0.1319 🔼 | **0.3590** | 0.3886 | 0.3188 | 0.4946 | 0.3020 | 21025 |
| 1c_Fixed_Char_900 | 0.2434 | 0.3672 | 0.2138 | +0.1534 🔼 | **0.3968** | 0.4574 | 0.3596 | 0.5625 | 0.3242 | 12518 |
| 3b_Sentence_80w | 0.2305 | 0.3416 | 0.1936 | +0.1480 🔼 | **0.3785** | 0.3696 | 0.3279 | 0.5127 | 0.3096 | 14944 |
| 3c_Sentence_220w | 0.2325 | 0.3500 | 0.2021 | +0.1479 🔼 | **0.3804** | 0.4592 | 0.3478 | 0.5634 | 0.2972 | 10990 |
| 4b_Recursive_450 | 0.2590 | 0.3647 | 0.2101 | +0.1546 🔼 | **0.4136** | 0.4031 | 0.3759 | 0.5072 | 0.3512 | 16898 |
| 4c_Recursive_1000 | 0.2482 | 0.3624 | 0.2202 | +0.1422 🔼 | **0.3904** | 0.4574 | 0.3717 | 0.5746 | 0.3248 | 12057 |
| 4d_Recursive_250 | 0.2456 | 0.3687 | 0.2223 | +0.1464 🔼 | **0.3920** | 0.3989 | 0.3373 | 0.5357 | 0.3472 | 26076 |
| 5b_Semantic_thr1200_max900 | 0.2562 | 0.3722 | 0.2167 | +0.1555 🔼 | **0.4117** | 0.4973 | 0.3696 | 0.5661 | 0.3343 | 12299 |
| 5c_Semantic_thr500_max400 | 0.2764 | 0.3685 | 0.2351 | +0.1334 🔼 | **0.4098** | 0.4424 | 0.3790 | 0.5565 | 0.3417 | 17533 |
| 5d_Semantic_prefix_all | 0.2739 | 0.3705 | 0.2469 | +0.1236 🔼 | **0.3975** | 0.4103 | 0.3808 | 0.5493 | 0.3366 | 13774 |
| 5e_Adaptive_Hybrid | 0.2478 | 0.3649 | 0.2247 | +0.1402 🔼 | **0.3880** | 0.4620 | 0.3478 | 0.5553 | 0.3257 | 12997 |
| 8b_Sentence_Window_6_3 | 0.2316 | 0.3641 | 0.2086 | +0.1555 🔼 | **0.3871** | 0.4230 | 0.3759 | 0.5371 | 0.3368 | 25654 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 5b_Semantic_thr1200_max900 | **0.9077** | 0.9077 | 0.000 |
| 2 | 3_Sentence_Boundary | **0.8833** | 0.8833 | 0.000 |
| 3 | 2_Fixed_Word | **0.8707** | 0.8707 | 0.000 |
| 4 | 5c_Semantic_thr500_max400 | **0.8420** | 0.8420 | 0.000 |
| 5 | 4b_Recursive_450 | **0.7941** | 0.7941 | 0.000 |
| 6 | 6_Whole_Document | **0.7758** | 0.7758 | 0.000 |
| 7 | 5d_Semantic_prefix_all | **0.7741** | 0.7741 | 0.000 |
| 8 | 4c_Recursive_1000 | **0.7636** | 0.7636 | 0.000 |
| 9 | 1c_Fixed_Char_900 | **0.6981** | 0.6981 | 0.000 |
| 10 | 5e_Adaptive_Hybrid | **0.6706** | 0.6706 | 0.000 |
| 11 | 5_Semantic_Context_Injected | **0.6550** | 0.6550 | 0.000 |
| 12 | 3c_Sentence_220w | **0.6445** | 0.6445 | 0.000 |
| 13 | 4_Recursive_Markdown | **0.6361** | 0.6361 | 0.000 |
| 14 | 4d_Recursive_250 | **0.5565** | 0.5565 | 0.000 |
| 15 | 8b_Sentence_Window_6_3 | **0.5525** | 0.5525 | 0.000 |

**Chiến lược được chọn: `5b_Semantic_thr1200_max900`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `volunteerdillema/tragedyofthecommonsimpactonsustainabilityissues_80.txt` — 12 ký tự

```text
###  Courses
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 11c ✅ — *"### Courses"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 12c ✅ — *"###  Courses"*

---

### `germany_inflation/1973theendofbrettonwoodswhenexchangerateslearnedtofloat666280_516.txt` — 112 ký tự

```text
* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 111c ✅ — *"* [ Test environment ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 112c ✅ — *"* [ Test environment  ](/en/service/banks-and-companies/cap-collateralmanagement-access-portal/test-environment)"*

---

### `tax_evasion/2350664pdfrefreqidfastlydefault3Aa3ced6ea50c1465ac18e25d786e32b4aabsegmentsorigininitiatoracceptTC1_8.txt` — 1547 ký tự

```text
that marginal-cost pricing is the more
general solution is not refuted by this
result.
D. TRANSFER PRICE WITH IMPERFECTLY
COMPETITIVE INTERMEDIATE
MARKET
We now turn to the substantially more
difficult case where the market for the in-
termediate product is not perfectly com-
petitive, so that-setting aside the de-
mand of the distribution division itself-
the external market for the intermediate
product facing the manufacturing divi-
sion has a sloped demand curve. How-
ever, we assume demand i...
```

- **1_Fixed_Char** (4 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"that marginal-cost pricing is the more general solution is not refuted by this result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERM..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"sloped demand curve. How- ever, we assume demand independence, that is, sales made by the manufacturing division in the intermediate market ..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"ernally, one would ex- pect that each additional sale to the dis- 4The demand curve is labeled D - p, repre- senting the quantity demanded i..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (3 chunks)
  - `[0]` 769c ✅ — *"that marginal-cost pricing is the more general solution is not refuted by this result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERM..."*
  - `[1]` 703c ⚠ starts_mid_sentence, ends_mid_sentence — *"sold by the distribution division, and, conversely, internal sales to the distribu- tion division do not reduce external de- mand. In genera..."*
  - `[2]` 284c ⚠ starts_mid_sentence — *"COST PER lJNIT 2/mmc G H p | DISTRIBUTION COST mdc mmc PER UNIT E qm 0 C qd D-p ; / / ~~~mdc a b FIG. 2.-BThis content downloaded from 175.1..."*
- **3_Sentence_Boundary** (2 chunks)
  - `[0]` 881c ⚠ trailing_heading_orphan — *"that marginal-cost pricing is the more general solution is not refuted by this result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERM..."*
  - `[1]` 705c ✅ — *"manufacturing division sells shoes both internally and externally, one would ex- pect that each additional sale to the dis- 4The demand curv..."*
- **4_Recursive_Markdown** (3 chunks)
  - `[0]` 592c ⚠ trailing_heading_orphan — *"that marginal-cost pricing is the more general solution is not refuted by this result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERM..."*
  - `[1]` 573c ⚠ trailing_heading_orphan — *"not reduce the demand for the final prod- uct sold by the distribution division, and, conversely, internal sales to the distribu- tion divis..."*
  - `[2]` 380c ✅ — *"175.159.177.154 on Fri, 12 Apr 2024 02:55:32 +00:00 All use subject to https:// P MANUFACTURING COST PER lJNIT 2/mmc G H p | DISTRIBUTION CO..."*
- **5_Semantic_Context_Injected** (3 chunks)
  - `[0]` 592c ⚠ trailing_heading_orphan — *"that marginal-cost pricing is the more general solution is not refuted by this result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERM..."*
  - `[1]` 630c ⚠ trailing_heading_orphan — *"[Document Topic: that marginal-cost pricing is the more] not reduce the demand for the final prod- uct sold by the distribution division, an..."*
  - `[2]` 437c ✅ — *"[Document Topic: that marginal-cost pricing is the more] 175.159.177.154 on Fri, 12 Apr 2024 02:55:32 +00:00 All use subject to https:// P M..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 1547c ⚠ oversized_chars — *"that marginal-cost pricing is the more general solution is not refuted by this result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERM..."*
- **7_Parent_Child** (5 chunks)
  - `[0]` 358c ⚠ trailing_heading_orphan — *"that marginal-cost pricing is the more general solution is not refuted by this result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERM..."*
  - `[1]` 363c ⚠ trailing_heading_orphan — *"the external market for the intermediate product facing the manufacturing divi- sion has a sloped demand curve. How- ever, we assume demand ..."*
  - `[2]` 336c ⚠ trailing_heading_orphan — *"tion division do not reduce external de- mand. In general, we would expect some demand dependence. For example, if the manufacturing divisio..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (27 chunks)
  - `[0]` 89c ✅ — *"that marginal-cost pricing is the more general solution is not refuted by this result. D."*
  - `[1]` 67c ⚠ trailing_heading_orphan, undersized — *"result. D. TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERMEDIATE"*
  - `[2]` 101c ⚠ trailing_heading_orphan — *"TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERMEDIATE MARKET We now turn to the substantially more"*
  - *(... 24 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (17 chunks)
  - `[0]` 78c ⚠ trailing_heading_orphan, undersized — *"that marginal-cost pricing is the more general solution is not refuted by this"*
  - `[1]` 10c ⚠ undersized — *"result. D."*
  - `[2]` 56c ⚠ trailing_heading_orphan, undersized — *"TRANSFER PRICE WITH IMPERFECTLY COMPETITIVE INTERMEDIATE"*
  - *(... 14 chunk nữa — xem chunk_inspection)*

---

### `interest_rate_parity/2798_262.txt` — 17782 ký tự

```text
41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage effects.  J. Int. Econ.  **1994** ,  36  , 373–389. [ [ Google Scholar ](https://scholar.google.com/scholar_lookup?title=The+real+exchange+rate+and+foreign+direct+investment+in+the+United+States.+Relative+wealth+vs.+relative+wage+effects&author=Klein,+M.W.&author=Rosengren,+E.&publication_year=1994&journal=J.+Int.+Econ.&volume=36&pages=373%E2%80%93389&doi=10...
```

- **1_Fixed_Char** (40 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
  - `[1]` 500c ⚠ ends_mid_sentence — *"+Int.+Econ.&volume=36&pages=373%E2%80%93389&doi=10.1016/0022-1996\(94\)90009-4) ] [ [ CrossRef ](https://doi.org/10.1016/0022-1996\(94\)9000..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"Japanese+investment+in+Asia,+1987%E2%80%932008&author=Takagi,+S.&author=Shi,+Z.&publication_year=2011&journal=Jpn.+World+Econ.&volume=23&pag..."*
  - *(... 37 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (15 chunks)
  - `[0]` 1545c ⚠ ends_mid_sentence, oversized_chars — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
  - `[1]` 1383c ✅ — *"(accessed on 4 January 2020). 44. Rua, A.; Composite Indicators for the Euro Area Economic Activity. Economic Bulletin and Financial Stabili..."*
  - `[2]` 1447c ⚠ starts_mid_sentence, ends_mid_sentence — *", 72 , 47–62. [ [ Google Scholar ](https://scholar.google.com/scholar_lookup?title=On+the+Construction+of+the+European+Economic+Sentiment+In..."*
  - *(... 12 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (11 chunks)
  - `[0]` 1823c ⚠ oversized_chars — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
  - `[1]` 1607c ⚠ oversized_chars — *"45. Strigel, W.H. Business Cycle Surveys: A New Quality in Economic Statistics. Analysing Modern Business Cycles. In  Essays Honoring Geoffr..."*
  - `[2]` 1552c ⚠ oversized_chars — *"Pap.  **2002** ,  133  , 1–49. Available online: [ https://www.ecb.europa.eu//pub/pdf/scpwps/ecbwp133.pdf ](https://www.ecb.europa.eu//pub/p..."*
  - *(... 8 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (39 chunks)
  - `[0]` 596c ✅ — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
  - `[1]` 560c ✅ — *"42. Takagi, S.; Shi, Z. Exchange rate movements and foreign direct investment (FDI): Japanese investment in Asia, 1987–2008.  Jpn. World Eco..."*
  - `[2]` 294c ✅ — *"43. European Commission. The Joint Harmonised EU Programme of Business and Consumer Surveys.  User Guide  . Available online: [ https://ec.e..."*
  - *(... 36 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (39 chunks)
  - `[0]` 596c ✅ — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
  - `[1]` 582c ✅ — *"[Document Topic: 41.] 42. Takagi, S.; Shi, Z. Exchange rate movements and foreign direct investment (FDI): Japanese investment in Asia, 1987..."*
  - `[2]` 316c ✅ — *"[Document Topic: 41.] 43. European Commission. The Joint Harmonised EU Programme of Business and Consumer Surveys.  User Guide  . Available ..."*
  - *(... 36 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 17782c ⚠ over_embedding_token_limit — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
- **7_Parent_Child** (26 chunks)
  - `[0]` 720c ✅ — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
  - `[1]` 799c ✅ — *"Jpn. World Econ.  **2011** ,  23  , 265–272. [ [ Google Scholar ](https://scholar.google.com/scholar_lookup?title=Exchange+rate+movements+an..."*
  - `[2]` 525c ✅ — *"Economic Bulletin and Financial Stability Report Articles and Banco de Portugal Economic Studies. Available online: [ https://www.bportugal...."*
  - *(... 23 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (131 chunks)
  - `[0]` 148c ✅ — *"41. Klein, M.W.; Rosengren, E. The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage ..."*
  - `[1]` 125c ✅ — *"The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage effects. J. Int."*
  - `[2]` 446c ✅ — *"J. Int. Econ.  **1994** ,  36  , 373–389. [ [ Google Scholar ](https://scholar.google.com/scholar_lookup?title=The+real+exchange+rate+and+fo..."*
  - *(... 128 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (69 chunks)
  - `[0]` 30c ⚠ undersized — *"41. Klein, M.W.; Rosengren, E."*
  - `[1]` 117c ✅ — *"The real exchange rate and foreign direct investment in the United States. Relative wealth vs. relative wage effects."*
  - `[2]` 1006c ✅ — *"J. Int. Econ.  **1994** ,  36  , 373–389. [ [ Google Scholar ](https://scholar.google.com/scholar_lookup?title=The+real+exchange+rate+and+fo..."*
  - *(... 66 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunking_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.