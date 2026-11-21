# Báo cáo chất lượng dữ liệu — domain `economics`

*Tạo lúc 2026-11-21T09:05:48 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 81.9 🟡** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 97.3 | 🟢 |
| content | 0.25 | 50.0 | 🔴 |
| conversation | 0.15 | 100.0 | 🟢 |
| gold | 0.25 | 87.1 | 🟢 |
| link | 0.15 | 87.6 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| content | % trùng chính xác | 19.17 | 1.0 | 19.17 |
| content | % doc quá ngắn | 30.54 | 0.5 | 15.27 |
| gold | % gold có lỗi nội dung nghiêm trọng | 25.71 | 0.5 | 12.86 |
| link | % turn gold không chia sẻ từ nào với query | 7.61 | 1.5 | 11.42 |
| content | % ký hiệu lạ/URL nặng | 16.13 | 0.4 | 6.45 |
| content | % nghi không phải tiếng Anh | 12.66 | 0.5 | 6.33 |
| integrity | % doc có ký tự điều khiển | 0.93 | 2 | 1.86 |
| content | % lặp bất thường | 2.51 | 0.5 | 1.25 |
| integrity | % doc có mojibake | 0.4 | 2 | 0.8 |
| content | % boilerplate | 2.37 | 0.3 | 0.71 |
| content | % gần trùng (ngoài trùng chính xác) | 0.99 | 0.7 | 0.69 |
| link | % turn overlap=0 (kể cả history) | 1.09 | 0.5 | 0.55 |

## 2. Khuyến nghị

- **[medium]** 0.4% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 30.54%.
- **[medium]** Trùng chính xác 19.17%.
- **[low]** 12.66% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 64.29% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 25.71% gold doc có lỗi nội dung nghiêm trọng.
- **[medium]** 7.61% turn gold KHÔNG chia sẻ từ nào với query.
- **[medium]** Bằng chứng nằm sau 650 ký tự ở 48.31% gold.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **50,220** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.4% | ký tự điều khiển 0.93% | HTML/entity sót 0.05%
- Benchmark: 22 hội thoại | schema=`qa_pair` | vai trò {'user': 92, 'assistant': 92} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 92/92
- qrels: 159 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 159} | qid 92

## 4. Chất lượng nội dung

- Ký tự: min=3 p25=35.0 **median=120.0** mean=394.5 p75=346.0 p90=909.0 p99=3822.0 max=39672 | outlier dài (>1279.0c): 7.15%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 85.8% / 88.56% / 93.83% / 97.76%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 45.85% |
| 101-300 | 26.05% |
| 301-650 | 13.9% |
| 651-800 | 2.76% |
| 801-1500 | 5.26% |
| 1501-3000 | 3.93% |
| 3001-6000 | 1.96% |
| >6000 | 0.28% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 15339 | 30.54% |
| mojibake | lỗi encoding (mojibake) | 199 | 0.4% |
| control_chars | ký tự điều khiển | 466 | 0.93% |
| html_residue | HTML/entity còn sót | 25 | 0.05% |
| boilerplate | boilerplate/menu/footer | 1191 | 2.37% |
| url_heavy | URL chiếm >25% nội dung | 6987 | 13.91% |
| symbol_heavy | ký hiệu lạ >30% | 1115 | 2.22% |
| repetitive | lặp từ/dòng bất thường | 1262 | 2.51% |
| non_english | nghi không phải tiếng Anh | 6358 | 12.66% |
| pii_email | chứa email | 199 | 0.4% |
| pii_phone | chứa số điện thoại | 423 | 0.84% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 4461 | 8.88% |
| starts_lower | bắt đầu bằng chữ thường | 2257 | 4.49% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **53.71%**
- Trùng chính xác: 9,626 doc dư (19.17%), 3901 nhóm
- Gần trùng: 588 cụm | doc dư gần-trùng ngoài trùng chính xác 136 (0.99%) | cụm lớn nhất 16
- Từ vựng (mẫu 10,055 doc): 33,112 từ | hapax 41.07% | Zipf -0.97 | https(5800), wiki(5423), 1(4897), 0(3813), s(3121), www(2972), 2(2969), com(2769), org(2747), x(2061), t(1725), 3(1690), en(1245), 4(1230), svg(1195)

## 5. Hội thoại

- **22** hội thoại, **92** turn | turn/hội thoại: mean 4.18 (min 3, max 6) | query: mean 18.0 từ, median 18.0, p95 23.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 47 | 51.09% |
| pronoun | 37 | 40.22% |
| connector | 8 | 8.7% |
| short_ellipsis | 0 | 0% |

→ **64.29%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 0 (0.0%)
- Chuyển chủ đề: {'weak': 30.0, 'shift': 21.43, 'on_topic': 48.57} | hội thoại nhảy chủ đề ≥50% turn: 22.73%

**Loại câu hỏi:** statement_other 41.3%, yes_no 41.3%, what 8.7%, how 4.35%, why 3.26%, wh_other 1.09%

## 6. Gold / qrels

- Nguồn gold: {'inline': 92} | qrels được dùng để eval: False
- Gold/turn: mean 1.73, max 6
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 92/92 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 50,150/50,220 (99.86%) | Gini 0.2808
- Độ dài gold vs corpus (median): 2128.0 vs 120.0 (tỷ lệ 17.73x)
- Gold có lỗi nghiêm trọng: 25.71% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.244** (có history: 0.251) | overlap=0: 7.61% | <20%: 38.04% | overlap=0 dù có history: 1.09%
- Overlap theo ngữ cảnh: {'standalone': 0.256, 'pronoun': 0.222, 'connector': 0.271}
- OOV: 13.04% (TB 1.4%)
- **Vị trí bằng chứng** (89 mẫu): {'0-20%': 40.45, '20-40%': 23.6, '40-60%': 12.36, '60-80%': 15.73, '80-100%': 7.87} | median offset 555c | sau 650c: 48.31% | sau 512 token: 2.25%

## 8. BM25 baseline

- 92 query | 70 gold + 200 nhiễu
- nDCG@10 single/history = 0.5686/0.7682 | Recall@10 = 0.7161/0.91

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 22 | 0.6537 | 0.6495 | 0.7409 | 0.7333 |
| 2 | 22 | 0.4506 | 0.8299 | 0.6364 | 0.9773 |
| 3 | 22 | 0.598 | 0.7869 | 0.7879 | 0.928 |
| 4 | 15 | 0.6337 | 0.8856 | 0.7389 | 1.0 |
| 5+ | 11 | 0.4872 | 0.6846 | 0.6515 | 0.9697 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 8 | 0.7409 | 0.833 | 0.9167 | 0.9583 |
| pronoun | 37 | 0.5312 | 0.7903 | 0.705 | 0.9662 |
| standalone | 47 | 0.5688 | 0.7398 | 0.6908 | 0.8574 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 4 | 0.3673 | 0.9831 | 0.3333 | 1.0 |
| statement_other | 38 | 0.6223 | 0.7655 | 0.7645 | 0.8456 |
| wh_other | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| what | 8 | 0.3955 | 0.7841 | 0.5625 | 1.0 |
| why | 3 | 0.6219 | 0.5546 | 0.7778 | 0.8889 |
| yes_no | 38 | 0.5571 | 0.7557 | 0.7281 | 0.9452 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 22 | 0.6537 | 0.6495 | 0.7409 | 0.7333 |
| on_topic | 34 | 0.5454 | 0.7925 | 0.6887 | 0.9755 |
| shift | 15 | 0.6462 | 0.8011 | 0.8444 | 0.9778 |
| weak | 21 | 0.4619 | 0.8297 | 0.6429 | 0.9405 |

- Turn khó: **5** (5.43%) — {'lexical_gap (overlap<0.2)': 4, 'ranking/distractor': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 196 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 15,339

**`Irreversibility/33265832_100.txt`** (17 ký tự)
```text
### Affiliations
```
**`Irreversibility/33265832_103.txt`** (17 ký tự)
```text
Item in Clipboard
```
**`Irreversibility/33265832_105.txt`** (49 ký tự)
```text
Ruben Krantz et al. Entropy (Basel) . 2018 .
```
**`Irreversibility/33265832_106.txt`** (12 ký tự)
```text
Show details
```
**`Irreversibility/33265832_107.txt`** (15 ký tự)
```text
Display options
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 199

**`nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_0.txt`** (2684 ký tự)
```text
6.254: Game Theory with Engineering Applications February 23, 2010 Lecture 6: Continuous and Discontinuous Games Lecturer: Asu Ozdaglar 1 Introduction In this lecture, we will focus on: • Existence of a mixed strategy Na…
```
**`nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_10.txt`** (1092 ký tự)
```text
1 ∂x1∂x2 · · · ∂2 ⎜⎜ u2(x) . ⎝ ⎟⎟ U(x) = ⎠ .. . ∂x2∂x1 . . . The next proposition provides a sufficient condition for the payoff functions to be diagonally strictly concave. Proposition 4 For all i ∈ I, assume that the s…
```
**`nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_4.txt`** (2246 ký tự)
```text
It can be established using Dasgupta-Maskin result that there exists a mixed strategy Nash equilibrium. Let us next proceed to find a mixed strategy Nash equilibrium. We focus on symmetric Nash equilibria, i.e., both fir…
```
**`nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_5.txt`** (1566 ký tự)
```text
Example 3: Consider a game with 2 players, Si = [0, 1] for i = 1, 2, and the payoffs are given by 2 u1(s1, s2) = s1s2 − s1 , 2 6-7 2 u2(s1, s2) = s1s2 − s2 . 2 Note that ui(s1, s2) is strictly concave in si. It can be se…
```
**`nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_8.txt`** (1043 ký tự)
```text
T �u(x¯) > 0. Theorem 4 Consider a strategic form game �I,(Si),(ui)�. For all i ∈ I, assume that the strategy sets Si are given by Eq. (3), where hi is a concave function, and there exists some x˜i ∈ Rmi such that hi(x˜i…
```

### ❌ `control_chars` — ký tự điều khiển — 466

**`hyperbolicsine/BellemareWichmanIHSFebruary2019pdf_0.txt`** (3786 ký tự)
```text
Elasticities and the Inverse Hyperbolic Sine Transformation∗ Marc F. Bellemare† Casey J. Wichman‡ February 24, 2019 Abstract Applied econometricians frequently apply the inverse hyperbolic sine (or arcsinh) transformatio…
```
**`hyperbolicsine/BellemareWichmanIHSFebruary2019pdf_3.txt`** (1844 ký tự)
```text
Researchers often adopt the arcsinh transformation to approximate a logarithm and interpret coefficients as they would for a logarithmic equation. In this case, one can approximate semi-elasticities as shown by Halvorsen…
```
**`inheritance_inequality/830_1.txt`** (3112 ký tự)
```text
Filippo Gusella Notes on Piketty's model n. 830 – Maggio 2020 Notes on Piketty's model Filippo Gusella* Abstract Thomas Piketty's Capital in the Twenty-First Century is primarily an empirical investigation into the histo…
```
**`inheritance_inequality/830_22.txt`** (2493 ký tự)
```text
λ z a (25) If we observe an increase of ω = s (1 + r) / (1 + g), that is an increase in the divergence between r and g, λ = (1 − ω)/(ω − p) can be considered a constant, a = log  1 p  / log  ω p  > 1 decreases and s…
```
**`kalman_filter/ssrn_36.txt`** (388 ký tự)
```text
t−4 ⎞ ⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎠ = ⎛ ⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎝ A1 0 0 0 0 0 0 0000 Ir 0 0 0 0 0 0 0000 0 Ir 0 0 0 0 0 0000 0 0 Ir 0 0 0 0 0000 0 00 Ir 0 0 0 0000 0 0 0 0 0 diag(α1,...,αn) 0 0000 0 0 0 00 0 αQ 0000 0 0 0 0 0 0 1 0000 0 0…
```

### ❌ `html_residue` — HTML/entity còn sót — 25

**`Irreversibility/743_135.txt`** (229 ký tự)
```text
<strong>Figure 1</strong><br/> <p>Evolution of country fitnesses throughout the iterations of the fitness and complexity algorithm both clearly show a convergence to a fixed point \(using <math display="inline"><semantic…
```
**`Irreversibility/743_137.txt`** (100 ký tự)
```text
</semantics></math> for exact replication of revealed comparative advantage \(RCA\) filtering\).</p>
```
**`Irreversibility/743_138.txt`** (1277 ký tự)
```text
") [ ](https://pub.mdpi-res.com/entropy/entropy-20-00743/article_deploy/html/images/entropy-20-00743-g002.png?1570523858 " <strong>Figure 2</strong><br/> <p>The normalized gross domestic product \(GDP\) per capita and fi…
```
**`Irreversibility/743_146.txt`** (87 ký tự)
```text
</semantics></math> filtered, correlation coefficient: 0.64, standard error: 0.028.</p>
```
**`Irreversibility/743_147.txt`** (452 ký tự)
```text
") [ ](https://pub.mdpi-res.com/entropy/entropy-20-00743/article_deploy/html/images/entropy-20-00743-g005.png?1570523858 " <strong>Figure 5</strong><br/> <p>Commodity complexity spectra, showing the export product basket…
```

### ❌ `boilerplate` — boilerplate/menu/footer — 1,191

**`deposit_interest/moneycreationinthemoderneconomypdf_0.txt`** (4791 ký tự)
```text
14 Quarterly Bulletin 2014 Q1 Money creation in the modern economy By Michael McLeay, Amar Radia and Ryland Thomas of the Bank’s Monetary Analysis Directorate.(1)  This article explains how the majority of money in the …
```
**`ppf_retire/ProductionE28093possibilityfrontier_5.txt`** (2245 ký tự)
```text
* [ Printable version ](/w/index.php?title=Production%E2%80%93possibility_frontier&printable=yes "Printable version of this page \[p\]") In other projects * [ Wikimedia Commons ](https://commons.wikimedia.org/wiki/Catego…
```
**`russia_sanction_oil/ussanctionsrussiacentralbankhtml_0.txt`** (7067 ký tự)
```text
SKIP TO CONTENTSKIP TO SITE INDEXSECTION NAVIGATION SEARCH Account Russia-Ukraine War Photos Maps A Family’s Tragedy in Odesa Life on the Front Line Fearing Russian Hit Squads You have been granted access, use your keybo…
```
**`econ_social/PMC5640760_24.txt`** (1181 ký tự)
```text
The REF data provides more information on the linkages between economics and other subjects via the submission to other UoAs of papers also submitted to the economics UoA. The proportion of joint submissions, shown in th…
```
**`Irreversibility/743_36.txt`** (97 ký tự)
```text
_clear_ [ _zoom_out_map_ ](/toggle_desktop_layout_cookie "Toggle desktop layout") _search_ _menu_
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 6,987

**`diminish_return/Supermodularfunction_5.txt`** (2506 ký tự)
```text
* [ Printable version ](/w/index.php?title=Supermodular_function&printable=yes "Printable version of this page \[p\]") From Wikipedia, the free encyclopedia Mathematical function class In [ mathematics ](/wiki/Mathematic…
```
**`diminish_return/Supermodularfunction_6.txt`** (2923 ký tự)
```text
Supermodularity in economics and game theory [ [ edit ](/w/index.php?title=Supermodular_function&action=edit&section=1 "Edit section: Supermodularity in economics and game theory") ] The concept of supermodularity is use…
```
**`gdp_network/InputE28093outputmodel_11.txt`** (2808 ký tự)
```text
Basic derivation [ [ edit ](/w/index.php?title=Input%E2%80%93output_model&action=edit&section=2 "Edit section: Basic derivation") ] The model depicts inter-industry relationships within an economy, showing how output fro…
```
**`gdp_network/InputE28093outputmodel_12.txt`** (2220 ký tự)
```text
{\displaystyle A} ![{\\displaystyle A}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7daff47fa58cdfd29dc333def748ff5fa4c923e3) be the matrix of coefficients a i j {\displaystyle a_{ij}} ![{\\displaystyle a_{ij…
```
**`tesla_free_charging/Complementarygood_39.txt`** (2399 ký tự)
```text
In [ economics ](/wiki/Economics "Economics") , a **complementary good** is a [ good ](/wiki/Goods_\(economics\) "Goods \(economics\)") whose appeal increases with the popularity of its complement. [ _[ further explanati…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 1,115

**`Irreversibility/33265832_13.txt`** (13 ký tự)
```text
#### Account
```
**`Irreversibility/33265832_137.txt`** (12 ký tự)
```text
**Figure 1**
```
**`Irreversibility/33265832_144.txt`** (12 ký tự)
```text
**Figure 2**
```
**`Irreversibility/33265832_151.txt`** (12 ký tự)
```text
**Figure 3**
```
**`Irreversibility/33265832_158.txt`** (12 ký tự)
```text
**Figure 4**
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 1,262

**`printmoney_inflation/vol_3.txt`** (694 ký tự)
```text
10 15 20 Average M1 Growth Average Inflation 0 5 10 15 20 0 5 10 15 20 Average M2 Growth Average Inflation 0 5 10 15 20 0 5 10 15 20 Figure 1: Scatter Plots of Average Inflation and Average Growth Rates of M0, M1 and M2 …
```
**`nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_10.txt`** (1092 ký tự)
```text
1 ∂x1∂x2 · · · ∂2 ⎜⎜ u2(x) . ⎝ ⎟⎟ U(x) = ⎠ .. . ∂x2∂x1 . . . The next proposition provides a sufficient condition for the payoff functions to be diagonally strictly concave. Proposition 4 For all i ∈ I, assume that the s…
```
**`nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_9.txt`** (905 ký tự)
```text
T (x∗ − x¯i) i i � i∈I i∈I > λ∗ i �hi(xi ∗ ) T (x¯i − xi ∗ ) + λ¯i�hi(x¯i) T (x∗ i − x¯i), i∈I i∈I 6-11 where to get the strict inequality, we used the assumption that the payoff functions are diagonally strictly concave…
```
**`new_keynesian/benchmarkdsge_17.txt`** (842 ký tự)
```text
ÃYτ s=1 Πχ t+s−1 Πt+s !−ε mct+τyd t+τ and g2 t = Et X∞ τ=0 (βθp) τ λt+τ ÃYτ s=1 Πχ t+s−1 Πt+s !1−ε p∗ t pt yd t+τ and then the first order condition is εg1 t = (ε − 1)g2 t . As it was the case for f’s that we found in th…
```
**`new_keynesian/benchmarkdsge_28.txt`** (718 ký tự)
```text
μt−1 zt zt−1 Ã 1 − S " xt zt zt xt−1 zt−1 zt−1 #! xt zt = 0. 3.2. Change of Variables We now redefine that variables to obtain a system on stationary variables that we can easily manipulate. Hence, we define ect = ct zt …
```

### ❌ `non_english` — nghi không phải tiếng Anh — 6,358

**`printmoney_inflation/vol_3.txt`** (694 ký tự)
```text
10 15 20 Average M1 Growth Average Inflation 0 5 10 15 20 0 5 10 15 20 Average M2 Growth Average Inflation 0 5 10 15 20 0 5 10 15 20 Figure 1: Scatter Plots of Average Inflation and Average Growth Rates of M0, M1 and M2 …
```
**`new_keynesian/benchmarkdsge_29.txt`** (559 ký tự)
```text
+βEtqet+1 λet+1 λet zt zt+1 S0 ∙ xet+1 xet zt+1 zt ¸ µxet+1 xet zt+1 zt ¶2 ft = η − 1 η (we∗ t ) 1−η λet (wet) η l d t + βθwEt µ Πχw t Πt+1¶1−η µwe∗ t+1 we∗ t zt+1 zt ¶η−1 ft+1 ft = ψdtϕt (Π∗w t ) −η(1+γ) ¡ l d t ¢1+γ + …
```
**`new_keynesian/benchmarkdsge_58.txt`** (843 ký tự)
```text
³ Πbt+1 − χwΠbt + ∆b we ∗ t+1´´ 42 Rearranging, (1 − a6) d bt + (1 − a6) ϕbt + η (1 + γ) (1 − a6) b wet − η (1 + γ) b we ∗ t + (1 + γ) (1 − a6)bl d t − f bt +a6Etf bt+1 + a6η (1 + γ)EtΠbt+1 − a6η (1 + γ) χwΠbt + a6η (1 +…
```
**`new_keynesian/benchmarkdsge_62.txt`** (956 ký tự)
```text
000 0 1 − a3 0 0 001 0 0 0 0 ⎞ ⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎠ LL = ⎛ ⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎝ 0 −βbz˜ 000 0 0 000 0 0 000 0 0 000 0 0 000 0 0 000 0 0 000 0 0 000 ⎞ ⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎠ MM = ⎛ ⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎝ 0 1 0 00 0 0 0 00 0 0 0 00 0 0 0 00 0 0 0…
```
**`new_keynesian/benchmarkdsge_63.txt`** (1377 ký tự)
```text
000 NN ⎤ ⎥ ⎥ ⎥ ⎥ ⎦ 49 and B = ⎡ ⎢ ⎢ ⎢ ⎢ ⎣ 0 QQ 0 I ⎤ ⎥ ⎥ ⎥ ⎥ ⎦ ∗ Σ1/2 . 4.4.4. Building the C and D matrices Define the observables vector: obst = (log Πt, log Rt, 4 log wt, 4 log yt) 0 . Note that: Πbt = P P (1, :) ∗ st…
```

### ❌ `pii_email` — chứa email — 199

**`printmoney_inflation/vol_0.txt`** (4050 ký tự)
```text
The Economic and Social Review, Vol. 35, No. 3, Winter, 2004, pp. 251-266 Inflation and Money Growth: Evidence from a Multi-Country Data-Set JOHN C. FRAIN* Central Bank and Financial Services Regulatory Authority of Irel…
```
**`volunteerdillema/174243pdfrefreqidfastlydefault3A88b79b5167e1aaf791f6cb7976234486absegmentsorigininitiatoracceptTC1_0.txt`** (2581 ký tự)
```text
Volunteer's Dilemma Author(s): Andreas Diekmann Source: The Journal of Conflict Resolution , Dec., 1985, Vol. 29, No. 4 (Dec., 1985), pp. 605-610 Published by: Sage Publications, Inc. Stable URL: https://www.jstor.org/st…
```
**`hyperbolicsine/BellemareWichmanIHSFebruary2019pdf_0.txt`** (3786 ký tự)
```text
Elasticities and the Inverse Hyperbolic Sine Transformation∗ Marc F. Bellemare† Casey J. Wichman‡ February 24, 2019 Abstract Applied econometricians frequently apply the inverse hyperbolic sine (or arcsinh) transformatio…
```
**`inheritance_inequality/830_1.txt`** (3112 ký tự)
```text
Filippo Gusella Notes on Piketty's model n. 830 – Maggio 2020 Notes on Piketty's model Filippo Gusella* Abstract Thomas Piketty's Capital in the Twenty-First Century is primarily an empirical investigation into the histo…
```
**`abolish_trade/lseacukstorageLIBRARYSecondarylibfilesharedrepositoryContentLSE20BrexitVote20blogbrexit02pdf_1.txt`** (2936 ký tự)
```text
Brexit, UK incomes fall by 1% in the optimistic case and 2.3% in the pessimistic case.  In the long run, reduced trade lowers productivity. Factoring in these effects substantially increases the costs of Brexit to a los…
```

### ❌ `pii_phone` — chứa số điện thoại — 423

**`stole/ajol_6.txt`** (5683 ký tự)
```text
and transparent. This includes setting reasonable tax rates that do not excessively burden taxpayers and providing clear guidelines on tax obligations. Fair tax policies can encourage voluntary compliance and discourage …
```
**`gaza_aid/2016246Mooliopdf_8.txt`** (3684 ký tự)
```text
Source: Author’s calculation through E-views 8 Software. LEGEND: a) Numbers in parenthesis are p-values for corresponding Statistic. b) * indicates that Statistic is significant at 5% significance level. Athens Journal o…
```
**`volunteerdillema/174243pdfrefreqidfastlydefault3A88b79b5167e1aaf791f6cb7976234486absegmentsorigininitiatoracceptTC1_0.txt`** (2581 ký tự)
```text
Volunteer's Dilemma Author(s): Andreas Diekmann Source: The Journal of Conflict Resolution , Dec., 1985, Vol. 29, No. 4 (Dec., 1985), pp. 605-610 Published by: Sage Publications, Inc. Stable URL: https://www.jstor.org/st…
```
**`abolish_trade/lseacukstorageLIBRARYSecondarylibfilesharedrepositoryContentLSE20BrexitVote20blogbrexit02pdf_1.txt`** (2936 ký tự)
```text
Brexit, UK incomes fall by 1% in the optimistic case and 2.3% in the pessimistic case.  In the long run, reduced trade lowers productivity. Factoring in these effects substantially increases the costs of Brexit to a los…
```
**`onrrp/2326853pdfrefreqidfastlydefault3A1e0b8cbcb0976b37cc46b0f2f97e70ababsegmentsorigininitiatoracceptTC1_1.txt`** (2503 ký tự)
```text
depositors or to earn higher profits than member institutions. At present, reserve requirements on nonmember banks vary from state to state, with the average required reserve ratio close to that imposed by the Federal Re…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 4,461

**`stole/ajol_3.txt`** (5927 ký tự)
```text
conducted a study to examine the effect of tax revenue on the economic development of Nigeria (Ofoegbu et al., 2016). Their findings revealed a positive and significant relationship between tax revenue and economic devel…
```
**`stole/ajol_4.txt`** (5594 ký tự)
```text
taxpurposes. Avoidance takes the form of investment in arts collection, emigration of persons and capital. And as observed by Toby (2003) the tax payer indulges in evasion by resorting to various practices. These practic…
```
**`stole/ajol_5.txt`** (5790 ký tự)
```text
strengthened, leading to increased compliance and greater resources for grassroots development. 3. DISCUSSION OF FINDINGS Investigate the relationship between tax revenue and economic development in Nigeria. The investig…
```
**`stole/ajol_6.txt`** (5683 ký tự)
```text
and transparent. This includes setting reasonable tax rates that do not excessively burden taxpayers and providing clear guidelines on tax obligations. Fair tax policies can encourage voluntary compliance and discourage …
```
**`negative_gdp/chapter07pdf_0.txt`** (3516 ký tự)
```text
CHAPTER 7: CHANGE IN PRIVATE INVENTORIES (Updated: December 2021) Definitions and Concepts Recording in the NIPAs Overview of Source Data and Estimating Methods Benchmark-year estimates Nonbenchmark-year estimates Most-r…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 2,257

**`stole/ajol_3.txt`** (5927 ký tự)
```text
conducted a study to examine the effect of tax revenue on the economic development of Nigeria (Ofoegbu et al., 2016). Their findings revealed a positive and significant relationship between tax revenue and economic devel…
```
**`stole/ajol_4.txt`** (5594 ký tự)
```text
taxpurposes. Avoidance takes the form of investment in arts collection, emigration of persons and capital. And as observed by Toby (2003) the tax payer indulges in evasion by resorting to various practices. These practic…
```
**`stole/ajol_5.txt`** (5790 ký tự)
```text
strengthened, leading to increased compliance and greater resources for grassroots development. 3. DISCUSSION OF FINDINGS Investigate the relationship between tax revenue and economic development in Nigeria. The investig…
```
**`stole/ajol_6.txt`** (5683 ký tự)
```text
and transparent. This includes setting reasonable tax rates that do not excessively burden taxpayers and providing clear guidelines on tax obligations. Fair tax policies can encourage voluntary compliance and discourage …
```
**`public_debt_default/ssrn_7.txt`** (4094 ký tự)
```text
implications for debt sustainability exercises and debt default thresholds. Indeed, in 16 Average reserve requirements for developing countries in his 1960 to early 1980s sample ran at about 0.25, more than three times t…
```

### ❌ Trùng chính xác — 9,626

*3901 nhóm*

- nhóm: `Irreversibility/743_410.txt`, `efficiency_equity/495_280.txt`, `interest_rate_parity/2798_313.txt`
```text
Multiple requests from the same IP address are counted as one view.
```
- nhóm: `fdic/pr24008html_8.txt`, `fdic/pr24014html_8.txt`
```text
_[ ![Home](/themes/custom/fdic_theme/fdic90-logo-white-orig-300x100.png) ](/ "Home") _
```
- nhóm: `federal_reserve_tax/deficittracker_130.txt`, `federal_reserve_tax/deficittracker_467.txt`
```text
* **The government ran a cumulative deficit of $418 billion** * Outlays in the first quarter of FY2023 were impacted by unique timing shifts, if not for which the cumulative deficit for FY2023 would have been $455 billio…
```
- nhóm: `federal_reserve_tax/deficittracker_301.txt`, `federal_reserve_tax/deficittracker_641.txt`
```text
While revenue has sagged relative to the prior fiscal year, outlays have exploded—they have been 51% greater so far in FY2020 than at the same point in FY2019. Most of this increase has come from the federal response to …
```
- nhóm: `hyperbolicsine/logtransformationpurposeandinterpretation9444b4b049c9_2.txt`, `hyperbolicsine/logtransformationpurposeandinterpretation9444b4b049c9_7.txt`
```text
[ Sign in ](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40kyawsawhtoon%2Flog- transformation-purpose-and-interpretation-9444b4b049c9&source=post_page--- two_column_layout_nav-----------------------glob…
```

### ❌ Gần trùng (khác nhau chút ít) — 136

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 11: `abolish_trade/YearWithoutaSummer_115.txt`, `bronze_coin/Aesgrave_87.txt`, `bronze_coin/Goldcoin_113.txt`, `economic_growth/Dynamicstochasticgeneralequilibrium_190.txt`, `economy_wealth/WealthinequalityintheUnitedStates_186.txt`
  - `abolish_trade/YearWithoutaSummer_115.txt`:
```text
* [ Privacy policy ](https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Privacy_policy) * [ About Wikipedia ](/wiki/Wikipedia:About) * [ Disclaimers ](/wiki/Wikipedia:General_disclaimer) * [ Contact Wikipedi…
```
  - `bronze_coin/Aesgrave_87.txt`:
```text
* [ Privacy policy ](https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Privacy_policy) * [ About Wikipedia ](/wiki/Wikipedia:About) * [ Disclaimers ](/wiki/Wikipedia:General_disclaimer) * [ Contact Wikipedi…
```
- cụm size 11: `bronze_coin/Historyofcoppercurre_63.txt`, `deregulation/GrammE28093LeachE280_245.txt`, `differenceindifference/Syntheticcontrolmethod_53.txt`, `domestic_foreign/Externaldebt_97.txt`, `economy_wealth/EconomyoftheUnitedStates_651.txt`
  - `bronze_coin/Historyofcoppercurre_63.txt`:
```text
* This page was last edited on 11 June 2023, at 19:42 (UTC) . * Text is available under the [ Creative Commons Attribution-ShareAlike License 4.0 ](//en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attributi…
```
  - `deregulation/GrammE28093LeachE280_245.txt`:
```text
* This page was last edited on 8 April 2024, at 09:16 (UTC) . * Text is available under the [ Creative Commons Attribution-ShareAlike License 4.0 ](//en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attributi…
```
- cụm size 10: `bell_number/Weakordering_0.txt`, `debt2gdp/NationaldebtoftheUnitedStates_0.txt`, `decoy_effect/Decoyeffect_0.txt`, `diminish_return/Supermodularfunction_0.txt`, `economic_growth/Balancedgrowthequilibrium_0.txt`
  - `bell_number/Weakordering_0.txt`:
```text
Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events …
```
  - `debt2gdp/NationaldebtoftheUnitedStates_0.txt`:
```text
Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events …
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

### ✅ Turn đầu có đại từ/liên từ lơ lửng
- Không phát hiện.

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 37

- `0_turn_2`: Is that why things like schools and hospitals end up underfunded in those countries?
- `1_turn_2`: Is it even possible to say which lottery they'd pick if we don't know their exact utility function?
- `1_turn_3`: Would one of those lotteries actually give better odds at every payoff, or are they kind of equal?
- `3_turn_2`: I wonder if there are any big examples where a country just couldn’t pay back its own treasury bonds because of a crisis like hyperinflation…
- `3_turn_3`: Would that kind of default make it way harder for them to borrow money later on?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 8

- `0_turn_3`: But what happens if the people in charge misuse the extra tax money? Does it still help regular folks?
- `10_turn_4`: Oh, does having more second-generation women hitting childbearing age kind of keep the birth numbers up even if each person has fewer kids?
- `17_turn_3`: Why does that negative quadratic form actually guarantee diagonal strict concavity in this case?
- `22_turn_3`: Why did they start out with the multiple-price auctions back in 1929, and then stick with them for some securities later on?
- `38_turn_4`: And if two people send in orders at the exact same moment, how do they decide who goes first?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 15

- `0_turn_3` (cos=0.0)
  - trước: Is that why things like schools and hospitals end up underfunded in those countries?
  - sau: But what happens if the people in charge misuse the extra tax money? Does it still help regular folks?
- `1_turn_3` (cos=0.0)
  - trước: Is it even possible to say which lottery they'd pick if we don't know their exact utility function?
  - sau: Would one of those lotteries actually give better odds at every payoff, or are they kind of equal?
- `1_turn_4` (cos=0.0)
  - trước: Would one of those lotteries actually give better odds at every payoff, or are they kind of equal?
  - sau: How much can you really tell just by looking at the expected values in that case?
- `3_turn_3` (cos=0.0)
  - trước: I wonder if there are any big examples where a country just couldn’t pay back its own treasury bonds because of a crisis…
  - sau: Would that kind of default make it way harder for them to borrow money later on?
- `3_turn_4` (cos=0.0)
  - trước: Would that kind of default make it way harder for them to borrow money later on?
  - sau: Is it common for governments to just let inflation wipe out their debt instead of flat-out refusing to pay?

## D. Gold / qrels

### ✅ Gold mồ côi (doc không có trong corpus)
- Không phát hiện.

### ✅ qrels qid không khớp turn nào
- Không phát hiện.

### ✅ Gold inline (benchmark) ≠ qrels
- Không phát hiện.

### ✅ Turn không có gold
- Không phát hiện.

### ❌ Gold doc có lỗi nội dung nghiêm trọng — 18

- `diminish_return/Supermodularfunction_5.txt` ['url_heavy']
```text
* [ Printable version ](/w/index.php?title=Supermodular_function&printable=yes "Printable version of this page \[p\]") From Wikipedia, the free encyclopedia Mathematical function class In [ mathematic…
```
- `diminish_return/Supermodularfunction_6.txt` ['url_heavy']
```text
Supermodularity in economics and game theory [ [ edit ](/w/index.php?title=Supermodular_function&action=edit&section=1 "Edit section: Supermodularity in economics and game theory") ] The concept of su…
```
- `nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_0.txt` ['mojibake']
```text
6.254: Game Theory with Engineering Applications February 23, 2010 Lecture 6: Continuous and Discontinuous Games Lecturer: Asu Ozdaglar 1 Introduction In this lecture, we will focus on: • Existence of…
```
- `nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_9.txt` ['mojibake', 'repetitive']
```text
T (x∗ − x¯i) i i � i∈I i∈I > λ∗ i �hi(xi ∗ ) T (x¯i − xi ∗ ) + λ¯i�hi(x¯i) T (x∗ i − x¯i), i∈I i∈I 6-11 where to get the strict inequality, we used the assumption that the payoff functions are diagona…
```
- `nash_continuous/48cb7ae4210825b7de3d7fc0bcc8553fMIT6254S10lec06bpdf_10.txt` ['mojibake', 'repetitive']
```text
1 ∂x1∂x2 · · · ∂2 ⎜⎜ u2(x) . ⎝ ⎟⎟ U(x) = ⎠ .. . ∂x2∂x1 . . . The next proposition provides a sufficient condition for the payoff functions to be diagonally strictly concave. Proposition 4 For all i ∈ …
```

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 7

- `0_turn_2` (pronoun) gold=['stole/ajol_6.txt']: Is that why things like schools and hospitals end up underfunded in those countries?
- `16_turn_1` (standalone) gold=['diminish_return/Supermodularfunction_7.txt']: In production models, why does balancing two factors like X and Y boost output more than focusing on just one?
- `28_turn_6` (standalone) gold=['ppf_retire/ProductionE28093possibilityfrontier_8.txt']: What happens if the number of working-age people goes up but everything else stays the same?
- `47_turn_2` (standalone) gold=['nominal_interest_rate/ECTA17408_9.txt']: What happens if banks start earning less from loans—do they just cut back on lending?
- `54_turn_2` (pronoun) gold=['sabotage_product/monopoly3rddegreepricediscrimination_73.txt']: Is that kind of like when consoles are region-locked to stop people from buying cheaper ones elsewhere?

### ❌ Bằng chứng nằm muộn (> 1500 ký tự) — 16

- `32_turn_1` offset=4308c gold=`single_currency/Optimumcurrencyarea_7.txt`
  - query: In a global currency system, how could countries handle local economic problems without their own monetary policies?
  - bằng chứng: Should countries in a currency union have idiosyncratic business cycles, then optimal monetary policy may diverge and union participants may be made worse off u…
- `0_turn_3` offset=3094c gold=`stole/ajol_5.txt`
  - query: But what happens if the people in charge misuse the extra tax money? Does it still help regular folks?
  - bằng chứng: These actions can help maximize tax revenue and support equitable socio-economic
- `10_turn_3` offset=2838c gold=`uspopulationgrowth/ImmigrantsComingAmericaOlderAges_7.txt`
  - query: Is that partly because immigrant women boost the number of people having kids, even if each woman has fewer children ove…
  - bằng chứng: the native population more youthful while the lack of births to immigrants is
- `10_turn_5` offset=2838c gold=`uspopulationgrowth/ImmigrantsComingAmericaOlderAges_7.txt`
  - query: What happens when that aging trend keeps going—does natural increase eventually turn negative after 2060?
  - bằng chứng: the native population more youthful while the lack of births to immigrants is
- `0_turn_1` offset=2527c gold=`stole/ajol_6.txt`
  - query: In global business, how do big companies use tax havens to avoid taxes in poorer countries, and what does that mean for …
  - bằng chứng: public services and investments.

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 12

- `54_turn_4` OOV=['bump', 'miners']: How come they don’t just bump up prices if miners are willing to pay more?
- `57_turn_2` OOV=['bumping', 'throw']: Would bumping up the annual rate by mistake throw off the daily inflation numbers over a couple years?
- `0_turn_2` OOV=['underfunded']: Is that why things like schools and hospitals end up underfunded in those countries?
- `0_turn_3` OOV=['folks']: But what happens if the people in charge misuse the extra tax money? Does it still help regular folks?
- `3_turn_4` OOV=['refusing']: Is it common for governments to just let inflation wipe out their debt instead of flat-out refusing to pay?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 5

*nguyên nhân: {'lexical_gap (overlap<0.2)': 4, 'ranking/distractor': 1}*

- `16_turn_1` ti=0 ctx=standalone overlap=0.0: In production models, why does balancing two factors like X and Y boost output more than focusing on just one?
  - gold ['diminish_return/Supermodularfunction_7.txt'] | top3 ['ppf_retire/ProductionE28093possibilityfrontier_12.txt', 'ppf_retire/ProductionE28093possibilityfrontier_5.txt', 'ppf_retire/ProductionE28093possibilityfrontier_14.txt']
- `54_turn_1` ti=0 ctx=standalone overlap=0.083: In the GPU market, why would NVIDIA want to keep gamers and crypto miners from easily switching between uses?
  - gold ['sabotage_product/monopoly3rddegreepricediscrimination_71.txt', 'sabotage_product/monopoly3rddegreepricediscrimination_73.txt'] | top3 ['omo_money_supply/rqt1212gpdf_8.txt', 'sabotage_product/theendofethereumminingcouldbeabonanzaforgpushoppers_30.txt', 'inflation_interest/neofisherismpdf_4.txt']
- `73_turn_1` ti=0 ctx=standalone overlap=0.091: In investment decisions, how does using a Taylor expansion help compare options with different risk and return?
  - gold ['invest_risk_return/1807_13.txt'] | top3 ['invest_risk_return/riskreturntradeoffasp_7.txt', 'ppf_retire/ProductionE28093possibilityfrontier_8.txt', 'invest_risk_return/1807_14.txt']
- `64_turn_1` ti=0 ctx=standalone overlap=0.1: In preference mapping, how does allowing for ties between goods change the number of bits needed?
  - gold ['bell_number/Weakordering_28.txt', 'bell_number/Weakordering_29.txt'] | top3 ['ppf_retire/ProductionE28093possibilityfrontier_12.txt', 'bell_number/MurrayandDelhunty2000pdf_1.txt', 'single_currency/Optimumcurrencyarea_17.txt']
- `47_turn_1` ti=0 ctx=standalone overlap=0.333: In banking, how do low interest rates affect how much banks want to lend?
  - gold ['nominal_interest_rate/ECTA17408_9.txt'] | top3 ['omo_money_supply/rqt1212gpdf_8.txt', 'omo_money_supply/rqt1212gpdf_10.txt', 'inflation_interest/neofisherismpdf_3.txt']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.