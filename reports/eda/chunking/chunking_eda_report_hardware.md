# Báo cáo EDA & đánh giá Chunking — domain `hardware`

*Tạo lúc 2026-11-20 23:30:42 | RETECO Track 2 (v4)*

## 1. Corpus

- Tổng tài liệu: **26,308** | schema: `content, doc_id`
- Ký tự: min=30, p25=196, **median=469**, mean=711.3, p75=1021, p90=1842, p95=2052, p99=2761, max=8385
- Từ: median=74, mean=115.2, max=1524
- Ước tính vượt 512 token: **3.25%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 9.83% |
| 101-300 | 26.5% |
| 301-650 | 24.82% |
| 651-800 | 6.56% |
| 801-1500 | 17.31% |
| 1501-3000 | 14.93% |
| 3001-6000 | 0.03% |
| >6000 | 0.01% |

- Cấu trúc: header 0.05% | bullet 0.78% | code 0.08% | URL 2.48% | nhiều dòng 5.47%
- Chất lượng dữ liệu: trùng 0.0% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 1.69% | thiếu dấu câu cuối 29.36% | mở đầu bằng đại từ 3.0%

## 2. Hội thoại Track 2

- Hội thoại: **14** | lượt: **58** | lượt có gold: 58
- Lượt/hội thoại: mean=4.14 (min 3, max 9)
- Độ dài query: mean=19.6 từ, median=20, max=25
- Gold docs/lượt: mean=1.97, max=4
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 2.03x | 370.8 | 49.69% | 49.49% | 0.71% | 0.71% | 0.07% | 1.95% | 0.0% | **76.9** |
| **2_Fixed_Word** | 1.59x | 485.3 | 34.65% | 35.12% | 1.22% | 1.22% | 0.0% | 0.0% | 0.0% | **83.82** |
| **3_Sentence_Boundary** | 1.49x | 509.7 | 0.0% | 0.0% | 3.16% | 3.16% | 1.85% | 0.34% | 0.0% | **98.49** |
| **4_Recursive_Markdown** | 1.66x | 422.0 | 1.11% | 1.14% | 3.25% | 3.25% | 2.95% | 0.06% | 0.0% | **97.89** |
| **5_Semantic_Context_Injected** | 1.63x | 474.9 | 1.14% | 1.14% | 3.16% | 0.0% | 2.95% | 0.03% | 0.0% | **98.62** |
| **6_Whole_Document** | 1.0x | 701.4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.8% | **98.31** |
| **7_Parent_Child** | 2.57x | 272.4 | 0.08% | 0.06% | 5.7% | 5.7% | 3.0% | 1.73% | 0.0% | **97.02** |
| **8_Sentence_Window** | 3.12x | 338.1 | 0.03% | 0.0% | 4.81% | 4.81% | 16.3% | 11.66% | 0.02% | **92.89** |
| **9_TextTiling_Semantic** | 2.03x | 346.3 | 0.0% | 0.0% | 3.28% | 3.28% | 11.25% | 11.82% | 0.0% | **94.15** |
| 1b_Fixed_Char_300 | 3.01x | 253.2 | 65.11% | 65.0% | 1.25% | 1.25% | 0.22% | 4.24% | 0.0% | **69.17** |
| 1c_Fixed_Char_900 | 1.41x | 522.3 | 28.68% | 28.64% | 0.39% | 0.39% | 0.04% | 0.0% | 0.0% | **86.94** |
| 3b_Sentence_80w | 2.37x | 357.2 | 0.02% | 0.04% | 5.9% | 5.9% | 2.44% | 0.76% | 0.0% | **97.31** |
| 3c_Sentence_220w | 1.19x | 609.7 | 0.0% | 0.0% | 1.09% | 1.09% | 0.46% | 0.25% | 0.0% | **99.35** |
| 4b_Recursive_450 | 2.21x | 316.2 | 2.48% | 2.51% | 4.38% | 4.38% | 3.18% | 0.11% | 0.0% | **96.8** |
| 4c_Recursive_1000 | 1.29x | 542.6 | 0.54% | 0.54% | 1.74% | 1.74% | 2.28% | 0.08% | 0.0% | **98.74** |
| 4d_Recursive_250 | 3.8x | 183.8 | 6.76% | 6.75% | 6.66% | 6.66% | 2.89% | 2.53% | 0.0% | **93.51** |
| 5b_Semantic_thr1200_max900 | 1.32x | 559.0 | 0.57% | 0.57% | 1.82% | 0.0% | 2.77% | 0.0% | 0.0% | **99.07** |
| 5c_Semantic_thr500_max400 | 2.33x | 366.0 | 2.89% | 2.92% | 4.63% | 0.0% | 3.3% | 0.21% | 0.0% | **97.48** |
| 5d_Semantic_prefix_all | 1.63x | 475.6 | 1.14% | 1.14% | 3.16% | 0.0% | 2.95% | 0.03% | 0.0% | **98.62** |
| 5e_Adaptive_Hybrid | 1.47x | 514.8 | 0.92% | 0.92% | 2.56% | 0.0% | 2.8% | 0.0% | 0.0% | **98.8** |
| 8b_Sentence_Window_6_3 | 2.2x | 447.5 | 0.0% | 0.0% | 3.78% | 3.78% | 15.18% | 5.24% | 0.05% | **94.99** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 52 gold + 9975 nhiễu | 58 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.2009 | 0.2595 | 0.1862 | +0.0733 🔼 | **0.2742** | 0.2644 | 0.3075 | 0.3966 | 0.2396 | 20550 |
| 2_Fixed_Word | 0.2146 | 0.2774 | 0.1962 | +0.0812 🔼 | **0.2958** | 0.2902 | 0.3190 | 0.4181 | 0.2791 | 16111 |
| 3_Sentence_Boundary | 0.2159 | 0.2764 | 0.2020 | +0.0744 🔼 | **0.2903** | 0.2874 | 0.3190 | 0.4095 | 0.2785 | 14972 |
| 4_Recursive_Markdown | 0.2120 | 0.2823 | 0.1931 | +0.0892 🔼 | **0.3012** | 0.3103 | 0.2989 | 0.3980 | 0.3009 | 16795 |
| 5_Semantic_Context_Injected | 0.2242 | 0.2670 | 0.2084 | +0.0586 🔼 | **0.2828** | 0.2787 | 0.3132 | 0.3908 | 0.2766 | 16448 |
| 6_Whole_Document | 0.2621 | 0.3303 | 0.2582 | +0.0721 🔼 | **0.3342** | 0.3764 | 0.3376 | 0.4368 | 0.3722 | 10027 |
| 7_Parent_Child | 0.2089 | 0.2658 | 0.1985 | +0.0673 🔼 | **0.2762** | 0.2529 | 0.2644 | 0.3405 | 0.3007 | 26143 |
| 8_Sentence_Window | 0.2003 | 0.2625 | 0.1743 | +0.0882 🔼 | **0.2885** | 0.2601 | 0.3103 | 0.3606 | 0.2878 | 33972 |
| 9_TextTiling_Semantic | 0.1994 | 0.2681 | 0.1878 | +0.0803 🔼 | **0.2797** | 0.2500 | 0.2859 | 0.3707 | 0.2908 | 21641 |
| 1b_Fixed_Char_300 | 0.1788 | 0.2475 | 0.1626 | +0.0849 🔼 | **0.2637** | 0.2284 | 0.2601 | 0.3491 | 0.2713 | 30555 |
| 1c_Fixed_Char_900 | 0.2400 | 0.2984 | 0.2228 | +0.0756 🔼 | **0.3156** | 0.2874 | 0.3319 | 0.4095 | 0.3244 | 14265 |
| 3b_Sentence_80w | 0.1900 | 0.2692 | 0.1725 | +0.0967 🔼 | **0.2867** | 0.3103 | 0.2874 | 0.3693 | 0.2898 | 24057 |
| 3c_Sentence_220w | 0.2389 | 0.3110 | 0.2183 | +0.0927 🔼 | **0.3316** | 0.3578 | 0.3376 | 0.4353 | 0.3301 | 11963 |
| 4b_Recursive_450 | 0.2357 | 0.2379 | 0.2053 | +0.0326 🔼 | **0.2683** | 0.2629 | 0.3190 | 0.3276 | 0.2585 | 22477 |
| 4c_Recursive_1000 | 0.2269 | 0.2965 | 0.2092 | +0.0873 🔼 | **0.3142** | 0.3391 | 0.3362 | 0.4239 | 0.3153 | 13044 |
| 4d_Recursive_250 | 0.2179 | 0.2118 | 0.2049 | +0.0069 | **0.2248** | 0.2040 | 0.2802 | 0.3103 | 0.2365 | 38628 |
| 5b_Semantic_thr1200_max900 | 0.2487 | 0.2959 | 0.2246 | +0.0713 🔼 | **0.3200** | 0.2874 | 0.3491 | 0.3865 | 0.3437 | 13368 |
| 5c_Semantic_thr500_max400 | 0.2403 | 0.2667 | 0.2207 | +0.0460 🔼 | **0.2863** | 0.3161 | 0.3305 | 0.3693 | 0.2982 | 23624 |
| 5d_Semantic_prefix_all | 0.2244 | 0.2674 | 0.2038 | +0.0636 🔼 | **0.2880** | 0.2960 | 0.3132 | 0.3908 | 0.2776 | 16448 |
| 5e_Adaptive_Hybrid | 0.2160 | 0.2784 | 0.2031 | +0.0753 🔼 | **0.2913** | 0.2830 | 0.3276 | 0.3894 | 0.2868 | 14785 |
| 8b_Sentence_Window_6_3 | 0.2156 | 0.2874 | 0.1963 | +0.0911 🔼 | **0.3067** | 0.2989 | 0.3319 | 0.4397 | 0.2726 | 23710 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 6_Whole_Document | **0.9914** | 0.9914 | 0.000 |
| 2 | 3c_Sentence_220w | **0.9619** | 0.9619 | 0.000 |
| 3 | 4c_Recursive_1000 | **0.8615** | 0.8615 | 0.000 |
| 4 | 5b_Semantic_thr1200_max900 | **0.8590** | 0.8590 | 0.000 |
| 5 | 8b_Sentence_Window_6_3 | **0.7706** | 0.7706 | 0.000 |
| 6 | 1c_Fixed_Char_900 | **0.7401** | 0.7401 | 0.000 |
| 7 | 3_Sentence_Boundary | **0.7124** | 0.7124 | 0.000 |
| 8 | 4_Recursive_Markdown | **0.7091** | 0.7091 | 0.000 |
| 9 | 5e_Adaptive_Hybrid | **0.7079** | 0.7079 | 0.000 |
| 10 | 5d_Semantic_prefix_all | **0.6699** | 0.6699 | 0.000 |
| 11 | 5_Semantic_Context_Injected | **0.6485** | 0.6485 | 0.000 |
| 12 | 5c_Semantic_thr500_max400 | **0.6262** | 0.6262 | 0.000 |
| 13 | 2_Fixed_Word | **0.6175** | 0.6175 | 0.000 |
| 14 | 3b_Sentence_80w | **0.5787** | 0.5787 | 0.000 |
| 15 | 8_Sentence_Window | **0.5529** | 0.5529 | 0.000 |

**Chiến lược được chọn: `6_Whole_Document`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `hardware_ex_18901_google_neg_301` — 109 ký tự

```text
Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 109c ✅ — *"Press PrtScn – Captures the whole screen to clipboard Open Paint or Word and press Ctrl + V to paste and save"*

---

### `hardware_ex_18337_google_neg_99` — 456 ký tự

```text
Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for use in commercial environments, not residential environmentsDynamic security enabled printer Print speed letter: Up to 65 ppm (black) Auto duplex printing; 2 paper trays (standard); HP Sure Start FCC Class A emissions - for use in commercial environments, not residential environments Dynamic security enabled printer
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 456c ✅ — *"Print onlyPrint speed letter: Up to 65 ppm (black)Auto duplex printing; 2 paper trays (standard); HP Sure StartFCC Class A emissions - for u..."*

---

### `hardware_ex_18337_neg_8` — 1998 ký tự

```text
HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People
Home
Printers
All Printers
HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless)
Order now
for dispatch
tomorrow
Compare
Share
HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless)
Print, scan, copy, and fax
Windows, Mac and Linux compatible
9.5 x 5.4cm touchscreen colour display
Duplex printing and scanning
WiFi
Colour
A4
25 ppm
25 ppm
4...
```

- **1_Fixed_Char** (5 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers HP Color La..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"inting and scanning WiFi Colour A4 25 ppm 25 ppm 41.8cm 41.9cm 34.1cm View Full Specification HP Color LaserJet Pro MFP 3302fdw A4 Colour Mu..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"380.75 £456.90 inc. VAT View cartridges for HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) Our Pick Buy ..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (3 chunks)
  - `[0]` 771c ⚠ ends_mid_sentence — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers HP Color La..."*
  - `[1]` 747c ⚠ starts_mid_sentence, ends_mid_sentence — *"price £456.90 £380.75 ex. VAT Our price £380.75 £456.90 inc. VAT In Stock View Product Free Delivery on this product HP Color LaserJet Pro M..."*
  - `[2]` 749c ⚠ starts_mid_sentence — *"Colour Multifunction Laser Printer (Wireless) Description Dynamic security enabled printer: Certain HP printers are intended to work only wi..."*
- **3_Sentence_Boundary** (3 chunks)
  - `[0]` 898c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers HP Color La..."*
  - `[1]` 911c ✅ — *"Our price £380.75 £456.90 inc. VAT View cartridges for HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) Ou..."*
  - `[2]` 305c ✅ — *"Reused HP chips and electronic circuitry enable the use of reused, remanufactured, and refilled cartridges. Learn More Overview: This HP Col..."*
- **4_Recursive_Markdown** (4 chunks)
  - `[0]` 642c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers HP Color La..."*
  - `[1]` 540c ⚠ trailing_heading_orphan — *"£479.90 Our price £456.90 £380.75 ex. VAT Our price £380.75 £456.90 inc. VAT In Stock View Product Free Delivery on this product HP Color La..."*
  - `[2]` 627c ✅ — *"Total price for this bundle HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) Description Dynamic security ..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (4 chunks)
  - `[0]` 642c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers HP Color La..."*
  - `[1]` 660c ⚠ trailing_heading_orphan — *"[Document Topic: HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People] £479.90 Our price £4..."*
  - `[2]` 747c ✅ — *"[Document Topic: HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People] Total price for this..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 1998c ⚠ oversized_chars — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers HP Color La..."*
- **7_Parent_Child** (6 chunks)
  - `[0]` 401c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers HP Color La..."*
  - `[1]` 369c ⚠ trailing_heading_orphan — *"9.5 x 5.4cm touchscreen colour display Duplex printing and scanning WiFi Colour A4 25 ppm 25 ppm 41.8cm 41.9cm 34.1cm View Full Specificatio..."*
  - `[2]` 305c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) Our price £456.90 £380.75 ex. VAT Our price £380.75 £456...."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (32 chunks)
  - `[0]` 128c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers"*
  - `[1]` 114c ⚠ trailing_heading_orphan — *"Printers All Printers HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) Order now"*
  - `[2]` 114c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) Order now for dispatch tomorrow"*
  - *(... 29 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (17 chunks)
  - `[0]` 128c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) | Cartridge People Home Printers All Printers"*
  - `[1]` 92c ⚠ trailing_heading_orphan — *"HP Color LaserJet Pro MFP 3302fdw A4 Colour Multifunction Laser Printer (Wireless) Order now"*
  - `[2]` 21c ⚠ trailing_heading_orphan, undersized — *"for dispatch tomorrow"*
  - *(... 14 chunk nữa — xem chunk_inspection)*

---

### `hardwarerecs_ex_15102_doc_1` — 3265 ký tự

```text
The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a different approach. For one, it is considerably slimmer than the Epson V600 and the design is in our opinion, better. It uses a different sensor, a CIS (Contact Image Sensor). Now what does this mean for you? CCD provides better image quality overall but not by a big margin. The most annoying thing about CIS sensors like the one on the Canon is that you have to...
```

- **1_Fixed_Char** (8 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"sors like the one on the Canon is that you have to really flatten the document on the scanning glass, because if there is a gap bigger than ..."*
  - `[2]` 499c ⚠ starts_mid_sentence, ends_mid_sentence — *"are not using it, it takes a minimal amount of space on your desk.  The software included on the Canon is: IJ Scan Utility (Windows), IJ Sca..."*
  - *(... 5 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (6 chunks)
  - `[0]` 649c ⚠ ends_mid_sentence — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 685c ⚠ starts_mid_sentence, ends_mid_sentence — *"scanning glass, because if there is a gap bigger than 1mm the picture will come out blurred. This problem appears especially when you scan b..."*
  - `[2]` 701c ⚠ starts_mid_sentence, ends_mid_sentence — *"Scan, Custom Scan, Stitch Scan, and OCR (Optical Character Recognition), ScanGear MP Driver, Quick Menu. They chose to with OCR from their p..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (5 chunks)
  - `[0]` 681c ✅ — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 775c ⚠ dangling_pronoun — *"This problem appears especially when you scan books. To help you scan books, Canon has mounted a lid on the scanner that can be raised and l..."*
  - `[2]` 750c ⚠ dangling_pronoun — *"This makes the software feel more integrated, but the OCR technology is limited in functionality and accuracy. It doesn't have the same layo..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (6 chunks)
  - `[0]` 628c ✅ — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 338c ⚠ dangling_pronoun — *"This problem appears especially when you scan books. To help you scan books, Canon has mounted a lid on the scanner that can be raised and l..."*
  - `[2]` 640c ✅ — *"The software included on the Canon is: IJ Scan Utility (Windows), IJ Scan Utility Lite (Mac), Auto Scan, Document Scan, Photo Scan, Custom S..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (6 chunks)
  - `[0]` 628c ✅ — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 425c ⚠ dangling_pronoun_mitigated_by_prefix — *"[Document Topic: The Canon CanoScan Lide 400 is the second flatbed scanner in review.] This problem appears especially when you scan books. ..."*
  - `[2]` 727c ✅ — *"[Document Topic: The Canon CanoScan Lide 400 is the second flatbed scanner in review.] The software included on the Canon is: IJ Scan Utilit..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 3265c ⚠ over_embedding_token_limit — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
- **7_Parent_Child** (12 chunks)
  - `[0]` 312c ✅ — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 315c ✅ — *"Now what does this mean for you? CCD provides better image quality overall but not by a big margin. The most annoying thing about CIS sensor..."*
  - `[2]` 147c ⚠ dangling_pronoun — *"This problem appears especially when you scan books. To help you scan books, Canon has mounted a lid on the scanner that can be raised and l..."*
  - *(... 9 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (15 chunks)
  - `[0]` 312c ✅ — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 255c ✅ — *"For one, it is considerably slimmer than the Epson V600 and the design is in our opinion, better. It uses a different sensor, a CIS (Contact..."*
  - `[2]` 368c ✅ — *"Now what does this mean for you? CCD provides better image quality overall but not by a big margin. The most annoying thing about CIS sensor..."*
  - *(... 12 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (8 chunks)
  - `[0]` 412c ✅ — *"The Canon CanoScan Lide 400 is the second flatbed scanner in review. When we evaluate it in comparison with the V600, we can see it is a dif..."*
  - `[1]` 554c ✅ — *"The most annoying thing about CIS sensors like the one on the Canon is that you have to really flatten the document on the scanning glass, b..."*
  - `[2]` 508c ✅ — *"The software included on the Canon is: IJ Scan Utility (Windows), IJ Scan Utility Lite (Mac), Auto Scan, Document Scan, Photo Scan, Custom S..."*
  - *(... 5 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunking_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.