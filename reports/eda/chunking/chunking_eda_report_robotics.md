# Báo cáo EDA & đánh giá Chunking — domain `robotics`

*Tạo lúc 2026-11-20 23:38:01 | RETECO Track 2 (v4)*

## 1. Corpus

- Tổng tài liệu: **61,961** | schema: `content, doc_id`
- Ký tự: min=3, p25=23, **median=81**, mean=291.1, p75=214, p90=751, p95=1696, p99=2889, max=28640
- Từ: median=8, mean=24.9, max=2390
- Ước tính vượt 512 token: **0.39%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 55.43% |
| 101-300 | 25.64% |
| 301-650 | 7.8% |
| 651-800 | 1.65% |
| 801-1500 | 3.13% |
| 1501-3000 | 5.44% |
| 3001-6000 | 0.84% |
| >6000 | 0.06% |

- Cấu trúc: header 12.33% | bullet 14.88% | code 6.9% | URL 14.74% | nhiều dòng 50.61%
- Chất lượng dữ liệu: trùng 34.75% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 12.18% | thiếu dấu câu cuối 58.62% | mở đầu bằng đại từ 1.08%

## 2. Hội thoại Track 2

- Hội thoại: **20** | lượt: **75** | lượt có gold: 75
- Lượt/hội thoại: mean=3.75 (min 3, max 6)
- Độ dài query: mean=18.4 từ, median=18, max=26
- Gold docs/lượt: mean=1.96, max=8
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 1.35x | 213.6 | 22.09% | 21.8% | 0.07% | 0.07% | 1.6% | 0.56% | 0.0% | **89.71** |
| **2_Fixed_Word** | 1.06x | 252.8 | 4.78% | 4.83% | 0.05% | 0.05% | 0.0% | 0.0% | 0.0% | **97.38** |
| **3_Sentence_Boundary** | 1.04x | 251.1 | 0.0% | 0.0% | 0.05% | 0.05% | 1.44% | 0.05% | 0.0% | **99.29** |
| **4_Recursive_Markdown** | 1.22x | 215.4 | 0.0% | 0.0% | 0.21% | 0.21% | 10.82% | 0.08% | 0.0% | **98.27** |
| **5_Semantic_Context_Injected** | 1.21x | 230.4 | 0.0% | 0.0% | 0.21% | 0.0% | 10.68% | 0.08% | 0.0% | **98.34** |
| **6_Whole_Document** | 1.0x | 270.5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.45% | **99.32** |
| **7_Parent_Child** | 1.18x | 219.7 | 0.0% | 0.0% | 0.64% | 0.64% | 7.43% | 1.02% | 0.0% | **98.16** |
| **8_Sentence_Window** | 2.91x | 147.1 | 0.03% | 0.0% | 0.5% | 0.5% | 49.38% | 9.61% | 0.0% | **89.98** |
| **9_TextTiling_Semantic** | 1.65x | 157.0 | 0.0% | 0.06% | 0.36% | 0.36% | 28.74% | 10.92% | 0.0% | **92.78** |
| 1b_Fixed_Char_300 | 1.68x | 173.0 | 34.51% | 34.98% | 0.33% | 0.33% | 2.95% | 2.53% | 0.0% | **83.19** |
| 1c_Fixed_Char_900 | 1.16x | 245.9 | 11.97% | 11.84% | 0.04% | 0.04% | 0.86% | 0.0% | 0.0% | **94.5** |
| 3b_Sentence_80w | 1.12x | 238.3 | 0.0% | 0.0% | 0.22% | 0.22% | 4.61% | 0.13% | 0.0% | **98.85** |
| 3c_Sentence_220w | 1.02x | 255.7 | 0.0% | 0.0% | 0.0% | 0.0% | 0.64% | 0.0% | 0.0% | **99.42** |
| 4b_Recursive_450 | 1.38x | 189.0 | 0.04% | 0.04% | 0.25% | 0.25% | 17.1% | 0.11% | 0.0% | **97.29** |
| 4c_Recursive_1000 | 1.11x | 237.3 | 0.0% | 0.0% | 0.18% | 0.18% | 5.44% | 0.09% | 0.0% | **99.08** |
| 4d_Recursive_250 | 1.93x | 134.1 | 0.26% | 0.21% | 0.34% | 0.34% | 30.02% | 1.22% | 0.0% | **94.94** |
| 5b_Semantic_thr1200_max900 | 1.13x | 243.3 | 0.0% | 0.0% | 0.13% | 0.0% | 6.38% | 0.09% | 0.0% | **98.99** |
| 5c_Semantic_thr500_max400 | 1.42x | 207.0 | 0.11% | 0.07% | 0.28% | 0.0% | 17.85% | 0.07% | 0.0% | **97.2** |
| 5d_Semantic_prefix_all | 1.21x | 232.0 | 0.0% | 0.0% | 0.21% | 0.0% | 10.68% | 0.08% | 0.0% | **98.34** |
| 5e_Adaptive_Hybrid | 1.17x | 236.4 | 0.0% | 0.0% | 0.09% | 0.0% | 8.8% | 0.13% | 0.0% | **98.61** |
| 8b_Sentence_Window_6_3 | 2.18x | 190.6 | 0.02% | 0.0% | 0.44% | 0.44% | 41.07% | 3.44% | 0.0% | **92.81** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 69 gold + 9987 nhiễu | 75 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.2609 | 0.3477 | 0.2389 | +0.1088 🔼 | **0.3697** | 0.4054 | 0.3670 | 0.5040 | 0.3196 | 14106 |
| 2_Fixed_Word | 0.2461 | 0.3708 | 0.2292 | +0.1416 🔼 | **0.3877** | 0.4232 | 0.3824 | 0.5235 | 0.3663 | 10818 |
| 3_Sentence_Boundary | 0.2302 | 0.3742 | 0.2237 | +0.1505 🔼 | **0.3807** | 0.4280 | 0.3505 | 0.5349 | 0.3660 | 10645 |
| 4_Recursive_Markdown | 0.2592 | 0.3495 | 0.2315 | +0.1180 🔼 | **0.3772** | 0.3951 | 0.3972 | 0.5190 | 0.3310 | 12593 |
| 5_Semantic_Context_Injected | 0.2647 | 0.4002 | 0.2475 | +0.1527 🔼 | **0.4174** | 0.4596 | 0.3972 | 0.5743 | 0.3800 | 12557 |
| 6_Whole_Document | 0.2061 | 0.3649 | 0.1921 | +0.1728 🔼 | **0.3789** | 0.4099 | 0.3287 | 0.5402 | 0.3266 | 10056 |
| 7_Parent_Child | 0.2648 | 0.3776 | 0.2385 | +0.1391 🔼 | **0.4039** | 0.4245 | 0.3994 | 0.5093 | 0.3846 | 12325 |
| 8_Sentence_Window | 0.3158 | 0.3854 | 0.2822 | +0.1032 🔼 | **0.4190** | 0.4595 | 0.4338 | 0.5171 | 0.3883 | 31963 |
| 9_TextTiling_Semantic | 0.2769 | 0.3700 | 0.2509 | +0.1191 🔼 | **0.3960** | 0.4132 | 0.3997 | 0.5338 | 0.3585 | 17955 |
| 1b_Fixed_Char_300 | 0.2587 | 0.3244 | 0.2329 | +0.0915 🔼 | **0.3502** | 0.4021 | 0.3635 | 0.4829 | 0.3145 | 17918 |
| 1c_Fixed_Char_900 | 0.2210 | 0.3419 | 0.1971 | +0.1448 🔼 | **0.3658** | 0.3846 | 0.3907 | 0.5310 | 0.3062 | 11843 |
| 3b_Sentence_80w | 0.2268 | 0.3590 | 0.2028 | +0.1562 🔼 | **0.3830** | 0.3971 | 0.3655 | 0.5049 | 0.3464 | 11535 |
| 3c_Sentence_220w | 0.2325 | 0.3739 | 0.2136 | +0.1603 🔼 | **0.3928** | 0.4459 | 0.3549 | 0.5460 | 0.3584 | 10276 |
| 4b_Recursive_450 | 0.2785 | 0.3992 | 0.2523 | +0.1469 🔼 | **0.4254** | 0.4289 | 0.3756 | 0.5703 | 0.3842 | 14536 |
| 4c_Recursive_1000 | 0.2305 | 0.3379 | 0.2103 | +0.1276 🔼 | **0.3581** | 0.4291 | 0.3585 | 0.4807 | 0.3204 | 11357 |
| 4d_Recursive_250 | 0.2379 | 0.3404 | 0.2156 | +0.1248 🔼 | **0.3627** | 0.3568 | 0.3408 | 0.4662 | 0.3452 | 20754 |
| 5b_Semantic_thr1200_max900 | 0.2130 | 0.3388 | 0.1988 | +0.1400 🔼 | **0.3530** | 0.4238 | 0.3374 | 0.5329 | 0.3048 | 11555 |
| 5c_Semantic_thr500_max400 | 0.2459 | 0.3917 | 0.2261 | +0.1656 🔼 | **0.4115** | 0.4551 | 0.3777 | 0.5257 | 0.3949 | 15007 |
| 5d_Semantic_prefix_all | 0.2627 | 0.4055 | 0.2317 | +0.1738 🔼 | **0.4365** | 0.4462 | 0.3994 | 0.5787 | 0.3843 | 12557 |
| 5e_Adaptive_Hybrid | 0.2544 | 0.3989 | 0.2264 | +0.1725 🔼 | **0.4269** | 0.3985 | 0.4035 | 0.5611 | 0.3868 | 12058 |
| 8b_Sentence_Window_6_3 | 0.2875 | 0.3561 | 0.2603 | +0.0958 🔼 | **0.3833** | 0.4349 | 0.4169 | 0.5250 | 0.3378 | 23647 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 5d_Semantic_prefix_all | **0.9524** | 0.9524 | 0.000 |
| 2 | 5e_Adaptive_Hybrid | **0.8955** | 0.8955 | 0.000 |
| 3 | 5_Semantic_Context_Injected | **0.8453** | 0.8453 | 0.000 |
| 4 | 4b_Recursive_450 | **0.8245** | 0.8245 | 0.000 |
| 5 | 7_Parent_Child | **0.7019** | 0.7019 | 0.000 |
| 6 | 5c_Semantic_thr500_max400 | **0.6979** | 0.6979 | 0.000 |
| 7 | 3c_Sentence_220w | **0.6783** | 0.6783 | 0.000 |
| 8 | 8_Sentence_Window | **0.6318** | 0.6318 | 0.000 |
| 9 | 2_Fixed_Word | **0.6190** | 0.6190 | 0.000 |
| 10 | 3_Sentence_Boundary | **0.5914** | 0.5914 | 0.000 |
| 11 | 6_Whole_Document | **0.5706** | 0.5706 | 0.000 |
| 12 | 9_TextTiling_Semantic | **0.5698** | 0.5698 | 0.000 |
| 13 | 4_Recursive_Markdown | **0.5687** | 0.5687 | 0.000 |
| 14 | 3b_Sentence_80w | **0.5667** | 0.5667 | 0.000 |
| 15 | 8b_Sentence_Window_6_3 | **0.4936** | 0.4936 | 0.000 |

**Chiến lược được chọn: `5d_Semantic_prefix_all`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `ros2humble/1433_64.txt` — 9 ký tự

```text
Copy link
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 9c ✅ — *"Copy link"*

---

### `gazebo/42_61.txt` — 74 ký tự

```text
[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 72c ✅ — *"[ farbod-new ](/farbod-new) opened this issue Dec 18, 2020 · 12 comments"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 74c ✅ — *"[ farbod-new ](/farbod-new) opened this issue  Dec 18, 2020  · 12 comments"*

---

### `colcon_doxygen/dwresphpresourcecomp_637.txt` — 1722 ký tự

```text
kphotoalbum-5.12.0-3.fc40.x86_64.rpm  
kpilot-5.3.0-40.fc40.x86_64.rpm  
kpilot-libs-5.3.0-40.fc40.i686.rpm  
kpilot-libs-5.3.0-40.fc40.x86_64.rpm  
kpimtextedit-24.02.2-1.fc41.i686.rpm  
kpimtextedit-24.02.2-1.fc41.x86_64.rpm  
kpimtextedit-devel-24.02.2-1.fc41.i686.rpm  
kpimtextedit-devel-24.02.2-1.fc41.x86_64.rpm  
kpimtextedit-doc-24.02.2-1.fc41.noarch.rpm  
kpipewire-6.0.3-3.fc41.i686.rpm  
kpipewire-6.0.3-3.fc41.x86_64.rpm  
kpipewire-devel-6.0.3-3.fc41.i686.rpm  
kpipewire-devel-6.0.3-3....
```

- **1_Fixed_Char** (4 chunks)
  - `[0]` 500c ✅ — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm   kpilot-5.3.0-40.fc40.x86_64.rpm   kpilot-libs-5.3.0-40.fc40.i686.rpm   kpilot-libs-5.3.0-40.fc40.x86_..."*
  - `[1]` 500c ⚠ starts_mid_sentence — *"l-6.0.3-3.fc41.i686.rpm   kpipewire-devel-6.0.3-3.fc41.x86_64.rpm   kpkpass-24.02.2-1.fc41.i686.rpm   kpkpass-24.02.2-1.fc41.x86_64.rpm   kp..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"perty-3.2.0-8.fc39.x86_64.rpm   kproperty-devel-3.2.0-8.fc39.i686.rpm   kproperty-devel-3.2.0-8.fc39.x86_64.rpm   kpublictransport-24.02.2-1..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 1644c ⚠ oversized_chars — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm kpilot-5.3.0-40.fc40.x86_64.rpm kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 1644c ⚠ oversized_chars — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm kpilot-5.3.0-40.fc40.x86_64.rpm kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm..."*
- **4_Recursive_Markdown** (3 chunks)
  - `[0]` 595c ⚠ trailing_heading_orphan — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm kpilot-5.3.0-40.fc40.x86_64.rpm kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm..."*
  - `[1]` 592c ⚠ trailing_heading_orphan — *"kpkpass-devel-24.02.2-1.fc41.x86_64.rpm kpkpass-doc-24.02.2-1.fc41.noarch.rpm kpmcore-24.02.2-1.fc41.i686.rpm kpmcore-24.02.2-1.fc41.x86_64...."*
  - `[2]` 455c ✅ — *"kqoauth-qt5-0.98-0.17.20140122git7c31a12.fc40.i686.rpm kqoauth-qt5-0.98-0.17.20140122git7c31a12.fc40.x86_64.rpm kqoauth-qt5-devel-0.98-0.17...."*
- **5_Semantic_Context_Injected** (3 chunks)
  - `[0]` 595c ⚠ trailing_heading_orphan — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm kpilot-5.3.0-40.fc40.x86_64.rpm kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm..."*
  - `[1]` 647c ⚠ trailing_heading_orphan — *"[Document Topic: kphotoalbum-5.12.0-3.fc40.x86_64.rpm] kpkpass-devel-24.02.2-1.fc41.x86_64.rpm kpkpass-doc-24.02.2-1.fc41.noarch.rpm kpmcore..."*
  - `[2]` 510c ✅ — *"[Document Topic: kphotoalbum-5.12.0-3.fc40.x86_64.rpm] kqoauth-qt5-0.98-0.17.20140122git7c31a12.fc40.i686.rpm kqoauth-qt5-0.98-0.17.20140122..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 1722c ⚠ oversized_chars — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm   kpilot-5.3.0-40.fc40.x86_64.rpm   kpilot-libs-5.3.0-40.fc40.i686.rpm   kpilot-libs-5.3.0-40.fc40.x86_..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 1644c ⚠ oversized_chars — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm kpilot-5.3.0-40.fc40.x86_64.rpm kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm..."*
- **8_Sentence_Window** (19 chunks)
  - `[0]` 140c ⚠ trailing_heading_orphan — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm kpilot-5.3.0-40.fc40.x86_64.rpm kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm"*
  - `[1]` 147c ⚠ trailing_heading_orphan — *"kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm kpimtextedit-24.02.2-1.fc41.i686.rpm kpimtextedit-24.02.2-1.fc41.x86..."*
  - `[2]` 163c ⚠ trailing_heading_orphan — *"kpimtextedit-24.02.2-1.fc41.i686.rpm kpimtextedit-24.02.2-1.fc41.x86_64.rpm kpimtextedit-devel-24.02.2-1.fc41.i686.rpm kpimtextedit-devel-24..."*
  - *(... 16 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (9 chunks)
  - `[0]` 140c ⚠ trailing_heading_orphan — *"kphotoalbum-5.12.0-3.fc40.x86_64.rpm kpilot-5.3.0-40.fc40.x86_64.rpm kpilot-libs-5.3.0-40.fc40.i686.rpm kpilot-libs-5.3.0-40.fc40.x86_64.rpm"*
  - `[1]` 206c ⚠ trailing_heading_orphan — *"kpimtextedit-24.02.2-1.fc41.i686.rpm kpimtextedit-24.02.2-1.fc41.x86_64.rpm kpimtextedit-devel-24.02.2-1.fc41.i686.rpm kpimtextedit-devel-24..."*
  - `[2]` 143c ⚠ trailing_heading_orphan — *"kpipewire-6.0.3-3.fc41.i686.rpm kpipewire-6.0.3-3.fc41.x86_64.rpm kpipewire-devel-6.0.3-3.fc41.i686.rpm kpipewire-devel-6.0.3-3.fc41.x86_64...."*
  - *(... 6 chunk nữa — xem chunk_inspection)*

---

### `moveit_config/CMakeCachetxt_27.txt` — 5053 ký tự

```text
gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux-
gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux-
gnu/liburdfdom_model.so;general;/usr/lib/x86_64-linux-
gnu/liburdfdom_world.so;general;/opt/ros/kinetic/lib/librosconsole_bridge.so;general;/opt/ros/kinetic/lib/libtf_conversions.so;general;/opt/ros/kinetic/lib/libkdl_conversions.so;general;/opt/ros/kinetic/lib/liborocos-
kdl.so.1.3.0;general;/opt/ros/kinetic/lib/libtf.so;general;/opt/ros/kinetic/lib/libtf2_ros.so;general;/opt/ros...
```

- **1_Fixed_Char** (12 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"opt/ros/kinetic/lib/libtf2_ros.so;general;/opt/ros/kinetic/lib/libactionlib.so;general;/opt/ros/kinetic/lib/libtf2.so;general;image_transpor..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"ibrosconsole.so;general;/opt/ros/kinetic/lib/librosconsole_log4cxx.so;general;/opt/ros/kinetic/lib/librosconsole_backend_interface.so;genera..."*
  - *(... 9 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 5053c ⚠ oversized_chars — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 5053c ⚠ oversized_chars — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
- **4_Recursive_Markdown** (9 chunks)
  - `[0]` 389c ✅ — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
  - `[1]` 455c ✅ — *"kdl.so.1.3.0;general;/opt/ros/kinetic/lib/libtf.so;general;/opt/ros/kinetic/lib/libtf2_ros.so;general;/opt/ros/kinetic/lib/libactionlib.so;g..."*
  - `[2]` 558c ⚠ trailing_heading_orphan — *"gnu/libboost_signals.so;general;/opt/ros/kinetic/lib/librosconsole.so;general;/opt/ros/kinetic/lib/librosconsole_log4cxx.so;general;/opt/ros..."*
  - *(... 6 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (9 chunks)
  - `[0]` 389c ✅ — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
  - `[1]` 529c ✅ — *"[Document Topic: gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux-] kdl.so.1.3.0;general;/opt/ros/kinetic/lib/libtf.so;general;/opt/ro..."*
  - `[2]` 632c ⚠ trailing_heading_orphan — *"[Document Topic: gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux-] gnu/libboost_signals.so;general;/opt/ros/kinetic/lib/librosconsole..."*
  - *(... 6 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 5053c ⚠ oversized_chars — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 5053c ⚠ oversized_chars — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
- **8_Sentence_Window** (19 chunks)
  - `[0]` 389c ✅ — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
  - `[1]` 728c ✅ — *"gnu/liburdfdom_model.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_world.so;general;/opt/ros/kinetic/lib/librosconsole_bridge.so;general;..."*
  - `[2]` 723c ⚠ trailing_heading_orphan — *"kdl.so.1.3.0;general;/opt/ros/kinetic/lib/libtf.so;general;/opt/ros/kinetic/lib/libtf2_ros.so;general;/opt/ros/kinetic/lib/libactionlib.so;g..."*
  - *(... 16 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (7 chunks)
  - `[0]` 171c ⚠ trailing_heading_orphan — *"gnu/liburdfdom_sensor.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model_state.so;general;/usr/lib/x86_64-linux- gnu/liburdfdom_model.so..."*
  - `[1]` 1123c ✅ — *"gnu/liburdfdom_world.so;general;/opt/ros/kinetic/lib/librosconsole_bridge.so;general;/opt/ros/kinetic/lib/libtf_conversions.so;general;/opt/..."*
  - `[2]` 1017c ⚠ trailing_heading_orphan — *"gnu/libpython2.7.so;general;/usr/lib/x86_64-linux- gnu/libboost_filesystem.so;general;/usr/lib/x86_64-linux- gnu/libboost_program_options.so..."*
  - *(... 4 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunking_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.