# Báo cáo EDA & đánh giá Chunking — domain `earth_science`

*Tạo lúc 2026-11-14 12:23:09 | RETECO Track 2 (v3)*

## 1. Corpus

- Tổng tài liệu: **121,249** | schema: `content, doc_id`
- Ký tự: min=2, p25=212, **median=278**, mean=338.1, p75=348, p90=455, p95=546, p99=643, max=233623
- Từ: median=15, mean=27.7, max=12603
- Ước tính vượt 512 token: **0.31%**

**Histogram độ dài (ký tự):**

| Khoảng | % tài liệu |
| :--- | ---: |
| 0-100 | 0.57% |
| 101-300 | 58.01% |
| 301-650 | 40.52% |
| 651-800 | 0.36% |
| 801-1500 | 0.11% |
| 1501-3000 | 0.13% |
| 3001-6000 | 0.13% |
| >6000 | 0.16% |

- Cấu trúc: header 1.62% | bullet 0.9% | code 0.09% | URL 13.09% | nhiều dòng 41.14%
- Chất lượng dữ liệu: trùng 2.98% | rỗng 0 | JSON lỗi 0 | bắt đầu chữ thường 36.35% | thiếu dấu câu cuối 88.36% | mở đầu bằng đại từ 0.23%

## 2. Hội thoại Track 2

- Hội thoại: **29** | lượt: **133** | lượt có gold: 133
- Lượt/hội thoại: mean=4.59 (min 3, max 10)
- Độ dài query: mean=17.0 từ, median=17, max=25
- Gold docs/lượt: mean=1.36, max=5
- Schema dò được: `{"conversation_keys": ["id", "metadata", "original_answer", "original_query", "task", "turns"], "turn_keys": ["answer", "conversation_history", "gold_doc_ids", "query", "subquestion_reasoning", "subquestion_reasoning_metadata", "turn_id"]}`

## 3. Chất lượng chunk (heuristic, trên mẫu ngẫu nhiên)

| Chiến lược | Nở | Chunk TB (c) | Đứt đầu | Đứt đuôi | Đại từ raw | Đại từ unresolved | Tiêu đề mồ côi | <80c | >512tok | Quality |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1_Fixed_Char** | 1.27x | 307.3 | 18.4% | 18.4% | 0.16% | 0.16% | 1.3% | 1.42% | 0.0% | **91.11** |
| **2_Fixed_Word** | 1.08x | 346.0 | 6.73% | 6.73% | 0.19% | 0.19% | 0.0% | 0.0% | 0.0% | **96.64** |
| **3_Sentence_Boundary** | 1.07x | 341.6 | 0.05% | 0.05% | 0.37% | 0.37% | 1.73% | 0.0% | 0.0% | **99.39** |
| **4_Recursive_Markdown** | 1.16x | 317.9 | 0.39% | 0.39% | 0.13% | 0.13% | 4.51% | 0.09% | 0.0% | **99.08** |
| **5_Semantic_Context_Injected** | 1.16x | 329.7 | 0.39% | 0.39% | 0.13% | 0.0% | 4.52% | 0.04% | 0.0% | **99.12** |
| **6_Whole_Document** | 1.0x | 377.2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% | **99.89** |
| **7_Parent_Child** | 1.26x | 284.6 | 0.04% | 0.28% | 2.19% | 2.19% | 4.46% | 1.51% | 0.0% | **98.15** |
| **8_Sentence_Window** | 2.27x | 212.5 | 0.59% | 0.22% | 1.28% | 1.28% | 33.73% | 22.07% | 0.0% | **88.79** |
| **9_TextTiling_Semantic** | 1.53x | 238.2 | 0.16% | 0.13% | 0.82% | 0.82% | 20.5% | 20.18% | 0.0% | **91.5** |
| 1b_Fixed_Char_300 | 1.75x | 227.2 | 39.0% | 38.74% | 0.26% | 0.26% | 2.0% | 9.98% | 0.0% | **79.6** |
| 1c_Fixed_Char_900 | 1.11x | 347.7 | 8.63% | 8.49% | 0.04% | 0.04% | 0.81% | 0.0% | 0.0% | **96.0** |
| 3b_Sentence_80w | 1.2x | 315.6 | 0.04% | 0.04% | 1.67% | 1.67% | 2.84% | 0.54% | 0.0% | **98.83** |
| 3c_Sentence_220w | 1.04x | 348.5 | 0.0% | 0.0% | 0.24% | 0.24% | 1.06% | 0.0% | 0.0% | **99.55** |
| 4b_Recursive_450 | 1.31x | 282.0 | 1.3% | 1.26% | 1.15% | 1.15% | 6.64% | 0.38% | 0.0% | **97.95** |
| 4c_Recursive_1000 | 1.11x | 336.2 | 0.23% | 0.23% | 0.18% | 0.18% | 3.44% | 0.05% | 0.0% | **99.32** |
| 4d_Recursive_250 | 1.97x | 185.4 | 10.19% | 10.37% | 1.8% | 1.8% | 8.64% | 5.82% | 0.0% | **92.02** |
| 5b_Semantic_thr1200_max900 | 1.12x | 341.4 | 0.31% | 0.31% | 0.09% | 0.0% | 3.85% | 0.0% | 0.0% | **99.27** |
| 5c_Semantic_thr500_max400 | 1.32x | 300.5 | 1.37% | 1.33% | 1.22% | 0.0% | 6.16% | 0.61% | 0.0% | **98.19** |
| 5d_Semantic_prefix_all | 1.16x | 329.8 | 0.39% | 0.39% | 0.13% | 0.0% | 4.52% | 0.04% | 0.0% | **99.12** |
| 5e_Adaptive_Hybrid | 1.14x | 335.1 | 0.26% | 0.26% | 0.22% | 0.0% | 4.38% | 0.0% | 0.0% | **99.2** |
| 8b_Sentence_Window_6_3 | 1.71x | 271.3 | 0.23% | 0.2% | 0.99% | 0.99% | 25.43% | 10.47% | 0.0% | **93.07** |

> Ghi chú: 'Đứt đầu/đuôi' xác định bằng vị trí thật trong tài liệu gốc. 'Đại từ unresolved' đã trừ chunk có prefix chủ đề (heuristic). Chunk là cả tài liệu không bị tính 'quá ngắn'.

## 4. Tác động lên retrieval (BM25 + kiểm soát length bias)

Corpus con: 66 gold + 9992 nhiễu | 133 query. **Chỉ so sánh tương đối.**

**Định nghĩa các cột:**
- `nDCG single` : chỉ query hiện tại
- `nDCG +Hist`  : query + toàn bộ lịch sử hội thoại
- `nDCG +Rand`  : query + N từ ngẫu nhiên (baseline cùng độ dài)
- `Δ Semantic` : `+Hist - +Rand` — lợi ích ngữ nghĩa thực (≈0 ⇒ history chỉ là length bias)
- `nDCG_eff`    : `single + max(0, Δ Semantic)` — metric dùng trong composite

| Chiến lược | nDCG single | nDCG +Hist | nDCG +Rand | Δ Semantic | **nDCG_eff** | R@5 hist | R@10 single | R@10 hist | MRR@10 hist | Chunks |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_Fixed_Char | 0.4985 | 0.6615 | 0.4629 | +0.1986 🔼 | **0.6971** | 0.7763 | 0.6811 | 0.8590 | 0.6291 | 12963 |
| 2_Fixed_Word | 0.4787 | 0.6554 | 0.4345 | +0.2209 🔼 | **0.6996** | 0.7350 | 0.6272 | 0.8421 | 0.6275 | 11335 |
| 3_Sentence_Boundary | 0.4692 | 0.6726 | 0.4265 | +0.2461 🔼 | **0.7153** | 0.7732 | 0.6372 | 0.8371 | 0.6503 | 11220 |
| 4_Recursive_Markdown | 0.4886 | 0.6411 | 0.4633 | +0.1778 🔼 | **0.6664** | 0.7648 | 0.6817 | 0.8452 | 0.6010 | 11920 |
| 5_Semantic_Context_Injected | 0.4724 | 0.6332 | 0.4297 | +0.2035 🔼 | **0.6759** | 0.7410 | 0.6704 | 0.8289 | 0.5968 | 11899 |
| 6_Whole_Document | 0.2731 | 0.5277 | 0.2527 | +0.2750 🔼 | **0.5481** | 0.5921 | 0.4041 | 0.6955 | 0.4989 | 10058 |
| 7_Parent_Child | 0.4666 | 0.6072 | 0.4301 | +0.1771 🔼 | **0.6437** | 0.7491 | 0.6378 | 0.8168 | 0.5691 | 13686 |
| 8_Sentence_Window | 0.4633 | 0.6429 | 0.4308 | +0.2121 🔼 | **0.6754** | 0.7614 | 0.6485 | 0.8299 | 0.6115 | 24680 |
| 9_TextTiling_Semantic | 0.4791 | 0.6258 | 0.4180 | +0.2078 🔼 | **0.6869** | 0.7545 | 0.6704 | 0.8221 | 0.5916 | 16854 |
| 1b_Fixed_Char_300 | 0.4540 | 0.6402 | 0.4333 | +0.2069 🔼 | **0.6609** | 0.7464 | 0.6497 | 0.8362 | 0.6064 | 18140 |
| 1c_Fixed_Char_900 | 0.4698 | 0.6846 | 0.4306 | +0.2540 🔼 | **0.7238** | 0.7644 | 0.6648 | 0.8271 | 0.6702 | 11283 |
| 3b_Sentence_80w | 0.5033 | 0.6325 | 0.4664 | +0.1661 🔼 | **0.6694** | 0.7487 | 0.6786 | 0.8346 | 0.5964 | 13106 |
| 3c_Sentence_220w | 0.4189 | 0.6443 | 0.3815 | +0.2628 🔼 | **0.6817** | 0.7375 | 0.5764 | 0.7945 | 0.6228 | 10695 |
| 4b_Recursive_450 | 0.4908 | 0.6108 | 0.4558 | +0.1550 🔼 | **0.6458** | 0.7268 | 0.6779 | 0.8289 | 0.5668 | 13539 |
| 4c_Recursive_1000 | 0.4695 | 0.6451 | 0.4348 | +0.2103 🔼 | **0.6798** | 0.7335 | 0.6604 | 0.8202 | 0.6201 | 11222 |
| 4d_Recursive_250 | 0.4506 | 0.5647 | 0.4199 | +0.1448 🔼 | **0.5954** | 0.6612 | 0.6591 | 0.7792 | 0.5247 | 20652 |
| 5b_Semantic_thr1200_max900 | 0.4592 | 0.6306 | 0.4299 | +0.2007 🔼 | **0.6599** | 0.7149 | 0.6234 | 0.8127 | 0.6055 | 11373 |
| 5c_Semantic_thr500_max400 | 0.4571 | 0.5831 | 0.4232 | +0.1599 🔼 | **0.6170** | 0.6996 | 0.6447 | 0.8061 | 0.5397 | 13696 |
| 5d_Semantic_prefix_all | 0.4752 | 0.6332 | 0.4328 | +0.2004 🔼 | **0.6756** | 0.7410 | 0.6704 | 0.8289 | 0.5968 | 11899 |
| 5e_Adaptive_Hybrid | 0.4725 | 0.6366 | 0.4313 | +0.2053 🔼 | **0.6778** | 0.7510 | 0.6566 | 0.8164 | 0.6086 | 11647 |
| 8b_Sentence_Window_6_3 | 0.4622 | 0.6497 | 0.4274 | +0.2223 🔼 | **0.6845** | 0.7520 | 0.6629 | 0.8343 | 0.6159 | 18500 |

> ⚠️ `Δ Semantic ≈ 0` (không có mũi tên) cảnh báo rằng việc nối lịch sử hội thoại KHÔNG cải thiện truy hồi so với việc nối từ ngẫu nhiên cùng độ dài → phần lớn gain đến từ length bias, không phải ngữ nghĩa. Composite dùng `nDCG_eff` đã trung hòa yếu tố này.

## 5. Xếp hạng tổng hợp

**Công thức:** `base = 0.45*nDCG_eff + 0.20*Recall + 0.25*Quality + 0.10*Cost` → nhân `(1 - trunc_penalty)`

| Hạng | Chiến lược | Composite | Base | Trunc penalty |
| ---: | :--- | ---: | ---: | ---: |
| 1 | 3_Sentence_Boundary | **0.9280** | 0.9280 | 0.000 |
| 2 | 1c_Fixed_Char_900 | **0.9091** | 0.9091 | 0.000 |
| 3 | 2_Fixed_Word | **0.8500** | 0.8500 | 0.000 |
| 4 | 4c_Recursive_1000 | **0.8323** | 0.8323 | 0.000 |
| 5 | 5_Semantic_Context_Injected | **0.8205** | 0.8205 | 0.000 |
| 6 | 5d_Semantic_prefix_all | **0.8198** | 0.8198 | 0.000 |
| 7 | 5e_Adaptive_Hybrid | **0.8175** | 0.8175 | 0.000 |
| 8 | 4_Recursive_Markdown | **0.8082** | 0.8082 | 0.000 |
| 9 | 3c_Sentence_220w | **0.8028** | 0.8028 | 0.000 |
| 10 | 3b_Sentence_80w | **0.8011** | 0.8011 | 0.000 |
| 11 | 1_Fixed_Char | **0.7806** | 0.7806 | 0.000 |
| 12 | 5b_Semantic_thr1200_max900 | **0.7588** | 0.7588 | 0.000 |
| 13 | 8b_Sentence_Window_6_3 | **0.7183** | 0.7183 | 0.000 |
| 14 | 9_TextTiling_Semantic | **0.7143** | 0.7143 | 0.000 |
| 15 | 4b_Recursive_450 | **0.7140** | 0.7140 | 0.000 |

**Chiến lược được chọn: `3_Sentence_Boundary`** (xem log ADR để biết lý do chi tiết, sinh từ số đo).

> ⚠️ **Lưu ý về thang điểm:** Composite được chuẩn hóa min-max **trong từng domain** (vì quality, cost, nDCG biến thiên khác nhau giữa các domain). Do đó composite=0.80 ở `earth_science` KHÔNG có nghĩa tốt hơn composite=0.72 ở `biology` — chỉ có nghĩa chiến lược đó vượt trội các đối thủ **trong cùng domain**. Muốn so sánh liên domain, xem trực tiếp các metric gốc.

## 6. Case studies (từng chunk có gắn cờ lỗi)

### `exhaust_smells/bad_smell1_128.txt` — 145 ký tự

```text
<span class="base"><span class="hw haf">bad spirits</span></span>
                    </a>
                                                </div>
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 145c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span>                     </a>                                                 <..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 77c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span> </a> </div>"*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 77c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span> </a> </div>"*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 145c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span>                     </a>                                                 <..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 145c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span>                     </a>                                                 <..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 145c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span>                     </a>                                                 <..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 77c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span> </a> </div>"*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 77c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span> </a> </div>"*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 145c ✅ — *"<span class="base"><span class="hw haf">bad spirits</span></span>                     </a>                                                 <..."*

---

### `composition_of_cloud/pollution_cloud1_461.txt` — 272 ký tự

```text
loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"_":"ankit.bansal@me.iitr.ac.in"}]},{"#name":"author","$":{"id":"au000004","author-id":"S0038092X21007908-dfde201c02b304ee848c51305ca
```

- **1_Fixed_Char** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **7_Parent_Child** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 272c ✅ — *"loc":"post"},"_":"a"}]},{"#name":"e-address","$":{"xmlns:xlink":true,"id":"ea3","type":"email","href":"mailto:ankit.bansal@me.iitr.ac.in"},"..."*

---

### `predicting_aurora/Aurora_(singer)2_17.txt` — 538 ký tự

```text
reason not to think of being a singer.[33]
According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] Her first work before embarking on her music career was washing a pizza restaurant using a hose.[34] Songs from her early works were written in this early stage of her life.[35][36] Another of her early compositions was "I Had a Dream", which referred to how hard the world can be.[26][24] Although she considered it a "really long and boring song about world pe...
```

- **1_Fixed_Char** (2 chunks)
  - `[0]` 500c ⚠ ends_mid_sentence — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*
  - `[1]` 88c ⚠ starts_mid_sentence — *"d it a "really long and boring song about world peace" she performed it once at her high"*
- **2_Fixed_Word** (1 chunks)
  - `[0]` 538c ✅ — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*
- **3_Sentence_Boundary** (1 chunks)
  - `[0]` 538c ✅ — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*
- **4_Recursive_Markdown** (1 chunks)
  - `[0]` 538c ✅ — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*
- **5_Semantic_Context_Injected** (1 chunks)
  - `[0]` 538c ✅ — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*
- **6_Whole_Document** (1 chunks)
  - `[0]` 538c ✅ — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*
- **7_Parent_Child** (2 chunks)
  - `[0]` 42c ⚠ undersized — *"reason not to think of being a singer.[33]"*
  - `[1]` 495c ✅ — *"According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] Her first work before embarking on her music ..."*
- **8_Sentence_Window** (1 chunks)
  - `[0]` 538c ✅ — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*
- **9_TextTiling_Semantic** (1 chunks)
  - `[0]` 538c ✅ — *"reason not to think of being a singer.[33] According to Aurora, the first song she ever finished writing was titled "The Lonely Man".[34] He..."*

---

### `dry_weather_river/usgov2.txt` — 43789 ký tự

```text
</div>

    <button class="mobile-nav-close">
      <span class="usa-sr-only">Close</span>
    </button>
  </div>
  <div class="main-menu">
    <div class="site-name">U.S. Geological Survey</div>
<ul class="usa-nav__primary" role="menu">
      <li class="usa-nav__primary-item dropdown" role="menuitem">
      <i class="fa fa-angle-down" aria-hidden="true"></i>
      <button class="usa-nav__link" aria-expanded="false" aria-controls="extended-mega-nav-section-science-mobile">
        Science
      ...
```

- **1_Fixed_Char** (98 chunks)
  - `[0]` 493c ⚠ trailing_heading_orphan — *"</div>      <button class="mobile-nav-close">       <span class="usa-sr-only">Close</span>     </button>   </div>   <div class="main-menu"> ..."*
  - `[1]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"av-section-science-mobile">         Science       </button>       <div id="extended-mega-nav-section-science-mobile" class="usa-nav__submenu..."*
  - `[2]` 500c ⚠ starts_mid_sentence, ends_mid_sentence — *"="/science/science-explorer" class="menu-sub-section section-title" data-drupal-link-system-path="node/277817">Science Explorer</a>         ..."*
  - *(... 95 chunk nữa — xem chunk_inspection)*
- **2_Fixed_Word** (22 chunks)
  - `[0]` 1960c ⚠ ends_mid_sentence, oversized_chars — *"</div> <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button> </div> <div class="main-menu"> <div class="site-na..."*
  - `[1]` 2041c ⚠ ends_mid_sentence, oversized_chars — *"class="menu-sub-section section-title" data-drupal-link-system-path="node/50544">Science Centers</a> </li> <li> <a href="/science/observator..."*
  - `[2]` 1881c ⚠ starts_mid_sentence, oversized_chars — *"</li> </ul> </div> <div class="megamenu-grid-col"> <ul class="menu menu--mega-menu-products-col-2 nav"> <li> <a href="/products/multimedia-g..."*
  - *(... 19 chunk nữa — xem chunk_inspection)*
- **3_Sentence_Boundary** (18 chunks)
  - `[0]` 2256c ⚠ trailing_heading_orphan, oversized_chars — *"</div> <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button> </div> <div class="main-menu"> <div class="site-na..."*
  - `[1]` 2292c ⚠ trailing_heading_orphan, oversized_chars — *"<li> <a href="/science/special-topics" class="section-title" data-drupal-link-system-path="node/281238">Special Topics</a> </li> <li> <a hre..."*
  - `[2]` 2184c ⚠ trailing_heading_orphan, oversized_chars — *"<li> <a href="/library" class="menu-sub-section section-title">USGS Library</a> </li> <li> <a href="https://store.usgs.gov" class="menu-sub-..."*
  - *(... 15 chunk nữa — xem chunk_inspection)*
- **4_Recursive_Markdown** (71 chunks)
  - `[0]` 593c ⚠ trailing_heading_orphan — *"</div>  <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button> </div> <div class="main-menu"> <div class="site-n..."*
  - `[1]` 613c ⚠ trailing_heading_orphan — *"<div class="megamenu-grid-col"> <ul class="menu menu--mega-menu-science-col-1 nav"> <li> <a href="/science/science-explorer" class="menu-sub..."*
  - `[2]` 397c ⚠ trailing_heading_orphan — *"</div>                       <div class="megamenu-grid-col">       <ul class="menu menu--mega-menu-science-col-3 nav">                      ..."*
  - *(... 68 chunk nữa — xem chunk_inspection)*
- **5_Semantic_Context_Injected** (71 chunks)
  - `[0]` 593c ⚠ trailing_heading_orphan — *"</div>  <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button> </div> <div class="main-menu"> <div class="site-n..."*
  - `[1]` 734c ⚠ trailing_heading_orphan — *"[Document Topic: </div> <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button> </div> <div…] <div class="megamen..."*
  - `[2]` 518c ⚠ trailing_heading_orphan — *"[Document Topic: </div> <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button> </div> <div…] </div>             ..."*
  - *(... 68 chunk nữa — xem chunk_inspection)*
- **6_Whole_Document** (1 chunks)
  - `[0]` 43789c ⚠ over_embedding_token_limit — *"</div>      <button class="mobile-nav-close">       <span class="usa-sr-only">Close</span>     </button>   </div>   <div class="main-menu"> ..."*
- **7_Parent_Child** (41 chunks)
  - `[0]` 928c ⚠ trailing_heading_orphan — *"</div> <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button> </div> <div class="main-menu"> <div class="site-na..."*
  - `[1]` 1031c ⚠ trailing_heading_orphan — *"<a href="/science/mission-areas" class="menu-sub-section section-title" data-drupal-link-system-path="node/50541">Mission Areas</a> </li> <l..."*
  - `[2]` 997c ✅ — *"<a href="/science/faqs" class="menu-sub-section section-title" data-drupal-link-system-path="group/466">Frequently Asked Questions</a> </li>..."*
  - *(... 38 chunk nữa — xem chunk_inspection)*
- **8_Sentence_Window** (275 chunks)
  - `[0]` 89c ⚠ trailing_heading_orphan — *"</div> <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button>"*
  - `[1]` 79c ⚠ trailing_heading_orphan, undersized — *"<span class="usa-sr-only">Close</span> </button> </div> <div class="main-menu">"*
  - `[2]` 82c ⚠ trailing_heading_orphan — *"</div> <div class="main-menu"> <div class="site-name">U.S. Geological Survey</div>"*
  - *(... 272 chunk nữa — xem chunk_inspection)*
- **9_TextTiling_Semantic** (98 chunks)
  - `[0]` 89c ⚠ trailing_heading_orphan — *"</div> <button class="mobile-nav-close"> <span class="usa-sr-only">Close</span> </button>"*
  - `[1]` 82c ⚠ trailing_heading_orphan — *"</div> <div class="main-menu"> <div class="site-name">U.S. Geological Survey</div>"*
  - `[2]` 653c ⚠ trailing_heading_orphan — *"<ul class="usa-nav__primary" role="menu"> <li class="usa-nav__primary-item dropdown" role="menuitem"> <i class="fa fa-angle-down" aria-hidde..."*
  - *(... 95 chunk nữa — xem chunk_inspection)*

---

## 7. Giới hạn của phân tích

- Heuristic không thay được đánh giá của người: hãy đọc `chunk_inspection_*.md`.
- Retrieval đo bằng BM25 trên corpus con; chưa đo dense/reranker/LLM answer quality.
- Số token là ước lượng; hãy đo lại bằng tokenizer thật của model embedding sẽ dùng.
- `ndcg10_semantic_gain` là proxy; nếu muốn kết luận vững, cần chạy dense retriever thật.