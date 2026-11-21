# Báo cáo chất lượng dữ liệu — domain `law`

*Tạo lúc 2026-11-21T09:06:14 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 95.1 🟢** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 98.7 | 🟢 |
| content | 0.25 | 96.2 | 🟢 |
| conversation | 0.15 | 86.7 | 🟢 |
| gold | 0.25 | 100.0 | 🟢 |
| link | 0.15 | 88.5 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 13.33 | 1 | 13.33 |
| link | % turn gold không chia sẻ từ nào với query | 7.58 | 1.5 | 11.37 |
| integrity | % doc có mojibake | 0.66 | 2 | 1.32 |
| content | % nghi không phải tiếng Anh | 2.1 | 0.5 | 1.05 |
| content | % doc quá ngắn | 1.69 | 0.5 | 0.84 |
| content | % boilerplate | 2.6 | 0.3 | 0.78 |
| content | % gần trùng (ngoài trùng chính xác) | 0.62 | 0.7 | 0.43 |
| content | % chứa PII (email/phone) | 2.97 | 0.1 | 0.3 |
| content | % lặp bất thường | 0.52 | 0.5 | 0.26 |
| link | % OOV trung bình của query | 0.55 | 0.3 | 0.17 |
| content | % ký hiệu lạ/URL nặng | 0.26 | 0.4 | 0.1 |
| content | % HTML sót | 0.07 | 0.4 | 0.03 |

## 2. Khuyến nghị

- **[medium]** 0.66% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 1.69%.
- **[low]** 2.1% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 66.67% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 2 hội thoại có đại từ/liên từ ở turn đầu.
- **[medium]** 7.58% turn gold KHÔNG chia sẻ từ nào với query.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **20,027** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.66% | ký tự điều khiển 0.0% | HTML/entity sót 0.07%
- Benchmark: 15 hội thoại | schema=`qa_pair` | vai trò {'user': 66, 'assistant': 66} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 66/66
- qrels: 145 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 145} | qid 66

## 4. Chất lượng nội dung

- Ký tự: min=30 p25=338.0 **median=791.0** mean=997.4 p75=1634.0 p90=1998.0 p99=2868.0 max=12902 | outlier dài (>5522.0c): 0.02%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 43.46% / 50.44% / 72.11% / 99.93%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 5.38% |
| 101-300 | 16.8% |
| 301-650 | 21.28% |
| 651-800 | 6.98% |
| 801-1500 | 21.67% |
| 1501-3000 | 27.82% |
| 3001-6000 | 0.05% |
| >6000 | 0.02% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 338 | 1.69% |
| mojibake | lỗi encoding (mojibake) | 133 | 0.66% |
| control_chars | ký tự điều khiển | 0 | 0.0% |
| html_residue | HTML/entity còn sót | 15 | 0.07% |
| boilerplate | boilerplate/menu/footer | 521 | 2.6% |
| url_heavy | URL chiếm >25% nội dung | 53 | 0.26% |
| symbol_heavy | ký hiệu lạ >30% | 0 | 0.0% |
| repetitive | lặp từ/dòng bất thường | 105 | 0.52% |
| non_english | nghi không phải tiếng Anh | 421 | 2.1% |
| pii_email | chứa email | 224 | 1.12% |
| pii_phone | chứa số điện thoại | 370 | 1.85% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 1994 | 9.96% |
| starts_lower | bắt đầu bằng chữ thường | 217 | 1.08% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **7.63%**
- Trùng chính xác: 0 doc dư (0.0%), 0 nhóm
- Gần trùng: 83 cụm | doc dư gần-trùng ngoài trùng chính xác 122 (0.62%) | cụm lớn nhất 29
- Từ vựng (mẫu 10,029 doc): 37,710 từ | hapax 38.69% | Zipf -0.958 | s(11491), may(6057), any(5624), law(4701), court(4612), other(4516), 1(3756), under(3559), such(3482), all(3252), must(3157), information(3129), section(2958), 2(2941), state(2868)

## 5. Hội thoại

- **15** hội thoại, **66** turn | turn/hội thoại: mean 4.4 (min 3, max 7) | query: mean 19.1 từ, median 19.0, p95 24.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 32 | 48.48% |
| pronoun | 26 | 39.39% |
| connector | 8 | 12.12% |
| short_ellipsis | 0 | 0% |

→ **66.67%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 2 (13.33%)
- Chuyển chủ đề: {'weak': 35.29, 'on_topic': 49.02, 'shift': 15.69} | hội thoại nhảy chủ đề ≥50% turn: 13.33%

**Loại câu hỏi:** statement_other 50.0%, yes_no 33.33%, what 15.15%, why 1.52%

## 6. Gold / qrels

- Nguồn gold: {'inline': 66} | qrels được dùng để eval: False
- Gold/turn: mean 2.2, max 6
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 66/66 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 19,966/20,027 (99.7%) | Gini 0.2783
- Độ dài gold vs corpus (median): 1248.0 vs 791.0 (tỷ lệ 1.58x)
- Gold có lỗi nghiêm trọng: 0.0% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.288** (có history: 0.27) | overlap=0: 7.58% | <20%: 31.82% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.324, 'pronoun': 0.231, 'connector': 0.326}
- OOV: 7.58% (TB 0.55%)
- **Vị trí bằng chứng** (65 mẫu): {'0-20%': 35.38, '20-40%': 18.46, '40-60%': 20.0, '60-80%': 10.77, '80-100%': 15.38} | median offset 416c | sau 650c: 30.77% | sau 512 token: 0.0%

## 8. BM25 baseline

- 66 query | 61 gold + 200 nhiễu
- nDCG@10 single/history = 0.54/0.7478 | Recall@10 = 0.6596/0.8932

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 15 | 0.7737 | 0.7737 | 0.94 | 0.94 |
| 2 | 15 | 0.4517 | 0.7598 | 0.5967 | 0.8733 |
| 3 | 15 | 0.5774 | 0.7702 | 0.6667 | 0.85 |
| 4 | 10 | 0.5819 | 0.7916 | 0.69 | 1.0 |
| 5+ | 11 | 0.2529 | 0.6255 | 0.3258 | 0.8182 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 8 | 0.7184 | 0.7027 | 0.7812 | 0.9375 |
| pronoun | 26 | 0.4001 | 0.7545 | 0.5442 | 0.9006 |
| standalone | 32 | 0.6092 | 0.7536 | 0.7229 | 0.876 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| statement_other | 33 | 0.6492 | 0.7703 | 0.7682 | 0.9475 |
| what | 10 | 0.3665 | 0.6455 | 0.47 | 0.76 |
| why | 1 | 1.0 | 0.3869 | 1.0 | 0.5 |
| yes_no | 22 | 0.4343 | 0.7768 | 0.5674 | 0.8902 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 15 | 0.7737 | 0.7737 | 0.94 | 0.94 |
| on_topic | 25 | 0.5659 | 0.723 | 0.714 | 0.854 |
| shift | 8 | 0.3817 | 0.8208 | 0.4479 | 0.9375 |
| weak | 18 | 0.3798 | 0.728 | 0.4444 | 0.8889 |

- Turn khó: **2** (3.03%) — {'lexical_gap (overlap<0.2)': 2}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 164 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 338

**`law_ex_106319_neg_29`** (47 ký tự)
```text
Previous Section Table of Contents Next Section
```
**`law_ex_105160_google_neg_248`** (42 ký tự)
```text
Figure 1. Hierarchy of Legislative History
```
**`law_ex_105160_google_neg_254`** (30 ký tự)
```text
Alternative Dispute Resolution
```
**`law_ex_105160_google_neg_281`** (46 ký tự)
```text
Intellectual Property Legislation & Regulation
```
**`law_ex_105160_google_neg_325`** (46 ký tự)
```text
Section 1: Samir Parikh Section 2: Raina Haque
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 133

**`law_ex_108164_neg_18`** (1984 ký tự)
```text
You should also aim to schedule any inspections or repairs at reasonable times and work with your tenants to minimise disruption. Notice times or property inspections should generally be outlined in the tenancy agreement…
```
**`law_ex_108164_neg_24`** (630 ký tự)
```text
Find out more about the comprehensive cover provided by Total Landlord Â and help keep your property safe and secure all year round. For a competitive quote and to discuss your insurance needs call 0203 907 1779 or get y…
```
**`law_ex_105227_google_neg_222`** (1449 ký tự)
```text
A unit price contract divides project costs into specific, measurable work units. These units can include cubic meters of concrete, tons of steel, or meters of piping. Instead of receiving a lump sum, the contractor is p…
```
**`law_ex_105227_google_neg_223`** (1210 ký tự)
```text
A Guaranteed Maximum Price contract establishes a fixed cost limit for a project. This ensures the owner will not pay more than the agreed maximum amount.Â If the actual project costs come in under the GMP, the savings a…
```
**`law_ex_105227_google_neg_225`** (1786 ký tự)
```text
A design-build contract combines design and construction under a single contract, meaning one entity is responsible for both phases. This streamlines communication, reduces conflicts between designers and contractors, an…
```

### ✅ `control_chars` — ký tự điều khiển
- Không phát hiện.

### ❌ `html_residue` — HTML/entity còn sót — 15

**`law_ex_110030_neg_40`** (1946 ký tự)
```text
FBI vs. US Marshal: Differences and Tips for Careers | Indeed.com FBI vs. US Marshal: Differences and Tips for Careers Written by Indeed Editorial Team Updated December 16, 2025 Working in federal law enforcement can be …
```
**`law_ex_110030_neg_45`** (1856 ký tự)
```text
Participating in programs such as internships or job shadow opportunities may also help you learn more about your options and discover the specific skills you need before training. &nbsp; The information on this site is …
```
**`law_ex_105227_google_neg_646`** (1797 ký tự)
```text
Federally regulated financial institutions (FRFIs) engage in business and strategic arrangements with external parties—entities or individuals—to perform business activities, functions, and services or obtain goods in su…
```
**`law_ex_105227_google_neg_682`** (592 ký tự)
```text
Where necessitated by risk and/or criticality, the FRFI should establish processes to ensure that third parties with elevated levels of technology and cyber risk comply with FRFI standards—or recognized industry standard…
```
**`law_ex_105563_google_neg_51`** (2380 ký tự)
```text
The Project is proud to present the 2012 John Paul Stevens Guiding Hand of Counsel Award to George H. Kendall for his life-long commitment to ensuring justice for the men and women on death row. In addition to personally…
```

### ❌ `boilerplate` — boilerplate/menu/footer — 521

**`law_ex_105614_doc_1`** (467 ký tự)
```text
It's a frightening thought that even lawyers don't read boilerplate contracts. The general consensus seems to be: even if I did read the terms of service for any given site or application, I would still sign up anyway. S…
```
**`law_ex_105614_doc_2`** (947 ký tự)
```text
Sometimes it is simply the length and complexity of contracts that puts people off reading them. For example, assuming a reading rate of 240 words a minute, Spotify's terms of service is estimated to take about 36 minute…
```
**`law_ex_107334_doc_1`** (2547 ký tự)
```text
On May 19, 2022, the Department of Justice (DOJ) issued revisions to its existing policy for charging offenses under the Computer Fraud and Abuse Act (CFAA) (2022 CFAA Policy). The revisions state that “good-faith” secur…
```
**`law_ex_107334_doc_4`** (1888 ký tự)
```text
### Common TOS Violations Do Not Amount to CFAA Violations, but Cease-and-Desist Letters Might Impact the Analysis If the CFAA also is not triggered by violating Terms of Service (TOS) or other boilerplate contractual vi…
```
**`law_ex_105160_neg_138`** (1906 ký tự)
```text
RULE 4.2 Political and Campaign Activities of Judicial Candidates in Public Elections A judicial candidate in a nonpartisan, public election shall: Act at all times in a manner consistent with the independence , integrit…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 53

**`law_ex_105160_neg_30`** (289 ký tự)
```text
Wayback Machine 15 captures 29 Oct 2020 - 22 Nov 2025 Oct NOV Dec 22 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - https://web.archive.org…
```
**`law_ex_105244_neg_10`** (875 ký tự)
```text
18 Summer 2017) < http://www.discoverypilot.com/sites/default/files/The%20Sedona%20Conference%20TAR%20Case%20Law%20Primer.pdf > . [26] See The Sedona Conference, ‘The Sedona Conference TAR Case Law Primer’ (Vol. 18 Summe…
```
**`law_ex_105563_neg_6`** (311 ký tự)
```text
Wayback Machine 8 captures 09 Aug 2017 - 08 May 2025 Feb MAR Apr 28 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Common Crawl Web crawl data from Common Crawl. TIMESTAMPS The Wayback Machine - …
```
**`law_ex_105563_neg_8`** (440 ký tự)
```text
The Archive Team Panic Downloads are full pulldowns of currently extant websites, meant to serve as emergency backups for needed sites that are in danger of closing, or which will be missed dearly if suddenly lost due to…
```
**`law_ex_105614_neg_0`** (342 ký tự)
```text
Wayback Machine 15 captures 09 May 2016 - 23 Jul 2024 Jun JUL Aug 23 2023 2024 2025 success fail About this capture COLLECTED BY Collection: Common Crawl Web crawl data from Common Crawl. TIMESTAMPS The Wayback Machine -…
```

### ✅ `symbol_heavy` — ký hiệu lạ >30%
- Không phát hiện.

### ❌ `repetitive` — lặp từ/dòng bất thường — 105

**`law_ex_105196_neg_3`** (1930 ký tự)
```text
Request A Consultation Scott and Scott LLP review summary View all sources Google (14) Birdeye (36) Facebook (1) 5 on Google , Feb 10, 2024 Salma good 5 on BirdEye , May 01, 2023 Kimberly You made the entire process so e…
```
**`law_ex_105509_neg_53`** (1929 ký tự)
```text
[ 6 ] British Overseas citizens retain their status by association with most former British colonies, [ 7 ] British subjects are connected specifically with Ireland or British India before 1949, [ 8 ] and British protect…
```
**`law_ex_105509_neg_59`** (1935 ký tự)
```text
^ "Common Travel Area guidance" . GOV.UK . 23 December 2022. Archived from the original on 17 January 2022 . Retrieved 16 November 2022 . ^ Bloom 2011 , pp. 649–650. ^ Makortoff, Kalyeena (19 April 2016). "These non-Brit…
```
**`law_ex_105509_neg_94`** (2001 ký tự)
```text
^ Jim Marshall , "British Overseas Territories Bill" , col. 495. ^ "2025 treaty on the British Indian Ocean Territory/Chagos Archipelago" . commonslibrary.parliament.uk . Retrieved 3 June 2025 . ^ Richard Spring , "Briti…
```
**`law_ex_105509_neg_95`** (1993 ký tự)
```text
gov.uk . Government of the United Kingdom . Retrieved 14 January 2020 . ^ "Youth Mobility Scheme visa (Tier 5)" . gov.uk . Government of the United Kingdom . Archived from the original on 25 April 2017 . Retrieved 8 Janu…
```

### ❌ `non_english` — nghi không phải tiếng Anh — 421

**`law_ex_105160_neg_30`** (289 ký tự)
```text
Wayback Machine 15 captures 29 Oct 2020 - 22 Nov 2025 Oct NOV Dec 22 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - https://web.archive.org…
```
**`law_ex_105244_neg_10`** (875 ký tự)
```text
18 Summer 2017) < http://www.discoverypilot.com/sites/default/files/The%20Sedona%20Conference%20TAR%20Case%20Law%20Primer.pdf > . [26] See The Sedona Conference, ‘The Sedona Conference TAR Case Law Primer’ (Vol. 18 Summe…
```
**`law_ex_105509_neg_28`** (1491 ký tự)
```text
of Agreement) Act 1925 1925 Balfour Declaration of 1926 1926 Royal and Parliamentary Titles Act 1927 Representation of the People Act 1928 1928 Eire (Confirmation of Agreement) Act 1929 1929 Statute of Westminster 1931 H…
```
**`law_ex_105509_neg_29`** (1970 ký tự)
```text
(Scotland) Act 1994 Referendums (Scotland & Wales) Act 1997 Scottish devolution referendum 1997 Welsh devolution referendum 1997 1998 GLA referendum 1998 Bank of England Act 1998 Good Friday Agreement 1998 Northern Irela…
```
**`law_ex_105509_neg_58`** (1997 ký tự)
```text
^ Daly 2001 , pp. 378–379. ^ Daly 2001 , pp. 380–381. ^ Ryan 2001 , pp. 859–860. ^ Heuston 1950 , p. 85. ^ Daly 2001 , pp. 382, 387. ^ Karatani 2003 , pp. 114–115, 122–126. ^ Wade 1948 , p. 70. ^ Weis 1979 , p. 17. ^ Kar…
```

### ❌ `pii_email` — chứa email — 224

**`law_ex_105244_neg_8`** (1893 ký tự)
```text
Tony Nolan QC is a Barrister and Nationally Accredited Mediator at the Victorian Bar. He was appointed special referee by Vickery J in McConnell Dowell Constructors (Aust) Pty Ltd v Santam Ltd & Others and in V601 Develo…
```
**`law_ex_105509_neg_0`** (1964 ký tự)
```text
Historical background information on nationality (accessible) - GOV.UK Cookies on GOV.UK We use some essential cookies to make this website work. We’d like to set additional cookies to understand how you use GOV.UK, reme…
```
**`law_ex_105722_neg_6`** (1965 ký tự)
```text
If the OLRC places the new law into a title that has been enacted into law, the law will appear in a statutory note rather than the main text. One such example is the Torture Victim Protection Act of 1991. Because the OL…
```
**`law_ex_106102_neg_7`** (763 ký tự)
```text
We can counter-sign, but what are the implications of having such a big gap between the effective date and when it is executed? Reply Now, how should a date be written? As in, should the date be MM/DD/YYYY, MM.DD.YYYY, o…
```
**`law_ex_106319_neg_12`** (1974 ký tự)
```text
The “cure” requirement does not apply to a breach of the executory contract or unexpired lease based on the insolvency or financial condition of the debtor — that is an ipso facto provision and is unenforceable under the…
```

### ❌ `pii_phone` — chứa số điện thoại — 370

**`law_ex_105160_neg_3`** (1941 ký tự)
```text
Since then, the Judicial Conference has made the following changes to the Code: March 1987: deleted the word "Judicial" from the name of the Code; September 1992: adopted substantial revisions to the Code; March 1996: re…
```
**`law_ex_105160_neg_30`** (289 ký tự)
```text
Wayback Machine 15 captures 29 Oct 2020 - 22 Nov 2025 Oct NOV Dec 22 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - https://web.archive.org…
```
**`law_ex_105160_neg_4`** (1682 ký tự)
```text
20544 202-502-1100 Canon 1: A Judge Should Uphold the Integrity and Independence of the Judiciary An independent and honorable judiciary is indispensable to justice in our society. A judge should maintain and enforce hig…
```
**`law_ex_105196_neg_15`** (1912 ký tự)
```text
Secured, Unsecured & Priority Claims in Bankruptcy Speak With Bankruptcy Attorney Today at 800-317-7730 Market Your Law Firm Lawyer Directory Get Help From a Bankruptcy Attorney Today at 1 (800) 317-7730 Bankruptcy Bankr…
```
**`law_ex_105196_neg_8`** (1907 ký tự)
```text
When consumers have attempted to cancel their subscription on the company’s website, they have been forced to navigate numerous pages in order to cancel. When consumers reach out to Adobe’s customer service to cancel, th…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 1,994

**`law_ex_105160_doc_2`** (1655 ký tự)
```text
Canon 3: A Judge Should Perform the Duties of the Office Fairly, Impartially and Diligently The duties of judicial office take precedence over all other activities. The judge should perform those duties with respect for …
```
**`law_ex_105828_doc_4`** (1000 ký tự)
```text
Unsuccessful law school applicant properly denied intervention may not appeal from judgment in underlying case · United States v. City of Los Angeles (9th Cir.) -- Appellee · Community groups and private individuals are …
```
**`law_ex_105867_doc_3`** (1495 ký tự)
```text
Back in 1918, the National Conference of Commissioners on Uniform State Laws "approved and recommended for enactment in all the states" the Uniform Fraudulent Conveyance Act. This Act contains, in Section 4: A reference …
```
**`law_ex_106419_doc_1`** (1619 ký tự)
```text
Title III of the ADA applies to places of public accommodation, which are private entities that are open to the public. Some examples of places of public accommodation are: Each location or organization must be considere…
```
**`law_ex_106657_doc_3`** (372 ký tự)
```text
In Opinion 10-206 (volume numbers omitted), we explained: A "pending proceeding" is one that has begun but has not yet reached final disposition, and an "impending proceeding" is one that is reasonably foreseeable but ha…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 217

**`law_ex_107522_doc_1`** (578 ký tự)
```text
rebus sic stantibus Clausula rebus sic stantibus is a clause in international conventions (international agreements or treaties) that provides for the unenforceability of a treaty due to fundamentally changed circumstanc…
```
**`law_ex_105160_neg_127`** (1804 ký tự)
```text
gifts incident to a public testimonial; invitations to the judge and the judge's spouse, domestic partner, or guest to attend without charge: an event associated with a bar-related function or other activity relating to …
```
**`law_ex_105160_neg_132`** (1939 ký tự)
```text
use or permit the use of campaign contributions for the private benefit of the judge, the candidate, or others except as permitted by law; use court staff, facilities, or other court resources in a campaign for judicial …
```
**`law_ex_105509_neg_28`** (1491 ký tự)
```text
of Agreement) Act 1925 1925 Balfour Declaration of 1926 1926 Royal and Parliamentary Titles Act 1927 Representation of the People Act 1928 1928 Eire (Confirmation of Agreement) Act 1929 1929 Statute of Westminster 1931 H…
```
**`law_ex_105509_neg_34`** (1409 ký tự)
```text
v t e British nationality law Nationality Principal British citizen British Overseas Territories citizen Other British subject British Overseas citizen British National (Overseas) British protected person Commonwealth ci…
```

### ✅ Trùng chính xác
- Không phát hiện.

### ❌ Gần trùng (khác nhau chút ít) — 122

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 29: `law_ex_106352_google_neg_512`, `law_ex_106352_google_neg_513`, `law_ex_106352_google_neg_514`, `law_ex_106352_google_neg_516`, `law_ex_106352_google_neg_517`
  - `law_ex_106352_google_neg_512`:
```text
Click to share on LinkedIn (Opens in new window) LinkedIn Click to share on Facebook (Opens in new window) Facebook Click to share on X (Opens in new window) X Click to email a link to a friend (Opens in new window) Emai…
```
  - `law_ex_106352_google_neg_513`:
```text
Click to share on LinkedIn (Opens in new window) LinkedIn Click to share on Facebook (Opens in new window) Facebook Click to share on X (Opens in new window) X Click to email a link to a friend (Opens in new window) Emai…
```
- cụm size 5: `law_ex_105563_neg_7`, `law_ex_106202_neg_23`, `law_ex_106352_neg_52`, `law_ex_107211_neg_0`, `law_ex_111040_neg_0`
  - `law_ex_105563_neg_7`:
```text
Wayback Machine 1 capture 02 Jun 2024 May JUN Jul 02 2023 2024 2025 success fail About this capture COLLECTED BY Organization: Archive Team Formed in 2009, the Archive Team (not to be confused with the archive.org Archiv…
```
  - `law_ex_106202_neg_23`:
```text
Wayback Machine 1 capture 18 Sep 2024 Aug SEP Oct 18 2023 2024 2025 success fail About this capture COLLECTED BY Organization: Archive Team Formed in 2009, the Archive Team (not to be confused with the archive.org Archiv…
```
- cụm size 5: `law_ex_112551_google_neg_266`, `law_ex_112551_google_neg_274`, `law_ex_112551_google_neg_280`, `law_ex_112551_google_neg_285`, `law_ex_112551_google_neg_291`
  - `law_ex_112551_google_neg_266`:
```text
Albuquerque PD does not place any limits on the use of biometric technologies (e.g., facial recognition) to search footage.
```
  - `law_ex_112551_google_neg_274`:
```text
SDPD PD does not place any limits on the use of biometric technologies (e.g., facial recognition) to search footage.
```
- cụm size 4: `law_ex_112551_google_neg_13`, `law_ex_112551_google_neg_16`, `law_ex_112551_google_neg_19`, `law_ex_112551_google_neg_21`
  - `law_ex_112551_google_neg_13`:
```text
SOURCE: Author estimates using California Department of Justice, Racial and Identity Profiling Act (RIPA) Wave 2 data, 2019. NOTES: The bars represent percentage-point differences in the likelihood of discovering somethi…
```
  - `law_ex_112551_google_neg_16`:
```text
SOURCE: Author estimates using California Department of Justice, Racial and Identity Profiling Act (RIPA) Wave 2 data, 2019. NOTES: The bars represent percentage point differences in the likelihood of enforcement between…
```
- cụm size 3: `law_ex_105509_google_neg_127`, `law_ex_105509_google_neg_132`, `law_ex_105509_google_neg_136`
  - `law_ex_105509_google_neg_127`:
```text
You need to do this even if you’ve already proved how long you’ve lived in the UK - for example, to get settled status. You need to prove you were: living in the UK for the 5 years before you apply living in the UK for t…
```
  - `law_ex_105509_google_neg_132`:
```text
You need to prove you were: living in the UK for the 5 years before you apply living in the UK for the 5 years before you apply outside the UK for no more than 450 days in those 3 years outside the UK for no more than 45…
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

- `ex_106319_turn_1`: In airline bankruptcies, is it possible for lease contracts to be transferred to another airline even if the original contract doesn’t allow it?
- `ex_106102_turn_1`: In contracts and forms, does it matter legally if the signature date is missing or left blank?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 26

- `ex_111150_turn_2`: Is it that trademarks mainly stop others from using certain names, while copyright deals more with creative stuff?
- `ex_111149_turn_2`: Wait, did any works actually get their copyright back after they'd already gone public domain?
- `ex_111149_turn_3`: Did those older movies that lost copyright before the law changed ever get their rights back, or were they just out for good?
- `ex_111142_turn_2`: Is that Parliament’s way of making sure GAAR only hits the really extreme cases?
- `ex_111142_turn_4`: I’m curious—do those examples in section 207 ever tip the scales when it’s a close call under the double reasonableness test?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 8

- `ex_111150_turn_4`: Then are those contract rights between performers and owners actually treated like intellectual property, or is that something different?
- `ex_111142_turn_3`: But what happens if some people think an arrangement isn’t reasonable, but others still see it as reasonable?
- `ex_110030_turn_2`: Oh, and what does it actually look like when Marshals handle courthouse security? Is that something the FBI ever does too?
- `ex_110030_turn_4`: Oh, is catching federal fugitives and running witness protection something only Marshals do, or does the FBI help with that too?
- `ex_106473_turn_2`: But what actually happens if someone just pays the seller directly, without any escrow or third party?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 8

- `ex_111142_turn_3` (cos=0.0)
  - trước: Is that Parliament’s way of making sure GAAR only hits the really extreme cases?
  - sau: But what happens if some people think an arrangement isn’t reasonable, but others still see it as reasonable?
- `ex_111142_turn_4` (cos=0.0)
  - trước: But what happens if some people think an arrangement isn’t reasonable, but others still see it as reasonable?
  - sau: I’m curious—do those examples in section 207 ever tip the scales when it’s a close call under the double reasonableness …
- `ex_111142_turn_5` (cos=0.0)
  - trước: I’m curious—do those examples in section 207 ever tip the scales when it’s a close call under the double reasonableness …
  - sau: I wonder if that makes appeals harder—do higher courts have to stick more closely to what the first tribunal decided?
- `ex_106718_turn_4` (cos=0.0)
  - trước: What happens if you just bring the peanut butter sandwich without any warning—would that still count as reasonable?
  - sau: Would a court actually blame the thief at all if they knew about their allergy but took the food anyway?
- `ex_106440_turn_7` (cos=0.0)
  - trước: Why was New York so strict about only allowing adultery for divorce back then, anyway?
  - sau: Would just being pregnant by someone else even count as proof of cheating if he couldn’t show she actually had an affair…

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

### ❌ Query không chia sẻ từ nào với gold — 5

- `ex_110030_turn_7` (pronoun) gold=['law_ex_110030_doc_0', 'law_ex_110030_doc_4']: Is that why their daily work looks so different from, say, what the FBI does?
- `ex_106718_turn_2` (pronoun) gold=['law_ex_106718_doc_3', 'law_ex_106718_doc_2']: I’m curious—does it make a difference legally if you brought the peanuts just to scare off the thief, not to hurt them?
- `ex_106718_turn_5` (pronoun) gold=['law_ex_106718_doc_0']: Is it a totally different legal situation if you actually try to hide the peanuts to catch the thief, instead of just labeling it?
- `ex_106440_turn_2` (standalone) gold=['law_ex_106440_doc_4', 'law_ex_106440_doc_0']: What kind of proof would judges actually take seriously back then, besides blood tests?
- `ex_105244_turn_5` (pronoun) gold=['law_ex_105244_doc_0']: Isn’t it way harder now to even know what’s out there, since digital files can be anywhere and everywhere?

### ❌ Bằng chứng nằm muộn (> 1500 ký tự) — 8

- `ex_105244_turn_5` offset=2714c gold=`law_ex_105244_doc_0`
  - query: Isn’t it way harder now to even know what’s out there, since digital files can be anywhere and everywhere?
  - bằng chứng: In Great Southern, teams of law graduates and junior solicitors were assigned the task of reviewing the hard copy documents to ascertain relevant and/or privile…
- `ex_111149_turn_1` offset=1864c gold=`law_ex_111149_doc_2`
  - query: In copyright law, how is extending a copyright term different from bringing a work back under copyright after it’s alrea…
  - bằng chứng: copyright term, as if they had never entered the public domain.
- `ex_107288_turn_2` offset=1761c gold=`law_ex_107288_doc_1`
  - query: What if the only reason someone isn't hired is because of who they're married to—does that still count as discrimination…
  - bằng chứng: National origin discrimination includes treating someone less favorably at work because he or she associates with (for example, marries) someone of a particular…
- `ex_111142_turn_2` offset=1698c gold=`law_ex_111142_doc_0`
  - query: Is that Parliament’s way of making sure GAAR only hits the really extreme cases?
  - bằng chứng: More recently, Chris Davidson, Head of the Anti-Avoidance Group at HMRC, commented that 'We can have a debate about [whether or not something is reasonable], bu…
- `ex_111142_turn_3` offset=1698c gold=`law_ex_111142_doc_0`
  - query: But what happens if some people think an arrangement isn’t reasonable, but others still see it as reasonable?
  - bằng chứng: More recently, Chris Davidson, Head of the Anti-Avoidance Group at HMRC, commented that 'We can have a debate about [whether or not something is reasonable], bu…

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 5

- `ex_110030_turn_4` OOV=['catching']: Oh, is catching federal fugitives and running witness protection something only Marshals do, or does the FBI help with that too?
- `ex_106718_turn_2` OOV=['scare']: I’m curious—does it make a difference legally if you brought the peanuts just to scare off the thief, not to hurt them?
- `ex_106319_turn_2` OOV=['jetblue']: If JetBlue takes over those leases, does Spirit still have to worry about any of the old obligations, or do they just walk away?
- `ex_106319_turn_3` OOV=['jetblue']: I’m curious—how does bankruptcy actually let Spirit’s lease contracts get sold off to someone like JetBlue? Do the courts have to sign off o…
- `ex_105244_turn_4` OOV=['slipping']: Is there anything that actually stops less relevant or even unfair stuff from slipping through because of how broad that test is?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 2

*nguyên nhân: {'lexical_gap (overlap<0.2)': 2}*

- `ex_106718_turn_5` ti=4 ctx=pronoun overlap=0.0: Is it a totally different legal situation if you actually try to hide the peanuts to catch the thief, instead of just labeling it?
  - gold ['law_ex_106718_doc_0'] | top3 ['law_ex_105244_doc_2', 'law_ex_107288_google_neg_429', 'law_ex_106419_neg_23']
- `ex_106440_turn_2` ti=1 ctx=standalone overlap=0.0: What kind of proof would judges actually take seriously back then, besides blood tests?
  - gold ['law_ex_106440_doc_0', 'law_ex_106440_doc_4'] | top3 ['law_ex_106440_doc_1', 'law_ex_108376_google_neg_723', 'law_ex_105867_doc_4']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.