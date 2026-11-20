# Báo cáo EDA & đánh giá Chunking — domain `sustainable_living`

*Tạo lúc 2026-11-20 23:38:29 | RETECO Track 2 (v4)*

## 1. Corpus

- Tổng tài liệu: **60,792** | schema: `content, doc_id`
- Ký tự: min=1, p25=37, **median=125**, mean=344.2, p75=341, p90=872, p95=1387, p99=2255, max=158299
- Từ: median=11, mean=43.0, max=14161
- Ước tính vượt 512 token: **0.52%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 44.42% |
| 101-300 | 27.74% |
| 301-650 | 13.98% |
| 651-800 | 2.85% |
| 801-1500 | 6.82% |
| 1501-3000 | 3.55% |
| 3001-6000 | 0.39% |
| >6000 | 0.25% |

- Cấu trúc: header 12.0% | bullet 15.86% | code 0.08% | URL 23.84% | nhiều dòng 57.9%
- Chất lượng dữ liệu: trùng 17.52% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 4.81% | thiếu dấu câu cuối 42.48% | mở đầu bằng đại từ 1.2%

## 2. Hội thoại Track 2

- Hội thoại: **23** | lượt: **84** | lượt có gold: 84
- Lượt/hội thoại: mean=3.65 (min 3, max 5)
- Độ dài query: mean=17.8 từ, median=18, max=24
- Gold docs/lượt: mean=2.17, max=10
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 1.35x | 242.9 | 24.28% | 24.83% | 0.44% | 0.44% | 0.18% | 1.11% | 0.0% | **88.49** |
| **2_Fixed_Word** | 1.15x | 286.5 | 11.98% | 11.94% | 0.48% | 0.48% | 0.0% | 0.0% | 0.0% | **94.39** |
| **3_Sentence_Boundary** | 1.11x | 286.1 | 0.0% | 0.0% | 0.27% | 0.27% | 3.07% | 0.14% | 0.0% | **99.32** |
| **4_Recursive_Markdown** | 1.22x | 254.8 | 0.0% | 0.0% | 0.33% | 0.33% | 4.11% | 0.08% | 0.0% | **99.25** |
| **5_Semantic_Context_Injected** | 1.2x | 273.4 | 0.0% | 0.0% | 0.33% | 0.0% | 3.53% | 0.04% | 0.0% | **99.42** |
| **6_Whole_Document** | 1.0x | 311.5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.35% | **99.54** |
| **7_Parent_Child** | 1.43x | 216.0 | 0.0% | 0.03% | 1.01% | 1.01% | 10.91% | 1.78% | 0.0% | **97.52** |
| **8_Sentence_Window** | 2.71x | 182.5 | 0.04% | 0.02% | 1.75% | 1.75% | 28.79% | 7.9% | 0.0% | **93.0** |
| **9_TextTiling_Semantic** | 1.63x | 189.4 | 0.0% | 0.03% | 1.13% | 1.13% | 16.02% | 9.1% | 0.0% | **94.87** |
| 1b_Fixed_Char_300 | 1.75x | 191.1 | 40.01% | 40.03% | 0.66% | 0.66% | 0.86% | 3.64% | 0.0% | **80.71** |
| 1c_Fixed_Char_900 | 1.14x | 285.0 | 11.14% | 11.32% | 0.09% | 0.09% | 0.13% | 0.0% | 0.0% | **94.89** |
| 3b_Sentence_80w | 1.3x | 251.8 | 0.0% | 0.0% | 0.92% | 0.92% | 8.7% | 0.34% | 0.0% | **98.24** |
| 3c_Sentence_220w | 1.04x | 299.7 | 0.0% | 0.0% | 0.24% | 0.24% | 1.01% | 0.05% | 0.0% | **99.54** |
| 4b_Recursive_450 | 1.42x | 218.3 | 0.04% | 0.0% | 0.6% | 0.6% | 9.27% | 0.07% | 0.0% | **98.36** |
| 4c_Recursive_1000 | 1.09x | 284.7 | 0.0% | 0.0% | 0.05% | 0.05% | 1.83% | 0.05% | 0.0% | **99.68** |
| 4d_Recursive_250 | 2.12x | 145.5 | 0.24% | 0.21% | 1.01% | 1.01% | 19.13% | 1.01% | 0.0% | **96.35** |
| 5b_Semantic_thr1200_max900 | 1.09x | 291.6 | 0.0% | 0.0% | 0.05% | 0.0% | 1.83% | 0.05% | 0.0% | **99.71** |
| 5c_Semantic_thr500_max400 | 1.45x | 242.2 | 0.03% | 0.0% | 0.55% | 0.0% | 9.24% | 0.14% | 0.0% | **98.47** |
| 5d_Semantic_prefix_all | 1.2x | 275.2 | 0.0% | 0.0% | 0.33% | 0.0% | 3.53% | 0.04% | 0.0% | **99.42** |
| 5e_Adaptive_Hybrid | 1.15x | 282.1 | 0.0% | 0.0% | 0.26% | 0.0% | 2.61% | 0.04% | 0.0% | **99.56** |
| 8b_Sentence_Window_6_3 | 1.98x | 236.5 | 0.0% | 0.03% | 1.01% | 1.01% | 22.16% | 5.04% | 0.0% | **95.0** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 99 gold + 9987 nhiễu | 84 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.3021 | 0.4289 | 0.2869 | +0.1420 🔼 | **0.4441** | 0.4749 | 0.4310 | 0.5938 | 0.4116 | 14439 |
| 2_Fixed_Word | 0.3552 | 0.4344 | 0.3352 | +0.0992 🔼 | **0.4544** | 0.4980 | 0.4583 | 0.5696 | 0.4166 | 11934 |
| 3_Sentence_Boundary | 0.3362 | 0.4471 | 0.3177 | +0.1294 🔼 | **0.4656** | 0.5060 | 0.4420 | 0.5840 | 0.4285 | 11451 |
| 4_Recursive_Markdown | 0.3333 | 0.4177 | 0.3016 | +0.1161 🔼 | **0.4494** | 0.4561 | 0.4881 | 0.5587 | 0.4076 | 12876 |
| 5_Semantic_Context_Injected | 0.3271 | 0.4165 | 0.3081 | +0.1084 🔼 | **0.4355** | 0.4814 | 0.4643 | 0.5614 | 0.3989 | 12727 |
| 6_Whole_Document | 0.3079 | 0.4471 | 0.2840 | +0.1631 🔼 | **0.4710** | 0.5094 | 0.4261 | 0.6153 | 0.4151 | 10086 |
| 7_Parent_Child | 0.3189 | 0.3866 | 0.2962 | +0.0904 🔼 | **0.4093** | 0.4174 | 0.4396 | 0.5462 | 0.3667 | 15125 |
| 8_Sentence_Window | 0.3275 | 0.3846 | 0.2886 | +0.0960 🔼 | **0.4235** | 0.4689 | 0.4658 | 0.5572 | 0.3654 | 29093 |
| 9_TextTiling_Semantic | 0.3046 | 0.3717 | 0.2872 | +0.0845 🔼 | **0.3891** | 0.4430 | 0.4483 | 0.5304 | 0.3380 | 17321 |
| 1b_Fixed_Char_300 | 0.3125 | 0.3814 | 0.2778 | +0.1036 🔼 | **0.4161** | 0.4528 | 0.4534 | 0.5352 | 0.3687 | 18912 |
| 1c_Fixed_Char_900 | 0.3189 | 0.4417 | 0.3091 | +0.1326 🔼 | **0.4515** | 0.4896 | 0.4360 | 0.5954 | 0.4227 | 11833 |
| 3b_Sentence_80w | 0.3142 | 0.4118 | 0.3012 | +0.1106 🔼 | **0.4248** | 0.4638 | 0.4459 | 0.5525 | 0.3968 | 13748 |
| 3c_Sentence_220w | 0.3166 | 0.4400 | 0.3116 | +0.1284 🔼 | **0.4450** | 0.5074 | 0.4261 | 0.6034 | 0.4083 | 10681 |
| 4b_Recursive_450 | 0.3471 | 0.4077 | 0.3121 | +0.0956 🔼 | **0.4427** | 0.4726 | 0.4637 | 0.5388 | 0.4031 | 15270 |
| 4c_Recursive_1000 | 0.3464 | 0.4447 | 0.3346 | +0.1101 🔼 | **0.4565** | 0.4836 | 0.4491 | 0.5872 | 0.4307 | 11419 |
| 4d_Recursive_250 | 0.2992 | 0.3132 | 0.2648 | +0.0484 🔼 | **0.3476** | 0.3677 | 0.4638 | 0.4752 | 0.2907 | 23208 |
| 5b_Semantic_thr1200_max900 | 0.3414 | 0.4391 | 0.3217 | +0.1174 🔼 | **0.4588** | 0.4856 | 0.4598 | 0.5813 | 0.4173 | 11491 |
| 5c_Semantic_thr500_max400 | 0.3483 | 0.4296 | 0.3220 | +0.1076 🔼 | **0.4559** | 0.4917 | 0.4677 | 0.5600 | 0.4210 | 15680 |
| 5d_Semantic_prefix_all | 0.3266 | 0.4165 | 0.3041 | +0.1124 🔼 | **0.4390** | 0.4814 | 0.4643 | 0.5614 | 0.3989 | 12727 |
| 5e_Adaptive_Hybrid | 0.3207 | 0.4181 | 0.3176 | +0.1005 🔼 | **0.4212** | 0.4536 | 0.4479 | 0.5872 | 0.3904 | 12122 |
| 8b_Sentence_Window_6_3 | 0.3526 | 0.4462 | 0.3220 | +0.1242 🔼 | **0.4768** | 0.4917 | 0.4920 | 0.5897 | 0.4273 | 21153 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 6_Whole_Document | **0.9210** | 0.9210 | 0.000 |
| 2 | 5b_Semantic_thr1200_max900 | **0.8646** | 0.8646 | 0.000 |
| 3 | 3_Sentence_Boundary | **0.8588** | 0.8588 | 0.000 |
| 4 | 8b_Sentence_Window_6_3 | **0.8567** | 0.8567 | 0.000 |
| 5 | 4c_Recursive_1000 | **0.8491** | 0.8491 | 0.000 |
| 6 | 4_Recursive_Markdown | **0.8163** | 0.8163 | 0.000 |
| 7 | 3c_Sentence_220w | **0.8063** | 0.8063 | 0.000 |
| 8 | 5c_Semantic_thr500_max400 | **0.7810** | 0.7810 | 0.000 |
| 9 | 5d_Semantic_prefix_all | **0.7552** | 0.7552 | 0.000 |
| 10 | 1c_Fixed_Char_900 | **0.7547** | 0.7547 | 0.000 |
| 11 | 2_Fixed_Word | **0.7521** | 0.7521 | 0.000 |
| 12 | 5_Semantic_Context_Injected | **0.7430** | 0.7430 | 0.000 |
| 13 | 5e_Adaptive_Hybrid | **0.7145** | 0.7145 | 0.000 |
| 14 | 4b_Recursive_450 | **0.7003** | 0.7003 | 0.000 |
| 15 | 3b_Sentence_80w | **0.6411** | 0.6411 | 0.000 |

**Chiến lược được chọn: `6_Whole_Document`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `renewable_energy/renewableenergycleanfacts_13.txt` — 14 ký tự

```text
##  Breadcrumb
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 13c ✅ — *"## Breadcrumb"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 14c ✅ — *"##  Breadcrumb"*

---

### `chicken_lawn/shouldigiveyogurttomychickensnope_43.txt` — 127 ký tự

```text
Are you rolling your eyes? Everybody knows about milk! It’s that white liquid
you find in the dairy case at your grocery store!
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 127c ✅ — *"Are you rolling your eyes? Everybody knows about milk! It’s that white liquid you find in the dairy case at your grocery store!"*

---

### `video_power/cphpg282942p1885350_7.txt` — 1372 ký tự

```text
* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346)
  * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885352 "Describes the two types of images, raster and vector.")
  * [ Color Modes  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885354 "Basic description of CMYK and RGB color spaces and when to use which.")
  * [ Image File Formats  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885348 "Overview of common image files such as JPG, GIF, and TIFF...
```

- **1_Fixed_Char** (3 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346)   * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=28..."*
  - `[1]` 499c ⚠ starts_mid_sentence, ends_mid_sentence — *"w of common image files such as JPG, GIF, and TIFF.")   * [ Scanning  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885349)   * [ What is..."*
  - `[2]` 472c ⚠ starts_mid_sentence — *"own  ](javascript:void\(0\);)     * [ Use GIMP to Change Resolution ](https://guides.lib.umich.edu/c.php?g=282942&p=1888164 "Shows how to ch..."*
- **2_Fixed_Word** (2 chunks)
  - `[0]` 1158c ⚠ ends_mid_sentence — *"* [ Home ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346) * [ Raster vs. Vector Images ](https://guides.lib.umich.edu/c.php?g=282942..."*
  - `[1]` 333c ⚠ starts_mid_sentence — *"how to change resolution using GIMP") * [ How to Resize an Image ](https://guides.lib.umich.edu/c.php?g=282942&p=1888161 "How to resize imag..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 1348c ✅ — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346) * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=2829..."*
- **4_Recursive_Markdown** (2 chunks)
  - `[0]` 650c ✅ — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346) * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=2829..."*
  - `[1]` 697c ✅ — *"* [ What is Resizing?  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885347) * [ How to Change Resolution  ](https://guides.lib.umich.edu..."*
- **5_Semantic_Context_Injected** (2 chunks)
  - `[0]` 650c ✅ — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346) * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=2829..."*
  - `[1]` 781c ✅ — *"[Document Topic: * [ Home ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346)] * [ What is Resizing?  ](https://guides.lib.umich.edu/c...."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 1372c ✅ — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346)   * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=28..."*
- **7_Parent_Child** (3 chunks)
  - `[0]` 568c ✅ — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346) * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=2829..."*
  - `[1]` 481c ✅ — *"* [ What is Resolution?  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885350) * [ What is Resizing?  ](https://guides.lib.umich.edu/c.ph..."*
  - `[2]` 297c ✅ — *"* [ How to Resize an Image  ](https://guides.lib.umich.edu/c.php?g=282942&p=1888161 "How to resize images using Adobe Photoshop") [ Toggle D..."*
- **8_Sentence_Window** (5 chunks)
  - `[0]` 355c ✅ — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346) * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=2829..."*
  - `[1]` 486c ✅ — *"Vector Images  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885352 "Describes the two types of images, raster and vector.") * [ Color Mo..."*
  - `[2]` 374c ✅ — *"* [ Image File Formats  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885348 "Overview of common image files such as JPG, GIF, and TIFF."..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (3 chunks)
  - `[0]` 355c ✅ — *"* [ Home  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885346) * [ Raster vs. Vector Images  ](https://guides.lib.umich.edu/c.php?g=2829..."*
  - `[1]` 694c ✅ — *"* [ Image File Formats  ](https://guides.lib.umich.edu/c.php?g=282942&p=1885348 "Overview of common image files such as JPG, GIF, and TIFF."..."*
  - `[2]` 297c ✅ — *"* [ How to Resize an Image  ](https://guides.lib.umich.edu/c.php?g=282942&p=1888161 "How to resize images using Adobe Photoshop") [ Toggle D..."*

---

### `low_surface/boilersystemexplainedlthw_151.txt` — 7526 ký tự

```text
Advertisement cookies are used to provide visitors with relevant ads and
marketing campaigns. These cookies track visitors across websites and collect
information to provide customized ads.  Cookie  |  Duration  |  Description  
---|---|---  
__gpi  |  1 year 24 days  |  Google Ads Service uses this cookie to collect
information about from multiple websites for retargeting ads.  
__Host-GAPS  |  2 years  |  This cookie allows the website to identify a user
and provide enhanced functionality and ...
```

- **1_Fixed_Char** (17 chunks)
  - `[0]` 499c ⚠ ends_mid_sentence — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"ify a user and provide enhanced functionality and personalisation.   _fbp  |  3 months  |  This cookie is set by Facebook to display adverti..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"bsite.   A3  |  1 year  |  Yahoo set this cookie for targeted advertising.   ab  |  1 year  |  Owned by agkn, this cookie is used for target..."*
  - *(... 14 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (13 chunks)
  - `[0]` 755c ⚠ ends_mid_sentence — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 668c ⚠ starts_mid_sentence, ends_mid_sentence — *"Facebook advertising, after visiting the website. _rxuuid | 1 year | Unruly Media sets this cookie to store information on how the end user ..."*
  - `[2]` 683c ⚠ starts_mid_sentence, ends_mid_sentence — *"helps to categorise the users interest and to create profiles in terms of resales of targeted marketing. This cookie is used to collect user..."*
  - *(... 10 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (10 chunks)
  - `[0]` 851c ⚠ trailing_heading_orphan — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 771c ✅ — *"how the end user uses the website and any advertising that the end user may have seen before visiting the said website. A3  |  1 year  |  Ya..."*
  - `[2]` 834c ⚠ trailing_heading_orphan — *"tracks audiences internally. The cookie is used to limit the number of repetitive ads shown to the user. CMID  |  1 year  |  Casale Media se..."*
  - *(... 7 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (13 chunks)
  - `[0]` 510c ✅ — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 544c ✅ — *"_fbp  |  3 months  |  This cookie is set by Facebook to display advertisements when either on Facebook or on a digital platform powered by F..."*
  - `[2]` 568c ✅ — *"anj  |  3 months  |  AppNexus sets the anj cookie that contains data stating whether a cookie ID is synced with partners. ANON_ID_old  |  3 ..."*
  - *(... 10 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (13 chunks)
  - `[0]` 510c ✅ — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 635c ✅ — *"[Document Topic: Advertisement cookies are used to provide visitors with relevant ads and] _fbp  |  3 months  |  This cookie is set by Faceb..."*
  - `[2]` 659c ✅ — *"[Document Topic: Advertisement cookies are used to provide visitors with relevant ads and] anj  |  3 months  |  AppNexus sets the anj cookie..."*
  - *(... 10 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 7526c ⚠ over_embedding_token_limit — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
- **7_Parent_Child** (24 chunks)
  - `[0]` 375c ✅ — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 322c ✅ — *"__Host-GAPS  |  2 years  |  This cookie allows the website to identify a user and provide enhanced functionality and personalisation. _fbp  ..."*
  - `[2]` 262c ✅ — *"_rxuuid  |  1 year  |  Unruly Media sets this cookie to store information on how the end user uses the website and any advertising that the ..."*
  - *(... 21 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (62 chunks)
  - `[0]` 189c ✅ — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 143c ⚠ dangling_pronoun, trailing_heading_orphan — *"These cookies track visitors across websites and collect information to provide customized ads. Cookie  |  Duration  |  Description ---|---|..."*
  - `[2]` 185c ✅ — *"Cookie  |  Duration  |  Description ---|---|--- __gpi  |  1 year 24 days  |  Google Ads Service uses this cookie to collect information abou..."*
  - *(... 59 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (22 chunks)
  - `[0]` 189c ✅ — *"Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites a..."*
  - `[1]` 263c ⚠ trailing_heading_orphan — *"Cookie  |  Duration  |  Description ---|---|--- __gpi  |  1 year 24 days  |  Google Ads Service uses this cookie to collect information abou..."*
  - `[2]` 203c ⚠ starts_with_connector, trailing_heading_orphan — *"and provide enhanced functionality and personalisation. _fbp  |  3 months  |  This cookie is set by Facebook to display advertisements when ..."*
  - *(... 19 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunking_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.