# Báo cáo chất lượng dữ liệu — domain `biology`

*Tạo lúc 2026-11-21T09:05:10 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 86.9 🟢** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 99.0 | 🟢 |
| content | 0.25 | 61.8 | 🔴 |
| conversation | 0.15 | 92.3 | 🟢 |
| gold | 0.25 | 99.4 | 🟢 |
| link | 0.15 | 86.1 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| content | % trùng chính xác | 13.82 | 1.0 | 13.82 |
| link | % turn gold không chia sẻ từ nào với query | 8.7 | 1.5 | 13.05 |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 7.69 | 1 | 7.69 |
| content | % nghi không phải tiếng Anh | 15.3 | 0.5 | 7.65 |
| content | % doc quá ngắn | 15.1 | 0.5 | 7.55 |
| content | % ký hiệu lạ/URL nặng | 10.86 | 0.4 | 4.34 |
| content | % gần trùng (ngoài trùng chính xác) | 4.24 | 0.7 | 2.97 |
| integrity | % doc có mojibake | 0.5 | 2 | 1.0 |
| content | % lặp bất thường | 1.85 | 0.5 | 0.93 |
| content | % boilerplate | 2.59 | 0.3 | 0.78 |
| gold | % gold có lỗi nội dung nghiêm trọng | 1.28 | 0.5 | 0.64 |
| link | % turn overlap=0 (kể cả history) | 0.87 | 0.5 | 0.43 |

## 2. Khuyến nghị

- **[medium]** 0.5% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 15.1%.
- **[medium]** Trùng chính xác 13.82%.
- **[medium]** Gần trùng 4.24% (MinHash).
- **[low]** 15.3% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 76.4% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 2 hội thoại có đại từ/liên từ ở turn đầu.
- **[medium]** 8.7% turn gold KHÔNG chia sẻ từ nào với query.
- **[medium]** Bằng chứng nằm sau 650 ký tự ở 54.55% gold.
- **[medium]** Bằng chứng nằm sau ~512 token ở 23.64% gold.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **57,359** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.5% | ký tự điều khiển 0.0% | HTML/entity sót 0.14%
- Benchmark: 26 hội thoại | schema=`qa_pair` | vai trò {'user': 115, 'assistant': 115} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 115/115
- qrels: 196 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 196} | qid 115

## 4. Chất lượng nội dung

- Ký tự: min=1 p25=104.0 **median=309.0** mean=329.6 p75=519.0 p90=606.0 p99=711.0 max=31131 | outlier dài (>1764.0c): 0.32%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 95.75% / 99.48% / 99.63% / 99.81%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 24.47% |
| 101-300 | 24.46% |
| 301-650 | 46.82% |
| 651-800 | 3.73% |
| 801-1500 | 0.15% |
| 1501-3000 | 0.17% |
| 3001-6000 | 0.12% |
| >6000 | 0.07% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 8661 | 15.1% |
| mojibake | lỗi encoding (mojibake) | 284 | 0.5% |
| control_chars | ký tự điều khiển | 2 | 0.0% |
| html_residue | HTML/entity còn sót | 79 | 0.14% |
| boilerplate | boilerplate/menu/footer | 1485 | 2.59% |
| url_heavy | URL chiếm >25% nội dung | 5835 | 10.17% |
| symbol_heavy | ký hiệu lạ >30% | 397 | 0.69% |
| repetitive | lặp từ/dòng bất thường | 1064 | 1.85% |
| non_english | nghi không phải tiếng Anh | 8774 | 15.3% |
| pii_email | chứa email | 131 | 0.23% |
| pii_phone | chứa số điện thoại | 702 | 1.22% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 27194 | 47.41% |
| starts_lower | bắt đầu bằng chữ thường | 16811 | 29.31% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **37.48%**
- Trùng chính xác: 7,925 doc dư (13.82%), 4613 nhóm
- Gần trùng: 1091 cụm | doc dư gần-trùng ngoài trùng chính xác 713 (4.24%) | cụm lớn nhất 11
- Từ vựng (mẫu 10,068 doc): 37,948 từ | hapax 44.42% | Zipf -0.888 | s(1990), https(1940), 1(1572), 10(1371), more(1310), human(1226), 2(1201), also(1168), may(1146), www(1093), other(1078), sleep(973), org(946), such(944), one(943)

## 5. Hội thoại

- **26** hội thoại, **115** turn | turn/hội thoại: mean 4.42 (min 3, max 11) | query: mean 16.2 từ, median 16.0, p95 22.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 47 | 40.87% |
| pronoun | 56 | 48.7% |
| connector | 12 | 10.43% |
| short_ellipsis | 0 | 0% |

→ **76.4%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 2 (7.69%)
- Chuyển chủ đề: {'on_topic': 52.81, 'shift': 29.21, 'weak': 17.98} | hội thoại nhảy chủ đề ≥50% turn: 38.46%

**Loại câu hỏi:** yes_no 42.61%, statement_other 33.91%, what 16.52%, how 4.35%, why 2.61%

## 6. Gold / qrels

- Nguồn gold: {'inline': 115} | qrels được dùng để eval: False
- Gold/turn: mean 1.7, max 7
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 115/115 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 57,281/57,359 (99.86%) | Gini 0.3289
- Độ dài gold vs corpus (median): 1747.0 vs 309.0 (tỷ lệ 5.65x)
- Gold có lỗi nghiêm trọng: 1.28% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.361** (có history: 0.353) | overlap=0: 8.7% | <20%: 20.0% | overlap=0 dù có history: 0.87%
- Overlap theo ngữ cảnh: {'standalone': 0.414, 'connector': 0.259, 'pronoun': 0.339}
- OOV: 13.04% (TB 1.42%)
- **Vị trí bằng chứng** (110 mẫu): {'0-20%': 40.91, '20-40%': 12.73, '40-60%': 27.27, '60-80%': 10.0, '80-100%': 9.09} | median offset 750c | sau 650c: 54.55% | sau 512 token: 23.64%

## 8. BM25 baseline

- 115 query | 78 gold + 200 nhiễu
- nDCG@10 single/history = 0.5837/0.8238 | Recall@10 = 0.7292/0.9479

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 26 | 0.7003 | 0.6916 | 0.8564 | 0.8564 |
| 2 | 26 | 0.5646 | 0.8725 | 0.6955 | 0.9776 |
| 3 | 26 | 0.5213 | 0.8234 | 0.6635 | 1.0 |
| 4 | 16 | 0.5418 | 0.9065 | 0.6685 | 0.9786 |
| 5+ | 21 | 0.5724 | 0.8648 | 0.7413 | 0.9365 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 12 | 0.3301 | 0.8133 | 0.3302 | 0.9548 |
| pronoun | 56 | 0.5893 | 0.8693 | 0.7488 | 0.986 |
| standalone | 47 | 0.6419 | 0.7723 | 0.8078 | 0.9007 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 5 | 0.2534 | 1.0 | 0.4 | 1.0 |
| statement_other | 39 | 0.6315 | 0.7265 | 0.7785 | 0.8835 |
| what | 19 | 0.596 | 0.8473 | 0.6825 | 0.9579 |
| why | 3 | 0.4807 | 0.8575 | 0.5111 | 0.8667 |
| yes_no | 49 | 0.581 | 0.8721 | 0.7551 | 0.9949 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 26 | 0.7003 | 0.6916 | 0.8564 | 0.8564 |
| on_topic | 47 | 0.5266 | 0.8822 | 0.6616 | 0.9845 |
| shift | 26 | 0.585 | 0.8038 | 0.6731 | 0.941 |
| weak | 16 | 0.5601 | 0.8997 | 0.8125 | 1.0 |

- Turn khó: **3** (2.61%) — {'lexical_gap (overlap<0.2)': 3}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 247 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

## 10. Giới hạn

- Cờ nội dung là HEURISTIC (regex, tỷ lệ stopword) → có dương tính giả.
- Gần trùng: MinHash trên 5-word shingle, tối đa 1500 shingle đầu.
- Phụ thuộc ngữ cảnh / loại câu hỏi dựa trên regex tiếng Anh.
- Vị trí bằng chứng dựa trên trùng từ khóa (không phải đánh giá câu trả lời thật).
- BM25 chạy trên corpus con: chỉ so sánh tương đối.
- Health score là chỉ báo thô; hệ số trừ nằm trong `compute_health()`.

## 11. Ví dụ lỗi chi tiết

*Mỗi loại lỗi liệt kê tối đa `--examples` ví dụ; loại không có lỗi được đánh dấu ✅.*
## A. Toàn vẹn cấu trúc

### ✅ File bị thiếu
- Không phát hiện.

### ✅ Dòng JSON lỗi / không phải object
- Không phát hiện.

### ✅ Doc thiếu trường id
- Không phát hiện.

### ✅ doc_id trùng
- Không phát hiện.

### ✅ Doc thiếu trường text
- Không phát hiện.

### ✅ Trường text sai kiểu (không phải string)
- Không phát hiện.

### ✅ Trường title rỗng/sai
- Không phát hiện.

### ✅ qrels: dòng sai format
- Không phát hiện.

### ✅ qrels: cặp (qid, doc) trùng
- Không phát hiện.

### ✅ qrels: relevance ≤ 0
- Không phát hiện.

### ✅ Benchmark: conversation_id trùng
- Không phát hiện.

### ✅ Benchmark: hội thoại rỗng
- Không phát hiện.

### ✅ Benchmark: role không xen kẽ
- Không phát hiện.

### ✅ Benchmark: turn thiếu query
- Không phát hiện.

## B. Chất lượng nội dung tài liệu

### ✅ `empty` — tài liệu rỗng
- Không phát hiện.

### ❌ `too_short` — quá ngắn (<50 ký tự) — 8,661

**`3D_vision/full_0_0.txt`** (43 ký tự)
```text
Skip to main content # Top bar navigation
```
**`3D_vision/full_146_1.txt`** (19 ký tự)
```text
| Google Scholar
```
**`3D_vision/full_15_0.txt`** (18 ký tự)
```text
Sections Sections
```
**`3D_vision/full_163_0.txt`** (26 ký tự)
```text
# Footer * Guidelines
```
**`3D_vision/full_17_0.txt`** (28 ký tự)
```text
About journal About journal
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 284

**`UV_causes_skin_cancer/index.html_10_0.txt`** (443 ký tự)
```text
About CDC Contact Us 800-232-4636 Facebook Twitter Instagram LinkedIn Youtube Pinterest Snapchat CONTACT CDC Contact Us Call 800-232-4636 Email Us ABOUT CDC About CDC Jobs Funding POLICIES Accessibility External Links Pr…
```
**`UV_causes_skin_cancer/index.html_10_1.txt`** (144 ký tự)
```text
�­ì´ Tagalog Ð ÑÑÑÐºÐ¸Ð¹ Ø§ÙØ¹Ø±Ø¨ÙØ© KreyÃ²l Ayisyen FranÃ§ais Polski PortuguÃªs Italiano Deutsch æ¥æ¬èª ÙØ§Ø±Ø³Û English About CDC
```
**`UV_causes_skin_cancer/index.html_10_2.txt`** (435 ký tự)
```text
Contact Us 800-232-4636 Facebook Twitter Instagram LinkedIn Youtube Pinterest Snapchat CONTACT CDC Contact Us Call 800-232-4636 Email Us ABOUT CDC About CDC Jobs Funding POLICIES Accessibility External Links Privacy Poli…
```
**`UV_causes_skin_cancer/index.html_10_3.txt`** (131 ký tự)
```text
ì´ Tagalog Ð ÑÑÑÐºÐ¸Ð¹ Ø§ÙØ¹Ø±Ø¨ÙØ© KreyÃ²l Ayisyen FranÃ§ais Polski PortuguÃªs Italiano Deutsch æ¥æ¬èª ÙØ§Ø±Ø³Û English
```
**`UV_causes_skin_cancer/index.html_11_0.txt`** (364 ký tự)
```text
CONTACT CDC Contact Us Call 800-232-4636 Email Us ABOUT CDC About CDC Jobs Funding POLICIES Accessibility External Links Privacy Policies No Fear Act FOIA OIG Nondiscrimination Vulnerability Disclosure Policy CONNECT WIT…
```

### ❌ `control_chars` — ký tự điều khiển — 2

**`mouldy_food_sick/what-moldy-foods-is-it-ok-to-eat-2018-11_11_0.txt`** (265 ký tự)
```text
Angle down icon An icon in the shape of an angle pointing down. If you notice mold on your bread — toss it. DmyTo/iStock This story is available exclusively to Business Insider subscribers. Become an Insider and start r…
```
**`mouldy_food_sick/what-moldy-foods-is-it-ok-to-eat-2018-11_13_0.txt`** (419 ký tự)
```text
According to the USDA , mold can cause allergic reactions or respiratory problems and certain kinds of molds produce poisonous mycotoxins that make people sick or cause infections. Invisible bacteria can also grow alongs…
```

### ❌ `html_residue` — HTML/entity còn sót — 79

**`birches_white_bark/northendangeredspeci_65_0.txt`** (365 ký tự)
```text
<h1>How to save the whitebark pine</h1> <p class="byline">by Kylie Mohr, High Country News <br />January 5, 2023</p> <p>Whitebark pines are unmistakable, with their stout, twisted trunks — shaped but not dominated by the…
```
**`birches_white_bark/northendangeredspeci_65_1.txt`** (438 ký tự)
```text
assessments-whitebark-pine">over half</a> of those still standing were husks of their former selves, their fate signaled by flaming red needles, and then, ghostly gray trunks with no branches at all.&nbsp;</p> <p>The tre…
```
**`birches_white_bark/northendangeredspeci_65_2.txt`** (360 ký tự)
```text
21010203">all threaten</a> this keystone species. It was officially <a href="https://www.fws.gov/press-release/2022-12/whitebark-pine-receives-esa- protection-threatened-species">listed</a> as threatened by the U.S. Fish…
```
**`birches_white_bark/northendangeredspeci_65_3.txt`** (471 ký tự)
```text
-whitebark- pine/">ecosystem</a>: Its branches create shade, which helps retain snowpack, and its roots hold the soil in place, preventing erosion. Whitebark pine cones nourish animals like grizzlies and Clark’s nutcrack…
```
**`birches_white_bark/northendangeredspeci_65_4.txt`** (275 ký tự)
```text
“If you come across it in your travels, it was a treat to have,” the <a href="http://www.charkoosta.com/news/elder-tony-incashola-remembers-whitebark- pine-from-his- youth/article_4c28c94c-e09f-11e9-9232-274e4ed71e48.htm…
```

### ❌ `boilerplate` — boilerplate/menu/footer — 1,485

**`animals_handedness/Laterality_2.txt`** (8391 ký tự)
```text
In other animals[edit] It has been shown that cerebral lateralization is a widespread phenomenon in the animal kingdom. Functional and structural differences between left and right brain hemispheres can be found in many …
```
**`organism_learn/adaptive_prediction_1.txt`** (5818 ký tự)
```text
Department of Molecular Genetics, Weizmann Institute of Science Rehovot 76100, Israel. 2 Department of Molecular Microbiology and Biotechnology, Tel Aviv University, Tel Aviv 69978, Israel. 3 Department of Molecular Cell…
```
**`organism_learn/adaptive_prediction_2.txt`** (5683 ký tự)
```text
1.00 Normalized promoter activity Wild-type strain Added sugar: Lactose Maltose None a 0 0.25 0.50 0.75 1.00 GFP-fused promoter b Evolved strain Figure 2 | Conditioned response in E. coli sugar metabolism. Promoter activ…
```
**`organism_learn/adaptive_prediction_3.txt`** (5126 ký tự)
```text
Nitrogen depletion High osmolarity Glucose depletion 46 1.5 3 29 0.001 Grape must Fermentation Respiration 4 5 19 Wine production process (time) 31 Diauxic shift Low pH Heat Ethanol Oxidative stress a 0 Fold cross-protec…
```
**`3D_vision/full_0_0.txt`** (43 ký tự)
```text
Skip to main content # Top bar navigation
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 5,835

**`UV_causes_skin_cancer/uva-vs-uvb_0_20.txt`** (372 ký tự)
```text
7 Moan J, et al. (2014). Ultraviolet radiation and health: Optimal time for sun exposure. https://www.ncbi.nlm.nih.gov/pubmed/25207380 Rafieepour A, et al. (2015). Seasonal variation in exposure level of types A and B ul…
```
**`UV_causes_skin_cancer/uva-vs-uvb_0_21.txt`** (344 ký tự)
```text
/media/stats/prevention-and-care/sunscreen-faqs Traveisan A, et al. (2006). Unusual high exposure to ultraviolet-C radiation. DOI: https://doi.org/10.1562/2005-10-27-ra-728 UV radiation. (n.d.). https://www.who.int/uv/fa…
```
**`UV_causes_skin_cancer/uva-vs-uvb_1_20.txt`** (372 ký tự)
```text
7 Moan J, et al. (2014). Ultraviolet radiation and health: Optimal time for sun exposure. https://www.ncbi.nlm.nih.gov/pubmed/25207380 Rafieepour A, et al. (2015). Seasonal variation in exposure level of types A and B ul…
```
**`UV_causes_skin_cancer/uva-vs-uvb_1_21.txt`** (344 ký tự)
```text
/media/stats/prevention-and-care/sunscreen-faqs Traveisan A, et al. (2006). Unusual high exposure to ultraviolet-C radiation. DOI: https://doi.org/10.1562/2005-10-27-ra-728 UV radiation. (n.d.). https://www.who.int/uv/fa…
```
**`UV_causes_skin_cancer/uva-vs-uvb_24_1.txt`** (440 ký tự)
```text
from ultraviolet (UV) rays? https://www.cancer.org/content/cancer/en/healthy/be-safe-in-sun/uv-protection.html American Cancer Society. (2019). Ultraviolet (UV) radiation. https://www.cancer.org/cancer/cancer-causes/radi…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 397

**`3D_vision/visual-perception_23_0.txt`** (18 ký tự)
```text
* * * *
```
**`UV_causes_skin_cancer/index.html_9_3.txt`** (29 ký tự)
```text
æ¥æ¬èª ÙØ§Ø±Ø³Û English
```
**`accelerate_plants_growth/PlantGrowth_29_0.txt`** (5 ký tự)
```text
* * *
```
**`animals_handedness/breathingtechniquesa_13_0.txt`** (23 ký tự)
```text
## **2\. Seed Mantra**
```
**`animals_handedness/breathingtechniquesa_30_0.txt`** (5 ký tự)
```text
* * *
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 1,064

**`neurons_learn/Hebbian_theory_2.txt`** (2475 ký tự)
```text
Principles[edit] From the point of view of artificial neurons and artificial neural networks, Hebb's principle can be described as a method of determining how to alter the weights between model neurons. The weight betwee…
```
**`3D_vision/Binocular_disparity_3_3.txt`** (165 ký tự)
```text
to the disparity of the right image. Normalized correlation: ∑ ∑ L ( r , c ) ⋅ R ( r , c − d ) ( ∑ ∑ L ( r , c ) 2 ) ⋅ ( ∑ ∑ R ( r , c − d )
```
**`3D_vision/Binocular_disparity_3_4.txt`** (207 ký tự)
```text
2 ) {\displaystyle {\frac {\sum {\sum {L(r,c)\cdot R(r,c-d)}}}{\sqrt {(\sum {\sum {L(r,c)^{2}}})\cdot (\sum {\sum {R(r,c-d)^{2}}})}}}} Sum of squared differences: ∑ ∑ ( L ( r , c ) − R ( r
```
**`3D_vision/Binocular_disparity_3_5.txt`** (196 ký tự)
```text
, c − d ) ) 2 {\displaystyle \sum {\sum {(L(r,c)-R(r,c-d))^{2}}}} Sum of absolute differences: ∑ ∑ | L ( r , c ) − R ( r , c − d ) | {\displaystyle \sum {\sum {\left|L(r,c
```
**`3D_vision/vision-and-visual-perception-challenges_73_0.txt`** (128 ký tự)
```text
If you want this to change , cite this article , link to us, or join us to help us democratize design knowledge ! ## Search
```

### ❌ `non_english` — nghi không phải tiếng Anh — 8,774

**`3D_vision/Binocular_disparity_3_4.txt`** (207 ký tự)
```text
2 ) {\displaystyle {\frac {\sum {\sum {L(r,c)\cdot R(r,c-d)}}}{\sqrt {(\sum {\sum {L(r,c)^{2}}})\cdot (\sum {\sum {R(r,c-d)^{2}}})}}}} Sum of squared differences: ∑ ∑ ( L ( r , c ) − R ( r
```
**`3D_vision/Binocular_disparity_3_5.txt`** (196 ký tự)
```text
, c − d ) ) 2 {\displaystyle \sum {\sum {(L(r,c)-R(r,c-d))^{2}}}} Sum of absolute differences: ∑ ∑ | L ( r , c ) − R ( r , c − d ) | {\displaystyle \sum {\sum {\left|L(r,c
```
**`3D_vision/full_102_0.txt`** (268 ký tự)
```text
Chen, J., Wu, E., Chen, X., Zhu, L., Li, X., Thorn, F., et al. (2016). Rapid integration of tactile and visual information by a newly sighted child. Curr. Biol. 26, 1069–1074. doi: 10.1016/j.cub.2016.02.065 PubMed Abstra…
```
**`3D_vision/full_104_0.txt`** (186 ký tự)
```text
Dehaene, S., and Cohen, L. (2007). Cultural recycling of cortical maps. Neuron 56, 384–398. doi: 10.1016/j.neuron.2007.10.004 PubMed Abstract | CrossRef Full Text | Google Scholar
```
**`3D_vision/full_106_0.txt`** (244 ký tự)
```text
Delboeuf, F. J. (1865). Note sur certaines illusions d’optique: essai d’une théorie psychophysique de la maniere dont l’oeil apprécie les distances et les angles. Bull. l’Académie R. Sci. Lett. Beaux Arts Belgique 19, 19…
```

### ❌ `pii_email` — chứa email — 131

**`3D_vision/full_162_0.txt`** (416 ký tự)
```text
*Correspondence: Amber Maimon, amber.maimon@runi.ac.il Disclaimer: All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those o…
```
**`3D_vision/vision-and-visual-perception-challenges_77_0.txt`** (102 ký tự)
```text
### Connect With Us Reach us at hello@interaction-design.org or through our online contact form .
```
**`3D_vision/visual-perception_19_0.txt`** (40 ký tự)
```text
* +852 2849 6900 * info@cdchk.org
```
**`3D_vision/visual-perception_21_0.txt`** (40 ký tự)
```text
* +852 2849 2280 * info@cdchk.org
```
**`accelerate_plants_growth/accelerate20growthpd_2_0.txt`** (300 ký tự)
```text
Works and What Does Not The most effective way growers can accelerate plant development is to increase the greenhouse air temperature. Erik Runkle is professor and floriculture Extension specialist in the department of h…
```

### ❌ `pii_phone` — chứa số điện thoại — 702

**`smallest_genome/Genome_7.txt`** (6423 ký tự)
```text
Genome size[edit] Log–log plot of the total number of annotated proteins in genomes submitted to GenBank as a function of genome size Genome size is the total number of the DNA base pairs in one copy of a haploid genome.…
```
**`3D_vision/full_103_0.txt`** (259 ký tự)
```text
Dehaene, S. (2005). 8 Evolution of Human Cortical Circuits for Reading and Arithmetic: The From monkey brain to human brain: A Fyssen Foundation symposium. Cambridge, MA: MIT press. doi: 10.7551/mitpress/3136.001.0001 Cr…
```
**`3D_vision/full_135_0.txt`** (227 ký tự)
```text
Ostrovsky, Y., Andalman, A., and Sinha, P. (2006). Vision following extended congenital blindness. Psychol. Sci. 17, 1009–1014. doi: 10.1111/j.1467-9280.2006.01827.x PubMed Abstract | CrossRef Full Text | Google Scholar
```
**`3D_vision/full_90_0.txt`** (263 ký tự)
```text
Amedi, A., Merabet, L. B., Bermpohl, F., and Pascual-Leone, A. (2005). The occipital cortex in the blind: lessons about plasticity and vision. Curr. Direct. Psychol. Sci. 14, 306–311. doi: 10.1111/j.0963-7214.2005.00387.…
```
**`3D_vision/visual-perception_18_0.txt`** (96 ký tự)
```text
* Unit 7, 4/F, Victoria Centre, 15 Watson Road, Fortress Hill, Hong Kong * +852 2849 6138
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 27,194

**`evolution_not_make_our_life_longer/Mutation_accumulation_theory_1.txt`** (1154 ký tự)
```text
Background and history[edit] Despite Charles Darwin's completion of his theory of biological evolution in the 19th century, the modern logical framework for evolutionary theories of aging wouldn't emerge until almost a c…
```
**`humans_closest_relatives_after_primates/Treeshrew_6.txt`** (3728 ký tự)
```text
Taxonomy[edit] They make up the entire order Scandentia, split into the families Tupaiidae, the treeshrews, and Ptilocercidae, the pen-tailed treeshrew. The 20 species are placed in five genera. Treeshrews were moved fro…
```
**`trees_grow_directions/Apical_dominance_1.txt`** (1232 ký tự)
```text
Overview[edit] Apical dominance occurs when the shoot apex inhibits the growth of lateral buds so that the plant may grow vertically. It is important for the plant to devote energy to growing upward so that it can get mo…
```
**`smallest_genome/Genome_7.txt`** (6423 ký tự)
```text
Genome size[edit] Log–log plot of the total number of annotated proteins in genomes submitted to GenBank as a function of genome size Genome size is the total number of the DNA base pairs in one copy of a haploid genome.…
```
**`immortal_organisms/Immortality_2.txt`** (18737 ký tự)
```text
Physical immortality[edit] Physical immortality is a state of life that allows a person to avoid death and maintain conscious thought. It can mean the unending existence of a person from a physical source other than orga…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 16,811

**`3D_vision/Binocular_disparity_3_1.txt`** (630 ký tự)
```text
be slightly rotated off level. Through a process known as image rectification, both images are rotated to allow for disparities in only the horizontal direction (i.e. there is no disparity in the y image coordinates). Th…
```
**`3D_vision/Binocular_disparity_3_2.txt`** (609 ký tự)
```text
are compared to all possible disparities in the right image by comparing their corresponding image patches. For example, for a disparity of 1, the patch in the left image would be compared to a similar-sized patch in the…
```
**`3D_vision/Binocular_disparity_3_3.txt`** (165 ký tự)
```text
to the disparity of the right image. Normalized correlation: ∑ ∑ L ( r , c ) ⋅ R ( r , c − d ) ( ∑ ∑ L ( r , c ) 2 ) ⋅ ( ∑ ∑ R ( r , c − d )
```
**`3D_vision/Binocular_disparity_3_7.txt`** (325 ký tự)
```text
remembering all values from the previous pixel. An even more efficient algorithm involves remembering column sums from the previous row (in addition to remembering all values from the previous pixel). Techniques that sav…
```
**`3D_vision/Binocular_disparity_4_1.txt`** (503 ký tự)
```text
scanning the terrain for obstacles. The rover captures a pair of images with its stereoscopic navigation cameras and disparity calculations are performed in order to detect elevated objects (such as boulders). Additional…
```

### ❌ Trùng chính xác — 7,925

*4613 nhóm*

- nhóm: `brain_no_pain_receptors_headache/Brain_2_0.txt`, `see_when_eyes_closed/Brain_2_0.txt`
```text
Development Main article: Neural development Brain of a human embryo in the sixth week of development The brain develops in an intricately orchestrated sequence of stages. It changes in shape from a simple swelling at th…
```
- nhóm: `eyes_smooth_transition/s41467018055470_231_0.txt`, `smallest_genome/s41467021221008_431_0.txt`, `wake_up_wrong/s41467022345032_463_0.txt`
```text
* [ Follow us on Facebook ](https://www.facebook.com/NatureCommunications) * [ Follow us on Twitter ](https://twitter.com/NatureComms) * [ Sign up for alerts ](https://www.nature.com/my-account/alerts/subscribe-journal?l…
```
- nhóm: `feel_excess_pressure/syc20373410_6_0.txt`, `feel_excess_pressure/syc20373410_78_0.txt`
```text
[ Find a Doctor ](https://www.mayoclinic.org/appointments/find-a-doctor)
```
- nhóm: `hair_turn_grey/15-best-hair-salons-singapore_45_2.txt`, `hair_turn_grey/15-best-hair-salons-singapore_46_2.txt`, `hair_turn_grey/15-best-hair-salons-singapore_47_2.txt`, `hair_turn_grey/15-best-hair-salons-singapore_48_2.txt`
```text
Treatment Review: Bond Repair That Packs a Shine! No harsh chemicals, just gorgeous hair! We review Chez Vous’ latest Liquid Hair Treatment which promises stronger hair and a celebrity-like shine Read More > Best Hair Tr…
```
- nhóm: `human_monogamy/Human_64_117.txt`, `human_monogamy/Human_7_237.txt`
```text
.1013. S2CID 1665503. ^ Marziali C (7 December 2010). "Reaching Toward the Fountain of Youth". USC Trojan Family Magazine. Archived from the original on 13 December 2010. Retrieved 7 December 2010. ^ Kalben BB (2002). "W…
```

### ❌ Gần trùng (khác nhau chút ít) — 713

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 11: `eyes_smooth_transition/s41467018055470_178_0.txt`, `eyes_smooth_transition/s41467018055470_184_0.txt`, `sense_dimmed_sleep/s12931022021413_392_0.txt`, `sense_dimmed_sleep/s12931022021413_395_0.txt`, `sense_dimmed_sleep/s12931022021413_398_0.txt`
  - `eyes_smooth_transition/s41467018055470_178_0.txt`:
```text
You can also search for this author in [ PubMed ](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Stephen%20LaBerge) [ Google Scholar ](http://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&a…
```
  - `eyes_smooth_transition/s41467018055470_184_0.txt`:
```text
You can also search for this author in [ PubMed ](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Philip%20G.%20Zimbardo) [ Google Scholar ](http://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scho…
```
- cụm size 10: `eyes_smooth_transition/s41467018055470_181_1.txt`, `sense_dimmed_sleep/s12931022021413_392_1.txt`, `sense_dimmed_sleep/s12931022021413_404_1.txt`, `sense_dimmed_sleep/s12931022021413_407_1.txt`, `sense_dimmed_sleep/s12931022021413_419_1.txt`
  - `eyes_smooth_transition/s41467018055470_181_1.txt`:
```text
20Baird%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
```
  - `sense_dimmed_sleep/s12931022021413_392_1.txt`:
```text
un%20Huang%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
```
- cụm size 8: `UV_causes_skin_cancer/uva-vs-uvb_60_0.txt`, `UV_causes_skin_cancer/uva-vs-uvb_60_1.txt`, `UV_causes_skin_cancer/uva-vs-uvb_61_1.txt`, `UV_causes_skin_cancer/uva-vs-uvb_62_0.txt`, `UV_causes_skin_cancer/uva-vs-uvb_62_1.txt`
  - `UV_causes_skin_cancer/uva-vs-uvb_60_0.txt`:
```text
About Us Contact Us Privacy Policy Privacy Settings Advertising Policy Health Topics Sitemap Medical Affairs Content Integrity Newsletters © 2024 Healthline Media LLC. All rights reserved. Our website services, content, …
```
  - `UV_causes_skin_cancer/uva-vs-uvb_60_1.txt`:
```text
Us Privacy Policy Privacy Settings Advertising Policy Health Topics Sitemap Medical Affairs Content Integrity Newsletters © 2024 Healthline Media LLC. All rights reserved. Our website services, content, and products are …
```
- cụm size 6: `human_monogamy/human-being_10_16.txt`, `human_monogamy/human-being_11_16.txt`, `human_monogamy/human-being_34_0.txt`, `human_monogamy/human-being_4_19.txt`, `human_monogamy/human-being_4_7.txt`
  - `human_monogamy/human-being_10_16.txt`:
```text
do scientists hope to learn from total solar eclipse in US? Hear a discussion about the uniqueness in humans which separates them from other animals What is it to be human? (more) See all videos for this article Hear psy…
```
  - `human_monogamy/human-being_11_16.txt`:
```text
do scientists hope to learn from total solar eclipse in US? Hear a discussion about the uniqueness in humans which separates them from other animals What is it to be human? (more) See all videos for this article Hear psy…
```
- cụm size 5: `eye_capture_shape/Determine-Eye-Shape_32_1.txt`, `eye_capture_shape/Determine-Eye-Shape_36_1.txt`, `eye_capture_shape/Determine-Eye-Shape_51_1.txt`, `eye_capture_shape/Determine-Eye-Shape_57_1.txt`, `eye_capture_shape/Determine-Eye-Shape_65_1.txt`
  - `eye_capture_shape/Determine-Eye-Shape_32_1.txt`:
```text
Shape-Step-1-Version-2.jpg","smallWidth":460,"smallHeight":345,"bigWidth":728,"bigHeight":546,"licensing":"<div class=\"mw-parser-output\"><p>\u00a9 2024 wikiHow, Inc. All rights reserved. wikiHow, Inc. is the copyright …
```
  - `eye_capture_shape/Determine-Eye-Shape_36_1.txt`:
```text
Eye-Shape-Step-3-Version-2.jpg","smallWidth":460,"smallHeight":345,"bigWidth":728,"bigHeight":546,"licensing":"<div class=\"mw-parser-output\"><p>\u00a9 2024 wikiHow, Inc. All rights reserved. wikiHow, Inc. is the copyri…
```

## C. Hội thoại / query

### ✅ Query rỗng
- Không phát hiện.

### ✅ Query trùng nhau
- Không phát hiện.

### ✅ Query quá ngắn (≤ 2 từ)
- Không phát hiện.

### ✅ Query quá dài (> 60 từ)
- Không phát hiện.

### ❌ Turn đầu có đại từ/liên từ lơ lửng — 2

- `74_turn_1`: In birch trees, how does their white bark protect them from sunlight and temperature swings?
- `75_turn_1`: In finger movement, why is it harder to move the ring finger independently compared to the others?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 56

- `2_turn_3`: I wonder if everyone’s nose picks up those 'primary smells' the same way, or does it vary a lot?
- `3_turn_3`: Is it usually about which paw they use more, or are some animals just better with one paw?
- `3_turn_5`: Is it possible for a species to have lots of individual preferences but no clear trend across the whole group?
- `3_turn_6`: Does the paw they pick change if they're playing versus trying to climb or grab food?
- `3_turn_7`: Is it true that parrots mostly use their left foot when eating, or is that just in some species?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 12

- `2_turn_2`: Oh, does having so many inactive smell receptors mean we’re actually missing out on some scents?
- `6_turn_6`: Why wouldn’t living longer help if there’s a lot of danger in the environment?
- `14_turn_4`: What about when someone has a condition that makes them see these flashes all the time—how is that different?
- `25_turn_3`: What about serotonin—does it actually make you feel more tired when you’ve been thinking hard for a while?
- `25_turn_4`: And does that mental tiredness actually make your body feel more sluggish too?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 26

- `2_turn_3` (cos=0.0)
  - trước: Oh, does having so many inactive smell receptors mean we’re actually missing out on some scents?
  - sau: I wonder if everyone’s nose picks up those 'primary smells' the same way, or does it vary a lot?
- `3_turn_6` (cos=0.0)
  - trước: Is it possible for a species to have lots of individual preferences but no clear trend across the whole group?
  - sau: Does the paw they pick change if they're playing versus trying to climb or grab food?
- `3_turn_7` (cos=0.0)
  - trước: Does the paw they pick change if they're playing versus trying to climb or grab food?
  - sau: Is it true that parrots mostly use their left foot when eating, or is that just in some species?
- `3_turn_8` (cos=0.0)
  - trước: Is it true that parrots mostly use their left foot when eating, or is that just in some species?
  - sau: Do frogs and toads actually show a clear side preference with their legs or eyes?
- `3_turn_10` (cos=0.0)
  - trước: How do they actually test for handedness in primates? Is it always the same kind of task?
  - sau: Is it true that fish will check things out with just one eye first?

## D. Gold / qrels

### ✅ Gold mồ côi (doc không có trong corpus)
- Không phát hiện.

### ✅ qrels qid không khớp turn nào
- Không phát hiện.

### ✅ Gold inline (benchmark) ≠ qrels
- Không phát hiện.

### ✅ Turn không có gold
- Không phát hiện.

### ❌ Gold doc có lỗi nội dung nghiêm trọng — 1

- `animals_handedness/Laterality_2.txt` ['boilerplate']
```text
In other animals[edit] It has been shown that cerebral lateralization is a widespread phenomenon in the animal kingdom. Functional and structural differences between left and right brain hemispheres c…
```

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 10

- `7_turn_3` (pronoun) gold=['cracking_joint/Crepitus_0.txt']: Have they ever found any real downsides to cracking your joints a lot over time?
- `32_turn_2` (pronoun) gold=['drink_sea_water/osmolality_of_human_blood_0.txt']: Is that why drinking seawater actually makes you feel even thirstier?
- `32_turn_3` (standalone) gold=['drink_sea_water/osmolality_of_human_blood_0.txt']: How do our kidneys actually deal with all that extra salt from seawater?
- `44_turn_1` (standalone) gold=['human_fear_dark/fear_response_dark_2.txt']: In fear responses, why do things seem scarier at night compared to during the day?
- `44_turn_2` (pronoun) gold=['human_fear_dark/fear_response_dark_2.txt']: Is it something about the amygdala acting differently at night that makes us jumpier during scary movies?

### ❌ Bằng chứng nằm muộn (> 1500 ký tự) — 39

- `33_turn_2` offset=12078c gold=`human_monogamy/Infidelity_1.txt`
  - query: What about all the people in open relationships—doesn’t that kind of throw a wrench in the idea that monogamy is just na…
  - bằng chứng: Symons (1979) determined that sexual jealousy is the major reason that many homosexual men are unsuccessful in maintaining monogamous relationships and suggests…
- `3_turn_9` offset=7488c gold=`animals_handedness/Laterality_2.txt`
  - query: How do they actually test for handedness in primates? Is it always the same kind of task?
  - bằng chứng: Emei music frogs (Babina daunchina) have a right-ear preference for positive or neutral signals such as a conspecific's advertisement call and white noise, but …
- `3_turn_10` offset=7488c gold=`animals_handedness/Laterality_2.txt`
  - query: Is it true that fish will check things out with just one eye first?
  - bằng chứng: Emei music frogs (Babina daunchina) have a right-ear preference for positive or neutral signals such as a conspecific's advertisement call and white noise, but …
- `3_turn_1` offset=6913c gold=`animals_handedness/Laterality_2.txt`
  - query: In animal behavior, do invertebrates also show a preference for one side like handedness in mammals?
  - bằng chứng: Fish which show a right-eye preference in the mirror test prefer to be on the left side of the school.
- `3_turn_8` offset=6913c gold=`animals_handedness/Laterality_2.txt`
  - query: Do frogs and toads actually show a clear side preference with their legs or eyes?
  - bằng chứng: Fish which show a right-eye preference in the mirror test prefer to be on the left side of the school.

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 15

- `2_turn_2` OOV=['scents']: Oh, does having so many inactive smell receptors mean we’re actually missing out on some scents?
- `7_turn_3` OOV=['downsides']: Have they ever found any real downsides to cracking your joints a lot over time?
- `14_turn_5` OOV=['shut']: Is it the optic nerve itself sending out weird signals when that happens, even with your eyes shut?
- `25_turn_4` OOV=['sluggish']: And does that mental tiredness actually make your body feel more sluggish too?
- `32_turn_2` OOV=['thirstier']: Is that why drinking seawater actually makes you feel even thirstier?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 3

*nguyên nhân: {'lexical_gap (overlap<0.2)': 3}*

- `44_turn_1` ti=0 ctx=standalone overlap=0.0: In fear responses, why do things seem scarier at night compared to during the day?
  - gold ['human_fear_dark/fear_response_dark_2.txt'] | top3 ['mechanism_mentally_tired/Fatigue_5.txt', 'tooth_paste_teeth/fluoridetoothpasteis_60_0.txt', 'mechanism_mentally_tired/Mental_disorder_0_98.txt']
- `32_turn_1` ti=0 ctx=standalone overlap=0.111: In drinking seawater, why can't our bodies handle the salt compared to our blood?
  - gold ['drink_sea_water/osmolality_of_human_blood_0.txt'] | top3 ['feel_excess_pressure/Baroreceptor_2.txt', 'wake_up_wrong/Sleep_inertia_2.txt', 'human_cats_blue_eyes/cat-breeds-with-blue-eyes_130_0.txt']
- `56_turn_1` ti=0 ctx=standalone overlap=0.111: In cell membranes, what actually keeps the two layers from just falling apart?
  - gold ['cell_membrane_break_apart/Entropic_force_2.txt'] | top3 ['yeast_dissolve_in_sugar/Osmosis_0.txt', 'eyes_smooth_transition/howtocreateseamlesst_42_0.txt', 'sense_dimmed_sleep/therelationshipbetwe_98_0.txt']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.