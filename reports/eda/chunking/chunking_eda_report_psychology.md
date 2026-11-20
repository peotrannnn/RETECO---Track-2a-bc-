# Báo cáo EDA & đánh giá Chunking — domain `psychology`

*Tạo lúc 2026-11-20 23:37:07 | RETECO Track 2 (v4)*

## 1. Corpus

- Tổng tài liệu: **52,835** | schema: `content, doc_id`
- Ký tự: min=3, p25=37, **median=130**, mean=384.4, p75=341, p90=775, p95=1307, p99=3832, max=226941
- Từ: median=12, mean=46.7, max=23141
- Ước tính vượt 512 token: **1.46%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 42.98% |
| 101-300 | 28.85% |
| 301-650 | 15.42% |
| 651-800 | 3.09% |
| 801-1500 | 5.53% |
| 1501-3000 | 2.64% |
| 3001-6000 | 1.01% |
| >6000 | 0.48% |

- Cấu trúc: header 11.44% | bullet 17.78% | code 0.61% | URL 23.69% | nhiều dòng 56.32%
- Chất lượng dữ liệu: trùng 17.18% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 1.76% | thiếu dấu câu cuối 36.39% | mở đầu bằng đại từ 1.36%

## 2. Hội thoại Track 2

- Hội thoại: **25** | lượt: **99** | lượt có gold: 99
- Lượt/hội thoại: mean=3.96 (min 3, max 6)
- Độ dài query: mean=16.8 từ, median=17, max=25
- Gold docs/lượt: mean=1.93, max=12
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 1.54x | 275.1 | 32.47% | 32.6% | 0.52% | 0.52% | 0.26% | 1.43% | 0.0% | **84.78** |
| **2_Fixed_Word** | 1.24x | 347.3 | 16.3% | 16.58% | 0.36% | 0.36% | 0.0% | 0.0% | 0.0% | **92.4** |
| **3_Sentence_Boundary** | 1.18x | 347.3 | 0.0% | 0.0% | 0.38% | 0.38% | 4.78% | 0.04% | 0.0% | **99.06** |
| **4_Recursive_Markdown** | 1.4x | 282.9 | 0.04% | 0.04% | 0.57% | 0.57% | 7.92% | 0.43% | 0.0% | **98.49** |
| **5_Semantic_Context_Injected** | 1.38x | 308.9 | 0.04% | 0.04% | 0.54% | 0.0% | 7.25% | 0.25% | 0.0% | **98.77** |
| **6_Whole_Document** | 1.0x | 396.9 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.95% | **99.33** |
| **7_Parent_Child** | 1.6x | 247.6 | 0.0% | 0.0% | 1.41% | 1.41% | 12.07% | 1.78% | 0.0% | **97.22** |
| **8_Sentence_Window** | 3.27x | 199.7 | 0.03% | 0.0% | 2.0% | 2.0% | 26.25% | 6.2% | 0.0% | **93.76** |
| **9_TextTiling_Semantic** | 1.96x | 202.1 | 0.03% | 0.0% | 1.76% | 1.76% | 15.7% | 14.62% | 0.0% | **93.36** |
| 1b_Fixed_Char_300 | 2.07x | 207.1 | 48.47% | 47.72% | 0.75% | 0.75% | 0.92% | 3.67% | 0.0% | **77.01** |
| 1c_Fixed_Char_900 | 1.23x | 338.7 | 17.96% | 17.71% | 0.16% | 0.16% | 0.41% | 0.0% | 0.0% | **91.85** |
| 3b_Sentence_80w | 1.45x | 295.5 | 0.0% | 0.0% | 1.24% | 1.24% | 10.28% | 0.31% | 0.0% | **97.92** |
| 3c_Sentence_220w | 1.09x | 370.6 | 0.0% | 0.0% | 0.23% | 0.23% | 2.25% | 0.0% | 0.0% | **99.01** |
| 4b_Recursive_450 | 1.71x | 232.0 | 0.12% | 0.12% | 0.88% | 0.88% | 12.45% | 0.53% | 0.0% | **97.63** |
| 4c_Recursive_1000 | 1.2x | 329.4 | 0.0% | 0.0% | 0.5% | 0.5% | 3.16% | 0.21% | 0.0% | **99.31** |
| 4d_Recursive_250 | 2.61x | 151.2 | 1.26% | 1.22% | 1.51% | 1.51% | 22.58% | 2.1% | 0.0% | **94.97** |
| 5b_Semantic_thr1200_max900 | 1.23x | 336.2 | 0.0% | 0.0% | 0.45% | 0.0% | 4.02% | 0.12% | 0.0% | **99.31** |
| 5c_Semantic_thr500_max400 | 1.75x | 260.0 | 0.28% | 0.26% | 1.05% | 0.0% | 13.16% | 0.37% | 0.0% | **97.67** |
| 5d_Semantic_prefix_all | 1.38x | 310.8 | 0.04% | 0.04% | 0.54% | 0.0% | 7.25% | 0.25% | 0.0% | **98.77** |
| 5e_Adaptive_Hybrid | 1.3x | 322.2 | 0.04% | 0.04% | 0.27% | 0.0% | 5.22% | 0.35% | 0.0% | **99.05** |
| 8b_Sentence_Window_6_3 | 2.35x | 265.7 | 0.0% | 0.0% | 1.68% | 1.68% | 21.62% | 1.87% | 0.0% | **95.67** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 85 gold + 9981 nhiễu | 99 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.2880 | 0.3796 | 0.2698 | +0.1098 🔼 | **0.3978** | 0.4257 | 0.3674 | 0.5381 | 0.3513 | 15990 |
| 2_Fixed_Word | 0.2992 | 0.4332 | 0.2921 | +0.1411 🔼 | **0.4403** | 0.4937 | 0.3935 | 0.6004 | 0.4060 | 12690 |
| 3_Sentence_Boundary | 0.2841 | 0.4161 | 0.2644 | +0.1517 🔼 | **0.4358** | 0.4554 | 0.3910 | 0.5684 | 0.3896 | 12117 |
| 4_Recursive_Markdown | 0.3204 | 0.4190 | 0.3008 | +0.1182 🔼 | **0.4386** | 0.4432 | 0.4444 | 0.5696 | 0.3937 | 14405 |
| 5_Semantic_Context_Injected | 0.3189 | 0.4336 | 0.2944 | +0.1392 🔼 | **0.4581** | 0.4775 | 0.4129 | 0.5572 | 0.4136 | 14203 |
| 6_Whole_Document | 0.2474 | 0.3980 | 0.2356 | +0.1624 🔼 | **0.4098** | 0.4192 | 0.3523 | 0.5367 | 0.3664 | 10066 |
| 7_Parent_Child | 0.3117 | 0.4043 | 0.2920 | +0.1123 🔼 | **0.4240** | 0.4721 | 0.3969 | 0.5549 | 0.3741 | 16485 |
| 8_Sentence_Window | 0.2773 | 0.3552 | 0.2554 | +0.0998 🔼 | **0.3771** | 0.4029 | 0.4007 | 0.5328 | 0.3095 | 34155 |
| 9_TextTiling_Semantic | 0.2426 | 0.3487 | 0.2185 | +0.1302 🔼 | **0.3728** | 0.3507 | 0.3712 | 0.4630 | 0.3315 | 20054 |
| 1b_Fixed_Char_300 | 0.3059 | 0.3688 | 0.2839 | +0.0849 🔼 | **0.3908** | 0.3921 | 0.3851 | 0.5058 | 0.3448 | 21507 |
| 1c_Fixed_Char_900 | 0.2878 | 0.4250 | 0.2838 | +0.1412 🔼 | **0.4290** | 0.5031 | 0.4179 | 0.5776 | 0.3944 | 12680 |
| 3b_Sentence_80w | 0.2983 | 0.4041 | 0.2899 | +0.1142 🔼 | **0.4125** | 0.4616 | 0.4040 | 0.5727 | 0.3727 | 15029 |
| 3c_Sentence_220w | 0.2678 | 0.4172 | 0.2541 | +0.1631 🔼 | **0.4309** | 0.4699 | 0.3826 | 0.5476 | 0.3970 | 11043 |
| 4b_Recursive_450 | 0.2782 | 0.4123 | 0.2364 | +0.1759 🔼 | **0.4541** | 0.4656 | 0.4019 | 0.5482 | 0.3887 | 17717 |
| 4c_Recursive_1000 | 0.3049 | 0.4377 | 0.2926 | +0.1451 🔼 | **0.4500** | 0.4302 | 0.4230 | 0.5962 | 0.4063 | 12385 |
| 4d_Recursive_250 | 0.2487 | 0.3742 | 0.2492 | +0.1250 🔼 | **0.3737** | 0.4123 | 0.3582 | 0.4712 | 0.3580 | 27376 |
| 5b_Semantic_thr1200_max900 | 0.3025 | 0.4253 | 0.2859 | +0.1394 🔼 | **0.4419** | 0.4312 | 0.4099 | 0.5551 | 0.4056 | 12611 |
| 5c_Semantic_thr500_max400 | 0.2976 | 0.3900 | 0.2788 | +0.1112 🔼 | **0.4088** | 0.4458 | 0.4045 | 0.5204 | 0.3629 | 18248 |
| 5d_Semantic_prefix_all | 0.3189 | 0.4336 | 0.3144 | +0.1192 🔼 | **0.4381** | 0.4775 | 0.4129 | 0.5572 | 0.4136 | 14203 |
| 5e_Adaptive_Hybrid | 0.3124 | 0.4184 | 0.2985 | +0.1199 🔼 | **0.4323** | 0.4264 | 0.4280 | 0.5549 | 0.3953 | 13380 |
| 8b_Sentence_Window_6_3 | 0.2830 | 0.3840 | 0.2608 | +0.1232 🔼 | **0.4062** | 0.4133 | 0.3876 | 0.5297 | 0.3534 | 24431 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 4c_Recursive_1000 | **0.9286** | 0.9286 | 0.000 |
| 2 | 5_Semantic_Context_Injected | **0.8970** | 0.8970 | 0.000 |
| 3 | 4_Recursive_Markdown | **0.8358** | 0.8358 | 0.000 |
| 4 | 5b_Semantic_thr1200_max900 | **0.8256** | 0.8256 | 0.000 |
| 5 | 4b_Recursive_450 | **0.8226** | 0.8226 | 0.000 |
| 6 | 5d_Semantic_prefix_all | **0.7914** | 0.7914 | 0.000 |
| 7 | 3_Sentence_Boundary | **0.7901** | 0.7901 | 0.000 |
| 8 | 5e_Adaptive_Hybrid | **0.7841** | 0.7841 | 0.000 |
| 9 | 2_Fixed_Word | **0.7693** | 0.7693 | 0.000 |
| 10 | 3c_Sentence_220w | **0.7445** | 0.7445 | 0.000 |
| 11 | 1c_Fixed_Char_900 | **0.7062** | 0.7062 | 0.000 |
| 12 | 7_Parent_Child | **0.6665** | 0.6665 | 0.000 |
| 13 | 3b_Sentence_80w | **0.6490** | 0.6490 | 0.000 |
| 14 | 6_Whole_Document | **0.6080** | 0.6080 | 0.000 |
| 15 | 5c_Semantic_thr500_max400 | **0.5559** | 0.5559 | 0.000 |

**Chiến lược được chọn: `4c_Recursive_1000`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `finger_motion/31194345_112.txt` — 14 ký tự

```text
2022 Sep 12  .
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 13c ✅ — *"2022 Sep 12 ."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 14c ✅ — *"2022 Sep 12  ."*

---

### `tipoftoungue/mymemorybooksreadinglist_33.txt` — 133 ký tự

```text
I've read only the first two books you mentioned by O'Brien, O'Brien's first
book (no longer published)s and a book by Harry Lorayne.
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 133c ✅ — *"I've read only the first two books you mentioned by O'Brien, O'Brien's first book (no longer published)s and a book by Harry Lorayne."*

---

### `focus_testing/NBK305233_151.txt` — 1457 ký tự

```text
The use of psychological tests in disability determinations has critical
implications for clients. As noted earlier, issues surrounding ecological
validity (i.e., whether test performance accurately reflects real-world
behavior) is of primary importance in SSA determination. Two approaches have
been identified in relation to the ecological validity of neuropsychological
assessment. The first focuses on “how well the test captures the essence of
everyday cognitive skills” in order to “identify pe...
```

- **1_Fixed_Char** (4 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"veryday cognitive skills” in order to “identify people who have difficulty performing real-world tasks, regardless of the etiology of the pr..."*
  - `[2]` 499c ⚠ starts_mid_sentence, ends_mid_sentence — *"cal validity is a complicated endeavor given the potential effect of non-cognitive factors (e.g., emotional, physical, and environmental) on..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (2 chunks)
  - `[0]` 913c ⚠ ends_mid_sentence — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
  - `[1]` 711c ⚠ starts_mid_sentence — *"employment status, questionnaires, or clinician ratings” (i.e., veridicality) ( Chaytor and Schmitter-Edgecombe, 2003 , pp. 182–183). Establ..."*
- **3_Sentence_Boundary** (2 chunks)
  - `[0]` 1071c ✅ — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
  - `[1]` 411c ⚠ starts_with_connector — *"and everyday performance. Specific concerns regarding test performance include (1) the test environment is often not representative (i.e., a..."*
- **4_Recursive_Markdown** (3 chunks)
  - `[0]` 524c ⚠ trailing_heading_orphan — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
  - `[1]` 520c ⚠ trailing_heading_orphan — *"performing real-world tasks, regardless of the etiology of the problem” (i.e., verisimilitude), and the second “relates performance on tradi..."*
  - `[2]` 411c ⚠ starts_with_connector — *"and everyday performance. Specific concerns regarding test performance include (1) the test environment is often not representative (i.e., a..."*
- **5_Semantic_Context_Injected** (3 chunks)
  - `[0]` 524c ⚠ trailing_heading_orphan — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
  - `[1]` 611c ⚠ trailing_heading_orphan — *"[Document Topic: The use of psychological tests in disability determinations has critical] performing real-world tasks, regardless of the et..."*
  - `[2]` 502c ⚠ starts_with_connector — *"[Document Topic: The use of psychological tests in disability determinations has critical] and everyday performance. Specific concerns regar..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 1457c ✅ — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
- **7_Parent_Child** (4 chunks)
  - `[0]` 384c ✅ — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
  - `[1]` 436c ✅ — *"The first focuses on “how well the test captures the essence of everyday cognitive skills” in order to “identify people who have difficulty ..."*
  - `[2]` 451c ⚠ trailing_heading_orphan — *"(  Chaytor and Schmitter-Edgecombe, 2003  , pp. 182–183). Establishing ecological validity is a complicated endeavor given the potential eff..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (12 chunks)
  - `[0]` 218c ⚠ trailing_heading_orphan — *"The use of psychological tests in disability determinations has critical implications for clients. As noted earlier, issues surrounding ecol..."*
  - `[1]` 196c ⚠ trailing_heading_orphan — *"As noted earlier, issues surrounding ecological validity (i.e., whether test performance accurately reflects real-world behavior) is of prim..."*
  - `[2]` 165c ✅ — *"behavior) is of primary importance in SSA determination. Two approaches have been identified in relation to the ecological validity of neuro..."*
  - *(... 9 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (7 chunks)
  - `[0]` 98c ✅ — *"The use of psychological tests in disability determinations has critical implications for clients."*
  - `[1]` 273c ⚠ trailing_heading_orphan — *"As noted earlier, issues surrounding ecological validity (i.e., whether test performance accurately reflects real-world behavior) is of prim..."*
  - `[2]` 75c ⚠ undersized — *"assessment. The first focuses on “how well the test captures the essence of"*
  - *(... 4 chunk nữa — xem chunk_inspection)*

---

### `polarization/Racialsegregation_220.txt` — 42292 ký tự

```text
1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5–19. [ CiteSeerX ](/wiki/CiteSeerX_\(identifier\) "CiteSeerX \(identifier\)") [ 10.1.1.536.5952 ](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.536.5952) .
2. ** ^  ** [ "ECRI General Policy Recommendation N°7: National legislation to combat racism and racial discrimination — Explanatory memorandum, Para. 16" ](http://www.coe.int/t/dghl/monitoring...
```

- **1_Fixed_Char** (94 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
  - `[1]` 500c ⚠ starts_mid_sentence — *", Para. 16" ](http://www.coe.int/t/dghl/monitoring/ecri/activities/GPR/EN/Recommendation_N7/Recommendation_7_en.asp) . 3. ** ^  ** [ "Recomm..."*
  - `[2]` 499c ⚠ ends_mid_sentence — *"28 August 2023. 5. ^  _**a** _ _**b** _ Edward H. Schafer (1963). [ _The golden peaches of Samarkand: a study of Tʻang exotics_ ](https://bo..."*
  - *(... 91 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (48 chunks)
  - `[0]` 1230c ✅ — *"1. ** ^ ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5–..."*
  - `[1]` 1350c ✅ — *"Schafer (1963). [ _The golden peaches of Samarkand: a study of Tʻang exotics_ ](https://books.google.com/books?id=jqAGIL02BWQC&q=chinese+uig..."*
  - `[2]` 1261c ⚠ starts_mid_sentence, ends_mid_sentence — *"\(identifier\)") [ 978-0-521-49781-7 ](/wiki/Special:BookSources/978-0-521-49781-7 "Special:BookSources/978-0-521-49781-7") . Retrieved 28 O..."*
  - *(... 45 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (38 chunks)
  - `[0]` 1436c ✅ — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
  - `[1]` 1361c ✅ — *"Retrieved  28 June  2010  . 6. ** ^  ** Mark Edward Lewis (2009). [ _China's cosmopolitan empire: the Tang dynasty_ ](https://books.google.c..."*
  - `[2]` 1389c ✅ — *"79. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 9780029336809  ](/wiki/Special:BookSources/9780029336809 "Special:BookSource..."*
  - *(... 35 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (86 chunks)
  - `[0]` 568c ✅ — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
  - `[1]` 347c ✅ — *"3. ** ^  ** [ "Recommendations of the Forum on Minority Issues A/HRC/10/11/Add.1 — para. 27" ](http://www2.ohchr.org/english/bodies/hrcounci..."*
  - `[2]` 519c ✅ — *"5. ^  _**a** _ _**b** _ Edward H. Schafer (1963). [ _The golden peaches of Samarkand: a study of Tʻang exotics_ ](https://books.google.com/b..."*
  - *(... 83 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (86 chunks)
  - `[0]` 568c ✅ — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
  - `[1]` 416c ✅ — *"[Document Topic: 1. ** ^ ** Schill, Michael; Wachter, Susan (2001).] 3. ** ^  ** [ "Recommendations of the Forum on Minority Issues A/HRC/10..."*
  - `[2]` 588c ✅ — *"[Document Topic: 1. ** ^ ** Schill, Michael; Wachter, Susan (2001).] 5. ^  _**a** _ _**b** _ Edward H. Schafer (1963). [ _The golden peaches..."*
  - *(... 83 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 42292c ⚠ over_embedding_token_limit — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
- **7_Parent_Child** (90 chunks)
  - `[0]` 568c ✅ — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
  - `[1]` 632c ✅ — *"3. ** ^  ** [ "Recommendations of the Forum on Minority Issues A/HRC/10/11/Add.1 — para. 27" ](http://www2.ohchr.org/english/bodies/hrcounci..."*
  - `[2]` 639c ✅ — *"University of California Press. p. 22. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 978-0-520-05462-2  ](/wiki/Special:BookSo..."*
  - *(... 87 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (281 chunks)
  - `[0]` 457c ✅ — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
  - `[1]` 512c ✅ — *"[ CiteSeerX ](/wiki/CiteSeerX_\(identifier\) "CiteSeerX \(identifier\)") [ 10.1.1.536.5952 ](https://citeseerx.ist.psu.edu/viewdoc/summary?d..."*
  - `[2]` 442c ✅ — *"16" ](http://www.coe.int/t/dghl/monitoring/ecri/activities/GPR/EN/Recommendation_N7/Recommendation_7_en.asp) . 3. ** ^  ** [ "Recommendation..."*
  - *(... 278 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (135 chunks)
  - `[0]` 900c ✅ — *"1. ** ^  ** Schill, Michael; Wachter, Susan (2001). "Principles to Guide Housing Policy at the Beginning of the Millennium". _Cityscape_ : 5..."*
  - `[1]` 65c ⚠ undersized — *"28 August 2023. 5. ^  _**a** _ _**b** _ Edward H. Schafer (1963)."*
  - `[2]` 269c ✅ — *"[ _The golden peaches of Samarkand: a study of Tʻang exotics_ ](https://books.google.com/books?id=jqAGIL02BWQC&q=chinese+uighurs+779+edict+l..."*
  - *(... 132 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunking_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.