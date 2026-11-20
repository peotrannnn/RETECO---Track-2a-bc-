# Báo cáo EDA & đánh giá Chunking — domain `politics`

*Tạo lúc 2026-11-20 23:36:12 | RETECO Track 2 (v4)*

## 1. Corpus

- Tổng tài liệu: **16,712** | schema: `content, doc_id`
- Ký tự: min=24, p25=347, **median=934**, mean=1097.6, p75=1825, p90=2176, p95=2556, p99=2939, max=18601
- Từ: median=142, mean=167.7, max=1906
- Ước tính vượt 512 token: **5.52%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 6.5% |
| 101-300 | 15.05% |
| 301-650 | 18.34% |
| 651-800 | 5.49% |
| 801-1500 | 21.06% |
| 1501-3000 | 33.17% |
| 3001-6000 | 0.32% |
| >6000 | 0.08% |

- Cấu trúc: header 0.05% | bullet 1.88% | code 0.81% | URL 3.33% | nhiều dòng 14.65%
- Chất lượng dữ liệu: trùng 0.0% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 1.43% | thiếu dấu câu cuối 18.74% | mở đầu bằng đại từ 3.3%

## 2. Hội thoại Track 2

- Hội thoại: **13** | lượt: **54** | lượt có gold: 54
- Lượt/hội thoại: mean=4.15 (min 3, max 6)
- Độ dài query: mean=18.6 từ, median=19, max=24
- Gold docs/lượt: mean=2.69, max=7
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 2.88x | 412.2 | 63.26% | 63.18% | 1.63% | 1.63% | 0.71% | 1.67% | 0.0% | **70.47** |
| **2_Fixed_Word** | 2.07x | 594.5 | 48.79% | 48.28% | 1.6% | 1.6% | 0.0% | 0.0% | 0.0% | **77.44** |
| **3_Sentence_Boundary** | 1.91x | 635.0 | 0.03% | 0.0% | 4.39% | 4.39% | 5.22% | 0.18% | 0.05% | **97.51** |
| **4_Recursive_Markdown** | 2.32x | 471.6 | 1.92% | 1.99% | 4.45% | 4.45% | 6.43% | 0.09% | 0.0% | **96.53** |
| **5_Semantic_Context_Injected** | 2.28x | 545.5 | 1.96% | 1.98% | 4.26% | 0.02% | 6.55% | 0.09% | 0.0% | **97.5** |
| **6_Whole_Document** | 1.0x | 1093.6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 5.7% | **96.11** |
| **7_Parent_Child** | 3.63x | 300.7 | 0.1% | 0.04% | 6.52% | 6.52% | 7.47% | 1.32% | 0.03% | **96.16** |
| **8_Sentence_Window** | 6.46x | 269.2 | 0.03% | 0.02% | 3.42% | 3.42% | 40.54% | 35.37% | 0.03% | **83.8** |
| **9_TextTiling_Semantic** | 3.21x | 342.5 | 0.12% | 0.0% | 3.72% | 3.72% | 24.57% | 26.55% | 0.03% | **88.28** |
| 1b_Fixed_Char_300 | 4.45x | 268.6 | 74.97% | 74.96% | 1.77% | 1.77% | 0.89% | 3.26% | 0.0% | **64.69** |
| 1c_Fixed_Char_900 | 1.86x | 630.2 | 44.39% | 44.33% | 1.02% | 1.02% | 0.7% | 0.0% | 0.0% | **79.56** |
| 3b_Sentence_80w | 3.37x | 402.6 | 0.06% | 0.0% | 6.78% | 6.78% | 6.12% | 0.73% | 0.03% | **96.46** |
| 3c_Sentence_220w | 1.39x | 825.3 | 0.0% | 0.0% | 2.59% | 2.59% | 3.74% | 0.14% | 0.07% | **98.21** |
| 4b_Recursive_450 | 3.29x | 331.9 | 3.38% | 3.33% | 5.6% | 5.6% | 7.31% | 0.24% | 0.0% | **95.31** |
| 4c_Recursive_1000 | 1.63x | 671.2 | 0.98% | 0.98% | 2.92% | 2.92% | 4.61% | 0.03% | 0.0% | **97.82** |
| 4d_Recursive_250 | 5.75x | 189.2 | 9.26% | 9.26% | 7.02% | 7.02% | 7.45% | 2.81% | 0.0% | **91.5** |
| 5b_Semantic_thr1200_max900 | 1.74x | 678.5 | 1.35% | 1.32% | 2.68% | 0.0% | 6.28% | 0.03% | 0.0% | **98.05** |
| 5c_Semantic_thr500_max400 | 3.54x | 391.9 | 3.63% | 3.59% | 5.89% | 0.0% | 7.03% | 0.28% | 0.0% | **96.44** |
| 5d_Semantic_prefix_all | 2.28x | 548.2 | 1.96% | 1.98% | 4.26% | 0.02% | 6.55% | 0.09% | 0.0% | **97.5** |
| 5e_Adaptive_Hybrid | 2.0x | 604.5 | 1.52% | 1.52% | 3.57% | 0.0% | 6.05% | 0.1% | 0.0% | **97.86** |
| 8b_Sentence_Window_6_3 | 4.34x | 373.6 | 0.0% | 0.01% | 2.73% | 2.73% | 39.43% | 22.98% | 0.07% | **87.23** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 63 gold + 9964 nhiễu | 54 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.1515 | 0.2976 | 0.1432 | +0.1544 🔼 | **0.3059** | 0.2965 | 0.2337 | 0.4184 | 0.3466 | 28906 |
| 2_Fixed_Word | 0.1845 | 0.2825 | 0.1672 | +0.1153 🔼 | **0.2998** | 0.2868 | 0.2683 | 0.4340 | 0.2790 | 20678 |
| 3_Sentence_Boundary | 0.1892 | 0.2955 | 0.1677 | +0.1278 🔼 | **0.3170** | 0.3238 | 0.2841 | 0.4186 | 0.3231 | 19296 |
| 4_Recursive_Markdown | 0.1861 | 0.2721 | 0.1680 | +0.1041 🔼 | **0.2902** | 0.2565 | 0.2769 | 0.3811 | 0.3098 | 23301 |
| 5_Semantic_Context_Injected | 0.1999 | 0.3003 | 0.1674 | +0.1329 🔼 | **0.3328** | 0.3081 | 0.3090 | 0.4275 | 0.3230 | 22961 |
| 6_Whole_Document | 0.2197 | 0.3179 | 0.1920 | +0.1259 🔼 | **0.3456** | 0.3311 | 0.3304 | 0.4461 | 0.3246 | 10027 |
| 7_Parent_Child | 0.1558 | 0.2346 | 0.1292 | +0.1054 🔼 | **0.2612** | 0.2590 | 0.2312 | 0.3578 | 0.2300 | 36348 |
| 8_Sentence_Window | 0.1509 | 0.2675 | 0.1314 | +0.1361 🔼 | **0.2870** | 0.2837 | 0.2345 | 0.4136 | 0.2712 | 62993 |
| 9_TextTiling_Semantic | 0.1730 | 0.2599 | 0.1526 | +0.1073 🔼 | **0.2803** | 0.2775 | 0.2925 | 0.3883 | 0.2762 | 31647 |
| 1b_Fixed_Char_300 | 0.1746 | 0.2901 | 0.1407 | +0.1494 🔼 | **0.3240** | 0.3238 | 0.2811 | 0.4334 | 0.3002 | 44746 |
| 1c_Fixed_Char_900 | 0.1817 | 0.3077 | 0.1495 | +0.1582 🔼 | **0.3399** | 0.3400 | 0.2687 | 0.4249 | 0.3308 | 18687 |
| 3b_Sentence_80w | 0.1627 | 0.2632 | 0.1509 | +0.1123 🔼 | **0.2750** | 0.2852 | 0.2275 | 0.4071 | 0.2794 | 33988 |
| 3c_Sentence_220w | 0.2027 | 0.3236 | 0.1727 | +0.1509 🔼 | **0.3536** | 0.3646 | 0.3099 | 0.4692 | 0.3359 | 13892 |
| 4b_Recursive_450 | 0.1612 | 0.2486 | 0.1371 | +0.1115 🔼 | **0.2727** | 0.2420 | 0.2524 | 0.3661 | 0.2593 | 32944 |
| 4c_Recursive_1000 | 0.1927 | 0.2925 | 0.1730 | +0.1195 🔼 | **0.3122** | 0.3183 | 0.2786 | 0.4332 | 0.2946 | 16387 |
| 4d_Recursive_250 | 0.1555 | 0.2412 | 0.1459 | +0.0953 🔼 | **0.2508** | 0.2418 | 0.2281 | 0.3254 | 0.2729 | 58011 |
| 5b_Semantic_thr1200_max900 | 0.1812 | 0.2928 | 0.1461 | +0.1467 🔼 | **0.3279** | 0.3183 | 0.2753 | 0.4203 | 0.3094 | 17538 |
| 5c_Semantic_thr500_max400 | 0.1752 | 0.2769 | 0.1654 | +0.1115 🔼 | **0.2867** | 0.2712 | 0.2383 | 0.3933 | 0.2806 | 35475 |
| 5d_Semantic_prefix_all | 0.1999 | 0.3003 | 0.1768 | +0.1235 🔼 | **0.3234** | 0.3081 | 0.3090 | 0.4275 | 0.3230 | 22961 |
| 5e_Adaptive_Hybrid | 0.1823 | 0.3016 | 0.1477 | +0.1539 🔼 | **0.3362** | 0.3425 | 0.2720 | 0.4194 | 0.3426 | 20104 |
| 8b_Sentence_Window_6_3 | 0.1721 | 0.3189 | 0.1594 | +0.1595 🔼 | **0.3316** | 0.3189 | 0.2528 | 0.4610 | 0.3315 | 42324 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 3c_Sentence_220w | **0.9619** | 0.9619 | 0.000 |
| 2 | 6_Whole_Document | **0.9336** | 0.9468 | 0.014 |
| 3 | 5_Semantic_Context_Injected | **0.7963** | 0.7963 | 0.000 |
| 4 | 5e_Adaptive_Hybrid | **0.7806** | 0.7806 | 0.000 |
| 5 | 5b_Semantic_thr1200_max900 | **0.7575** | 0.7575 | 0.000 |
| 6 | 5d_Semantic_prefix_all | **0.7552** | 0.7552 | 0.000 |
| 7 | 3_Sentence_Boundary | **0.7065** | 0.7065 | 0.000 |
| 8 | 4c_Recursive_1000 | **0.7058** | 0.7058 | 0.000 |
| 9 | 8b_Sentence_Window_6_3 | **0.6725** | 0.6725 | 0.000 |
| 10 | 1c_Fixed_Char_900 | **0.6663** | 0.6663 | 0.000 |
| 11 | 4_Recursive_Markdown | **0.5324** | 0.5324 | 0.000 |
| 12 | 5c_Semantic_thr500_max400 | **0.4775** | 0.4775 | 0.000 |
| 13 | 2_Fixed_Word | **0.4767** | 0.4767 | 0.000 |
| 14 | 1b_Fixed_Char_300 | **0.4712** | 0.4712 | 0.000 |
| 15 | 9_TextTiling_Semantic | **0.4352** | 0.4352 | 0.000 |

**Chiến lược được chọn: `3c_Sentence_220w`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `politics_ex_89978_google_neg_512` — 149 ký tự

```text
Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement services.
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 149c ✅ — *"Impact: These rates affect the age structure of the population, influencing demand in sectors such as education, healthcare, and retirement ..."*

---

### `politics_ex_93264_google_neg_194` — 908 ký tự

```text
“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers, and much of the Israeli public. The U.S. government is not going to seriously consider conditioning aid to Israel in the middle of this debacle. Instead of isolating and alienating Netanyahu, which seemed to be the trend, Washington must now engage and deepen cooperation with him. With more world leaders publicly backing him against Iran, Netanyahu may be ...
```

- **1_Fixed_Char** (2 chunks)
  - `[0]` 499c ⚠ ends_mid_sentence — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 458c ⚠ starts_mid_sentence — *"blicly backing him against Iran, Netanyahu may be able to draw out the Gaza operation—continuing to dangle the threat of a Rafah invasion an..."*
- **2_Fixed_Word** (2 chunks)
  - `[0]` 712c ⚠ ends_mid_sentence — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 308c ⚠ starts_mid_sentence — *"the appearance of negotiations for a cease-fire, when it has become evident to many that he is not interested in one. Meanwhile, he can stal..."*
- **3_Sentence_Boundary** (2 chunks)
  - `[0]` 717c ✅ — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 484c ✅ — *"With more world leaders publicly backing him against Iran, Netanyahu may be able to draw out the Gaza operation—continuing to dangle the thr..."*
- **4_Recursive_Markdown** (2 chunks)
  - `[0]` 423c ✅ — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 484c ✅ — *"With more world leaders publicly backing him against Iran, Netanyahu may be able to draw out the Gaza operation—continuing to dangle the thr..."*
- **5_Semantic_Context_Injected** (2 chunks)
  - `[0]` 423c ✅ — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 619c ✅ — *"[Document Topic: “Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his…] With ..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 908c ✅ — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
- **7_Parent_Child** (4 chunks)
  - `[0]` 286c ✅ — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 136c ✅ — *"Instead of isolating and alienating Netanyahu, which seemed to be the trend, Washington must now engage and deepen cooperation with him."*
  - `[2]` 293c ✅ — *"With more world leaders publicly backing him against Iran, Netanyahu may be able to draw out the Gaza operation—continuing to dangle the thr..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (2 chunks)
  - `[0]` 717c ✅ — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 621c ✅ — *"Instead of isolating and alienating Netanyahu, which seemed to be the trend, Washington must now engage and deepen cooperation with him. Wit..."*
- **9_TextTiling_Semantic** (2 chunks)
  - `[0]` 423c ✅ — *"“Direct conflict between Israel and Iran could bolster Netanyahu at a time when he has lost the trust of Biden, his fellow cabinet ministers..."*
  - `[1]` 621c ✅ — *"Instead of isolating and alienating Netanyahu, which seemed to be the trend, Washington must now engage and deepen cooperation with him. Wit..."*

---

### `politics_ex_91695_google_neg_22` — 2579 ký tự

```text
Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. §§ 12101 et seq. Implementing Regulations: 29 CFR Parts 1630, 1602 (Title I, EEOC) 28 CFR Part 35 (Title II, Department of Justice) 49 CFR Parts 27, 37, 38 (Title II, III, Department of Transportation) 28 CFR Part 36 (Title III, Department of Justice) 47 CFR §§ 64.601 et seq. (Title IV, FCC) Architectural Barriers Act of 1968 42 U.S.C. §§ 4151 et seq. Implem...
```

- **1_Fixed_Char** (6 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"riers Act of 1968 42 U.S.C. §§ 4151 et seq. Implementing Regulation: 41 CFR Subpart 101-19.6 Civil Rights of Institutionalized Persons Act 4..."*
  - `[2]` 498c ⚠ starts_mid_sentence, ends_mid_sentence — *"seq. Section 501 of the Rehabilitation Act of 1973, as amended 29 U.S.C. § 791 Implementing Regulation: 29 CFR § 1614.203 Section 503 of the..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (4 chunks)
  - `[0]` 701c ⚠ ends_mid_sentence — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 709c ⚠ starts_mid_sentence, ends_mid_sentence — *"42 U.S.C. §§ 1997 et seq. Fair Housing Amendments Act of 1988 42 U.S.C. §§ 3601 et seq. Implementing Regulation: 24 CFR Parts 100 et seq. In..."*
  - `[2]` 756c ⚠ starts_mid_sentence, ends_mid_sentence — *"Act of 1973, as amended 29 U.S.C. § 794 Over 20 Implementing Regulations for federally assisted programs, including: 34 CFR Part 104 (Depart..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (5 chunks)
  - `[0]` 796c ✅ — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 690c ✅ — *"Individuals with Disabilities Education Act 20 U.S.C. §§ 1400 et seq. Implementing Regulation: 34 CFR Part 300 National Voter Registration A..."*
  - `[2]` 511c ✅ — *"Section 501 of the Rehabilitation Act of 1973, as amended 29 U.S.C. § 791 Implementing Regulation: 29 CFR § 1614.203 Section 503 of the Reha..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (5 chunks)
  - `[0]` 614c ✅ — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 290c ✅ — *"Fair Housing Amendments Act of 1988 42 U.S.C. §§ 3601 et seq. Implementing Regulation: 24 CFR Parts 100 et seq. Individuals with Disabilitie..."*
  - `[2]` 511c ✅ — *"Section 501 of the Rehabilitation Act of 1973, as amended 29 U.S.C. § 791 Implementing Regulation: 29 CFR § 1614.203 Section 503 of the Reha..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (5 chunks)
  - `[0]` 614c ✅ — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 427c ✅ — *"[Document Topic: Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities…] Fai..."*
  - `[2]` 648c ✅ — *"[Document Topic: Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities…] Sec..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 2579c ⚠ over_embedding_token_limit — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
- **7_Parent_Child** (9 chunks)
  - `[0]` 156c ✅ — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 336c ✅ — *"Implementing Regulations: 29 CFR Parts 1630, 1602 (Title I, EEOC) 28 CFR Part 35 (Title II, Department of Justice) 49 CFR Parts 27, 37, 38 (..."*
  - `[2]` 302c ✅ — *"Implementing Regulation: 41 CFR Subpart 101-19.6 Civil Rights of Institutionalized Persons Act 42 U.S.C. §§ 1997 et seq. Fair Housing Amendm..."*
  - *(... 6 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (7 chunks)
  - `[0]` 614c ✅ — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 309c ✅ — *"(Title IV, FCC) Architectural Barriers Act of 1968 42 U.S.C. §§ 4151 et seq. Implementing Regulation: 41 CFR Subpart 101-19.6 Civil Rights o..."*
  - `[2]` 290c ✅ — *"Fair Housing Amendments Act of 1988 42 U.S.C. §§ 3601 et seq. Implementing Regulation: 24 CFR Parts 100 et seq. Individuals with Disabilitie..."*
  - *(... 4 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (5 chunks)
  - `[0]` 676c ✅ — *"Air Carrier Access Act of 1986 49 U.S.C. § 41705 Implementing Regulation: 14 CFR Part 382 Americans with Disabilities Act of 1990 42 U.S.C. ..."*
  - `[1]` 228c ✅ — *"Implementing Regulation: 24 CFR Parts 100 et seq. Individuals with Disabilities Education Act 20 U.S.C. §§ 1400 et seq. Implementing Regulat..."*
  - `[2]` 511c ✅ — *"Section 501 of the Rehabilitation Act of 1973, as amended 29 U.S.C. § 791 Implementing Regulation: 29 CFR § 1614.203 Section 503 of the Reha..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*

---

### `politics_ex_93254_neg_104` — 11177 ký tự

```text
Gaza Strip at Google Maps
v
t
e
Palestine
articles
History
Early history
Canaanites
Philistines
Roman Empire
Islamic Rule
Crusaders
Ayyubid dynasty
Mamluk Dynasty
Ottoman Empire
Modern history
History of the Palestinians
Slavery in Palestine
Palestinian nationalism
British Mandate
Nakba
Naksa
Palestinian Declaration of Independence
Years in Palestine
Conflict
Israeli–Palestinian
Timeline
1948 Palestine war
1948 Palestinian expulsion and flight
Palestinian insurgency in South Lebanon
First Lebano...
```

- **1_Fixed_Char** (25 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"Gaza Strip at Google Maps v t e Palestine articles History Early history Canaanites Philistines Roman Empire Islamic Rule Crusaders Ayyubid ..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"lestinian insurgency in South Lebanon First Lebanon War First Intifada Second Intifada Gaza War (2008–2009) Gaza war (2023–) Black September..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"s Politics State of Palestine ( International recognition ) Political parties DFLP Fatah Hamas FIDA Palestinian National Initiative PPP PFLP..."*
  - *(... 22 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (16 chunks)
  - `[0]` 901c ⚠ ends_mid_sentence — *"Gaza Strip at Google Maps v t e Palestine articles History Early history Canaanites Philistines Roman Empire Islamic Rule Crusaders Ayyubid ..."*
  - `[1]` 922c ⚠ starts_mid_sentence, ends_mid_sentence — *"Gaza Strip West Bank Enclaves Northern West Bank Southern West Bank Borders Cities Governorates Landforms Depopulated villages World Heritag..."*
  - `[2]` 962c ⚠ starts_mid_sentence, ends_mid_sentence — *"Forces Palestinian Preventive Security United States security assistance to the Palestinian National Authority Foreign affairs Palestine and..."*
  - *(... 13 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (12 chunks)
  - `[0]` 1040c ⚠ trailing_heading_orphan — *"Gaza Strip at Google Maps v t e Palestine articles History Early history Canaanites Philistines Roman Empire Islamic Rule Crusaders Ayyubid ..."*
  - `[1]` 1125c ⚠ trailing_heading_orphan — *"PFLP Third Way PPSF Palestinian right of return Palestinian political violence Elections Legal status of Palestine Anti-Palestinianism Gover..."*
  - `[2]` 1072c ⚠ trailing_heading_orphan — *"watermelon Cinema Costume and embroidery keffiyeh thobe tatreez Cuisine ( wine ) Dance Demographics Education ( universities and colleges ) ..."*
  - *(... 9 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (18 chunks)
  - `[0]` 616c ⚠ trailing_heading_orphan — *"Gaza Strip at Google Maps v t e Palestine articles History Early history Canaanites Philistines Roman Empire Islamic Rule Crusaders Ayyubid ..."*
  - `[1]` 616c ⚠ trailing_heading_orphan — *"Fatah–Hamas conflict Battle of Gaza 2009 Hamas political violence in Gaza Hamas–Salafist conflict Hamas-Jund Ansar Allah clash Geography Gaz..."*
  - `[2]` 635c ⚠ trailing_heading_orphan — *"Palestinian National Council Palestinian Legislative Council Judicial system Gaza Strip Gaza Strip under Resolution 2803 Gaza Strip under Ha..."*
  - *(... 15 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (18 chunks)
  - `[0]` 616c ⚠ trailing_heading_orphan — *"Gaza Strip at Google Maps v t e Palestine articles History Early history Canaanites Philistines Roman Empire Islamic Rule Crusaders Ayyubid ..."*
  - `[1]` 660c ⚠ trailing_heading_orphan — *"[Document Topic: Gaza Strip at Google Maps] Fatah–Hamas conflict Battle of Gaza 2009 Hamas political violence in Gaza Hamas–Salafist conflic..."*
  - `[2]` 679c ⚠ trailing_heading_orphan — *"[Document Topic: Gaza Strip at Google Maps] Palestinian National Council Palestinian Legislative Council Judicial system Gaza Strip Gaza Str..."*
  - *(... 15 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 11177c ⚠ over_embedding_token_limit — *"Gaza Strip at Google Maps v t e Palestine articles History Early history Canaanites Philistines Roman Empire Islamic Rule Crusaders Ayyubid ..."*
- **7_Parent_Child** (27 chunks)
  - `[0]` 447c ⚠ trailing_heading_orphan — *"Gaza Strip at Google Maps v t e Palestine articles History Early history Canaanites Philistines Roman Empire Islamic Rule Crusaders Ayyubid ..."*
  - `[1]` 432c ⚠ trailing_heading_orphan — *"Palestinian insurgency in South Lebanon First Lebanon War First Intifada Second Intifada Gaza War (2008–2009) Gaza war (2023–) Black Septemb..."*
  - `[2]` 473c ⚠ trailing_heading_orphan — *"World Heritage Sites Politics State of Palestine ( International recognition ) Political parties DFLP Fatah Hamas FIDA Palestinian National ..."*
  - *(... 24 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (401 chunks)
  - `[0]` 31c ⚠ trailing_heading_orphan, undersized — *"Gaza Strip at Google Maps v t e"*
  - `[1]` 22c ⚠ trailing_heading_orphan, undersized — *"t e Palestine articles"*
  - `[2]` 40c ⚠ trailing_heading_orphan, undersized — *"Palestine articles History Early history"*
  - *(... 398 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (274 chunks)
  - `[0]` 27c ⚠ trailing_heading_orphan, undersized — *"Gaza Strip at Google Maps v"*
  - `[1]` 3c ⚠ trailing_heading_orphan, undersized — *"t e"*
  - `[2]` 18c ⚠ trailing_heading_orphan, undersized — *"Palestine articles"*
  - *(... 271 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunking_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.