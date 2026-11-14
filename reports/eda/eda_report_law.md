# Báo cáo EDA & đánh giá Chunking — domain `law`

*Tạo lúc 2026-11-14 12:25:49 | RETECO Track 2 (v3)*

## 1. Corpus

- Tổng tài liệu: **20,027** | schema: `content, doc_id`
- Ký tự: min=30, p25=338, **median=791**, mean=997.4, p75=1634, p90=1998, p95=2414, p99=2868, max=12902
- Từ: median=123, mean=156.2, max=1803
- Ước tính vượt 512 token: **4.94%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 5.38% |
| 101-300 | 16.8% |
| 301-650 | 21.28% |
| 651-800 | 6.98% |
| 801-1500 | 21.67% |
| 1501-3000 | 27.82% |
| 3001-6000 | 0.05% |
| >6000 | 0.02% |

- Cấu trúc: header 0.01% | bullet 1.92% | code 0.0% | URL 2.66% | nhiều dòng 11.93%
- Chất lượng dữ liệu: trùng 0.0% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 1.08% | thiếu dấu câu cuối 14.11% | mở đầu bằng đại từ 3.51%

## 2. Hội thoại Track 2

- Hội thoại: **15** | lượt: **66** | lượt có gold: 66
- Lượt/hội thoại: mean=4.4 (min 3, max 7)
- Độ dài query: mean=19.1 từ, median=19, max=27
- Gold docs/lượt: mean=2.2, max=6
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 2.69x | 406.4 | 60.95% | 60.62% | 1.47% | 1.47% | 0.17% | 2.1% | 0.0% | **71.57** |
| **2_Fixed_Word** | 1.96x | 576.7 | 45.55% | 46.01% | 1.5% | 1.5% | 0.0% | 0.0% | 0.0% | **78.78** |
| **3_Sentence_Boundary** | 1.85x | 609.6 | 0.0% | 0.0% | 3.38% | 3.38% | 2.75% | 0.32% | 0.0% | **98.29** |
| **4_Recursive_Markdown** | 2.17x | 464.2 | 1.49% | 1.47% | 3.4% | 3.4% | 3.72% | 0.11% | 0.0% | **97.48** |
| **5_Semantic_Context_Injected** | 2.13x | 535.4 | 1.5% | 1.48% | 3.28% | 0.02% | 3.8% | 0.12% | 0.0% | **98.22** |
| **6_Whole_Document** | 1.0x | 1010.7 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 4.75% | **96.69** |
| **7_Parent_Child** | 3.44x | 293.3 | 0.04% | 0.0% | 5.8% | 5.8% | 4.65% | 2.09% | 0.0% | **96.7** |
| **8_Sentence_Window** | 4.6x | 340.3 | 0.01% | 0.0% | 3.19% | 3.19% | 21.87% | 22.52% | 0.05% | **89.88** |
| **9_TextTiling_Semantic** | 2.8x | 364.7 | 0.11% | 0.05% | 2.7% | 2.7% | 13.39% | 20.2% | 0.0% | **91.89** |
| 1b_Fixed_Char_300 | 4.15x | 265.9 | 73.77% | 73.92% | 1.72% | 1.72% | 0.26% | 4.23% | 0.0% | **65.06** |
| 1c_Fixed_Char_900 | 1.75x | 616.8 | 41.6% | 41.63% | 1.29% | 1.29% | 0.31% | 0.0% | 0.0% | **80.77** |
| 3b_Sentence_80w | 3.23x | 386.9 | 0.06% | 0.0% | 5.54% | 5.54% | 4.05% | 1.28% | 0.0% | **97.1** |
| 3c_Sentence_220w | 1.35x | 786.8 | 0.0% | 0.0% | 1.96% | 1.96% | 2.26% | 0.15% | 0.0% | **98.76** |
| 4b_Recursive_450 | 3.06x | 329.5 | 3.61% | 3.58% | 5.08% | 5.08% | 4.13% | 0.36% | 0.0% | **95.87** |
| 4c_Recursive_1000 | 1.56x | 645.5 | 0.51% | 0.51% | 2.14% | 2.14% | 3.0% | 0.0% | 0.0% | **98.55** |
| 4d_Recursive_250 | 5.32x | 189.2 | 10.64% | 10.6% | 5.99% | 5.99% | 3.85% | 3.32% | 0.0% | **91.63** |
| 5b_Semantic_thr1200_max900 | 1.64x | 662.0 | 0.79% | 0.76% | 2.38% | 0.03% | 3.57% | 0.03% | 0.0% | **98.72** |
| 5c_Semantic_thr500_max400 | 3.27x | 389.7 | 3.82% | 3.78% | 4.95% | 0.05% | 4.05% | 0.5% | 0.0% | **96.84** |
| 5d_Semantic_prefix_all | 2.13x | 537.4 | 1.5% | 1.48% | 3.28% | 0.02% | 3.8% | 0.12% | 0.0% | **98.22** |
| 5e_Adaptive_Hybrid | 1.88x | 591.9 | 1.04% | 1.04% | 3.11% | 0.05% | 3.96% | 0.11% | 0.0% | **98.49** |
| 8b_Sentence_Window_6_3 | 3.1x | 465.7 | 0.02% | 0.0% | 2.71% | 2.71% | 20.76% | 12.16% | 0.1% | **92.73** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 61 gold + 9969 nhiễu | 66 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.2014 | 0.2746 | 0.1828 | +0.0918 🔼 | **0.2932** | 0.3061 | 0.3414 | 0.4417 | 0.2664 | 26769 |
| 2_Fixed_Word | 0.2066 | 0.2835 | 0.1796 | +0.1039 🔼 | **0.3105** | 0.3045 | 0.3149 | 0.4331 | 0.2811 | 19573 |
| 3_Sentence_Boundary | 0.2285 | 0.3092 | 0.2067 | +0.1025 🔼 | **0.3310** | 0.3311 | 0.3331 | 0.4205 | 0.3337 | 18480 |
| 4_Recursive_Markdown | 0.2034 | 0.2759 | 0.1842 | +0.0917 🔼 | **0.2951** | 0.2889 | 0.3255 | 0.4508 | 0.2762 | 21740 |
| 5_Semantic_Context_Injected | 0.2270 | 0.3091 | 0.2012 | +0.1079 🔼 | **0.3349** | 0.2977 | 0.3545 | 0.4508 | 0.3321 | 21336 |
| 6_Whole_Document | 0.2256 | 0.2934 | 0.1976 | +0.0958 🔼 | **0.3214** | 0.3376 | 0.3578 | 0.4563 | 0.2977 | 10030 |
| 7_Parent_Child | 0.1957 | 0.2811 | 0.1804 | +0.1007 🔼 | **0.2964** | 0.2990 | 0.3106 | 0.4285 | 0.2785 | 34006 |
| 8_Sentence_Window | 0.1546 | 0.2588 | 0.1368 | +0.1220 🔼 | **0.2766** | 0.2889 | 0.2735 | 0.4212 | 0.2460 | 43242 |
| 9_TextTiling_Semantic | 0.1803 | 0.2814 | 0.1723 | +0.1091 🔼 | **0.2894** | 0.3154 | 0.2740 | 0.3876 | 0.2982 | 27023 |
| 1b_Fixed_Char_300 | 0.1986 | 0.2440 | 0.1850 | +0.0590 🔼 | **0.2576** | 0.2391 | 0.3255 | 0.3854 | 0.2520 | 41240 |
| 1c_Fixed_Char_900 | 0.1999 | 0.2818 | 0.1833 | +0.0985 🔼 | **0.2984** | 0.3253 | 0.3508 | 0.4495 | 0.2662 | 17394 |
| 3b_Sentence_80w | 0.1971 | 0.2662 | 0.1793 | +0.0869 🔼 | **0.2840** | 0.3003 | 0.2972 | 0.4184 | 0.2769 | 31923 |
| 3c_Sentence_220w | 0.2074 | 0.2893 | 0.1802 | +0.1091 🔼 | **0.3165** | 0.3146 | 0.3490 | 0.4722 | 0.2743 | 13481 |
| 4b_Recursive_450 | 0.1921 | 0.2764 | 0.1819 | +0.0945 🔼 | **0.2866** | 0.2934 | 0.2942 | 0.4134 | 0.2981 | 30452 |
| 4c_Recursive_1000 | 0.1863 | 0.2762 | 0.1675 | +0.1087 🔼 | **0.2950** | 0.3109 | 0.3056 | 0.4343 | 0.2725 | 15540 |
| 4d_Recursive_250 | 0.1777 | 0.2895 | 0.1692 | +0.1203 🔼 | **0.2980** | 0.3053 | 0.2639 | 0.4404 | 0.2934 | 52937 |
| 5b_Semantic_thr1200_max900 | 0.2171 | 0.3029 | 0.1830 | +0.1199 🔼 | **0.3370** | 0.3242 | 0.3460 | 0.4551 | 0.3098 | 16312 |
| 5c_Semantic_thr500_max400 | 0.2147 | 0.3152 | 0.1898 | +0.1254 🔼 | **0.3401** | 0.3237 | 0.3025 | 0.4513 | 0.3404 | 32454 |
| 5d_Semantic_prefix_all | 0.2268 | 0.3091 | 0.2001 | +0.1090 🔼 | **0.3358** | 0.2977 | 0.3545 | 0.4508 | 0.3321 | 21336 |
| 5e_Adaptive_Hybrid | 0.1921 | 0.2774 | 0.1782 | +0.0992 🔼 | **0.2913** | 0.2985 | 0.3187 | 0.4306 | 0.2930 | 18691 |
| 8b_Sentence_Window_6_3 | 0.1768 | 0.2538 | 0.1485 | +0.1053 🔼 | **0.2821** | 0.2692 | 0.3119 | 0.4073 | 0.2451 | 29286 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 5b_Semantic_thr1200_max900 | **0.9046** | 0.9046 | 0.000 |
| 2 | 5d_Semantic_prefix_all | **0.8837** | 0.8837 | 0.000 |
| 3 | 5_Semantic_Context_Injected | **0.8788** | 0.8788 | 0.000 |
| 4 | 6_Whole_Document | **0.8739** | 0.8739 | 0.000 |
| 5 | 3c_Sentence_220w | **0.8344** | 0.8344 | 0.000 |
| 6 | 5c_Semantic_thr500_max400 | **0.8146** | 0.8146 | 0.000 |
| 7 | 3_Sentence_Boundary | **0.8013** | 0.8013 | 0.000 |
| 8 | 4_Recursive_Markdown | **0.6189** | 0.6189 | 0.000 |
| 9 | 4c_Recursive_1000 | **0.6015** | 0.6015 | 0.000 |
| 10 | 5e_Adaptive_Hybrid | **0.5797** | 0.5797 | 0.000 |
| 11 | 1c_Fixed_Char_900 | **0.5557** | 0.5557 | 0.000 |
| 12 | 7_Parent_Child | **0.5550** | 0.5550 | 0.000 |
| 13 | 2_Fixed_Word | **0.5343** | 0.5343 | 0.000 |
| 14 | 4d_Recursive_250 | **0.4711** | 0.4711 | 0.000 |
| 15 | 3b_Sentence_80w | **0.4631** | 0.4631 | 0.000 |

**Chiến lược được chọn: `5b_Semantic_thr1200_max900`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `law_ex_111040_google_neg_340` — 150 ký tự

```text
Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has been imposed.
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 150c ✅ — *"Final conviction means a conviction, whether entered on a verdict or plea, including a plea of nolo contendere, for which a sentence has bee..."*

---

### `law_ex_108545_google_neg_94` — 812 ký tự

```text
Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, international courts use precedent at least in part to convince ‘lower’ (domestic) courts of the legitimacy of judgements. Several empirical observations are consistent with this view, which are examined through a network analysis of European Court of Human Rights (ECtHR) citations. First, the Court cites precedent based on the legal issues in the case, not the ...
```

- **1_Fixed_Char** (2 chunks)
  - `[0]` 499c ⚠ ends_mid_sentence — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
  - `[1]` 362c ⚠ starts_mid_sentence — *"nt based on the legal issues in the case, not the country of origin. Second, the Court is more careful to embed judgements in its existing c..."*
- **2_Fixed_Word** (2 chunks)
  - `[0]` 779c ⚠ ends_mid_sentence — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
  - `[1]` 187c ⚠ starts_mid_sentence — *"persuading domestic judges is highest. These findings contribute to a developing literature that suggests international and domestic review ..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 812c ✅ — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
- **4_Recursive_Markdown** (2 chunks)
  - `[0]` 518c ✅ — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
  - `[1]` 293c ✅ — *"Second, the Court is more careful to embed judgements in its existing case law when the expected value of persuading domestic judges is high..."*
- **5_Semantic_Context_Injected** (2 chunks)
  - `[0]` 518c ✅ — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
  - `[1]` 403c ✅ — *"[Document Topic: Why and how do international courts justify decisions with citations to their own case law?] Second, the Court is more care..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 812c ✅ — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
- **7_Parent_Child** (3 chunks)
  - `[0]` 258c ✅ — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
  - `[1]` 259c ✅ — *"Several empirical observations are consistent with this view, which are examined through a network analysis of European Court of Human Right..."*
  - `[2]` 293c ✅ — *"Second, the Court is more careful to embed judgements in its existing case law when the expected value of persuading domestic judges is high..."*
- **8_Sentence_Window** (2 chunks)
  - `[0]` 518c ✅ — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*
  - `[1]` 553c ✅ — *"Several empirical observations are consistent with this view, which are examined through a network analysis of European Court of Human Right..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 812c ✅ — *"Why and how do international courts justify decisions with citations to their own case law? We argue that, like domestic review courts, inte..."*

---

### `law_ex_107334_google_neg_263` — 2384 ký tự

```text
An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The primary purpose of an IRB is to ensure that the rights, welfare, and safety of participants are protected throughout the research process. The process of gaining IRB approval begins with submitting a detailed research proposal outlining the study's objectives, methods, and ethical considerations. The IRB reviews the proposal to ensure that the research does no...
```

- **1_Fixed_Char** (6 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"s the proposal to ensure that the research does not pose undue risk to participants and that ethical guidelines are followed. One of the key..."*
  - `[2]` 499c ⚠ starts_mid_sentence, ends_mid_sentence — *"is demonstrating how the researchers will maintain confidentiality. The IRB requires researchers to outline how they will store and handle s..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (4 chunks)
  - `[0]` 811c ⚠ ends_mid_sentence — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 856c ⚠ starts_mid_sentence, ends_mid_sentence — *"will assess how researchers plan to obtain consent from participants and ensure that participants understand their rights, including the rig..."*
  - `[2]` 817c ⚠ starts_mid_sentence, ends_mid_sentence — *"risks and benefits of the research. Researchers must demonstrate that the benefits of the study outweigh any potential risks to the particip..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (3 chunks)
  - `[0]` 851c ✅ — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 942c ✅ — *"The IRB will assess how researchers plan to obtain consent from participants and ensure that participants understand their rights, including..."*
  - `[2]` 950c ✅ — *"Researchers must demonstrate that the benefits of the study outweigh any potential risks to the participants and that appropriate measures a..."*
- **4_Recursive_Markdown** (5 chunks)
  - `[0]` 575c ✅ — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 542c ✅ — *"One of the key ethical considerations in this process is obtaining informed consent. The IRB will assess how researchers plan to obtain cons..."*
  - `[2]` 484c ✅ — *"Ethical practices related to confidentiality include anonymizing data, securely storing recordings or transcripts, and ensuring that only au..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (5 chunks)
  - `[0]` 575c ✅ — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 681c ✅ — *"[Document Topic: An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human…] O..."*
  - `[2]` 623c ✅ — *"[Document Topic: An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human…] E..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 2384c ⚠ oversized_chars — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
- **7_Parent_Child** (8 chunks)
  - `[0]` 276c ✅ — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 383c ✅ — *"The process of gaining IRB approval begins with submitting a detailed research proposal outlining the study's objectives, methods, and ethic..."*
  - `[2]` 307c ✅ — *"The IRB will assess how researchers plan to obtain consent from participants and ensure that participants understand their rights, including..."*
  - *(... 5 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (7 chunks)
  - `[0]` 575c ✅ — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 574c ✅ — *"The process of gaining IRB approval begins with submitting a detailed research proposal outlining the study's objectives, methods, and ethic..."*
  - `[2]` 542c ✅ — *"One of the key ethical considerations in this process is obtaining informed consent. The IRB will assess how researchers plan to obtain cons..."*
  - *(... 4 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (4 chunks)
  - `[0]` 851c ✅ — *"An Institutional Review Board (IRB) is a committee established to review, approve, and monitor research involving human participants. The pr..."*
  - `[1]` 459c ✅ — *"Another important aspect of gaining IRB approval is demonstrating how the researchers will maintain confidentiality. The IRB requires resear..."*
  - `[2]` 709c ✅ — *"In addition to protecting participants' privacy, the IRB also evaluates the potential risks and benefits of the research. Researchers must d..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*

---

### `law_ex_107150_neg_15` — 3532 ký tự

```text
External links
[
edit
]
"
CRS Annotated Constitution: 9th Amendment
" by the
Congressional Research Service
(2000)
"
Proposed Amendments to the Constitution
" by
James Madison
(1789)
"
Bill of Rights Institute: Ninth Amendment
"
v
t
e
Constitution of the United States
Articles
Preamble
I
II
III
IV
V
VI
VII
Amendments
Bill of Rights
1
2
3
4
5
6
7
8
9
10
1795–1804
11
12
Reconstruction
13
14
15
20th century
16
17
18
19
20
21
22
23
24
25
26
27
Unratified
Congressional Apportionment
Titles of Nobilit...
```

- **1_Fixed_Char** (8 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"fied Congressional Apportionment Titles of Nobility Corwin Amendment Child Labor Equal Rights District of Columbia Voting Rights Proposed Ba..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"ctims' Rights Convention to propose amendments State ratifying conventions Formation History Articles of Confederation Mount Vernon Conferen..."*
  - *(... 5 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (5 chunks)
  - `[0]` 704c ⚠ ends_mid_sentence — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
  - `[1]` 1028c ⚠ starts_mid_sentence, ends_mid_sentence — *"Rights District of Columbia Voting Rights Proposed Balanced budget Blaine amendment Bricker amendment Campaign finance reform Christian amen..."*
  - `[2]` 1034c ⚠ starts_mid_sentence, ends_mid_sentence — *"Hillsborough Convention Fayetteville Convention Ratification Rhode Island Massachusetts Drafting and ratification timeline Clauses Admission..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (4 chunks)
  - `[0]` 868c ⚠ trailing_heading_orphan — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
  - `[1]` 1172c ⚠ trailing_heading_orphan — *"Parental Rights amendment School Prayer Single subject Victims' Rights Convention to propose amendments State ratifying conventions Formatio..."*
  - `[2]` 1120c ⚠ trailing_heading_orphan — *"Guarantee House Apportionment Impeachment Import-Export Ineligibility Militia Natural-born citizen Necessary and Proper No Religious Test Oa..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (6 chunks)
  - `[0]` 620c ⚠ trailing_heading_orphan — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
  - `[1]` 628c ⚠ trailing_heading_orphan — *"Bricker amendment Campaign finance reform Christian amendment Crittenden Compromise Electoral College abolition Equal Opportunity to Govern ..."*
  - `[2]` 637c ⚠ trailing_heading_orphan — *"The Federalist Papers Anti-Federalist Papers Massachusetts Compromise Virginia Ratifying Convention New York Circular Letter Hillsborough Co..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (6 chunks)
  - `[0]` 620c ⚠ trailing_heading_orphan — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
  - `[1]` 764c ⚠ trailing_heading_orphan — *"[Document Topic: External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) "…] Bric..."*
  - `[2]` 773c ⚠ trailing_heading_orphan — *"[Document Topic: External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) "…] The ..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 3532c ⚠ over_embedding_token_limit — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
- **7_Parent_Child** (8 chunks)
  - `[0]` 337c ⚠ trailing_heading_orphan — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
  - `[1]` 366c ⚠ trailing_heading_orphan — *"3 4 5 6 7 8 9 10 1795–1804 11 12 Reconstruction 13 14 15 20th century 16 17 18 19 20 21 22 23 24 25 26 27 Unratified Congressional Apportion..."*
  - `[2]` 495c ⚠ trailing_heading_orphan — *"Electoral College abolition Equal Opportunity to Govern Federal Marriage Flag Desecration Human Life "Liberty" amendment Ludlow amendment Pa..."*
  - *(... 5 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (123 chunks)
  - `[0]` 23c ⚠ undersized — *"External links [ edit ]"*
  - `[1]` 50c ⚠ trailing_heading_orphan, undersized — *"edit ] " CRS Annotated Constitution: 9th Amendment"*
  - `[2]` 83c ⚠ trailing_heading_orphan — *"" CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service"*
  - *(... 120 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (4 chunks)
  - `[0]` 704c ⚠ trailing_heading_orphan — *"External links [ edit ] " CRS Annotated Constitution: 9th Amendment " by the Congressional Research Service (2000) " Proposed Amendments to ..."*
  - `[1]` 1040c ⚠ trailing_heading_orphan — *"Electoral College abolition Equal Opportunity to Govern Federal Marriage Flag Desecration Human Life "Liberty" amendment Ludlow amendment Pa..."*
  - `[2]` 927c ⚠ trailing_heading_orphan — *"Copyright and Patent Double Jeopardy Due Process Elections Engagements Equal Protection Establishment Exceptions Excessive Bail Ex Post Fact..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunk_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.