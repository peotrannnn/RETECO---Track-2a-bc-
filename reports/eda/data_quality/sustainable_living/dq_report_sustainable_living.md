# Báo cáo chất lượng dữ liệu — domain `sustainable_living`

*Tạo lúc 2026-11-21T09:07:48 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 85.2 🟢** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 99.7 | 🟢 |
| content | 0.25 | 48.7 | 🔴 |
| conversation | 0.15 | 95.7 | 🟢 |
| gold | 0.25 | 98.5 | 🟢 |
| link | 0.15 | 93.7 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| content | % trùng chính xác | 17.52 | 1.0 | 17.52 |
| content | % doc quá ngắn | 29.63 | 0.5 | 14.81 |
| content | % ký hiệu lạ/URL nặng | 20.35 | 0.4 | 8.14 |
| content | % nghi không phải tiếng Anh | 15.44 | 0.5 | 7.72 |
| link | % turn gold không chia sẻ từ nào với query | 3.57 | 1.5 | 5.35 |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 4.35 | 1 | 4.35 |
| gold | % gold có lỗi nội dung nghiêm trọng | 3.03 | 0.5 | 1.51 |
| content | % lặp bất thường | 2.81 | 0.5 | 1.41 |
| content | % boilerplate | 2.51 | 0.3 | 0.75 |
| content | % gần trùng (ngoài trùng chính xác) | 1.04 | 0.7 | 0.73 |
| link | % turn overlap=0 (kể cả history) | 1.19 | 0.5 | 0.59 |
| link | % OOV trung bình của query | 1.22 | 0.3 | 0.37 |

## 2. Khuyến nghị

- **[medium]** 0.17% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 29.63%.
- **[medium]** Trùng chính xác 17.52%.
- **[medium]** Gần trùng 1.04% (MinHash).
- **[low]** 15.44% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 60.66% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 1 hội thoại có đại từ/liên từ ở turn đầu.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **60,792** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.17% | ký tự điều khiển 0.0% | HTML/entity sót 0.03%
- Benchmark: 23 hội thoại | schema=`qa_pair` | vai trò {'user': 84, 'assistant': 84} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 84/84
- qrels: 182 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 182} | qid 84

## 4. Chất lượng nội dung

- Ký tự: min=1 p25=37.0 **median=125.0** mean=344.2 p75=341.0 p90=872.0 p99=2255.0 max=158299 | outlier dài (>1253.0c): 6.06%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 86.14% / 88.99% / 95.81% / 99.36%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 44.42% |
| 101-300 | 27.74% |
| 301-650 | 13.98% |
| 651-800 | 2.85% |
| 801-1500 | 6.82% |
| 1501-3000 | 3.55% |
| 3001-6000 | 0.39% |
| >6000 | 0.25% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 18010 | 29.63% |
| mojibake | lỗi encoding (mojibake) | 106 | 0.17% |
| control_chars | ký tự điều khiển | 1 | 0.0% |
| html_residue | HTML/entity còn sót | 20 | 0.03% |
| boilerplate | boilerplate/menu/footer | 1528 | 2.51% |
| url_heavy | URL chiếm >25% nội dung | 11448 | 18.83% |
| symbol_heavy | ký hiệu lạ >30% | 921 | 1.52% |
| repetitive | lặp từ/dòng bất thường | 1708 | 2.81% |
| non_english | nghi không phải tiếng Anh | 9387 | 15.44% |
| pii_email | chứa email | 158 | 0.26% |
| pii_phone | chứa số điện thoại | 994 | 1.64% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 6874 | 11.31% |
| starts_lower | bắt đầu bằng chữ thường | 2926 | 4.81% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **57.45%**
- Trùng chính xác: 10,650 doc dư (17.52%), 4435 nhóm
- Gần trùng: 392 cụm | doc dư gần-trùng ngoài trùng chính xác 144 (1.04%) | cụm lớn nhất 29
- Từ vựng (mẫu 10,081 doc): 31,205 từ | hapax 40.63% | Zipf -0.968 | 0(11815), https(5458), wiki(5377), 1(4695), com(3585), 2(3388), www(3153), 3(2598), 5(2225), 4(2078), s(1831), 6(1831), energy(1687), 7(1642), 8(1621)

## 5. Hội thoại

- **23** hội thoại, **84** turn | turn/hội thoại: mean 3.65 (min 3, max 5) | query: mean 17.8 từ, median 18.0, p95 22.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 47 | 55.95% |
| pronoun | 32 | 38.1% |
| connector | 5 | 5.95% |
| short_ellipsis | 0 | 0% |

→ **60.66%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 1 (4.35%)
- Chuyển chủ đề: {'weak': 31.15, 'on_topic': 50.82, 'shift': 18.03} | hội thoại nhảy chủ đề ≥50% turn: 26.09%

**Loại câu hỏi:** statement_other 42.86%, yes_no 30.95%, what 20.24%, how 4.76%, wh_other 1.19%

## 6. Gold / qrels

- Nguồn gold: {'inline': 84} | qrels được dùng để eval: False
- Gold/turn: mean 2.17, max 10
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 84/84 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 60,693/60,792 (99.84%) | Gini 0.2817
- Độ dài gold vs corpus (median): 1054.0 vs 125.0 (tỷ lệ 8.43x)
- Gold có lỗi nghiêm trọng: 3.03% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.272** (có history: 0.265) | overlap=0: 3.57% | <20%: 35.71% | overlap=0 dù có history: 1.19%
- Overlap theo ngữ cảnh: {'standalone': 0.307, 'pronoun': 0.235, 'connector': 0.191}
- OOV: 14.29% (TB 1.22%)
- **Vị trí bằng chứng** (82 mẫu): {'0-20%': 50.0, '20-40%': 13.41, '40-60%': 18.29, '60-80%': 9.76, '80-100%': 8.54} | median offset 290c | sau 650c: 28.05% | sau 512 token: 3.66%

## 8. BM25 baseline

- 84 query | 99 gold + 200 nhiễu
- nDCG@10 single/history = 0.5727/0.7434 | Recall@10 = 0.7085/0.9057

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 23 | 0.7385 | 0.7415 | 0.8333 | 0.8333 |
| 2 | 23 | 0.5217 | 0.7402 | 0.7 | 0.9841 |
| 3 | 23 | 0.5248 | 0.7767 | 0.6475 | 0.8665 |
| 4 | 10 | 0.49 | 0.717 | 0.6533 | 0.96 |
| 5+ | 5 | 0.4312 | 0.6664 | 0.565 | 0.95 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 5 | 0.6861 | 0.8 | 0.8 | 1.0 |
| pronoun | 32 | 0.396 | 0.7209 | 0.6037 | 0.9212 |
| standalone | 47 | 0.681 | 0.7527 | 0.7702 | 0.8851 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 4 | 0.25 | 0.5336 | 0.25 | 1.0 |
| statement_other | 36 | 0.6408 | 0.7529 | 0.7366 | 0.8463 |
| wh_other | 1 | 0.5 | 1.0 | 1.0 | 1.0 |
| what | 17 | 0.5263 | 0.8105 | 0.6838 | 0.9755 |
| yes_no | 26 | 0.5613 | 0.7089 | 0.7452 | 0.9242 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 23 | 0.7385 | 0.7415 | 0.8333 | 0.8333 |
| on_topic | 31 | 0.5529 | 0.7445 | 0.7444 | 0.9306 |
| shift | 11 | 0.4769 | 0.7385 | 0.5697 | 0.9818 |
| weak | 19 | 0.4599 | 0.7467 | 0.5794 | 0.9085 |

- Turn khó: **5** (5.95%) — {'lexical_gap (overlap<0.2)': 4, 'ranking/distractor': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 235 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 18,010

**`Lithium_in_the_earth/Lithium_0.txt`** (37 ký tự)
```text
From Wikipedia, the free encyclopedia
```
**`Lithium_in_the_earth/Lithium_101.txt`** (24 ký tự)
```text
#### Hard-rock deposits
```
**`Lithium_in_the_earth/Lithium_107.txt`** (12 ký tự)
```text
### Sources
```
**`Lithium_in_the_earth/Lithium_109.txt`** (12 ký tự)
```text
### Pricing
```
**`Lithium_in_the_earth/Lithium_113.txt`** (15 ký tự)
```text
### Extraction
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 106

**`bokashi/homecompostingthebokashimethod_100.txt`** (34 ký tự)
```text
Â© 2022 Sustainable Planet Limited
```
**`bokashi/homecompostingthebokashimethod_14.txt`** (208 ký tự)
```text
Technically speaking, the bokashi method is a form of fermentation rather than composting â bokashi ferments (or pickles), it is a way to quickly ferment food scraps so that they can be composted faster.Â Â
```
**`bokashi/homecompostingthebokashimethod_16.txt`** (248 ký tự)
```text
1. Is much quicker than traditional composting.Â 2. Gives off less odour.Â 3. Requires less maintenance.Â 4. Takes up less space.Â 5. Allows you to compost dairy and meat products.Â 6. Produces a plant-nutritious liquid …
```
**`bokashi/homecompostingthebokashimethod_19.txt`** (2310 ký tự)
```text
1. **Obtain equipment** . Before you start your bokashi composting, youâll need an airtight bucket with a drainage spout and some bokashi bran. The bucket (often called a âbokashi bucketâ or âbokashi binâ) will…
```
**`bokashi/homecompostingthebokashimethod_37.txt`** (199 ký tự)
```text
May 2, 2023 ![](https://assets-global.website- files.com/61db9967c56e16d806ec7afb/61e4a18165434171c77b9423_Clock.svg) Â min read ](/blog/the-weirdest-sustainable-materials-that-can-replace-plastic)
```

### ❌ `control_chars` — ký tự điều khiển — 1

**`solar/booksvstheinternet_260.txt`** (177 ký tự)
```text
Lastly, of course, was to remove all but maybe two or three books from the shelves, recycling, donating, or utilizing the pages of discarded books for arts and craft projects. 
```

### ❌ `html_residue` — HTML/entity còn sót — 20

**`b12/BER201708c_36.txt`** (931 ký tự)
```text
* [ About ](/ber/About "About") * [ Research ](/ber/Research "Research") * [ Facilities ](/ber/Facilities "Facilities") * [ Human Subjects Protection Program ](/ber/human-subjects "Human Subjects Protection Program") * […
```
**`inner_insulation/moistureresistance_39.txt`** (2297 ký tự)
```text
Properties and Surrounding Conditions of Concrete Engineering Priority Available Inadvisable Ordinary Cement 1 The Concrete in General Climate Ordinary Cement Slag Cement, Pozzolana Cement, Fly-ash Cement, Composite Ceme…
```
**`mosquito_control/447_134.txt`** (2836 ký tự)
```text
<strong>Figure 1</strong><br/> <p>Schematic representation of the electrostatic field produced by a negatively charged insulator, covering a negatively charged conductor.</p> ") [ ](https://pub.mdpi-res.com/insects/insec…
```
**`rebound/responsiblelivingconceptseducationandfutureperspectives_1.txt`** (147 ký tự)
```text
[ ![Environment & Urbanization](https://www.environmentandurbanization.org/sites/default/files/eandulogo.png) ](/ "Environment &amp; Urbanization")
```
**`recycle_cloth/secondhandclothes_0.txt`** (149 ký tự)
```text
[ ![Frankie &amp; Ruby](//frankieandruby.co.uk/cdn/shop/files/Logo_new_colour_ways-2_ec66073d-6445-4ffc-b776-8610d799beb1_500x.png?v=1630914736) ](/)
```

### ❌ `boilerplate` — boilerplate/menu/footer — 1,528

**`water_plant/SolubleSalts_0.txt`** (632 ký tự)
```text
SKIP TO CONTENT SITE MAP Enter Search Terms Search GIVE logo University of California Agriculture and Natural Resources The California Garden Web The California Garden Web UC Master Gardener Program UC ANR Home SHARE PRI…
```
**`Lithium_in_the_earth/winter_5.txt`** (9 ký tự)
```text
Read more
```
**`Lithium_in_the_earth/winter_52.txt`** (98 ký tự)
```text
Read more about the costs and benefits of rooftop solar and batteries in the Solar Consumer Guide.
```
**`Lithium_in_the_earth/winter_59.txt`** (97 ký tự)
```text
Read more Rebates and assistance - Find out what support is available in your state or territory.
```
**`alle/262982_100.txt`** (83 ký tự)
```text
[ READ MORE ](https://www.medicalnewstoday.com/articles/319619?utm_source=ReadNext)
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 11,448

**`siphon/siphonrevisedhtml_4.txt`** (14208 ký tự)
```text
I had many feed back regarding the siphon design on usage of smaller funnel inlet to the stand pipe. My standard design make use of 50mm ~ 25mm reducer as illustrated below. [ ![](https://blogger.googleusercontent.com/im…
```
**`Lithium_in_the_earth/Lithiumionbattery_100.txt`** (389 ký tự)
```text
∂ c ∂ t = D ε ∂ 2 c ∂ x 2 . {\displaystyle {\frac {\partial c}{\partial t}}={\frac {D}{\varepsilon }}{\frac {\partial ^{2}c}{\partial x^{2}}}.} ![{\\displaystyle {\\frac {\\partial c}{\\partial t}}={\\frac {D}{\\varepsil…
```
**`Lithium_in_the_earth/Lithiumionbattery_177.txt`** (237 ký tự)
```text
This section is an excerpt from [ Electric vehicle supply chain ](/wiki/Electric_vehicle_supply_chain "Electric vehicle supply chain") . [ [ edit ](https://en.wikipedia.org/w/index.php?title=Electric_vehicle_supply_chain…
```
**`Lithium_in_the_earth/Lithiumionbattery_39.txt`** (252 ký tự)
```text
LiC 6 ↽ − − ⇀ C 6 \+ Li \+ \+ e − {\displaystyle {\ce {LiC6 <=> C6 + Li+ + e^-}}} ![{\\displaystyle {\\ce {LiC6 <=> C6 + Li+ + e^-}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0169904f54e5d1a00fbca78f4bf8a…
```
**`Lithium_in_the_earth/Lithiumionbattery_41.txt`** (262 ký tự)
```text
CoO 2 \+ Li \+ \+ e − ↽ − − ⇀ LiCoO 2 {\displaystyle {\ce {CoO2 + Li+ + e- <=> LiCoO2}}} ![{\\displaystyle {\\ce {CoO2 + Li+ + e- <=> LiCoO2}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/30cdc79eb9e6715e9bf…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 921

**`Lithium_in_the_earth/Lithium_184.txt`** (5 ký tự)
```text
[199]
```
**`Lithium_in_the_earth/energydemand_101.txt`** (6 ký tự)
```text
######
```
**`Lithium_in_the_earth/energydemand_13.txt`** (12 ký tự)
```text
#### Policy
```
**`Lithium_in_the_earth/energydemand_161.txt`** (2 ký tự)
```text
##
```
**`Lithium_in_the_earth/energydemand_209.txt`** (2 ký tự)
```text
##
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 1,708

**`Lithium_in_the_earth/Lithium_1.txt`** (283 ký tự)
```text
This article is about the chemical element. For the use of lithium as a medication, see [ Lithium (medication) ](/wiki/Lithium_\(medication\) "Lithium \(medication\)") . For other uses, see [ Lithium (disambiguation) ](/…
```
**`Lithium_in_the_earth/Lithium_148.txt`** (253 ký tự)
```text
Lithium compounds are used as [ pyrotechnic colorants ](/wiki/Pyrotechnic_colorant "Pyrotechnic colorant") and oxidizers in red [ fireworks ](/wiki/Fireworks "Fireworks") and [ flares ](/wiki/Flare_\(pyrotechnic\) "Flare…
```
**`Lithium_in_the_earth/Lithium_2.txt`** (129 ký tự)
```text
"3Li" redirects here. For the isotope of lithium with three nucleons ( 3 Li ), see [ Lithium-3 ](/wiki/Lithium-3 "Lithium-3") .
```
**`Lithium_in_the_earth/Lithium_39.txt`** (229 ký tự)
```text
Main articles: [ Nucleosynthesis ](/wiki/Nucleosynthesis "Nucleosynthesis") , [ Stellar nucleosynthesis ](/wiki/Stellar_nucleosynthesis "Stellar nucleosynthesis") , and [ Lithium burning ](/wiki/Lithium_burning "Lithium …
```
**`Lithium_in_the_earth/Lithium_46.txt`** (180 ký tự)
```text
See also: [ Lithium compounds ](/wiki/Category:Lithium_compounds "Category:Lithium compounds") and [ Lithium minerals ](/wiki/Category:Lithium_minerals "Category:Lithium minerals")
```

### ❌ `non_english` — nghi không phải tiếng Anh — 9,387

**`perennial_crop/comfreytrialshtml_3.txt`** (727 ký tự)
```text
2016 - Comfrey 'Bocking 14' Biomass Records Site Overview Cuts Fertility Climate: Temperate Cut Date Flowering Days between Cuts Weight kg Weight per plant - kg Input Date Quantity - L Latitude: 41 1 29.04.16 yes n/a 23.…
```
**`hot_water_cylinder/Legionella_22.txt`** (399 ký tự)
```text
Documented sources include cooling towers, [20] swimming pools (especially in Scandinavian countries), domestic water systems and showers, ice-making machines, [21] refrigerated cabinets, whirlpool spas, [22] [23] hot sp…
```
**`co2_emission_regulation/finalsafefriawebversion200701pdf_4476.txt`** (1361 ký tự)
```text
(2) CO2 Standards Table VII-353 – Cumulative Changes in Fuel Consumption and CO2 and Related Emissions for MY’s 1977-2029 Under CO2 Program Impacts on Model Year MY 1977- 2016 MY 2017 MY 2018 MY 2019 MY 2020 MY 2021 MY 2…
```
**`software_carbon/Emissionintensity_57.txt`** (2796 ký tự)
```text
Lifecycle greenhouse gas emissions by electricity source [6] Technology | Description | 50th percentile (g CO 2 -eq/kWh e ) ---|---|--- [ Hydroelectric ](/wiki/Hydroelectricity "Hydroelectricity") | reservoir | 4 [ Wind …
```
**`train_station/PMC8672270_14.txt`** (354 ký tự)
```text
Table 1: Nominal values for normal human adult breathing at sea-level Condition Rate (Breaths/min) Tidal Volume (L/breath) Minute Ventilation (L/min) Nominal At-Rest 12 0.5 6 Normal Activity 16 1 16 Moderate Exercise 20 …
```

### ❌ `pii_email` — chứa email — 158

**`sea_water/FULLTEXT01pdf_0.txt`** (4081 ký tự)
```text
Solar Thermal Technologies for Seawater Desalination: State of the art __________________________________________________________________________________________ Jenny Lindblom, Renewable Energy Systems, Luleå University…
```
**`alle/21137325_117.txt`** (120 ký tự)
```text
* 1 College of Chinese Medicinal Materials, Jilin Agricultural University, Changchun 130118, China. fengjie_lei@163.com
```
**`alle/21137325_99.txt`** (120 ký tự)
```text
* 1 College of Chinese Medicinal Materials, Jilin Agricultural University, Changchun 130118, China. fengjie_lei@163.com
```
**`almond_milk/almondmilk_66.txt`** (168 ký tự)
```text
4. ![](https://secure.gravatar.com/avatar/8582e23d3f3c25caa7c1e9609544655a?s=80&d=identicon&r=g) [ Miyu Limlíriel ](http://marionettamiyu@wordpress.com) says: Reply
```
**`almond_milk/drought_36.txt`** (321 ký tự)
```text
[ US Dept of Commerce ](http://www.commerce.gov) [ National Oceanic and Atmospheric Administration ](http://www.noaa.gov) [ National Weather Service ](https://www.weather.gov) Safety 1325 East West Highway Silver Spring,…
```

### ❌ `pii_phone` — chứa số điện thoại — 994

**`video_power/uhdtvenergyuseESpdf_13.txt`** (663 ký tự)
```text
dark scenes, it was dramatically higher (often double) on extremely bright scenes, as evident by the energy usage spikes in the graph below of a 20-minute segment from Exodus—Gods and Kings. The lesson from this testing …
```
**`video_power/uhdtvenergyuseESpdf_14.txt`** (946 ký tự)
```text
50 130 132 134 136 138 140 142 144 146 148 150 Time (m) Exodus 4K HDR Exodus 4K Page 8 the Big Picture: Ultra High-Definition Televisions Could Add $1 Billion to Viewers’ Annual Electric Bills nrdc widespread, average 4K…
```
**`video_power/uhdtvenergyuseESpdf_6.txt`** (617 ký tự)
```text
times the amount of electricity consumed by all the homes in San Francisco each year. n $1 billion in additional annual costs to consumers to operate their televisions. n 5 million extra metric tons of carbon dioxide pol…
```
**`tea_tree_oil/teatreeoil_25.txt`** (315 ký tự)
```text
If someone may have swallowed tea tree oil, immediately check the [ web **POISON** CONTROL ® ](https://triage.webpoisoncontrol.org) online tool or call Poison Control at 1-800-222-1222. Don't wait to see what will happen…
```
**`renewable_energy/241RaugeiEROIEPrevisedII201203VMFpdf_5.txt`** (2977 ký tự)
```text
modules with performance ratios derived from extensive experimental field data is arguably the most valid approach to assessing the level of energy performance that can be expected of a PV system today. Conversely, defau…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 6,874

**`perennial_crop/comfreytrialshtml_3.txt`** (727 ký tự)
```text
2016 - Comfrey 'Bocking 14' Biomass Records Site Overview Cuts Fertility Climate: Temperate Cut Date Flowering Days between Cuts Weight kg Weight per plant - kg Input Date Quantity - L Latitude: 41 1 29.04.16 yes n/a 23.…
```
**`electricity_switch_cars/20WWSItalypdf_6.txt`** (1100 ký tự)
```text
BAU 2050 217.4 24.4 13.2 24.3 36.1 1.9 0.1 WWS 2050 83.2 19.2 20.3 35.6 23.5 1.5 0 -42.19 -11.58 -7.97 -61.74 Table 2. 2050 WWS End-Use Demand by Sector 2050 annual average end-use electric plus heat load (GW) by sector …
```
**`drought_garden/Xeriscaping_17.txt`** (1775 ký tự)
```text
Lawns and applications [ [ edit ](/w/index.php?title=Xeriscaping&action=edit&section=12 "Edit section: Lawns and applications") ] One of the major challenges to the public [ acceptance ](/wiki/Acceptance "Acceptance") of…
```
**`spring_store_energy/S187661021502576Xpdf_7.txt`** (1035 ký tự)
```text
Table 1. Energy data on spring-based energy storage systems. Reference Power density Gravimetric energy density Volumetric energy density Steel coiled spring [26] - 0.14 kJ/kg 1080 kJ/m3 CNT yarn spring [21] - 4.20 kJ/kg…
```
**`white_paper/howbleachdamagestheenvironmentandourhealth_88.txt`** (303 ký tự)
```text
Bleach poses harmful impacts to the environment in a few ways. Specifically, bleach is a major concern for water quality, soils, and wildlife. Bleach is considered an unstable chemical solution, meaning it is highly reac…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 2,926

**`drought_garden/Xeriscaping_3.txt`** (4820 ký tự)
```text
sitelinks- wikipedia "Edit interlanguage links") * [ Article ](/wiki/Xeriscaping "View the content page \[c\]") * [ Talk ](/wiki/Talk:Xeriscaping "Discuss improvements to the content page \[t\]") English * [ Read ](/wiki…
```
**`almond_milk/cawatercapstone1pdf_1.txt`** (1124 ký tự)
```text
and sometimes conflicting water interests. The drought could end next year or it could continue, with even greater consequences in the coming years. But even during good years, disputes over water are common and claims o…
```
**`almond_milk/cawatercapstone1pdf_2.txt`** (1093 ký tự)
```text
tensions among neighbors and damage to public roads, structures, and, ironically, water delivery canals from the land subsiding over depleted aquifers. The good news is that solutions to our water problem exist. They are…
```
**`almond_milk/cawatercapstone1pdf_5.txt`** (1076 ký tự)
```text
populations of fish and wildlife under existing conditions.2 The Board’s findings indicate that we currently divert almost 5 million acre-feet more water in an average year from the Delta than is compatible with a health…
```
**`almond_milk/cawatercapstone1pdf_6.txt`** (1132 ký tự)
```text
rate of the aquifer. Chronic overdraft has led to falling groundwater levels, dry wells, land subsidence, decreased groundwater storage capacity, decreased water quality, and stream depletion (Borchers et al., 2014). PAG…
```

### ❌ Trùng chính xác — 10,650

*4435 nhóm*

- nhóm: `car_rail/notrainsrequired_1.txt`, `car_rail/notrainsrequired_175.txt`, `car_rail/notrainsrequired_176.txt`
```text
[ __ ](javascript:void\(0\))
```
- nhóm: `credit_card/sustainablecard_18.txt`, `white_paper/en_18.txt`
```text
* [ labels ](https://paperwise.eu/en/examples/eco-friendly-packaging/eco-friendly-labels/) * [ lifestyle packaging ](https://paperwise.eu/en/examples/eco-friendly-packaging/eco-friendly-lifestyle-packaging/) * [ mini cor…
```
- nhóm: `pesticide/benefitsneonicotinoidseedtreatmentssoybeanproduction_28.txt`, `smoke_detector/americiumionizationsmokedetectors_51.txt`
```text
* [ Accessibility Statement ](/accessibility/epa-accessibility-statement) * [ Budget & Performance ](/planandbudget) * [ Contracting ](/contracts) * [ EPA www Web Snapshot ](/utilities/wwwepagov-snapshots) * [ Grants ](/…
```
- nhóm: `sustainable_christmas/christmasspiritindex_88.txt`, `sustainable_christmas/howtodecorateafibreopticchristmastree_88.txt`
```text
* [ Shop by Height ](javascript:void\(0\) "Shop by Height")
```
- nhóm: `sustainable_christmas/christmasspiritindex_96.txt`, `sustainable_christmas/howtodecorateafibreopticchristmastree_96.txt`
```text
* [ Outdoor LED Trees ](https://www.christmastreeworld.co.uk/artificial-christmas-trees/led-outdoor-christmas-trees.html "Outdoor LED Christmas Trees")
```

### ❌ Gần trùng (khác nhau chút ít) — 144

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 29: `banana_peel/canyoueatbananapeels_28.txt`, `banana_peel/canyoueatbananapeels_32.txt`, `banana_peel/canyoueatbananapeels_34.txt`, `banana_peel/canyoueatbananapeels_36.txt`, `banana_peel/canyoueatbananapeels_38.txt`
  - `banana_peel/canyoueatbananapeels_28.txt`:
```text
* [ Diners, Drive-Ins and Dives ](//www.foodnetwork.com/shows/diners-drive-ins-and-dives)
```
  - `banana_peel/canyoueatbananapeels_32.txt`:
```text
* [ Diners, Drive-Ins and Dives ](//www.foodnetwork.com/shows/diners-drive-ins-and-dives)
```
- cụm size 29: `co2_emission_regulation/finalsafefriawebversion200701pdf_117.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_134.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_154.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_34.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3732.txt`
  - `co2_emission_regulation/finalsafefriawebversion200701pdf_117.txt`:
```text
2017 MY 2018 MY 2019 MY 2020 MY 2021 MY 2022 MY 2023 MY 2024 MY 2025 MY 2026 MY
```
  - `co2_emission_regulation/finalsafefriawebversion200701pdf_134.txt`:
```text
2018 MY 2019 MY 2020 MY 2021 MY 2022 MY 2023 MY 2024 MY 2025 MY 2026 MY 2027 MY
```
- cụm size 27: `co2_emission_regulation/finalsafefriawebversion200701pdf_233.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3780.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3793.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3809.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3860.txt`
  - `co2_emission_regulation/finalsafefriawebversion200701pdf_233.txt`:
```text
0.5%/Year PC 0.5%/Year LT 1.5%/Year PC 1.5%/Year LT 1.0%/Year PC 2.0%/Year LT 1.0%/Year PC 2.0%/Year LT 2.0%/Year PC 3.0%/Year LT
```
  - `co2_emission_regulation/finalsafefriawebversion200701pdf_3780.txt`:
```text
PC 0.5%/Year LT 1.5%/Year PC 1.5%/Year LT 1.0%/Year PC 2.0%/Year LT 1.0%/Year PC 2.0%/Year LT 2.0%/Year PC 3.0%/Year LT 2.0%/Year
```
- cụm size 18: `co2_emission_regulation/finalsafefriawebversion200701pdf_3763.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3802.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3818.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3850.txt`, `co2_emission_regulation/finalsafefriawebversion200701pdf_3927.txt`
  - `co2_emission_regulation/finalsafefriawebversion200701pdf_3763.txt`:
```text
2021 Augural 2022-2025 0.0%/Year PC 0.0%/Year LT 0.5%/Year PC 0.5%/Year LT 1.5%/Year PC 1.5%/Year LT 1.0%/Year PC 2.0%/Year LT 1.0%/Year
```
  - `co2_emission_regulation/finalsafefriawebversion200701pdf_3802.txt`:
```text
2021 Augural 2022-2025 0.0%/Year PC 0.0%/Year LT 0.5%/Year PC 0.5%/Year LT 1.5%/Year PC 1.5%/Year LT 1.0%/Year PC 2.0%/Year LT 1.0%/Year
```
- cụm size 14: `ant/Boricacid_7.txt`, `car_rail/Handcar_7.txt`, `lithium_mining/Electriccar_7.txt`, `lithium_mining/Electricvehiclebattery_7.txt`, `per_capital/ListofcountriesbyGDP28nominal29_7.txt`
  - `ant/Boricacid_7.txt`:
```text
* [ Help ](/wiki/Help:Contents "Guidance on how to use and edit Wikipedia") * [ Learn to edit ](/wiki/Help:Introduction "Learn how to edit Wikipedia") * [ Community portal ](/wiki/Wikipedia:Community_portal "The hub for …
```
  - `car_rail/Handcar_7.txt`:
```text
* [ Help ](/wiki/Help:Contents "Guidance on how to use and edit Wikipedia") * [ Learn to edit ](/wiki/Help:Introduction "Learn how to edit Wikipedia") * [ Community portal ](/wiki/Wikipedia:Community_portal "The hub for …
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

### ❌ Turn đầu có đại từ/liên từ lơ lửng — 1

- `2_turn_1`: In biodegradable plastics, do they always need microbes to break down, or is that different from compostable ones?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 32

- `1_turn_2`: What happens if I just list it online—does that make it more likely someone will actually use it up responsibly?
- `1_turn_3`: I’m curious—do those reuse suggestions actually end up being better for the environment than just dropping it off as hazardous waste?
- `2_turn_2`: What happens if those compostable plastics end up leaving behind toxins like PFAS—doesn’t that kind of defeat the purpose?
- `2_turn_4`: What makes some of those blends like PLA actually work in a backyard compost, while others need the industrial setup?
- `2_turn_5`: Does calling something biodegradable actually mean it disappears completely, or could bits of plastic still stick around?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 5

- `11_turn_2`: What about trains and buses that already run on electricity—does that change how much extra power we'd really need?
- `54_turn_2`: But if they're still using huge monoculture plantations, doesn't that kind of cancel out the organic benefits?
- `54_turn_3`: Oh, does that mean if a plantation was built on cleared rainforest, the organic label can’t really fix the original damage?
- `99_turn_4`: What about stuff like oil or chemicals from the shingles—can you actually get that out with normal filters?
- `103_turn_3`: What about those vinegar or alcohol-based deodorants—do they actually use less packaging than the usual sticks?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 11

- `5_turn_3` (cos=0.0)
  - trước: Is it using the shower that really increases the risk if the water isn’t hot enough?
  - sau: What if I just turn it up to 70°C for a bit each day—would that actually keep things safe?
- `15_turn_2` (cos=0.0)
  - trước: In car-free city design, how is a city with no cars or streets different from cities that just limit cars?
  - sau: I’m curious—would daily life there actually feel comfortable and green, even if building it isn’t totally eco-friendly?
- `20_turn_2` (cos=0.0)
  - trước: Regarding oil-filled radiators, how can I stop it from wasting energy after I leave the room?
  - sau: How do I figure out which setting matches what my conservatory actually needs?
- `38_turn_3` (cos=0.0)
  - trước: Would breathing that in for half an hour be like smoking a few cigarettes, or is it totally different?
  - sau: I'm curious—how do the UFPs from a cigarette actually stack up against what you'd get from a waterpipe or just standing …
- `55_turn_2` (cos=0.0)
  - trước: In sustainable credit cards, how does your choice affect the environment or social issues when you spend?
  - sau: What kinds of projects do they actually put the money toward, then?

## D. Gold / qrels

### ✅ Gold mồ côi (doc không có trong corpus)
- Không phát hiện.

### ✅ qrels qid không khớp turn nào
- Không phát hiện.

### ✅ Gold inline (benchmark) ≠ qrels
- Không phát hiện.

### ✅ Turn không có gold
- Không phát hiện.

### ❌ Gold doc có lỗi nội dung nghiêm trọng — 3

- `perennial_crop/comfreytrialshtml_3.txt` ['non_english']
```text
2016 - Comfrey 'Bocking 14' Biomass Records Site Overview Cuts Fertility Climate: Temperate Cut Date Flowering Days between Cuts Weight kg Weight per plant - kg Input Date Quantity - L Latitude: 41 1 …
```
- `hot_water_cylinder/Legionella_22.txt` ['non_english']
```text
Documented sources include cooling towers, [20] swimming pools (especially in Scandinavian countries), domestic water systems and showers, ice-making machines, [21] refrigerated cabinets, whirlpool sp…
```
- `train_station/PMC8672270_14.txt` ['non_english']
```text
Table 1: Nominal values for normal human adult breathing at sea-level Condition Rate (Breaths/min) Tidal Volume (L/breath) Minute Ventilation (L/min) Nominal At-Rest 12 0.5 6 Normal Activity 16 1 16 M…
```

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 3

- `1_turn_1` (standalone) gold=['water_spray/what_does_reduce_reuse_recycle_mean_22.txt']: In disposing of water repellent sprays, does giving away a half-used can help the environment more than destroying it?
- `1_turn_3` (pronoun) gold=['water_spray/what_does_reduce_reuse_recycle_mean_22.txt']: I’m curious—do those reuse suggestions actually end up being better for the environment than just dropping it off as hazardous waste?
- `106_turn_3` (standalone) gold=['hybrid_cars/Lifecycleassessment_13.txt']: I wonder if newer battery tech and updated factories make those old studies less accurate now?

### ❌ Bằng chứng nằm muộn (> 1500 ký tự) — 10

- `104_turn_1` offset=7324c gold=`sustainable_plastic/Bioplastic_3.txt`
  - query: In plastics, what exactly are bioplastics and how are they different from regular plastics?
  - bằng chứng: structure of the polymer, and different bioplastics have different structures,
- `57_turn_2` offset=6202c gold=`water/Pumpedstoragehydroelectricity_4.txt`
  - query: I wonder if those pump efficiency numbers make a big difference in whether this setup actually saves money?
  - bằng chứng: [1] [2] The reservoirs used with pumped storage can be quite small
- `106_turn_4` offset=3575c gold=`hybrid_cars/Lifecycleassessment_7.txt`
  - query: Is there a way those official methods make sure everyone’s comparing hybrids and gas cars the same way?
  - bằng chứng: * **Assumptions and limitations** , [22] which includes any assumptions or decisions made throughout the study that may influence the final results.
- `104_turn_3` offset=2599c gold=`sustainable_plastic/Bioplastic_8.txt`
  - query: Would using plastics that don’t break down easily be a big problem for backyard projects?
  - bằng chứng: but have a lower carbon footprint than petroleum-based plastics used for the
- `104_turn_2` offset=2460c gold=`sustainable_plastic/Bioplastic_20.txt`
  - query: What actually happens to these plastics if I just toss them out after a project?
  - bằng chứng: cultivation of renewable raw materials to produce bioplastics.

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 12

- `2_turn_2` OOV=['defeat']: What happens if those compostable plastics end up leaving behind toxins like PFAS—doesn’t that kind of defeat the purpose?
- `4_turn_2` OOV=['18m']: Would that much comfrey actually cover an 18m² bed every year, or would I need to plant more?
- `11_turn_1` OOV=['jacobson']: Regarding Italy's switch to electric cars, how much does Mark Jacobson estimate electricity demand would rise compared to rough calculations…
- `28_turn_1` OOV=['certify']: In Energy Star ratings, does the need for quick cost savings make it hard to certify portable fans?
- `30_turn_2` OOV=['temps']: Would running these radiators at lower temps actually help a boiler work more efficiently than with regular radiators?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 5

*nguyên nhân: {'lexical_gap (overlap<0.2)': 4, 'ranking/distractor': 1}*

- `1_turn_1` ti=0 ctx=standalone overlap=0.0: In disposing of water repellent sprays, does giving away a half-used can help the environment more than destroying it?
  - gold ['water_spray/what_does_reduce_reuse_recycle_mean_22.txt'] | top3 ['mosquito/9427576_28.txt', 'asparagas/Permaculture_132.txt', 'credit_card/responsiblecreditcards_4.txt']
- `106_turn_3` ti=2 ctx=standalone overlap=0.0: I wonder if newer battery tech and updated factories make those old studies less accurate now?
  - gold ['hybrid_cars/Lifecycleassessment_13.txt'] | top3 ['soy_ink/Soyink_57.txt', 'alle/ginsengbenefits_70.txt', 'water_plant/howtofertilizeplantsinwaterhtm_15.txt']
- `38_turn_1` ti=0 ctx=standalone overlap=0.091: In train station air quality, how much air does someone typically breathe in during half an hour?
  - gold ['train_station/PMC8672270_10.txt', 'train_station/PMC8672270_12.txt', 'train_station/PMC8672270_14.txt'] | top3 ['ceremics/makingcompostforyourvegetablegarden_57.txt', 'water/Pumpedstoragehydroelectricity_5.txt', 'rain_water/designingadiyslowsandfilterwhattoconsider_16.txt']
- `77_turn_3` ti=2 ctx=pronoun overlap=0.091: Are there any plants around here that actually kill mosquitoes, not just keep them away?
  - gold ['mosquito/9427576_28.txt'] | top3 ['mosquito/9427576_31.txt', 'mosquito/9427576_26.txt', 'mosquito/9427576_27.txt']
- `106_turn_1` ti=0 ctx=standalone overlap=0.3: In comparing hybrid and traditional cars, how do the things we measure affect which seems more sustainable?
  - gold ['hybrid_cars/Lifecycleassessment_18.txt', 'hybrid_cars/Lifecycleassessment_25.txt', 'hybrid_cars/Lifecycleassessment_32.txt'] | top3 ['rent_solar/solarleasingoption_24.txt', 'co2_emission_regulation/finalsafefriawebversion200701pdf_1944.txt', 'rebound/longevity3stepstowardsresponsibleliving_19.txt']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.