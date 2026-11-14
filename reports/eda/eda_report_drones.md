# Báo cáo EDA & đánh giá Chunking — domain `drones`

*Tạo lúc 2026-11-14 12:22:41 | RETECO Track 2 (v3)*

## 1. Corpus

- Tổng tài liệu: **16,381** | schema: `content, doc_id`
- Ký tự: min=30, p25=240, **median=537**, mean=772.0, p75=1113, p90=1911, p95=2098, p99=2754, max=13156
- Từ: median=84, mean=122.0, max=1546
- Ước tính vượt 512 token: **3.0%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 7.68% |
| 101-300 | 23.36% |
| 301-650 | 25.67% |
| 651-800 | 7.31% |
| 801-1500 | 19.39% |
| 1501-3000 | 16.58% |
| 3001-6000 | 0.01% |
| >6000 | 0.01% |

- Cấu trúc: header 0.02% | bullet 0.77% | code 0.02% | URL 3.95% | nhiều dòng 6.72%
- Chất lượng dữ liệu: trùng 0.0% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 1.18% | thiếu dấu câu cuối 27.04% | mở đầu bằng đại từ 3.72%

## 2. Hội thoại Track 2

- Hội thoại: **11** | lượt: **38** | lượt có gold: 38
- Lượt/hội thoại: mean=3.45 (min 3, max 5)
- Độ dài query: mean=18.9 từ, median=19, max=25
- Gold docs/lượt: mean=2.82, max=7
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 2.1x | 374.6 | 51.28% | 50.97% | 0.95% | 0.95% | 0.12% | 2.38% | 0.0% | **75.99** |
| **2_Fixed_Word** | 1.61x | 503.5 | 35.85% | 35.57% | 1.12% | 1.12% | 0.0% | 0.0% | 0.0% | **83.42** |
| **3_Sentence_Boundary** | 1.48x | 535.8 | 0.0% | 0.0% | 3.15% | 3.15% | 1.96% | 0.14% | 0.03% | **98.56** |
| **4_Recursive_Markdown** | 1.7x | 431.6 | 1.89% | 1.89% | 3.65% | 3.65% | 2.8% | 0.24% | 0.0% | **97.38** |
| **5_Semantic_Context_Injected** | 1.67x | 484.8 | 1.89% | 1.89% | 3.63% | 0.0% | 2.85% | 0.24% | 0.0% | **98.18** |
| **6_Whole_Document** | 1.0x | 733.4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.65% | **98.22** |
| **7_Parent_Child** | 2.6x | 281.8 | 0.04% | 0.0% | 6.35% | 6.35% | 3.0% | 1.93% | 0.02% | **96.81** |
| **8_Sentence_Window** | 3.24x | 340.8 | 0.02% | 0.0% | 5.36% | 5.36% | 15.57% | 10.12% | 0.02% | **93.27** |
| **9_TextTiling_Semantic** | 2.11x | 349.2 | 0.05% | 0.0% | 3.77% | 3.77% | 12.65% | 14.0% | 0.02% | **93.29** |
| 1b_Fixed_Char_300 | 3.14x | 253.7 | 66.33% | 66.36% | 1.29% | 1.29% | 0.27% | 5.04% | 0.0% | **68.37** |
| 1c_Fixed_Char_900 | 1.45x | 534.8 | 29.84% | 30.05% | 0.9% | 0.9% | 0.03% | 0.0% | 0.0% | **86.22** |
| 3b_Sentence_80w | 2.38x | 371.5 | 0.02% | 0.0% | 6.52% | 6.52% | 2.59% | 0.69% | 0.02% | **97.16** |
| 3c_Sentence_220w | 1.18x | 639.2 | 0.0% | 0.0% | 1.61% | 1.61% | 1.14% | 0.04% | 0.04% | **99.09** |
| 4b_Recursive_450 | 2.3x | 318.8 | 3.09% | 3.07% | 4.9% | 4.9% | 3.18% | 0.24% | 0.0% | **96.35** |
| 4c_Recursive_1000 | 1.31x | 560.2 | 1.03% | 1.03% | 1.95% | 1.95% | 2.06% | 0.04% | 0.0% | **98.57** |
| 4d_Recursive_250 | 3.98x | 183.5 | 7.11% | 7.08% | 6.8% | 6.8% | 2.93% | 2.09% | 0.0% | **93.47** |
| 5b_Semantic_thr1200_max900 | 1.34x | 576.3 | 1.05% | 1.05% | 1.76% | 0.0% | 2.46% | 0.07% | 0.0% | **98.92** |
| 5c_Semantic_thr500_max400 | 2.42x | 369.9 | 3.6% | 3.6% | 5.23% | 0.0% | 3.02% | 0.25% | 0.0% | **97.21** |
| 5d_Semantic_prefix_all | 1.67x | 485.7 | 1.89% | 1.89% | 3.63% | 0.0% | 2.85% | 0.24% | 0.0% | **98.18** |
| 5e_Adaptive_Hybrid | 1.49x | 530.5 | 1.35% | 1.35% | 2.52% | 0.0% | 2.66% | 0.13% | 0.0% | **98.64** |
| 8b_Sentence_Window_6_3 | 2.25x | 452.7 | 0.0% | 0.0% | 4.02% | 4.02% | 15.04% | 4.88% | 0.02% | **95.08** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 48 gold + 9967 nhiễu | 38 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.1436 | 0.2080 | 0.1258 | +0.0822 🔼 | **0.2258** | 0.2209 | 0.2526 | 0.3323 | 0.2522 | 21764 |
| 2_Fixed_Word | 0.1599 | 0.2370 | 0.1505 | +0.0865 🔼 | **0.2464** | 0.2406 | 0.2123 | 0.3441 | 0.3050 | 16529 |
| 3_Sentence_Boundary | 0.1794 | 0.2486 | 0.1609 | +0.0877 🔼 | **0.2671** | 0.2660 | 0.2518 | 0.3441 | 0.3231 | 15148 |
| 4_Recursive_Markdown | 0.1547 | 0.2221 | 0.1384 | +0.0837 🔼 | **0.2384** | 0.2171 | 0.2342 | 0.3555 | 0.2688 | 17525 |
| 5_Semantic_Context_Injected | 0.1333 | 0.2059 | 0.1407 | +0.0652 🔼 | **0.1985** | 0.2340 | 0.2070 | 0.3125 | 0.2681 | 17166 |
| 6_Whole_Document | 0.1747 | 0.2514 | 0.1390 | +0.1124 🔼 | **0.2871** | 0.2656 | 0.2526 | 0.3476 | 0.3268 | 10015 |
| 7_Parent_Child | 0.1530 | 0.2147 | 0.1363 | +0.0784 🔼 | **0.2314** | 0.2305 | 0.2544 | 0.3336 | 0.2519 | 27052 |
| 8_Sentence_Window | 0.1506 | 0.2100 | 0.1252 | +0.0848 🔼 | **0.2354** | 0.2283 | 0.2561 | 0.3274 | 0.2668 | 34065 |
| 9_TextTiling_Semantic | 0.1386 | 0.2199 | 0.1313 | +0.0886 🔼 | **0.2272** | 0.2428 | 0.2289 | 0.3266 | 0.2725 | 21642 |
| 1b_Fixed_Char_300 | 0.1448 | 0.2098 | 0.1163 | +0.0935 🔼 | **0.2383** | 0.2117 | 0.2281 | 0.2924 | 0.2440 | 32642 |
| 1c_Fixed_Char_900 | 0.1743 | 0.2385 | 0.1560 | +0.0825 🔼 | **0.2568** | 0.2529 | 0.2526 | 0.3441 | 0.3015 | 14795 |
| 3b_Sentence_80w | 0.1657 | 0.2380 | 0.1491 | +0.0889 🔼 | **0.2546** | 0.2678 | 0.2684 | 0.3660 | 0.2844 | 24703 |
| 3c_Sentence_220w | 0.1569 | 0.2243 | 0.1387 | +0.0856 🔼 | **0.2425** | 0.2634 | 0.2342 | 0.3476 | 0.2596 | 12046 |
| 4b_Recursive_450 | 0.1765 | 0.2476 | 0.1544 | +0.0932 🔼 | **0.2697** | 0.2494 | 0.2289 | 0.3358 | 0.3356 | 23858 |
| 4c_Recursive_1000 | 0.1605 | 0.2240 | 0.1441 | +0.0799 🔼 | **0.2404** | 0.2516 | 0.2474 | 0.3529 | 0.2505 | 13374 |
| 4d_Recursive_250 | 0.1355 | 0.2251 | 0.1179 | +0.1072 🔼 | **0.2427** | 0.2160 | 0.2281 | 0.3217 | 0.2380 | 41595 |
| 5b_Semantic_thr1200_max900 | 0.1331 | 0.2153 | 0.1313 | +0.0840 🔼 | **0.2171** | 0.2428 | 0.2026 | 0.3345 | 0.2643 | 13763 |
| 5c_Semantic_thr500_max400 | 0.1317 | 0.2170 | 0.1195 | +0.0975 🔼 | **0.2292** | 0.2310 | 0.2289 | 0.3358 | 0.2572 | 25165 |
| 5d_Semantic_prefix_all | 0.1333 | 0.2059 | 0.1259 | +0.0800 🔼 | **0.2133** | 0.2340 | 0.2070 | 0.3125 | 0.2681 | 17166 |
| 5e_Adaptive_Hybrid | 0.1548 | 0.2273 | 0.1455 | +0.0818 🔼 | **0.2366** | 0.2450 | 0.2211 | 0.3476 | 0.2924 | 15253 |
| 8b_Sentence_Window_6_3 | 0.1501 | 0.2130 | 0.1329 | +0.0801 🔼 | **0.2302** | 0.2362 | 0.2561 | 0.3222 | 0.2720 | 23555 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 6_Whole_Document | **0.9334** | 0.9334 | 0.000 |
| 2 | 3_Sentence_Boundary | **0.7788** | 0.7788 | 0.000 |
| 3 | 3b_Sentence_80w | **0.7392** | 0.7392 | 0.000 |
| 4 | 4b_Recursive_450 | **0.6896** | 0.6896 | 0.000 |
| 5 | 4c_Recursive_1000 | **0.6628** | 0.6628 | 0.000 |
| 6 | 3c_Sentence_220w | **0.6575** | 0.6575 | 0.000 |
| 7 | 1c_Fixed_Char_900 | **0.6293** | 0.6293 | 0.000 |
| 8 | 4_Recursive_Markdown | **0.6014** | 0.6014 | 0.000 |
| 9 | 5e_Adaptive_Hybrid | **0.5763** | 0.5763 | 0.000 |
| 10 | 7_Parent_Child | **0.5336** | 0.5336 | 0.000 |
| 11 | 8_Sentence_Window | **0.5085** | 0.5085 | 0.000 |
| 12 | 8b_Sentence_Window_6_3 | **0.5038** | 0.5038 | 0.000 |
| 13 | 5c_Semantic_thr500_max400 | **0.4884** | 0.4884 | 0.000 |
| 14 | 4d_Recursive_250 | **0.4816** | 0.4816 | 0.000 |
| 15 | 2_Fixed_Word | **0.4745** | 0.4745 | 0.000 |

**Chiến lược được chọn: `6_Whole_Document`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `drones_ex_2707_google_neg_85` — 108 ký tự

```text
360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 108c ✅ — *"360° Flip RC Plane Toy Drone Remote Control Glider Jet Flying 2.4G LED Light UK£14.96 Buy It Now See Details"*

---

### `drones_ex_2913_google_neg_215` — 513 ký tự

```text
Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airports, and high-security facilities. With close to 200 systems deployed globally across more than 20 countries and 6 continents, it consistently delivers full-spectrum drone protection while ensuring operational continuity, regulatory compliance, and safety. To explore the full technical framework behind Cyber Over RF, read the white paper:Cyber Over RF: The U...
```

- **1_Fixed_Char** (2 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
  - `[1]` 63c ⚠ starts_mid_sentence, undersized — *"Over RF, read the white paper:Cyber Over RF: The Ultimate Guide"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 513c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 513c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 513c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 513c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 513c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
- **7_Parent_Child** (2 chunks)
  - `[0]` 396c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
  - `[1]` 116c ✅ — *"To explore the full technical framework behind Cyber Over RF, read the white paper:Cyber Over RF: The Ultimate Guide"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 513c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 513c ✅ — *"Field-Proven Across Sectors: The Sentrycs CoRF C-UAS solution is already deployed across military bases, border patrol units, civilian airpo..."*

---

### `Drones_ex_2782_neg_24` — 1992 ký tự

```text
M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mostly used in Micro and Nano cameras. NTSC and PAL
What are PAL and NTSC? PAL and NTSC are video standards used in different parts of the world back in the days. They differ mainly in frame rate and resolution. PAL has a resolution of 720×576 at 25fps (frames per second), while NTSC has 720×480 at 30 fps. Which One Should You Use? While choosing between PAL an...
```

- **1_Fixed_Char** (5 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 499c ⚠ starts_mid_sentence, ends_mid_sentence — *"One Should You Use? While choosing between PAL and NTSC used to be crucial for compatibility reasons, modern FPV equipment generally support..."*
  - `[2]` 498c ⚠ starts_mid_sentence, ends_mid_sentence — *"to the higher resolution, PAL offers more vertical space to place OSD elements, and making OSD text slightly sharper. Selecting the Correct ..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (4 chunks)
  - `[0]` 700c ⚠ ends_mid_sentence — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 754c ⚠ starts_mid_sentence, ends_mid_sentence — *"FPV equipment generally supports both formats, making the choice more about personal preference and specific use cases. Resolution vs. Frame..."*
  - `[2]` 689c ⚠ starts_mid_sentence, ends_mid_sentence — *"OSD displays correctly. For example, if you chose PAL in Betaflight but have a NTSC camera, you might find the bottom part of the OSD missin..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (3 chunks)
  - `[0]` 705c ✅ — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 768c ✅ — *"Frame Rate : PAL offers slightly higher resolution, giving pilots slightly clearer image, while NTSC provides a higher frame rate, which can..."*
  - `[2]` 532c ✅ — *"TVL TVL, or “TV lines,” is the term used by manufacturers to measure the resolution of analog FPV cameras. TVL is measured by connecting the..."*
- **4_Recursive_Markdown** (5 chunks)
  - `[0]` 188c ✅ — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 516c ✅ — *"What are PAL and NTSC? PAL and NTSC are video standards used in different parts of the world back in the days. They differ mainly in frame r..."*
  - `[2]` 468c ✅ — *": PAL offers slightly higher resolution, giving pilots slightly clearer image, while NTSC provides a higher frame rate, which can result in ..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (5 chunks)
  - `[0]` 188c ✅ — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 634c ✅ — *"[Document Topic: M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses.] What are PAL and NTSC?..."*
  - `[2]` 586c ✅ — *"[Document Topic: M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses.] : PAL offers slightly ..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 1992c ⚠ oversized_chars — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
- **7_Parent_Child** (7 chunks)
  - `[0]` 299c ✅ — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 170c ⚠ dangling_pronoun — *"They differ mainly in frame rate and resolution. PAL has a resolution of 720×576 at 25fps (frames per second), while NTSC has 720×480 at 30 ..."*
  - `[2]` 234c ⚠ starts_with_connector — *"While choosing between PAL and NTSC used to be crucial for compatibility reasons, modern FPV equipment generally supports both formats, maki..."*
  - *(... 4 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (12 chunks)
  - `[0]` 211c ✅ — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 172c ✅ — *"NTSC and PAL What are PAL and NTSC? PAL and NTSC are video standards used in different parts of the world back in the days. They differ main..."*
  - `[2]` 258c ✅ — *"PAL and NTSC are video standards used in different parts of the world back in the days. They differ mainly in frame rate and resolution. PAL..."*
  - *(... 9 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (4 chunks)
  - `[0]` 175c ✅ — *"M12 lenses allow more light in, resulting in marginally better image quality compared to M8 lenses. M8 lenses are highly compact and are mos..."*
  - `[1]` 518c ✅ — *"NTSC and PAL What are PAL and NTSC? PAL and NTSC are video standards used in different parts of the world back in the days. They differ main..."*
  - `[2]` 667c ✅ — *"Frame Rate : PAL offers slightly higher resolution, giving pilots slightly clearer image, while NTSC provides a higher frame rate, which can..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*

---

### `drones_ex_2209_google_neg_35` — 2964 ký tự

```text
Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to learn how to download the right app for your DJI product on your Android device and get to flying and filming in no time! Why Can’t I Download DJI Apps from the Google Play Store? From early 2021, DJI has discontinued support for their apps including DJI Fly, DJI Mimo and more on the Google Play Store. Unfortunately for Android users, this means that you are n...
```

- **1_Fixed_Char** (7 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"ately for Android users, this means that you are no longer able to download DJI apps via the Google Play Store. Whilst some older DJI apps a..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence, dangling_pronoun — *"that they can provide the latest app updates to users efficiently, without having to go through the process of Play Store updates. Where Do ..."*
  - *(... 4 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (5 chunks)
  - `[0]` 659c ⚠ ends_mid_sentence — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 704c ⚠ starts_mid_sentence, ends_mid_sentence — *"Google Play Store. Whilst some older DJI apps are still available for download via the Google Play Store, the latest version of these apps r..."*
  - `[2]` 699c ⚠ starts_mid_sentence, ends_mid_sentence — *"to download for your Android device online. Download your DJI apps by visiting the DJI Download Centre. After downloading the app you requir..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (5 chunks)
  - `[0]` 782c ✅ — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 722c ✅ — *"Why? Good question. Whilst no official word has come from DJI regarding this change, it is most likely to help DJI ensure that they can prov..."*
  - `[2]` 705c ✅ — *"Different DJI products require different apps. Check out the table below to find out exactly which app is designed to help maximise your DJI..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (6 chunks)
  - `[0]` 561c ✅ — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 603c ✅ — *"Whilst some older DJI apps are still available for download via the Google Play Store, the latest version of these apps required to operate ..."*
  - `[2]` 629c ✅ — *"Download your DJI apps by visiting the DJI Download Centre. After downloading the app you require, open the app and allow the app to access ..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (6 chunks)
  - `[0]` 561c ✅ — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 701c ✅ — *"[Document Topic: Struggling to download the right DJI app for your Android smartphone or tablet?] Whilst some older DJI apps are still avail..."*
  - `[2]` 727c ✅ — *"[Document Topic: Struggling to download the right DJI app for your Android smartphone or tablet?] Download your DJI apps by visiting the DJI..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 2964c ⚠ over_embedding_token_limit — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
- **7_Parent_Child** (11 chunks)
  - `[0]` 317c ✅ — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 243c ✅ — *"From early 2021, DJI has discontinued support for their apps including DJI Fly, DJI Mimo and more on the Google Play Store. Unfortunately fo..."*
  - `[2]` 235c ✅ — *"Whilst some older DJI apps are still available for download via the Google Play Store, the latest version of these apps required to operate ..."*
  - *(... 8 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (16 chunks)
  - `[0]` 317c ✅ — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 447c ✅ — *"Check out this guide to learn how to download the right app for your DJI product on your Android device and get to flying and filming in no ..."*
  - `[2]` 464c ✅ — *"From early 2021, DJI has discontinued support for their apps including DJI Fly, DJI Mimo and more on the Google Play Store. Unfortunately fo..."*
  - *(... 13 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (8 chunks)
  - `[0]` 561c ✅ — *"Struggling to download the right DJI app for your Android smartphone or tablet? Not to worry, we’re here to help! Check out this guide to le..."*
  - `[1]` 663c ✅ — *"Whilst some older DJI apps are still available for download via the Google Play Store, the latest version of these apps required to operate ..."*
  - `[2]` 274c ✅ — *"After downloading the app you require, open the app and allow the app to access any device functions required. You should be alerted of thes..."*
  - *(... 5 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunk_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.