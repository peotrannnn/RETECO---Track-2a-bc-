# Báo cáo chất lượng dữ liệu — domain `medicalsciences`

*Tạo lúc 2026-11-21T09:06:40 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 93.3 🟢** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 98.6 | 🟢 |
| content | 0.25 | 95.0 | 🟢 |
| conversation | 0.15 | 69.2 | 🔴 |
| gold | 0.25 | 100.0 | 🟢 |
| link | 0.15 | 96.5 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 30.77 | 1 | 30.77 |
| link | % turn gold không chia sẻ từ nào với query | 2.27 | 1.5 | 3.41 |
| content | % nghi không phải tiếng Anh | 3.68 | 0.5 | 1.84 |
| integrity | % doc có mojibake | 0.69 | 2 | 1.38 |
| content | % doc quá ngắn | 1.85 | 0.5 | 0.93 |
| content | % lặp bất thường | 1.8 | 0.5 | 0.9 |
| content | % boilerplate | 1.61 | 0.3 | 0.48 |
| content | % gần trùng (ngoài trùng chính xác) | 0.45 | 0.7 | 0.32 |
| content | % ký hiệu lạ/URL nặng | 0.62 | 0.4 | 0.25 |
| content | % chứa PII (email/phone) | 2.33 | 0.1 | 0.23 |
| link | % OOV trung bình của query | 0.17 | 0.3 | 0.05 |
| content | % HTML sót | 0.06 | 0.4 | 0.02 |

## 2. Khuyến nghị

- **[medium]** 0.69% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 1.85%.
- **[low]** 3.68% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 70.97% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 4 hội thoại có đại từ/liên từ ở turn đầu.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **23,297** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.69% | ký tự điều khiển 0.0% | HTML/entity sót 0.06%
- Benchmark: 13 hội thoại | schema=`qa_pair` | vai trò {'user': 44, 'assistant': 44} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 44/44
- qrels: 101 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 101} | qid 44

## 4. Chất lượng nội dung

- Ký tự: min=26 p25=361.0 **median=830.0** mean=1031.8 p75=1711.0 p90=2059.0 p99=2878.0 max=10027 | outlier dài (>5761.0c): 0.03%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 41.88% / 48.85% / 70.6% / 99.91%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 5.88% |
| 101-300 | 15.02% |
| 301-650 | 20.99% |
| 651-800 | 6.97% |
| 801-1500 | 21.75% |
| 1501-3000 | 29.3% |
| 3001-6000 | 0.07% |
| >6000 | 0.02% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 430 | 1.85% |
| mojibake | lỗi encoding (mojibake) | 161 | 0.69% |
| control_chars | ký tự điều khiển | 0 | 0.0% |
| html_residue | HTML/entity còn sót | 13 | 0.06% |
| boilerplate | boilerplate/menu/footer | 374 | 1.61% |
| url_heavy | URL chiếm >25% nội dung | 145 | 0.62% |
| symbol_heavy | ký hiệu lạ >30% | 1 | 0.0% |
| repetitive | lặp từ/dòng bất thường | 419 | 1.8% |
| non_english | nghi không phải tiếng Anh | 857 | 3.68% |
| pii_email | chứa email | 192 | 0.82% |
| pii_phone | chứa số điện thoại | 352 | 1.51% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 2829 | 12.14% |
| starts_lower | bắt đầu bằng chữ thường | 324 | 1.39% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **9.05%**
- Trùng chính xác: 0 doc dư (0.0%), 0 nhóm
- Gần trùng: 72 cụm | doc dư gần-trùng ngoài trùng chính xác 88 (0.45%) | cụm lớn nhất 5
- Từ vựng (mẫu 10,028 doc): 60,046 từ | hapax 45.65% | Zipf -0.905 | s(5963), may(4709), 1(4592), patients(3866), 2(3676), health(3582), these(3380), more(3192), also(3138), other(2965), 3(2941), blood(2938), risk(2763), such(2597), treatment(2590)

## 5. Hội thoại

- **13** hội thoại, **44** turn | turn/hội thoại: mean 3.38 (min 3, max 6) | query: mean 18.1 từ, median 18.0, p95 21.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 22 | 50.0% |
| pronoun | 19 | 43.18% |
| connector | 3 | 6.82% |
| short_ellipsis | 0 | 0% |

→ **70.97%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 4 (30.77%)
- Chuyển chủ đề: {'weak': 41.94, 'on_topic': 45.16, 'shift': 12.9} | hội thoại nhảy chủ đề ≥50% turn: 15.38%

**Loại câu hỏi:** statement_other 45.45%, yes_no 43.18%, what 4.55%, how 4.55%, wh_other 2.27%

## 6. Gold / qrels

- Nguồn gold: {'inline': 44} | qrels được dùng để eval: False
- Gold/turn: mean 2.3, max 5
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 44/44 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 23,248/23,297 (99.79%) | Gini 0.2809
- Độ dài gold vs corpus (median): 795.0 vs 830.0 (tỷ lệ 0.96x)
- Gold có lỗi nghiêm trọng: 0.0% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.282** (có history: 0.23) | overlap=0: 2.27% | <20%: 29.55% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.357, 'pronoun': 0.203, 'connector': 0.232}
- OOV: 2.27% (TB 0.17%)
- **Vị trí bằng chứng** (44 mẫu): {'0-20%': 54.55, '20-40%': 9.09, '40-60%': 20.45, '60-80%': 11.36, '80-100%': 4.55} | median offset 111c | sau 650c: 18.18% | sau 512 token: 0.0%

## 8. BM25 baseline

- 44 query | 49 gold + 200 nhiễu
- nDCG@10 single/history = 0.5725/0.6846 | Recall@10 = 0.6822/0.8814

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 13 | 0.8018 | 0.8018 | 0.9462 | 0.9462 |
| 2 | 13 | 0.5683 | 0.5409 | 0.7372 | 0.8526 |
| 3 | 13 | 0.4914 | 0.6386 | 0.5615 | 0.8 |
| 4 | 3 | 0.2866 | 0.9783 | 0.1944 | 1.0 |
| 5+ | 2 | 0.0651 | 0.7153 | 0.125 | 1.0 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 3 | 0.6462 | 0.8348 | 0.5556 | 1.0 |
| pronoun | 19 | 0.3586 | 0.5881 | 0.4816 | 0.8254 |
| standalone | 22 | 0.7471 | 0.7475 | 0.8727 | 0.9136 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 2 | 0.4419 | 0.8641 | 0.5 | 1.0 |
| statement_other | 20 | 0.703 | 0.7688 | 0.7883 | 0.935 |
| wh_other | 1 | 0.8503 | 1.0 | 1.0 | 1.0 |
| what | 2 | 0.5877 | 0.5801 | 0.75 | 0.75 |
| yes_no | 19 | 0.4326 | 0.5715 | 0.5658 | 0.8202 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 13 | 0.8018 | 0.8018 | 0.9462 | 0.9462 |
| on_topic | 14 | 0.5546 | 0.5822 | 0.725 | 0.7929 |
| shift | 4 | 0.0 | 0.7453 | 0.0 | 1.0 |
| weak | 13 | 0.5386 | 0.659 | 0.5821 | 0.8756 |

- Turn khó: **1** (2.27%) — {'lexical_gap (overlap<0.2)': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 139 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 430

**`medicalsciences_ex_32541_neg_5`** (38 ký tự)
```text
All Rights Reserved. | About this site
```
**`medicalsciences_ex_33725_neg_189`** (26 ký tự)
```text
[ PubMed : 18279736 ] 581.
```
**`medicalsciences_ex_32169_google_neg_21`** (31 ký tự)
```text
We have no competing interests.
```
**`medicalsciences_ex_32169_google_neg_232`** (35 ký tự)
```text
Correspondence to Olivier Castagna.
```
**`medicalsciences_ex_32169_google_neg_258`** (40 ký tự)
```text
This article was published in Perfusion.
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 161

**`medicalsciences_ex_33726_neg_2`** (1911 ký tự)
```text
There are no data on the use of AREXVY in pregnant or breastfeeding individuals. AREXVY is not approved for use in persons <50 years of age. Vaccination with AREXVY may not result in protection of all vaccine recipients.…
```
**`medicalsciences_ex_33726_neg_6`** (1413 ký tự)
```text
The GSK proprietary AS01 adjuvant system contains QS-21 StimulonÂ® adjuvant licensed from Antigenics LLC, a wholly owned subsidiary of Agenus Inc. (NASDAQ: AGEN), MPL and liposomes. Harpaz R, et al. Advisory Committee on…
```
**`medicalsciences_ex_33726_neg_9`** (1803 ký tự)
```text
Healthcare Providers: RSV Vaccination for Adults 60 Years of Age and Over | CDC Skip directly to site content Skip directly to search EspaÃ±ol | Other Languages An official website of the United States government Here's …
```
**`medicalsciences_ex_33729_neg_12`** (1886 ký tự)
```text
The Vi polysaccharide vaccine is administered as a single injection and is approved for adults and children aged â¥2 years. The oral Ty21a vaccine is administered in 4 doses on alternating days over 1 week and is approv…
```
**`medicalsciences_ex_33729_neg_23`** (1554 ký tự)
```text
Breathing problems or wheezing Racing heart Fever or general ill feeling Swollen lymph nodes Swelling of the face, lips, mouth, tongue, or throat Trouble swallowing or throat tightness Itching, skin rash, or pale red bum…
```

### ✅ `control_chars` — ký tự điều khiển
- Không phát hiện.

### ❌ `html_residue` — HTML/entity còn sót — 13

**`medicalsciences_ex_32541_google_neg_458`** (767 ký tự)
```text
Figure 18. (A) The semi-infinite regime of an electrochemical cell, (B) the transmission line (TL) depiction of the semi-infinite regime, (C) finite boundary diffusion at t < td spans, (D) transmissive, and (E) reflectiv…
```
**`medicalsciences_ex_32541_google_neg_478`** (241 ký tự)
```text
Figure 18. (A) The semi-infinite regime of an electrochemical cell, (B) the transmission line (TL) depiction of the semi-infinite regime, (C) finite boundary diffusion at t < td spans, (D) transmissive, and (E) reflectiv…
```
**`medicalsciences_ex_34233_google_neg_166`** (423 ký tự)
```text
Star 5 (5) You must be signed in to star a gist Fork 0 (0) You must be signed in to fork a gist Embed Select an option Embed Embed this gist in your website. Share Copy sharable link for this gist. Clone via HTTPS Clone …
```
**`medicalsciences_ex_34468_google_neg_185`** (424 ký tự)
```text
What you need to know about data mining and data-analytic thinking Foster Provost and Tom Fawcett | 5.00 Kirk BorneGreat book for Business Analytics and for building #AnalyticThinking &gt;&gt; â#DataScience for Busines…
```
**`medicalsciences_ex_34468_google_neg_186`** (346 ký tự)
```text
Kirk BorneRecent top-selling books in #AI &amp; #MachineLearning: https://t.co/Ij9I7SzR4d âââââ #BigData #DataScience #DataMining #Algorithms #PredictiveAnalytics #Python âââââ ...in the TOP 10: 1)The…
```

### ❌ `boilerplate` — boilerplate/menu/footer — 374

**`medicalsciences_ex_32347_neg_0`** (1613 ký tự)
```text
Reversible cataract after exposure to distilled water: a case report | BMC Ophthalmology Skip to main content BMC journals have moved to Springer Nature Link. Learn more about website changes. Reversible cataract after e…
```
**`medicalsciences_ex_32347_neg_13`** (1850 ký tự)
```text
Written informed consent was obtained from the patient. Consent for publication Full verbal and written consent has been obtained from the patient for submission of this manuscript for publication. Competing interests Th…
```
**`medicalsciences_ex_32347_neg_14`** (1870 ký tự)
```text
How To Use Emergency Eye Wash [First Aid Guide] Skip to Content Home How To: How To Use Emergency Eye Wash [First Aid Guide] In an emergency, eye injuries can happen without warning, often leaving people panicked and uns…
```
**`medicalsciences_ex_32347_neg_19`** (1969 ký tự)
```text
Saline Solution: What It Is, Types & Uses Home / Health Library / Medical Treatments / Saline Solution Advertisement Advertisement Saline Solution Saline solution is a mixture of salt and water that you can use to rinse …
```
**`medicalsciences_ex_32347_neg_20`** (1965 ký tự)
```text
This is because normal saline and human blood have the same balance of water and salt. What is saline solution used for? You can use saline solution to manage a wide range of health concerns from day to day. Below are so…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 145

**`medicalsciences_ex_32169_neg_12`** (327 ký tự)
```text
Wayback Machine 6 captures 08 Jun 2022 - 17 Oct 2025 Sep OCT Nov 17 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Common Crawl Web crawl data from Common Crawl. TIMESTAMPS The Wayback Machine - …
```
**`medicalsciences_ex_32347_neg_24`** (337 ký tự)
```text
Wayback Machine 5 captures 20 Oct 2016 - 14 Feb 2025 Jan FEB Mar 14 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Common Crawl Web crawl data from Common Crawl. TIMESTAMPS The Wayback Machine - …
```
**`medicalsciences_ex_33988_neg_7`** (1074 ký tự)
```text
Learn More References: https://blog.famicity.com/2017/12/what-are-double-cousins/?lang=en http://familypedia.wikia.com/wiki/Double_first_cousin https://www.famlii.com/what-is-a-double-cousin-genetically https://www.famli…
```
**`medicalsciences_ex_32169_google_neg_102`** (517 ký tự)
```text
Anatomy & Physiology. Provided by: OpenStax CNX. Located at: http://cnx.org/contents/14fb4ad7-39a1-4eee-ab6e-3ef2482e3e22@8.25. License: CC BY: Attribution. License Terms: Download for free at http://cnx.org/contents/14f…
```
**`medicalsciences_ex_32169_google_neg_254`** (377 ký tự)
```text
See the Australian Guidelines for Aquatic Physiotherapists Working in and/or Managing Hydrotherapy Pools for a description on what the Physiotherapist needs to consider with hydrotherapy. https://www.hydroworx.com/blog/h…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 1

**`medicalsciences_ex_32435_google_neg_399`** (184 ký tự)
```text
3. [latex]{}_{\text{42}}^{\text{99}}{\text{Mo}}_{\text{57}}\to {}_{\text{43}}^{\text{99}}{\text{Tc}}_{\text{56}}+{\beta }^{-}+{\bar{v}}_{e}\\[/latex] 7. (a) 6.958 MeV (b) 5.7 × 10−10 g
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 419

**`medicalsciences_ex_34095_doc_1`** (259 ký tự)
```text
ACR = albumin (mg/L) ÷ creatinine (g/L) → mg/g; or albumin (mg/L) ÷ creatinine (mmol/L) → mg/mmol. PCR = protein (mg/L) ÷ creatinine (g/L) → mg/g; or protein (mg/L) ÷ creatinine (mmol/L) → mg/mmol. Conversions: mg/g = mg…
```
**`medicalsciences_ex_32169_neg_9`** (1968 ký tự)
```text
Pulmonary oedema in healthy SCUBA divers: new physiopathological pathways. Clin. Physiol. Funct. Imaging 30, 181–186. doi: 10.1111/j.1475-097X.2010.00922.x PubMed Abstract | CrossRef Full Text | Google Scholar Koehle, M.…
```
**`medicalsciences_ex_32347_neg_12`** (1963 ký tự)
```text
Reversible cataract as the presenting sign of diabetes mellitus: report of two cases and literature review. Iran J Pediatr. 2012;22(1):125–8. PubMed PubMed Central Google Scholar Jacob TJC, Duncan G. Glucose-induced memb…
```
**`medicalsciences_ex_32427_neg_34`** (1854 ký tự)
```text
[ DOI ] [ PubMed ] [ Google Scholar ] 16. Roberts SCM, Mericle AA, Mubbaraman MS, et al. State policies targeting alcohol use during pregnancy and alcohol use among pregnant women 1985–2016: evidence from the behavioral …
```
**`medicalsciences_ex_32427_neg_35`** (1856 ký tự)
```text
American Medical Association: Preventing, Identifying & Treating Violence & Abuse.Americ https://www.ama-assn.org/delivering-care/ethics/preventing-identifying-treating-violence-abuse . Accessed November 12, 2019. 24. Am…
```

### ❌ `non_english` — nghi không phải tiếng Anh — 857

**`medicalsciences_ex_34095_doc_1`** (259 ký tự)
```text
ACR = albumin (mg/L) ÷ creatinine (g/L) → mg/g; or albumin (mg/L) ÷ creatinine (mmol/L) → mg/mmol. PCR = protein (mg/L) ÷ creatinine (g/L) → mg/g; or protein (mg/L) ÷ creatinine (mmol/L) → mg/mmol. Conversions: mg/g = mg…
```
**`medicalsciences_ex_34095_doc_2`** (276 ký tự)
```text
Quick unit harmonization The calculator accepts common lab units and converts automatically. - mg/dL → mg/L: ×10 - Creatinine mg/dL → g/L: ×0.01 - µmol/L → mmol/L: ÷1000 - µg/mL = mg/L - Creatinine MW ≈ 113.12 mg/mmol - …
```
**`medicalsciences_ex_34486_doc_2`** (309 ký tự)
```text
Thoracic spinal cord - Thinner, because ventral gray horns contain fewer motor neurons - Dorsal median sulcus and dorsolaterally sulci bilaterally form dorsal columns - Fasciculus gracilis (lower extremity afferent pathw…
```
**`medicalsciences_ex_32169_neg_12`** (327 ký tự)
```text
Wayback Machine 6 captures 08 Jun 2022 - 17 Oct 2025 Sep OCT Nov 17 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Common Crawl Web crawl data from Common Crawl. TIMESTAMPS The Wayback Machine - …
```
**`medicalsciences_ex_32169_neg_22`** (1973 ký tự)
```text
Front Physiol . 19 (12) 699493. doi : 10.3389/fphys.2021.699493 . PMC 8326965 . PMID 34349668 . ^ Nishiyama, Akira; Kitada, Kento; Suzuki, Miwa (2022). "Blood pressure adaptation in vertebrates: comparative biology" . Ki…
```

### ❌ `pii_email` — chứa email — 192

**`medicalsciences_ex_32427_neg_1`** (1821 ký tự)
```text
The contents are intended for general information purposes only, and readers are encouraged to consult their own attorney concerning their specific situation and specific legal questions. Find articles by Wendy Keegan 1 …
```
**`medicalsciences_ex_32427_neg_11`** (1954 ký tự)
```text
Mandatory and permissive reporting laws: obligations, challenges, moral dilemmas, and opportunities - PMC Skip to main content Official websites use .gov A .gov website belongs to an official government organization in t…
```
**`medicalsciences_ex_32427_neg_7`** (1991 ký tự)
```text
20 Conclusion Though the circumstances of each patient encounter and blood draw request will be unique, this article offers some general insight into the practical effects of mandatory blood draw statutes for hospitals a…
```
**`medicalsciences_ex_32431_neg_1`** (1819 ký tự)
```text
Find articles by Charles Laing b, d , David Lorr David Lorr , BSc c Department of Neurophsiology, University of Linkoping, Sweden Find articles by David Lorr c , David A Green David A Green , PhD a Gravitational Physiolo…
```
**`medicalsciences_ex_32431_neg_22`** (1875 ký tự)
```text
Heart Rate Recovery: Coming Back Full-Circle to the Baroreceptor Reflex - PMC Skip to main content Official websites use .gov A .gov website belongs to an official government organization in the United States. Secure .go…
```

### ❌ `pii_phone` — chứa số điện thoại — 352

**`medicalsciences_ex_34638_doc_2`** (524 ký tự)
```text
Stroke (CVA) or mini-stroke (TIA) For those who have had a stroke (also called cerebrovascular accident, CVA) or a mini-stroke (also called transient ischemic attack, TIA), you must wait six (6) months before donating to…
```
**`medicalsciences_ex_32169_neg_12`** (327 ký tự)
```text
Wayback Machine 6 captures 08 Jun 2022 - 17 Oct 2025 Sep OCT Nov 17 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Common Crawl Web crawl data from Common Crawl. TIMESTAMPS The Wayback Machine - …
```
**`medicalsciences_ex_32169_neg_23`** (1215 ký tự)
```text
^ a b "Thermal Conductivity of some common Materials" . The Engineering Toolbax . Retrieved 10 October 2008 . ^ Nuckols, M.L.; Giblo, J; Wood-Putnam, J.L. (September 15–18, 2008). "Thermal Characteristics of Diving Garme…
```
**`medicalsciences_ex_32347_neg_13`** (1850 ký tự)
```text
Written informed consent was obtained from the patient. Consent for publication Full verbal and written consent has been obtained from the patient for submission of this manuscript for publication. Competing interests Th…
```
**`medicalsciences_ex_32347_neg_23`** (1520 ký tự)
```text
It’s generally safe if you follow the instructions on the bottle. Making your own is simple and inexpensive. What are the risks of using saline solution? Using saline that’s not sterile can lead to infections. When in do…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 2,829

**`medicalsciences_ex_32347_doc_1`** (671 ký tự)
```text
Distilled water is widely used in operating theaters to clean surgical instruments. Because it is transparent and odorless, it may be difficult for surgical personnel to distinguish distilled water from normal saline or …
```
**`medicalsciences_ex_32431_doc_2`** (802 ký tự)
```text
In the current issue of Circulation Research, McCrory et al report on the association of heart rate recovery following simple orthostatic challenge – otherwise known as "standing up" – with all-cause mortality.[1](#R1) T…
```
**`medicalsciences_ex_32435_doc_2`** (228 ký tự)
```text
Disadvantages of gamma rays compared with X-rays - Poorer quality radiographs - Exposure times can be longer - Sources need replacing - Radiation cannot be switched off - Poorer geometric unsharpness - Remote handling ne…
```
**`medicalsciences_ex_32591_doc_2`** (685 ký tự)
```text
Gonorrhea is a sexually transmitted infection (STI) caused by the bacterium Neisseria gonorrhoeae. Following transmission, N. gonorrhoeae infects mucosa of exposed anatomic sites, such as the urogenital tract, rectum, ph…
```
**`medicalsciences_ex_33726_doc_2`** (1323 ký tự)
```text
GSK plc (LSE/NYSE: GSK) today announced positive topline data from the phase 3 trial in adults 50 years and older evaluating the immunogenicity, reactogenicity and safety of AREXVY (Respiratory Syncytial Virus Vaccine, A…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 324

**`medicalsciences_ex_32239_doc_3`** (858 ký tự)
```text
how much (more) time you need to learn Dutch and possibly also English at the required language levels: learning Dutch at the right level takes on average one and a half to two years; how quickly you can collect all docu…
```
**`medicalsciences_ex_33863_doc_0`** (2101 ký tự)
```text
visceral sensation Most of the time we go through our daily lives without being consciously aware of the events occurring continuously in our internal organs, or viscera — the heart, lungs, stomach, intestines, kidney, e…
```
**`medicalsciences_ex_33988_doc_1`** (847 ký tự)
```text
double first cousins share the same amount of DNA that you would share with a grandparent, a half-sibling or an aunt or uncle. And they transfer this genetic closeness to their offspring: children of double first cousins…
```
**`medicalsciences_ex_32169_neg_24`** (8601 ký tự)
```text
v t e Major branches of physics Divisions Pure Applied Engineering Approaches Experimental Theoretical Computational Classical Classical mechanics Newtonian Analytical Celestial Continuum Acoustics Classical electromagne…
```
**`medicalsciences_ex_32427_neg_5`** (1979 ký tự)
```text
shall be civilly liable in damages to the person tested unless for gross negligence, willful or wanton act, or omission.” A provider’s decision to comply with police orders against a patient’s expressed wishes might be u…
```

### ✅ Trùng chính xác
- Không phát hiện.

### ❌ Gần trùng (khác nhau chút ít) — 88

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 5: `medicalsciences_ex_34486_google_neg_145`, `medicalsciences_ex_34486_google_neg_307`, `medicalsciences_ex_34486_google_neg_318`, `medicalsciences_ex_34486_google_neg_366`, `medicalsciences_ex_34486_google_neg_85`
  - `medicalsciences_ex_34486_google_neg_145`:
```text
The iconic gray mantle of the human brain, which appears to make up most of the mass of the brain, is the cerebrum (Figure 13.6). The wrinkled portion is the cerebral cortex, and the rest of the structure is beneath that…
```
  - `medicalsciences_ex_34486_google_neg_307`:
```text
The iconic gray mantle of the human brain, which appears to make up most of the mass of the brain, is the cerebrum (Figure 1). The wrinkled portion is the cerebral cortex, and the rest of the structure is beneath that ou…
```
- cụm size 4: `medicalsciences_ex_32431_google_neg_358`, `medicalsciences_ex_34029_google_neg_111`, `medicalsciences_ex_34029_google_neg_329`, `medicalsciences_ex_34711_google_neg_241`
  - `medicalsciences_ex_32431_google_neg_358`:
```text
PDF [403 KB]PDF [403 KB] FiguresFigure ViewerDownload Figures (PPT) Download Figures (PPT) SaveAdd To Online LibraryPowered ByMendeleyAdd To My Reading ListExport CitationCreate Citation Alert Add To Online LibraryPowere…
```
  - `medicalsciences_ex_34029_google_neg_111`:
```text
FiguresFigure ViewerDownload Figures (PPT) Download Figures (PPT) SaveAdd To Online LibraryPowered ByMendeleyAdd To My Reading ListExport CitationCreate Citation Alert Add To Online LibraryPowered ByMendeley Add To My Re…
```
- cụm size 4: `medicalsciences_ex_34029_google_neg_121`, `medicalsciences_ex_34467_google_neg_581`, `medicalsciences_ex_34467_google_neg_583`, `medicalsciences_ex_34467_google_neg_584`
  - `medicalsciences_ex_34029_google_neg_121`:
```text
You are free to share(copy and redistribute) this article in any medium or format and to adapt(remix, transform, and build upon) the material for any purpose, even commercially within the parameters below: Creative Commo…
```
  - `medicalsciences_ex_34467_google_neg_581`:
```text
You are free to share (copy and redistribute) this article in any medium or format and to adapt (remix, transform, and build upon) the material for any purpose, even commercially within the parameters below: Creative Com…
```
- cụm size 4: `medicalsciences_ex_34486_google_neg_147`, `medicalsciences_ex_34486_google_neg_308`, `medicalsciences_ex_34486_google_neg_321`, `medicalsciences_ex_34486_google_neg_367`
  - `medicalsciences_ex_34486_google_neg_147`:
```text
The diencephalon is the one region of the adult brain that retains its name from embryologic development. The etymology of the word diencephalon translates to âthrough brain.â It is the connection between the cerebru…
```
  - `medicalsciences_ex_34486_google_neg_308`:
```text
The diencephalon is the one region of the adult brain that retains its name from embryologic development. The etymology of the word diencephalon translates to “through brain.” It is the connection between the cerebrum an…
```
- cụm size 4: `medicalsciences_ex_34486_google_neg_148`, `medicalsciences_ex_34486_google_neg_309`, `medicalsciences_ex_34486_google_neg_323`, `medicalsciences_ex_34486_google_neg_368`
  - `medicalsciences_ex_34486_google_neg_148`:
```text
The midbrain and hindbrain (composed of the pons and the medulla) are collectively referred to as the brain stem (Figure 13.12). The structure emerges from the ventral surface of the forebrain as a tapering cone that con…
```
  - `medicalsciences_ex_34486_google_neg_309`:
```text
The midbrain and hindbrain (composed of the pons and the medulla) are collectively referred to as the brain stem (Figure 7). The structure emerges from the ventral surface of the forebrain as a tapering cone that connect…
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

### ❌ Turn đầu có đại từ/liên từ lơ lửng — 4

- `ex_34651_turn_1`: In glucose meters, how come they only pick up glucose and not other sugars like sucrose in water?
- `ex_34029_turn_1`: In erythropoietic protoporphyria, why is it so hard to treat the disease by just giving the missing ferrochelatase enzyme?
- `ex_33726_turn_1`: In vaccine safety, is it okay for people to get SHINGRIX at the same time as TWINRIX or AREXVY, or is there a higher risk of side effects?
- `ex_32435_turn_1`: In medical radiography, does it matter that gamma rays come from the nucleus while x-rays come from outside it?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 19

- `ex_34769_turn_2`: Is it harder to stick to a diet when you’re sleep-deprived because you feel hungrier or less satisfied after meals?
- `ex_34769_turn_3`: I wonder if losing sleep makes it easier to put the weight back on, even after dieting?
- `ex_34719_turn_2`: Is it the leftover oxygen in your lungs that lets you stay conscious longer when you hold your breath?
- `ex_34687_turn_3`: Are there any cases where you actually shouldn’t do regular CPR if someone’s had open heart surgery?
- `ex_34651_turn_2`: Is there something about the structure of sucrose that makes it invisible to the enzyme in the meter?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 3

- `ex_34651_turn_3`: Oh, so is it the hydrogen peroxide part that actually triggers the meter’s reading?
- `ex_34651_turn_4`: And does the oxygen part in that reaction explain why the meter just ignores sucrose in water?
- `ex_32435_turn_3`: Now I’m curious—how is gamma radiation actually used in medicine if it’s not for regular scans?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 4

- `ex_34599_turn_3` (cos=0.0)
  - trước: Is there any idea how a vaccine could even trigger long COVID symptoms, biologically speaking?
  - sau: I wonder if not having those big controlled trials makes it harder to trust the results?
- `ex_34296_turn_5` (cos=0.0)
  - trước: Are there things those standard tests just can’t pick up if the trigger is something like cold shock?
  - sau: Is it even practical to do this kind of test in a regular clinic, or would it be too risky?
- `ex_33726_turn_3` (cos=0.0)
  - trước: Are there any studies coming up that look at mixing SHINGRIX with other vaccines like the flu or COVID shots?
  - sau: Do they need to be given in different spots if you get them together?
- `ex_32435_turn_2` (cos=0.0)
  - trước: In medical radiography, does it matter that gamma rays come from the nucleus while x-rays come from outside it?
  - sau: Would using something that powerful make it harder to get clear images for everyday scans?

## D. Gold / qrels

### ✅ Gold mồ côi (doc không có trong corpus)
- Không phát hiện.

### ✅ qrels qid không khớp turn nào
- Không phát hiện.

### ✅ Gold inline (benchmark) ≠ qrels
- Không phát hiện.

### ✅ Turn không có gold
- Không phát hiện.

### ✅ Gold doc có lỗi nội dung nghiêm trọng
- Không phát hiện.

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 1

- `ex_32435_turn_2` (pronoun) gold=['medicalsciences_ex_32435_doc_2']: Would using something that powerful make it harder to get clear images for everyday scans?

### ✅ Bằng chứng nằm muộn (> 1500 ký tự)
- Không phát hiện.

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 1

- `ex_34769_turn_2` OOV=['hungrier']: Is it harder to stick to a diet when you’re sleep-deprived because you feel hungrier or less satisfied after meals?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 1

*nguyên nhân: {'lexical_gap (overlap<0.2)': 1}*

- `ex_34599_turn_2` ti=1 ctx=pronoun overlap=0.1: Is there any idea how a vaccine could even trigger long COVID symptoms, biologically speaking?
  - gold ['medicalsciences_ex_34599_doc_3'] | top3 ['medicalsciences_ex_34599_doc_0', 'medicalsciences_ex_34599_neg_54', 'medicalsciences_ex_34599_doc_2']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.