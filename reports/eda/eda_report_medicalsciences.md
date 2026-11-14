# Báo cáo EDA & đánh giá Chunking — domain `medicalsciences`

*Tạo lúc 2026-11-14 12:26:46 | RETECO Track 2 (v3)*

## 1. Corpus

- Tổng tài liệu: **23,297** | schema: `content, doc_id`
- Ký tự: min=26, p25=361, **median=830**, mean=1031.8, p75=1711, p90=2059, p95=2469, p99=2878, max=10027
- Từ: median=125, mean=155.5, max=1255
- Ước tính vượt 512 token: **4.31%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 5.88% |
| 101-300 | 15.02% |
| 301-650 | 20.99% |
| 651-800 | 6.97% |
| 801-1500 | 21.75% |
| 1501-3000 | 29.3% |
| 3001-6000 | 0.07% |
| >6000 | 0.02% |

- Cấu trúc: header 0.01% | bullet 3.07% | code 0.01% | URL 3.63% | nhiều dòng 10.66%
- Chất lượng dữ liệu: trùng 0.0% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 1.39% | thiếu dấu câu cuối 17.76% | mở đầu bằng đại từ 3.34%

## 2. Hội thoại Track 2

- Hội thoại: **13** | lượt: **44** | lượt có gold: 44
- Lượt/hội thoại: mean=3.38 (min 3, max 6)
- Độ dài query: mean=18.1 từ, median=18, max=28
- Gold docs/lượt: mean=2.3, max=5
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 2.75x | 408.7 | 61.76% | 61.61% | 1.0% | 1.0% | 0.44% | 1.98% | 0.0% | **71.3** |
| **2_Fixed_Word** | 1.93x | 599.5 | 45.35% | 45.22% | 1.14% | 1.14% | 0.0% | 0.0% | 0.0% | **79.08** |
| **3_Sentence_Boundary** | 1.79x | 635.5 | 0.06% | 0.0% | 3.76% | 3.76% | 3.26% | 0.31% | 0.0% | **98.06** |
| **4_Recursive_Markdown** | 2.2x | 470.1 | 1.57% | 1.59% | 3.93% | 3.93% | 4.13% | 0.05% | 0.0% | **97.23** |
| **5_Semantic_Context_Injected** | 2.16x | 542.4 | 1.55% | 1.57% | 3.84% | 0.02% | 4.21% | 0.02% | 0.0% | **98.11** |
| **6_Whole_Document** | 1.0x | 1035.8 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 4.4% | **96.66** |
| **7_Parent_Child** | 3.4x | 304.4 | 0.04% | 0.03% | 5.98% | 5.98% | 4.58% | 1.27% | 0.0% | **96.84** |
| **8_Sentence_Window** | 5.55x | 293.3 | 0.05% | 0.09% | 3.27% | 3.27% | 29.35% | 29.5% | 0.0% | **87.01** |
| **9_TextTiling_Semantic** | 2.84x | 366.4 | 0.04% | 0.05% | 3.15% | 3.15% | 19.36% | 21.72% | 0.0% | **90.52** |
| 1b_Fixed_Char_300 | 4.26x | 266.0 | 74.3% | 73.98% | 1.25% | 1.25% | 0.51% | 4.12% | 0.0% | **65.06** |
| 1c_Fixed_Char_900 | 1.76x | 627.0 | 41.85% | 41.68% | 0.74% | 0.74% | 0.31% | 0.0% | 0.0% | **80.9** |
| 3b_Sentence_80w | 3.12x | 407.8 | 0.03% | 0.02% | 5.9% | 5.9% | 3.63% | 0.5% | 0.0% | **97.23** |
| 3c_Sentence_220w | 1.32x | 815.1 | 0.0% | 0.0% | 1.85% | 1.85% | 2.27% | 0.15% | 0.0% | **98.51** |
| 4b_Recursive_450 | 3.13x | 330.5 | 3.18% | 3.2% | 5.26% | 5.26% | 4.68% | 0.11% | 0.0% | **95.94** |
| 4c_Recursive_1000 | 1.55x | 665.8 | 0.55% | 0.55% | 2.41% | 2.41% | 2.8% | 0.0% | 0.0% | **98.48** |
| 4d_Recursive_250 | 5.48x | 188.1 | 8.92% | 8.9% | 6.42% | 6.42% | 4.55% | 2.72% | 0.0% | **92.3** |
| 5b_Semantic_thr1200_max900 | 1.65x | 674.3 | 0.91% | 0.97% | 2.43% | 0.03% | 3.97% | 0.0% | 0.0% | **98.64** |
| 5c_Semantic_thr500_max400 | 3.33x | 393.5 | 3.32% | 3.34% | 5.23% | 0.02% | 4.4% | 0.21% | 0.0% | **97.07** |
| 5d_Semantic_prefix_all | 2.16x | 543.2 | 1.55% | 1.57% | 3.84% | 0.02% | 4.21% | 0.02% | 0.0% | **98.11** |
| 5e_Adaptive_Hybrid | 1.88x | 607.1 | 1.31% | 1.31% | 3.23% | 0.0% | 3.92% | 0.03% | 0.0% | **98.37** |
| 8b_Sentence_Window_6_3 | 3.72x | 405.5 | 0.03% | 0.0% | 2.49% | 2.49% | 27.8% | 19.06% | 0.03% | **90.06** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 49 gold + 9977 nhiễu | 44 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.1433 | 0.1927 | 0.1380 | +0.0547 🔼 | **0.1980** | 0.1939 | 0.2311 | 0.3197 | 0.1760 | 27523 |
| 2_Fixed_Word | 0.1915 | 0.2261 | 0.1858 | +0.0403 🔼 | **0.2318** | 0.1909 | 0.2936 | 0.3489 | 0.2155 | 19411 |
| 3_Sentence_Boundary | 0.1695 | 0.2292 | 0.1664 | +0.0628 🔼 | **0.2323** | 0.2117 | 0.2576 | 0.3481 | 0.2293 | 18117 |
| 4_Recursive_Markdown | 0.1949 | 0.2247 | 0.1789 | +0.0458 🔼 | **0.2407** | 0.2042 | 0.2936 | 0.3614 | 0.2118 | 22090 |
| 5_Semantic_Context_Injected | 0.1999 | 0.2286 | 0.1929 | +0.0357 🔼 | **0.2356** | 0.2155 | 0.2992 | 0.3652 | 0.2139 | 21679 |
| 6_Whole_Document | 0.2153 | 0.2232 | 0.2029 | +0.0203 🔼 | **0.2356** | 0.2042 | 0.3201 | 0.3405 | 0.2262 | 10026 |
| 7_Parent_Child | 0.1812 | 0.2167 | 0.1769 | +0.0398 🔼 | **0.2210** | 0.2061 | 0.3030 | 0.3311 | 0.2145 | 34127 |
| 8_Sentence_Window | 0.1646 | 0.1825 | 0.1642 | +0.0183 🔼 | **0.1829** | 0.1769 | 0.2633 | 0.3064 | 0.1646 | 54342 |
| 9_TextTiling_Semantic | 0.1828 | 0.2062 | 0.1765 | +0.0297 🔼 | **0.2125** | 0.1909 | 0.2879 | 0.3670 | 0.1823 | 27810 |
| 1b_Fixed_Char_300 | 0.1537 | 0.1876 | 0.1441 | +0.0435 🔼 | **0.1972** | 0.2042 | 0.2538 | 0.3053 | 0.1756 | 42535 |
| 1c_Fixed_Char_900 | 0.1962 | 0.2464 | 0.1874 | +0.0590 🔼 | **0.2552** | 0.2098 | 0.2841 | 0.3943 | 0.2264 | 17736 |
| 3b_Sentence_80w | 0.1486 | 0.1830 | 0.1446 | +0.0384 🔼 | **0.1870** | 0.1750 | 0.2216 | 0.2723 | 0.1888 | 31501 |
| 3c_Sentence_220w | 0.2094 | 0.2206 | 0.1905 | +0.0301 🔼 | **0.2395** | 0.2117 | 0.3144 | 0.3254 | 0.2211 | 13361 |
| 4b_Recursive_450 | 0.2029 | 0.2011 | 0.1926 | +0.0085 | **0.2114** | 0.2061 | 0.3220 | 0.3311 | 0.1885 | 31308 |
| 4c_Recursive_1000 | 0.1964 | 0.2456 | 0.1722 | +0.0734 🔼 | **0.2698** | 0.2174 | 0.2992 | 0.3913 | 0.2267 | 15649 |
| 4d_Recursive_250 | 0.1862 | 0.2218 | 0.1843 | +0.0375 🔼 | **0.2237** | 0.2080 | 0.2652 | 0.3659 | 0.2138 | 54983 |
| 5b_Semantic_thr1200_max900 | 0.1959 | 0.2296 | 0.1852 | +0.0444 🔼 | **0.2403** | 0.2155 | 0.2841 | 0.3708 | 0.2077 | 16672 |
| 5c_Semantic_thr500_max400 | 0.1804 | 0.2310 | 0.1734 | +0.0576 🔼 | **0.2380** | 0.2098 | 0.2848 | 0.3583 | 0.2259 | 33401 |
| 5d_Semantic_prefix_all | 0.1999 | 0.2286 | 0.1846 | +0.0440 🔼 | **0.2439** | 0.2155 | 0.2992 | 0.3652 | 0.2139 | 21679 |
| 5e_Adaptive_Hybrid | 0.2037 | 0.2133 | 0.1948 | +0.0185 🔼 | **0.2222** | 0.2023 | 0.3182 | 0.3356 | 0.1965 | 18913 |
| 8b_Sentence_Window_6_3 | 0.1817 | 0.2157 | 0.1729 | +0.0428 🔼 | **0.2245** | 0.1985 | 0.2746 | 0.3443 | 0.2085 | 36477 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 4c_Recursive_1000 | **0.9506** | 0.9506 | 0.000 |
| 2 | 6_Whole_Document | **0.7776** | 0.7776 | 0.000 |
| 3 | 5d_Semantic_prefix_all | **0.7664** | 0.7664 | 0.000 |
| 4 | 5b_Semantic_thr1200_max900 | **0.7582** | 0.7582 | 0.000 |
| 5 | 3c_Sentence_220w | **0.7560** | 0.7560 | 0.000 |
| 6 | 4_Recursive_Markdown | **0.7328** | 0.7328 | 0.000 |
| 7 | 5_Semantic_Context_Injected | **0.7234** | 0.7234 | 0.000 |
| 8 | 1c_Fixed_Char_900 | **0.7227** | 0.7227 | 0.000 |
| 9 | 5c_Semantic_thr500_max400 | **0.6889** | 0.6889 | 0.000 |
| 10 | 3_Sentence_Boundary | **0.6570** | 0.6570 | 0.000 |
| 11 | 5e_Adaptive_Hybrid | **0.6528** | 0.6528 | 0.000 |
| 12 | 7_Parent_Child | **0.5892** | 0.5892 | 0.000 |
| 13 | 4b_Recursive_450 | **0.5550** | 0.5550 | 0.000 |
| 14 | 4d_Recursive_250 | **0.5537** | 0.5537 | 0.000 |
| 15 | 2_Fixed_Word | **0.5460** | 0.5460 | 0.000 |

**Chiến lược được chọn: `4c_Recursive_1000`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `medicalsciences_ex_34769_google_neg_184` — 173 ký tự

```text
In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mechanisms is presented in Figure 1.
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 173c ✅ — *"In the following paragraphs, we will discuss potential underlying mechanisms linking sleep to excessive fat tissue. An overview of those mec..."*

---

### `medicalsciences_ex_34711_google_neg_462` — 826 ký tự

```text
Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infections (PANDAS), or Sydenham's chorea (with psychiatric symptoms) present a sudden, seemingly inexplicable change in children, and we understand that getting accurate diagnosis, proper treatment and family support can make a profound difference for both the child’s health and the entire family’s well-being. Our goal is to provide outstanding care based on groundb...
```

- **1_Fixed_Char** (2 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
  - `[1]` 376c ⚠ starts_mid_sentence — *"al is to provide outstanding care based on groundbreaking research, and to tailor care to your child’s unique combination of symptoms and yo..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 826c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 826c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
- **4_Recursive_Markdown** (2 chunks)
  - `[0]` 617c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
  - `[1]` 208c ✅ — *"Stanford was the first academic institution to start a mutlidisciplinary PANS service. We hosted the first national PANS conference in the s..."*
- **5_Semantic_Context_Injected** (2 chunks)
  - `[0]` 617c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
  - `[1]` 344c ✅ — *"[Document Topic: Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/…] Stan..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 826c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
- **7_Parent_Child** (2 chunks)
  - `[0]` 443c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
  - `[1]` 382c ✅ — *"Our goal is to provide outstanding care based on groundbreaking research, and to tailor care to your child’s unique combination of symptoms ..."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 826c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 826c ✅ — *"Pediatric Acute-onset Neuropsychiatric Syndrome (PANS), Pediatric Autoimmune Neuropsychiatric Disorder Associated w/ Streptococcal Infection..."*

---

### `medicalsciences_ex_34233_google_neg_144` — 2477 ký tự

```text
Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal Albert Hall to Prague’s A Studio Rubin; from Chicago’s Theatre Chopin to Mumbai’s Sophia Bhabha Auditorium; from Edinburgh’s Assembly Ballroom to Horningsham’s Village Hall." He has become an institution as a solo performer on the modern fringe festival circuit. It’s fitting, then, that this man, who espouses the tradition of wandering theatre troupes from a...
```

- **1_Fixed_Char** (6 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 499c ⚠ starts_mid_sentence, ends_mid_sentence — *"the tradition of wandering theatre troupes from a bygone era, should now turn to The Bard for his latest monodrama.Utton first appeared at t..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"mands the weight of years and a lifetime of theatrical experience—along with stamina. In the intimacy of A Studio Rubin, we are as close as ..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (4 chunks)
  - `[0]` 745c ⚠ ends_mid_sentence — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 684c ⚠ starts_mid_sentence, ends_mid_sentence — *"year, he performs the world premiere of his adaptation of Shakespeare’s great tragedy, King Lear. While he may not have Lear’s “fourscore an..."*
  - `[2]` 709c ⚠ starts_mid_sentence, ends_mid_sentence — *"by his imagination.To explore King Lear in the span of an hour is a huge undertaking, but Utton rises to the occasion. He remains faithful t..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (4 chunks)
  - `[0]` 860c ✅ — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 777c ⚠ starts_with_connector — *"While he may not have Lear’s “fourscore and upward” years, the 73 he has certainly add to the credibility of his remarkable performance. If ..."*
  - `[2]` 797c ✅ — *"For his solo show, he juggles the scene order, initially presenting Lear in a state of madness. Over time, we come to understand that senile..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (5 chunks)
  - `[0]` 402c ✅ — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 582c ✅ — *"It’s fitting, then, that this man, who espouses the tradition of wandering theatre troupes from a bygone era, should now turn to The Bard fo..."*
  - `[2]` 614c ✅ — *"In the intimacy of A Studio Rubin, we are as close as possible to the actor, who can hide nothing from us. And Utton doesn’t want to. He inv..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (5 chunks)
  - `[0]` 402c ✅ — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 721c ✅ — *"[Document Topic: Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging…] I..."*
  - `[2]` 753c ✅ — *"[Document Topic: Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging…] I..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 2477c ⚠ over_embedding_token_limit — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
- **7_Parent_Child** (10 chunks)
  - `[0]` 402c ✅ — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 320c ✅ — *"It’s fitting, then, that this man, who espouses the tradition of wandering theatre troupes from a bygone era, should now turn to The Bard fo..."*
  - `[2]` 261c ⚠ starts_with_connector — *"While he may not have Lear’s “fourscore and upward” years, the 73 he has certainly add to the credibility of his remarkable performance. If ..."*
  - *(... 7 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (7 chunks)
  - `[0]` 985c ✅ — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 395c ⚠ starts_with_connector — *"While he may not have Lear’s “fourscore and upward” years, the 73 he has certainly add to the credibility of his remarkable performance. If ..."*
  - `[2]` 419c ✅ — *"In the intimacy of A Studio Rubin, we are as close as possible to the actor, who can hide nothing from us. And Utton doesn’t want to. He inv..."*
  - *(... 4 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (5 chunks)
  - `[0]` 723c ✅ — *"Pip Utton is a self-styled "strolling player," a point he emphasizes by noting that he has performed in venues "ranging from London’s Royal ..."*
  - `[1]` 681c ⚠ starts_with_connector — *"While he may not have Lear’s “fourscore and upward” years, the 73 he has certainly add to the credibility of his remarkable performance. If ..."*
  - `[2]` 194c ✅ — *"For his solo show, he juggles the scene order, initially presenting Lear in a state of madness. Over time, we come to understand that senile..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*

---

### `medicalsciences_ex_32545_neg_5` — 3179 ký tự

```text
PubMed Disclaimer
Publication types
Review
Actions
Search in PubMed
Search in MeSH
Add to Search
MeSH terms
Animals
Actions
Search in PubMed
Search in MeSH
Add to Search
Arachidonic Acid / administration & dosage
Actions
Search in PubMed
Search in MeSH
Add to Search
Arachidonic Acid / metabolism
Actions
Search in PubMed
Search in MeSH
Add to Search
Cytokines / biosynthesis
Actions
Search in PubMed
Search in MeSH
Add to Search
Dietary Fats / administration & dosage
Actions
Search in PubMed
Search...
```

- **1_Fixed_Char** (7 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"PubMed Disclaimer Publication types Review Actions Search in PubMed Search in MeSH Add to Search MeSH terms Animals Actions Search in PubMed..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"istration & dosage Actions Search in PubMed Search in MeSH Add to Search Dietary Fats / metabolism* Actions Search in PubMed Search in MeSH ..."*
  - `[2]` 499c ⚠ starts_mid_sentence, ends_mid_sentence — *"Acids, Omega-6 / metabolism* Actions Search in PubMed Search in MeSH Add to Search Humans Actions Search in PubMed Search in MeSH Add to Sea..."*
  - *(... 4 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (6 chunks)
  - `[0]` 717c ⚠ ends_mid_sentence — *"PubMed Disclaimer Publication types Review Actions Search in PubMed Search in MeSH Add to Search MeSH terms Animals Actions Search in PubMed..."*
  - `[1]` 722c ⚠ starts_mid_sentence, ends_mid_sentence — *"Search Fatty Acids, Omega-3 / administration & dosage Actions Search in PubMed Search in MeSH Add to Search Fatty Acids, Omega-3 / metabolis..."*
  - `[2]` 728c ⚠ starts_mid_sentence, ends_mid_sentence — *"to Search Leukocytes / cytology Actions Search in PubMed Search in MeSH Add to Search Leukocytes / metabolism Actions Search in PubMed Searc..."*
  - *(... 3 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (4 chunks)
  - `[0]` 840c ⚠ trailing_heading_orphan — *"PubMed Disclaimer Publication types Review Actions Search in PubMed Search in MeSH Add to Search MeSH terms Animals Actions Search in PubMed..."*
  - `[1]` 837c ⚠ trailing_heading_orphan — *"Fatty Acids, Omega-6 / administration & dosage Actions Search in PubMed Search in MeSH Add to Search Fatty Acids, Omega-6 / metabolism* Acti..."*
  - `[2]` 840c ⚠ trailing_heading_orphan — *"Lipid Metabolism Actions Search in PubMed Search in MeSH Add to Search Lipoxins / metabolism Actions Search in PubMed Search in MeSH Add to ..."*
  - *(... 1 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (5 chunks)
  - `[0]` 603c ⚠ trailing_heading_orphan — *"PubMed Disclaimer Publication types Review Actions Search in PubMed Search in MeSH Add to Search MeSH terms Animals Actions Search in PubMed..."*
  - `[1]` 630c ⚠ trailing_heading_orphan — *"Fatty Acids, Omega-3 / administration & dosage Actions Search in PubMed Search in MeSH Add to Search Fatty Acids, Omega-3 / metabolism* Acti..."*
  - `[2]` 595c ⚠ trailing_heading_orphan — *"Search in PubMed Search in MeSH Add to Search Leukocytes / metabolism Actions Search in PubMed Search in MeSH Add to Search Leukotrienes / m..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (5 chunks)
  - `[0]` 603c ⚠ trailing_heading_orphan — *"PubMed Disclaimer Publication types Review Actions Search in PubMed Search in MeSH Add to Search MeSH terms Animals Actions Search in PubMed..."*
  - `[1]` 666c ⚠ trailing_heading_orphan — *"[Document Topic: PubMed Disclaimer] Fatty Acids, Omega-3 / administration & dosage Actions Search in PubMed Search in MeSH Add to Search Fat..."*
  - `[2]` 631c ⚠ trailing_heading_orphan — *"[Document Topic: PubMed Disclaimer] Search in PubMed Search in MeSH Add to Search Leukocytes / metabolism Actions Search in PubMed Search in..."*
  - *(... 2 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 3179c ⚠ over_embedding_token_limit — *"PubMed Disclaimer Publication types Review Actions Search in PubMed Search in MeSH Add to Search MeSH terms Animals Actions Search in PubMed..."*
- **7_Parent_Child** (9 chunks)
  - `[0]` 350c ⚠ trailing_heading_orphan — *"PubMed Disclaimer Publication types Review Actions Search in PubMed Search in MeSH Add to Search MeSH terms Animals Actions Search in PubMed..."*
  - `[1]` 353c ⚠ trailing_heading_orphan — *"Cytokines / biosynthesis Actions Search in PubMed Search in MeSH Add to Search Dietary Fats / administration & dosage Actions Search in PubM..."*
  - `[2]` 339c ⚠ trailing_heading_orphan — *"Fatty Acids, Omega-3 / metabolism* Actions Search in PubMed Search in MeSH Add to Search Fatty Acids, Omega-6 / administration & dosage Acti..."*
  - *(... 6 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (103 chunks)
  - `[0]` 50c ⚠ trailing_heading_orphan, undersized — *"PubMed Disclaimer Publication types Review Actions"*
  - `[1]` 46c ⚠ trailing_heading_orphan, undersized — *"Review Actions Search in PubMed Search in MeSH"*
  - `[2]` 56c ⚠ trailing_heading_orphan, undersized — *"Search in PubMed Search in MeSH Add to Search MeSH terms"*
  - *(... 100 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (30 chunks)
  - `[0]` 50c ⚠ trailing_heading_orphan, undersized — *"PubMed Disclaimer Publication types Review Actions"*
  - `[1]` 45c ⚠ trailing_heading_orphan, undersized — *"Search in PubMed Search in MeSH Add to Search"*
  - `[2]` 26c ⚠ trailing_heading_orphan, undersized — *"MeSH terms Animals Actions"*
  - *(... 27 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunk_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.