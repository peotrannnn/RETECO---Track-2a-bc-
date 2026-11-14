# Báo cáo EDA & đánh giá Chunking — domain `biology`

*Tạo lúc 2026-11-14 12:21:51 | RETECO Track 2 (v3)*

## 1. Corpus

- Tổng tài liệu: **57,359** | schema: `content, doc_id`
- Ký tự: min=1, p25=104, **median=309**, mean=329.6, p75=519, p90=606, p95=643, p99=711, max=31131
- Từ: median=40, mean=47.5, max=4780
- Ước tính vượt 512 token: **0.23%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 24.47% |
| 101-300 | 24.46% |
| 301-650 | 46.82% |
| 651-800 | 3.73% |
| 801-1500 | 0.15% |
| 1501-3000 | 0.17% |
| 3001-6000 | 0.12% |
| >6000 | 0.07% |

- Cấu trúc: header 9.55% | bullet 16.75% | code 0.15% | URL 12.68% | nhiều dòng 57.06%
- Chất lượng dữ liệu: trùng 13.82% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 29.31% | thiếu dấu câu cuối 66.96% | mở đầu bằng đại từ 1.29%

## 2. Hội thoại Track 2

- Hội thoại: **26** | lượt: **115** | lượt có gold: 115
- Lượt/hội thoại: mean=4.42 (min 3, max 11)
- Độ dài query: mean=16.2 từ, median=16, max=24
- Gold docs/lượt: mean=1.7, max=7
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 1.32x | 267.7 | 23.6% | 23.52% | 0.61% | 0.61% | 0.0% | 3.34% | 0.0% | **88.35** |
| **2_Fixed_Word** | 1.03x | 329.9 | 2.44% | 2.44% | 0.1% | 0.1% | 0.0% | 0.0% | 0.0% | **98.86** |
| **3_Sentence_Boundary** | 1.02x | 330.6 | 0.0% | 0.0% | 0.34% | 0.34% | 0.0% | 0.0% | 0.0% | **99.89** |
| **4_Recursive_Markdown** | 1.05x | 320.7 | 0.0% | 0.05% | 0.38% | 0.38% | 0.05% | 0.1% | 0.0% | **99.83** |
| **5_Semantic_Context_Injected** | 1.04x | 329.3 | 0.0% | 0.0% | 0.24% | 0.0% | 0.05% | 0.0% | 0.0% | **99.96** |
| **6_Whole_Document** | 1.0x | 337.1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.15% | **99.94** |
| **7_Parent_Child** | 1.46x | 230.1 | 0.1% | 0.27% | 3.05% | 3.05% | 2.51% | 2.95% | 0.0% | **97.76** |
| **8_Sentence_Window** | 2.14x | 220.0 | 0.02% | 0.05% | 2.18% | 2.18% | 15.67% | 10.6% | 0.0% | **94.25** |
| **9_TextTiling_Semantic** | 1.42x | 237.0 | 0.0% | 0.0% | 1.38% | 1.38% | 8.79% | 14.9% | 0.0% | **94.5** |
| 1b_Fixed_Char_300 | 1.75x | 204.9 | 41.66% | 41.27% | 0.77% | 0.77% | 0.26% | 9.18% | 0.0% | **78.72** |
| 1c_Fixed_Char_900 | 1.02x | 332.1 | 1.91% | 1.96% | 0.05% | 0.05% | 0.0% | 0.0% | 0.0% | **99.12** |
| 3b_Sentence_80w | 1.32x | 283.7 | 0.0% | 0.04% | 2.98% | 2.98% | 1.21% | 0.53% | 0.0% | **98.69** |
| 3c_Sentence_220w | 1.01x | 332.8 | 0.0% | 0.0% | 0.3% | 0.3% | 0.0% | 0.0% | 0.0% | **99.9** |
| 4b_Recursive_450 | 1.37x | 246.4 | 0.51% | 0.51% | 2.01% | 2.01% | 2.42% | 1.43% | 0.0% | **98.35** |
| 4c_Recursive_1000 | 1.02x | 330.4 | 0.0% | 0.0% | 0.25% | 0.25% | 0.05% | 0.05% | 0.0% | **99.91** |
| 4d_Recursive_250 | 2.07x | 161.6 | 2.1% | 2.07% | 4.07% | 4.07% | 5.81% | 3.93% | 0.0% | **95.82** |
| 5b_Semantic_thr1200_max900 | 1.02x | 332.0 | 0.0% | 0.0% | 0.24% | 0.0% | 0.0% | 0.0% | 0.0% | **99.98** |
| 5c_Semantic_thr500_max400 | 1.35x | 274.3 | 0.52% | 0.63% | 2.19% | 0.0% | 1.67% | 1.74% | 0.0% | **98.8** |
| 5d_Semantic_prefix_all | 1.04x | 329.6 | 0.0% | 0.0% | 0.24% | 0.0% | 0.05% | 0.0% | 0.0% | **99.96** |
| 5e_Adaptive_Hybrid | 1.03x | 330.7 | 0.0% | 0.0% | 0.19% | 0.0% | 0.05% | 0.05% | 0.0% | **99.96** |
| 8b_Sentence_Window_6_3 | 1.49x | 273.3 | 0.07% | 0.07% | 0.98% | 0.98% | 10.76% | 4.57% | 0.0% | **96.86** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 78 gold + 9982 nhiễu | 115 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.3186 | 0.4413 | 0.2743 | +0.1670 🔼 | **0.4856** | 0.4816 | 0.4881 | 0.5716 | 0.4345 | 13640 |
| 2_Fixed_Word | 0.3221 | 0.4497 | 0.2702 | +0.1795 🔼 | **0.5016** | 0.4713 | 0.4555 | 0.5880 | 0.4426 | 10598 |
| 3_Sentence_Boundary | 0.3079 | 0.4540 | 0.2613 | +0.1927 🔼 | **0.5006** | 0.4843 | 0.4222 | 0.5612 | 0.4596 | 10546 |
| 4_Recursive_Markdown | 0.3431 | 0.4701 | 0.3087 | +0.1614 🔼 | **0.5045** | 0.5062 | 0.5034 | 0.6141 | 0.4453 | 10981 |
| 5_Semantic_Context_Injected | 0.3394 | 0.4477 | 0.2974 | +0.1503 🔼 | **0.4897** | 0.4859 | 0.4990 | 0.5822 | 0.4254 | 10799 |
| 6_Whole_Document | 0.1927 | 0.3749 | 0.1606 | +0.2143 🔼 | **0.4070** | 0.4560 | 0.3267 | 0.5666 | 0.3400 | 10060 |
| 7_Parent_Child | 0.3229 | 0.4314 | 0.2865 | +0.1449 🔼 | **0.4678** | 0.4419 | 0.4715 | 0.5713 | 0.4100 | 15148 |
| 8_Sentence_Window | 0.3091 | 0.4647 | 0.2671 | +0.1976 🔼 | **0.5067** | 0.4504 | 0.4583 | 0.5742 | 0.4706 | 21816 |
| 9_TextTiling_Semantic | 0.2835 | 0.4516 | 0.2492 | +0.2024 🔼 | **0.4859** | 0.4548 | 0.4033 | 0.5764 | 0.4410 | 14427 |
| 1b_Fixed_Char_300 | 0.3224 | 0.4250 | 0.2797 | +0.1453 🔼 | **0.4677** | 0.4352 | 0.4519 | 0.5528 | 0.4243 | 18153 |
| 1c_Fixed_Char_900 | 0.3085 | 0.4450 | 0.2687 | +0.1763 🔼 | **0.4848** | 0.4802 | 0.4268 | 0.5864 | 0.4363 | 10497 |
| 3b_Sentence_80w | 0.3402 | 0.4563 | 0.2856 | +0.1707 🔼 | **0.5109** | 0.4799 | 0.4877 | 0.5903 | 0.4428 | 13827 |
| 3c_Sentence_220w | 0.2957 | 0.4546 | 0.2648 | +0.1898 🔼 | **0.4855** | 0.5176 | 0.4164 | 0.5984 | 0.4365 | 10312 |
| 4b_Recursive_450 | 0.3108 | 0.4413 | 0.2717 | +0.1696 🔼 | **0.4804** | 0.4480 | 0.4601 | 0.5505 | 0.4398 | 14254 |
| 4c_Recursive_1000 | 0.3248 | 0.4561 | 0.2887 | +0.1674 🔼 | **0.4922** | 0.4955 | 0.4642 | 0.5847 | 0.4515 | 10500 |
| 4d_Recursive_250 | 0.3086 | 0.4285 | 0.2742 | +0.1543 🔼 | **0.4629** | 0.4686 | 0.4434 | 0.5484 | 0.4227 | 21741 |
| 5b_Semantic_thr1200_max900 | 0.3175 | 0.4615 | 0.2704 | +0.1911 🔼 | **0.5086** | 0.4908 | 0.4567 | 0.5989 | 0.4482 | 10556 |
| 5c_Semantic_thr500_max400 | 0.3273 | 0.4469 | 0.2909 | +0.1560 🔼 | **0.4833** | 0.4838 | 0.4670 | 0.5730 | 0.4392 | 14123 |
| 5d_Semantic_prefix_all | 0.3396 | 0.4461 | 0.2922 | +0.1539 🔼 | **0.4935** | 0.4772 | 0.4990 | 0.5822 | 0.4236 | 10799 |
| 5e_Adaptive_Hybrid | 0.3181 | 0.4503 | 0.2856 | +0.1647 🔼 | **0.4828** | 0.4589 | 0.4664 | 0.5909 | 0.4301 | 10676 |
| 8b_Sentence_Window_6_3 | 0.2992 | 0.4512 | 0.2571 | +0.1941 🔼 | **0.4933** | 0.4682 | 0.4338 | 0.5782 | 0.4514 | 15293 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 4_Recursive_Markdown | **0.9598** | 0.9598 | 0.000 |
| 2 | 5b_Semantic_thr1200_max900 | **0.9304** | 0.9304 | 0.000 |
| 3 | 3b_Sentence_80w | **0.8994** | 0.8994 | 0.000 |
| 4 | 5d_Semantic_prefix_all | **0.8834** | 0.8834 | 0.000 |
| 5 | 2_Fixed_Word | **0.8739** | 0.8739 | 0.000 |
| 6 | 5_Semantic_Context_Injected | **0.8669** | 0.8669 | 0.000 |
| 7 | 4c_Recursive_1000 | **0.8525** | 0.8525 | 0.000 |
| 8 | 3_Sentence_Boundary | **0.8303** | 0.8303 | 0.000 |
| 9 | 5e_Adaptive_Hybrid | **0.8177** | 0.8177 | 0.000 |
| 10 | 3c_Sentence_220w | **0.7952** | 0.7952 | 0.000 |
| 11 | 1c_Fixed_Char_900 | **0.7794** | 0.7794 | 0.000 |
| 12 | 5c_Semantic_thr500_max400 | **0.7441** | 0.7441 | 0.000 |
| 13 | 8_Sentence_Window | **0.7386** | 0.7386 | 0.000 |
| 14 | 8b_Sentence_Window_6_3 | **0.7271** | 0.7271 | 0.000 |
| 15 | 4b_Recursive_450 | **0.6980** | 0.6980 | 0.000 |

**Chiến lược được chọn: `4_Recursive_Markdown`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `immune_system_detect_tumor/11582immunotherapy_63_0.txt` — 31 ký tự

```text
#####  How cancer vaccines work
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 30c ✅ — *"##### How cancer vaccines work"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*
- **6_Whole_Document** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*
- **7_Parent_Child** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 31c ✅ — *"#####  How cancer vaccines work"*

---

### `fast_asleep/Cellstatetransitions_34_5.txt` — 322 ký tự

```text
2021.03.24.436752
Google Scholar
Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a fluorescent group. Exp. Biol. Med. 47, 200-202. https://doi.org/10.3181/00379727-47-13084P
Google ScholarCrossref
Corominas-Murtra, B., Scheele, C. L. G. J., Kishi, K., Ellenbroek, S.
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*
- **8_Sentence_Window** (8 chunks)
  - `[0]` 57c ⚠ undersized — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H."*
  - `[1]` 44c ⚠ undersized — *"Coons, A. H., Creech, H. J. and Jones, R. N."*
  - `[2]` 99c ✅ — *"J. and Jones, R. N. (1941). Immunological properties of an antibody containing a fluorescent group."*
  - *(... 5 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 322c ✅ — *"2021.03.24.436752 Google Scholar Coons, A. H., Creech, H. J. and Jones, R. N. (1941). Immunological properties of an antibody containing a f..."*

---

### `human_monogamy/Human_4_68.txt` — 637 ký tự

```text
dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is prominently reflected in human culture and has led to the development of food science. Until the development of agriculture, Homo sapiens employed a hunter-gatherer method as their sole means of food collection. This involved combining stationary food sources (such as fruits, grains, tubers, and mushrooms, insect larvae and aquatic mollusks) with wild game, ...
```

- **1_Fixed_Char** (2 chunks)
  - `[0]` 499c ⚠ ends_mid_sentence — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
  - `[1]` 187c ⚠ starts_mid_sentence — *"sect larvae and aquatic mollusks) with wild game, which must be hunted and captured in order to be consumed. It has been proposed that human..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 637c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 637c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 637c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 637c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 637c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
- **7_Parent_Child** (2 chunks)
  - `[0]` 351c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
  - `[1]` 285c ⚠ dangling_pronoun — *"This involved combining stationary food sources (such as fruits, grains, tubers, and mushrooms, insect larvae and aquatic mollusks) with wil..."*
- **8_Sentence_Window** (2 chunks)
  - `[0]` 558c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*
  - `[1]` 410c ✅ — *"Until the development of agriculture, Homo sapiens employed a hunter-gatherer method as their sole means of food collection. This involved c..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 637c ✅ — *"dietary patterns through both genetic specialization and cultural conventions to use nutritionally balanced food sources. The human diet is ..."*

---

### `baby_memories/Mirror_test_0.txt` — 15815 ký tự

```text
The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral technique developed in 1970 by American psychologist Gordon Gallup Jr. as an attempt to determine whether an animal possesses the ability of visual self-recognition. The MSR test is the traditional method for attempting to measure physiological and cognitive self-awareness. However, agreement has been reached that animals can be self-aware in ways not measured by ...
```

- **1_Fixed_Char** (36 chunks)
  - `[0]` 499c ⚠ ends_mid_sentence — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"animals can be self-aware in ways not measured by the mirror test, such as distinguishing between their own and others' songs and scents, an..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"rom the anesthetic, it is given access to a mirror. If the animal then touches or investigates the mark, it is taken as an indication that t..."*
  - *(... 33 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (26 chunks)
  - `[0]` 784c ✅ — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 692c ⚠ starts_mid_sentence, ends_mid_sentence, starts_with_connector — *"and thus intelligence that is highly visual. In the classic MSR test, an animal is anesthetized and then marked (e.g. paint or sticker) on a..."*
  - `[2]` 763c ⚠ starts_mid_sentence, ends_mid_sentence — *"elephant, Giant oceanic manta rays, dolphins, orcas, the Eurasian magpie, and the cleaner wrasse. A wide range of species has been reported ..."*
  - *(... 23 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (23 chunks)
  - `[0]` 873c ✅ — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 746c ✅ — *"In the classic MSR test, an animal is anesthetized and then marked (e.g. paint or sticker) on an area of the body the animal normally cannot..."*
  - `[2]` 854c ✅ — *"A wide range of species has been reported to fail the test, including several species of monkeys, giant pandas, and sea lions. The inspirati..."*
  - *(... 20 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (33 chunks)
  - `[0]` 408c ✅ — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 302c ⚠ starts_with_connector — *"However, agreement has been reached that animals can be self-aware in ways not measured by the mirror test, such as distinguishing between t..."*
  - `[2]` 421c ✅ — *"In the classic MSR test, an animal is anesthetized and then marked (e.g. paint or sticker) on an area of the body the animal normally cannot..."*
  - *(... 30 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (33 chunks)
  - `[0]` 408c ✅ — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 434c ⚠ starts_with_connector — *"[Document Topic: The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge…] However,..."*
  - `[2]` 553c ✅ — *"[Document Topic: The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge…] In the c..."*
  - *(... 30 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 15815c ⚠ over_embedding_token_limit — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
- **7_Parent_Child** (54 chunks)
  - `[0]` 408c ✅ — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 302c ⚠ starts_with_connector — *"However, agreement has been reached that animals can be self-aware in ways not measured by the mirror test, such as distinguishing between t..."*
  - `[2]` 239c ✅ — *"In the classic MSR test, an animal is anesthetized and then marked (e.g. paint or sticker) on an area of the body the animal normally cannot..."*
  - *(... 51 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (64 chunks)
  - `[0]` 873c ✅ — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 724c ⚠ starts_with_connector — *"However, agreement has been reached that animals can be self-aware in ways not measured by the mirror test, such as distinguishing between t..."*
  - `[2]` 457c ✅ — *"When the animal recovers from the anesthetic, it is given access to a mirror. If the animal then touches or investigates the mark, it is tak..."*
  - *(... 61 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (29 chunks)
  - `[0]` 711c ✅ — *"The mirror test—sometimes called the mark test, mirror self-recognition (MSR) test, red spot technique, or rouge test—is a behavioral techni..."*
  - `[1]` 421c ✅ — *"In the classic MSR test, an animal is anesthetized and then marked (e.g. paint or sticker) on an area of the body the animal normally cannot..."*
  - `[2]` 324c ✅ — *"Very few species have passed the MSR test. Species that have include the great apes, a single Asian elephant, Giant oceanic manta rays, dolp..."*
  - *(... 26 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunk_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.