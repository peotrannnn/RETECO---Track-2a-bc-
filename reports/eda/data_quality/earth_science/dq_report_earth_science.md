# Báo cáo chất lượng dữ liệu — domain `earth_science`

*Tạo lúc 2026-11-21T09:05:29 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 79.1 🟡** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 98.9 | 🟢 |
| content | 0.25 | 36.9 | 🔴 |
| conversation | 0.15 | 96.5 | 🟢 |
| gold | 0.25 | 87.1 | 🟢 |
| link | 0.15 | 92.6 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| content | % nghi không phải tiếng Anh | 64.59 | 0.5 | 32.3 |
| content | % HTML sót | 36.06 | 0.4 | 14.42 |
| gold | % gold có lỗi nội dung nghiêm trọng | 24.24 | 0.5 | 12.12 |
| content | % lặp bất thường | 14.23 | 0.5 | 7.12 |
| link | % turn gold không chia sẻ từ nào với query | 4.51 | 1.5 | 6.76 |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 3.45 | 1 | 3.45 |
| content | % trùng chính xác | 2.98 | 1.0 | 2.98 |
| content | % ký hiệu lạ/URL nặng | 7.24 | 0.4 | 2.9 |
| content | % gần trùng (ngoài trùng chính xác) | 2.61 | 0.7 | 1.83 |
| integrity | % doc có mojibake | 0.55 | 2 | 1.1 |
| gold | % gold có bản gần trùng không-gold (false-negative) | 1.52 | 0.5 | 0.76 |
| link | % OOV trung bình của query | 2.1 | 0.3 | 0.63 |

## 2. Khuyến nghị

- **[medium]** 0.55% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 1.23%.
- **[medium]** Trùng chính xác 2.98%.
- **[medium]** Gần trùng 2.61% (MinHash).
- **[medium]** Boilerplate 1.94% / HTML sót 36.06%.
- **[low]** 64.59% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 75.96% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 1 hội thoại có đại từ/liên từ ở turn đầu.
- **[medium]** 1 gold có bản gần trùng KHÔNG phải gold.
- **[medium]** 24.24% gold doc có lỗi nội dung nghiêm trọng.
- **[medium]** Bằng chứng nằm sau 650 ký tự ở 66.15% gold.
- **[medium]** Bằng chứng nằm sau ~512 token ở 20.77% gold.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **121,249** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.55% | ký tự điều khiển 0.0% | HTML/entity sót 36.06%
- Benchmark: 29 hội thoại | schema=`qa_pair` | vai trò {'user': 133, 'assistant': 133} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 133/133
- qrels: 181 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 181} | qid 133

## 4. Chất lượng nội dung

- Ký tự: min=2 p25=212.0 **median=278.0** mean=338.1 p75=348.0 p90=455.0 p99=643.0 max=233623 | outlier dài (>756.0c): 0.55%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 99.1% / 99.46% / 99.57% / 99.7%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 0.57% |
| 101-300 | 58.01% |
| 301-650 | 40.52% |
| 651-800 | 0.36% |
| 801-1500 | 0.11% |
| 1501-3000 | 0.13% |
| 3001-6000 | 0.13% |
| >6000 | 0.16% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 1489 | 1.23% |
| mojibake | lỗi encoding (mojibake) | 663 | 0.55% |
| control_chars | ký tự điều khiển | 6 | 0.0% |
| html_residue | HTML/entity còn sót | 43720 | 36.06% |
| boilerplate | boilerplate/menu/footer | 2353 | 1.94% |
| url_heavy | URL chiếm >25% nội dung | 7959 | 6.56% |
| symbol_heavy | ký hiệu lạ >30% | 822 | 0.68% |
| repetitive | lặp từ/dòng bất thường | 17259 | 14.23% |
| non_english | nghi không phải tiếng Anh | 78317 | 64.59% |
| pii_email | chứa email | 180 | 0.15% |
| pii_phone | chứa số điện thoại | 3967 | 3.27% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 84120 | 69.38% |
| starts_lower | bắt đầu bằng chữ thường | 44076 | 36.35% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **78.93%**
- Trùng chính xác: 3,616 doc dư (2.98%), 2202 nhóm
- Gần trùng: 410 cụm | doc dư gần-trùng ngoài trùng chính xác 502 (2.61%) | cụm lớn nhất 17
- Từ vựng (mẫu 10,060 doc): 51,826 từ | hapax 59.2% | Zipf -0.992 | 0(12427), 1(9021), class(7176), div(6082), quot(6028), 2(5104), span(4023), 3(3303), e(2924), data(2815), 4(2741), 5(2633), t(2261), s(2166), r(2145)

## 5. Hội thoại

- **29** hội thoại, **133** turn | turn/hội thoại: mean 4.59 (min 3, max 10) | query: mean 17.0 từ, median 17.0, p95 21.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 54 | 40.6% |
| pronoun | 63 | 47.37% |
| connector | 16 | 12.03% |
| short_ellipsis | 0 | 0% |

→ **75.96%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 1 (3.45%)
- Chuyển chủ đề: {'weak': 36.54, 'on_topic': 33.65, 'shift': 29.81} | hội thoại nhảy chủ đề ≥50% turn: 27.59%

**Loại câu hỏi:** statement_other 39.85%, yes_no 38.35%, what 11.28%, how 6.02%, why 2.26%, wh_other 1.5%, social 0.75%

## 6. Gold / qrels

- Nguồn gold: {'inline': 133} | qrels được dùng để eval: False
- Gold/turn: mean 1.36, max 5
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 133/133 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 121,183/121,249 (99.95%) | Gini 0.3277
- Độ dài gold vs corpus (median): 3605.0 vs 278.0 (tỷ lệ 12.97x)
- Gold có lỗi nghiêm trọng: 24.24% | false-negative tiềm năng: 1 (1.52%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.422** (có history: 0.425) | overlap=0: 4.51% | <20%: 16.54% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.468, 'pronoun': 0.368, 'connector': 0.477}
- OOV: 21.05% (TB 2.1%)
- **Vị trí bằng chứng** (130 mẫu): {'0-20%': 50.77, '20-40%': 11.54, '40-60%': 23.85, '60-80%': 6.15, '80-100%': 7.69} | median offset 1024c | sau 650c: 66.15% | sau 512 token: 20.77%

## 8. BM25 baseline

- 133 query | 66 gold + 200 nhiễu
- nDCG@10 single/history = 0.6634/0.8336 | Recall@10 = 0.8528/0.9486

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 29 | 0.7637 | 0.7637 | 0.954 | 0.954 |
| 2 | 29 | 0.6984 | 0.8618 | 0.8851 | 0.9483 |
| 3 | 29 | 0.6241 | 0.8974 | 0.7845 | 0.9655 |
| 4 | 20 | 0.5542 | 0.8191 | 0.85 | 0.95 |
| 5+ | 26 | 0.6405 | 0.8203 | 0.7821 | 0.9231 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 16 | 0.5305 | 0.8838 | 0.7083 | 0.9375 |
| pronoun | 63 | 0.6227 | 0.8615 | 0.836 | 0.9683 |
| standalone | 54 | 0.7503 | 0.7863 | 0.9151 | 0.929 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 8 | 0.8867 | 0.9438 | 0.9688 | 1.0 |
| social | 1 | 1.0 | 0.6309 | 1.0 | 1.0 |
| statement_other | 53 | 0.6436 | 0.8078 | 0.8491 | 0.9371 |
| wh_other | 2 | 0.338 | 0.8155 | 1.0 | 1.0 |
| what | 15 | 0.5708 | 0.8883 | 0.8 | 1.0 |
| why | 3 | 0.9892 | 0.9595 | 1.0 | 1.0 |
| yes_no | 51 | 0.6633 | 0.8245 | 0.8366 | 0.9314 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 29 | 0.7637 | 0.7637 | 0.954 | 0.954 |
| on_topic | 35 | 0.6607 | 0.8537 | 0.8762 | 0.9714 |
| shift | 31 | 0.6443 | 0.82 | 0.7339 | 0.9355 |
| weak | 38 | 0.605 | 0.8796 | 0.8509 | 0.9342 |

- Turn khó: **4** (3.01%) — {'lexical_gap (overlap<0.2)': 3, 'ranking/distractor': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 321 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 1,489

**`-999_celsius_degree/absolute_hot3_6.txt`** (34 ký tự)
```text
</div> </div>
```
**`-999_celsius_degree/common_cold3_15.txt`** (17 ký tự)
```text
-card__content">
```
**`-999_celsius_degree/common_cold4_102.txt`** (17 ký tự)
```text
</section>
```
**`-999_celsius_degree/highest_tem2_19.txt`** (19 ký tự)
```text
</div> </nav>
```
**`-999_celsius_degree/highest_tem4_13.txt`** (18 ký tự)
```text
-block clearfix">
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 663

**`22_halo/halo_season_31_105.txt`** (135 ký tự)
```text
3_Z7BpViV_sfPJAVD2cscFzcIlVlvC6PXZmUd-29adTjzN3mVezUMqX_dtGOkbx5D3OVUhKzuvdrHfh7gDz2tkn-106SjJrk8" data-item-title="【摩根智慧】如何在高息股上 進一步加�
```
**`22_halo/halo_season_31_106.txt`** (318 ký tự)
```text
�收益？" data-item-thumb="http://cdn.taboola.com/libtrc/static/thumbnails/0d005223c9f970622e83ecb6099ade1e.jpg" data-item-syndicated="true" class="videoCube trc_spotlight_item origin-undefined thumbnail_top syndicatedItem t…
```
**`22_halo/halo_season_31_17.txt`** (276 ký tự)
```text
.com/" rel="noopener dofollow" target="_blank" data-ga-onclick="Web Top Nav Edition#gujarati#url" class="edHin">ગુજરાતી</a><a href="https://marathi.economictimes.com/" rel="noopener dofollow" target="_blank" data-ga-oncl…
```
**`22_halo/halo_season_31_18.txt`** (308 ký tự)
```text
�ी</a><a href="https://bengali.economictimes.com/" rel="noopener dofollow" target="_blank" data-ga-onclick="Web Top Nav Edition#bengali#url" class="edHin">বাংলা</a><a href="https://kannada.economictimes.com/" rel="noopen…
```
**`22_halo/halo_season_31_58.txt`** (421 ký tự)
```text
international"><meta content="3" itemprop="position">International<meta content="International" itemprop="name"></a></span>›<span itemtype="https://schema.org/ListItem" itemscope="" itemprop="itemListElement"><a itemprop…
```

### ❌ `control_chars` — ký tự điều khiển — 6

**`contrial_formation/gmd1.txt`** (39910 ký tự)
```text
Geosci. Model Dev., 5, 543–580, 2012 www.geosci-model-dev.net/5/543/2012/ doi:10.5194/gmd-5-543-2012 © Author(s) 2012. CC Attribution 3.0 License. Geoscientific Model Development A contrail cirrus prediction model U. Sch…
```
**`ears/topo_scale1.txt`** (35697 ký tự)
```text
Geosci. Model Dev., 7, 387–405, 2014 www.geosci-model-dev.net/7/387/2014/ doi:10.5194/gmd-7-387-2014 © Author(s) 2014. CC Attribution 3.0 License. Geoscientific Model Development Open Access TopoSCALE v.1.0: downscaling …
```
**`contrial_formation/gmd2.txt`** (33476 ký tự)
```text
∂ ∂t X(t) + ∂ ∂t X˜ , (25) X˜ := X(t + 1t). (26) The time derivatives of the positions are computed using the wind vector (U,V ,ω) and ice particle terminal fall speed VT , ∂x/∂t = U, ∂y/∂t = V , ∂p/∂t = ω + gρVT . (27) …
```
**`contrial_formation/gmd4.txt`** (30534 ký tự)
```text
. We see that the computed values generally are close to the measured ones. The values RHi0 and RHii differ considerably for young plumes. This highlights the importance of the water emitted by the aircraft engines in ad…
```
**`contrial_formation/gmd5.txt`** (40116 ký tự)
```text
The analytical solution of this equation is: N (t) = BN0 e −B t B + AN0(1 − e−B t) , for B t > 0. (A24) The solution simplifies to N (t) = N0 1 + AN0 , forB t 1, (A25) www.geosci-model-dev.net/5/543/2012/ Geosci. Model D…
```

### ❌ `html_residue` — HTML/entity còn sót — 43,720

**`hottest_antarctic/wmo3.txt`** (24187 ký tự)
```text
<div class="content-tags flex gap-x-10 gap-y-2 md:gap-y-3 flex-wrap"> <div class="flex gap-x-2 items-center text-xs md:text-sm uppercase"> <span class="label-icon flex-none w-3.5 h-3.5 rounded-lg bg-wmo-cyan"></span> Pre…
```
**`cdf_file/washington2.txt`** (2280 ký tự)
```text
<p><tt>float time(time);<br> </tt></p> <div style="margin-left: 2em"><tt>time:units = "hours";</tt></div> </div> <p><tt>//global attributes:</tt></p> <div style="margin-left: 2em"><tt>:x_min = -180.f;<br> :x_max = 180.f;…
```
**`cdf_file/washington3.txt`** (2015 ký tự)
```text
<pre><tt> program netCDF_example1 c c ----------------------------------------------------------------- c Declare and set constants, parameters and scratch variables c ----------------------------------------------------…
```
**`predicting_aurora/agu5.txt`** (214529 ký tự)
```text
<!-- Go to https://www.addtoany.com/buttons/customize/ to customize your tools --><script type="text/javascript" defer="defer" src="https://static.addtoany.com/menu/page.js"></script><div class="relative"><a id="share-ac…
```
**`dry_weather_river/usgov3.txt`** (34402 ký tự)
```text
<li>streams gain water from inflow of groundwater through the streambed (gaining stream),</li> <li>streams lose water to groundwater by outflow through the streambed (losing stream), or</li> <li>they do both, gaining in …
```

### ❌ `boilerplate` — boilerplate/menu/footer — 2,353

**`methane_clathrates/BF001445042.txt`** (3459 ký tự)
```text
Skip to main content Log in Menu Find a journal Publish with us Track your research Search Cart Home Climatic Change Article Role of methane clathrates in past and future climates Published: June 1990 Volume 16, pages 24…
```
**`geomagnetic_pulse/Geomagnetic_jerk5.txt`** (5141 ký tự)
```text
From Wikipedia, the free encyclopedia Sudden change in the Earth's magnetic field In geophysics, a geomagnetic jerk or secular geomagnetic variation impulse is a relatively sudden change in the second derivative of the E…
```
**`prime_meridian/s00190_015_0844_y4.txt`** (39349 ký tự)
```text
1 The situation at GreenwichThe Airy Transit Circle is a nineteenth-century telescopic instrument at the Royal Observatory, Greenwich, famous as the origin for global longitude. Recognized as a place of world heritage by…
```
**`india_cyclone/nature10552_ref12.txt`** (5423 ký tự)
```text
Sign up for alerts RSS feed nature letters article Letter Published: 02 November 2011 Arabian Sea tropical cyclones intensified by emissions of black carbon and other aerosols Amato T. Evan1, James P. Kossin2,3, Chul ‘Ed…
```
**`teten/Clausius_E2_80_93Clapeyron_relation5.txt`** (9452 ký tự)
```text
e s ( T ) = 6.1094 exp ⁡ ( 17.625 T T + 243.04 ) , {\displaystyle e_{s}(T)=6.1094\exp \left({\frac {17.625T}{T+243.04}}\right),} where e s {\displaystyle e_{s}} is in hPa, and T {\displaystyle T} is in degrees Celsius (w…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 7,959

**`schmidt_nets/rf5.txt`** (577 ký tự)
```text
<td> Old&nbsp;sources: </td> <td> <a href="https://CRAN.R-project.org/src/contrib/Archive/RockFab"> <span class="CRAN"> RockFab archive </span> </a> </td> </tr> </tbody></table> <h4>Reverse dependencies:</h4> <table> <tb…
```
**`era5_data/Create_and_Delete_Files_and_Directories_from_Windows_Command_Prompt2.txt`** (14037 ký tự)
```text
This article has been viewed 1,551,191 times. Learn more... Learning how to do simple file management at the Command Prompt (cmd) comes in handy when you're learning to code. When you create files and folders at the comm…
```
**`-999_celsius_degree/absolute_hot1_2.txt`** (217 ký tự)
```text
div class="pbs_loc hide-desktop"> <div class="pbs_loc_st"> <a class="pbs_loc_name ga" href="https://www.pbs.org/cgi-registry/stationlink.cgir"></a> </div> </div>
```
**`-999_celsius_degree/absolute_hot1_4.txt`** (273 ký tự)
```text
><a href="https://www.pbs.org/explore/" title="" target="_blank" class="ga" rel="noopener">Explore</a></li> <li><a href="https://www.pbs.org/cgi-registry/whatson/index.cgir" title="" target="_blank" class="ga" rel="noope…
```
**`-999_celsius_degree/absolute_hot1_5.txt`** (237 ký tự)
```text
<li class="shop_link "> <a href="https://shop.pbs.org/?utm_source=PBS&amp;utm_medium=Link&amp;utm_campaign=pbs_global_shopbuttontopnav" title="" target="_blank" class="ga" rel="noopener">
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 822

**`-999_celsius_degree/highest_tem2_19.txt`** (19 ký tự)
```text
</div> </nav>
```
**`22_halo/halo_season_33_7.txt`** (307 ký tự)
```text
</span></li><li class=""><span>2</span></li><li class="active"><span>3</span></li><li><span>4</span></li><li><span>5</span></li><li><span>6</span></li><li><span>7</span></li><li><span>8</span></li></ul></div><div data-ga…
```
**`acidity_of_rock/PH5_2.txt`** (207 ký tự)
```text
] − 1 {\displaystyle {\begin{aligned}C_{\ce {A}}&=[{\ce {A}}]+\Sigma p\beta _{pqr}[{\ce {A}}]^{p}[{\ce {B}}]^{q}[{\ce {H}}]^{r}\\C_{\ce {B}}&=[{\ce {B}}]+\Sigma q\beta _{pqr}[{\ce {A}}]^{p}[{\ce {B
```
**`annual_harmonics/Pythagorean_theorem3_15.txt`** (203 ký tự)
```text
(\cos \theta _{1}\cos \theta _{2}+\sin \theta _{1}\sin \theta _{2}\right)\\&=r_{1}^{2}+r_{2}^{2}-2r_{1}r_{2}\cos \left(\theta _{1}-\theta _{2}\right)\\&=r_{1}^{2}+r_{2}^{2}-2r_{1}r_{2}\cos \Delta \theta,
```
**`annual_harmonics/Pythagorean_theorem5_13.txt`** (192 ký tự)
```text
� a 2 R sinh 2 ⁡ b 2 R . {\displaystyle \sinh ^{2}{\frac {c}{2R}}=\sinh ^{2}{\frac {a}{2R}}+\sinh ^{2}{\frac {b}{2R}}+2\sinh ^{2}{\frac {a}{2R}}\sinh ^{2}{\frac {b}{2R}}\,.}
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 17,259

**`humidity_and_rain/Kelvin_equation2.txt`** (3673 ký tự)
```text
part2 ------------------- Formulation[edit] The original form of the Kelvin equation, published in 1871, is: p ( r 1 , r 2 ) = P − γ ρ v a p o r ( ρ l i q u i d − ρ v a p o r ) ( 1 r 1 + 1 r 2 ) , {\displaystyle p(r_{1},…
```
**`humidity_and_rain/Kelvin_equation4.txt`** (5369 ký tự)
```text
part4 ------------------- Derivation using the Gibbs free energy[edit] The formal definition of the Gibbs free energy for a parcel of volume V {\displaystyle V} , pressure P {\displaystyle P} and temperature T {\displays…
```
**`humidity_and_rain/Kelvin_equation5.txt`** (4547 ký tự)
```text
part5 ------------------- Apparent paradox[edit] An equation similar to that of Kelvin can be derived for the solubility of small particles or droplets in a liquid, by means of the connection between vapour pressure and …
```
**`shape_of_waves/Dispersion_%28water_waves%292.txt`** (16166 ký tự)
```text
part2 ------------------- Frequency dispersion for surface gravity waves[edit] This section is about frequency dispersion for waves on a fluid layer forced by gravity, and according to linear theory. For surface tension …
```
**`shape_of_waves/Wave_shoaling3.txt`** (3605 ký tự)
```text
part3 ------------------- Physics[edit] When waves enter shallow water they slow down. Under stationary conditions, the wave length is reduced. The energy flux must remain constant and the reduction in group (transport) …
```

### ❌ `non_english` — nghi không phải tiếng Anh — 78,317

**`cdf_file/washington4.txt`** (1727 ký tự)
```text
c Write the netCDF file name c write(7,*) 'netcdf mine{' c c Write the dimensions c write(7,*) 'dimensions:' write(7,*) 'lon=', nlon, ';' write(7,*) 'lat=', nlat, ';' write(7,*) 'level=', nlevel, ';' write(7,*) 'time=UNL…
```
**`predicting_aurora/agu5.txt`** (214529 ký tự)
```text
<!-- Go to https://www.addtoany.com/buttons/customize/ to customize your tools --><script type="text/javascript" defer="defer" src="https://static.addtoany.com/menu/page.js"></script><div class="relative"><a id="share-ac…
```
**`hydrostatic_equilibrium/Isostasy3.txt`** (924 ký tự)
```text
= ( c ρ c ) + ( b 1 ρ m ) {\displaystyle (h_{1}+c+b_{1})\rho _{c}=(c\rho _{c})+(b_{1}\rho _{m})} b 1 ( ρ m − ρ c ) = h 1 ρ c {\displaystyle {b_{1}(\rho _{m}-\rho _{c})}=h_{1}\rho _{c}} b 1 = h 1 ρ c ρ m − ρ c {\displayst…
```
**`old_topographic_map/india4.txt`** (3485 ký tự)
```text
NE 44-1 Chanda (4.2 MB) NE 44-2 Sirpur (4.0 MB) NE 44-3 Jagdalpur (4.1 MB) NE 44-4 Bhawanipatna (5.0 MB) NE 44-5 Nizamabad (4.4 MB) NE 44-6 Chinnur (4.2 MB) NE 44-7 Malakanagiri (4.7 MB) NE 44-8 Vizianagram (4.9 MB) NE 4…
```
**`reflecting_sunlights/news1.txt`** (233623 ký tự)
```text
<body class="" style="overflow: initial;"><script> </script><div id="__next"><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PB2GX" height="0" width="0" style="display:none;visibility:hidden"></ifr…
```

### ❌ `pii_email` — chứa email — 180

**`contrial_formation/gmd1.txt`** (39910 ký tự)
```text
Geosci. Model Dev., 5, 543–580, 2012 www.geosci-model-dev.net/5/543/2012/ doi:10.5194/gmd-5-543-2012 © Author(s) 2012. CC Attribution 3.0 License. Geoscientific Model Development A contrail cirrus prediction model U. Sch…
```
**`hottest_antarctic/wmo3.txt`** (24187 ký tự)
```text
<div class="content-tags flex gap-x-10 gap-y-2 md:gap-y-3 flex-wrap"> <div class="flex gap-x-2 items-center text-xs md:text-sm uppercase"> <span class="label-icon flex-none w-3.5 h-3.5 rounded-lg bg-wmo-cyan"></span> Pre…
```
**`predicting_aurora/agu5.txt`** (214529 ký tự)
```text
<!-- Go to https://www.addtoany.com/buttons/customize/ to customize your tools --><script type="text/javascript" defer="defer" src="https://static.addtoany.com/menu/page.js"></script><div class="relative"><a id="share-ac…
```
**`ears/topo_scale1.txt`** (35697 ký tự)
```text
Geosci. Model Dev., 7, 387–405, 2014 www.geosci-model-dev.net/7/387/2014/ doi:10.5194/gmd-7-387-2014 © Author(s) 2014. CC Attribution 3.0 License. Geoscientific Model Development Open Access TopoSCALE v.1.0: downscaling …
```
**`reflecting_sunlights/news1.txt`** (233623 ký tự)
```text
<body class="" style="overflow: initial;"><script> </script><div id="__next"><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PB2GX" height="0" width="0" style="display:none;visibility:hidden"></ifr…
```

### ❌ `pii_phone` — chứa số điện thoại — 3,967

**`geomagnetic_pulse/Geomagnetic_jerk5.txt`** (5141 ký tự)
```text
From Wikipedia, the free encyclopedia Sudden change in the Earth's magnetic field In geophysics, a geomagnetic jerk or secular geomagnetic variation impulse is a relatively sudden change in the second derivative of the E…
```
**`aurora_equator/Carrington_Event4.txt`** (18302 ký tự)
```text
Associated solar flare[edit] Just before noon on 1 September 1859, the English amateur astronomers Richard Christopher Carrington and Richard Hodgson independently recorded the earliest observations of a solar flare.[8] …
```
**`propagation_of_sound_after_lightning/Lightning4.txt`** (41025 ký tự)
```text
Branching of cloud to cloud lightning, New Delhi, India. Multiple paths of cloud-to-cloud lightning, Swifts Creek, Australia. Intra-clouds lightning over the Baltic Sea. Cloud-to-cloud lightning, Albury, Australia Effect…
```
**`contrial_formation/gmd1.txt`** (39910 ký tự)
```text
Geosci. Model Dev., 5, 543–580, 2012 www.geosci-model-dev.net/5/543/2012/ doi:10.5194/gmd-5-543-2012 © Author(s) 2012. CC Attribution 3.0 License. Geoscientific Model Development A contrail cirrus prediction model U. Sch…
```
**`prime_meridian/s00190_015_0844_y4.txt`** (39349 ký tự)
```text
1 The situation at GreenwichThe Airy Transit Circle is a nineteenth-century telescopic instrument at the Royal Observatory, Greenwich, famous as the origin for global longitude. Recognized as a place of world heritage by…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 84,120

**`humidity_and_rain/Kelvin_equation4.txt`** (5369 ký tự)
```text
part4 ------------------- Derivation using the Gibbs free energy[edit] The formal definition of the Gibbs free energy for a parcel of volume V {\displaystyle V} , pressure P {\displaystyle P} and temperature T {\displays…
```
**`make_martian_dirt/How_to_make_simulant_Martian_dirt2.txt`** (1625 ký tự)
```text
NASA graph of elemental composition of Mars soil. The five most abundant ingredients, account for almost 90% of the dirt taken from Mars samples. SiO2 - 49.5% Fe2O3 - 17.9% Al2O3 - 7.2% MgO - 7.7% CaO - 6.7% That seems l…
```
**`shape_of_waves/Wave_shoaling2.txt`** (1460 ký tự)
```text
part2 ------------------- Overview[edit] Waves nearing the coast change wave height through different effects. Some of the important wave processes are refraction, diffraction, reflection, wave breaking, wave–current int…
```
**`shape_of_waves/Wave_shoaling3.txt`** (3605 ký tự)
```text
part3 ------------------- Physics[edit] When waves enter shallow water they slow down. Under stationary conditions, the wave length is reduced. The energy flux must remain constant and the reduction in group (transport) …
```
**`geomagnetic_pulse/Geomagnetic_jerk5.txt`** (5141 ký tự)
```text
From Wikipedia, the free encyclopedia Sudden change in the Earth's magnetic field In geophysics, a geomagnetic jerk or secular geomagnetic variation impulse is a relatively sudden change in the second derivative of the E…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 44,076

**`number_of_hadley_cell/Hadley_cell2.txt`** (20091 ký tự)
```text
part2 ------------------- Mechanism and characteristics[edit] On average, the Hadley circulation is composed of two cells in the northern and southern hemispheres that circulate air within the tropics. The Hadley circula…
```
**`hurricanes_in_the_southern_Atlantic_basin/Tropical_cyclone1.txt`** (59802 ký tự)
```text
part1 ------------------- A tropical cyclone is a rapidly rotating storm system characterized by a low-pressure center, a closed low-level atmospheric circulation, strong winds, and a spiral arrangement of thunderstorms …
```
**`pole_flip/Geomagnetic_reversal1.txt`** (1749 ký tự)
```text
part1 ------------------- A geomagnetic reversal is a change in a planet's magnetic field such that the positions of magnetic north and magnetic south are interchanged (not to be confused with geographic north and geogra…
```
**`pole_flip/Geomagnetic_reversal5.txt`** (1666 ký tự)
```text
part5 ------------------- Character of transitions[edit] Duration[edit] Most estimates for the duration of a polarity transition are between 1,000 and 10,000 years, but some estimates are as quick as a human lifetime. Du…
```
**`pole_flip/Geomagnetic_reversal6.txt`** (2760 ký tự)
```text
part6 ------------------- Causes[edit] NASA computer simulation using the model of Glatzmaier and Roberts. The tubes represent magnetic field lines, blue when the field points towards the center and yellow when away. The…
```

### ❌ Trùng chính xác — 3,616

*2202 nhóm*

- nhóm: `atmosphere_venus/Venus_goddess4_5.txt`, `aurora_equator/Equator4_4.txt`, `prime_meridian/Greenwich_Mean_Time4_3.txt`
```text
Cite verifiedCite While every effort has been made to follow citation style rules, there may be some discrepancies. Please refer to the appropriate style manual or other sources if you have any questions. Select Citation…
```
- nhóm: `colder_winter_after_solstice/hong_kong_cold_winter3_2.txt`, `merged_hurricanes/super_typhoon3_2.txt`
```text
st0" data-qa="follow-button">+ FOLLOW</button></div></div></div><div data-qa="GenericArticle-Author" class="css-16mapcj eg5341w16"><div class="speech-skip-target e1oct4f923 css-8vzp8b e4nambs3" data-qa="ArticleAuthorBloc…
```
- nhóm: `eyes_of_tornadoes/does_it_has_eye2_208.txt`, `eyes_of_tornadoes/does_it_has_eye2_96.txt`, `salt_pits/red_pits2_41.txt`
```text
<faceplate-tracker source="post_detail" action="click" noun="reply_comment" slot="comment-reply" class="contents"> <button rpl="" class="button border-md text-12 button-plain disabled:text-interactive-content-disabled te…
```
- nhóm: `interpolating_wind_speed/wind_speed_acc3_91.txt`, `no_hydrocarbons_in_sveconorwegian_belt/late_mesoproterozoic_sirdal_magmatic_belt3_91.txt`
```text
var t, r = e[1] || {}; if ("string" == typeof e[0]? 0 === (t = e[0]).length && u.il && (t = "" + u._A.location.href) : e[0] && e[0].url? t = e[0].url : u._A?.URL && e[0] &&
```
- nhóm: `mass_of_earth/surface_mass3_731.txt`, `mass_of_earth/surface_mass3_990.txt`
```text
ns="http://www.w3.org/2000/svg"><path d="m5 8.5 7 7 7.005-7" class="icon_svg-stroke" stroke="#666" stroke-width="1.5" fill="none" stroke-linecap="round"></path></svg></span></span></div></button></div></div></div></span>…
```

### ❌ Gần trùng (khác nhau chút ít) — 502

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 17: `airborne_fraction/Airborne_fraction1.txt`, `airborne_fraction/Carbon_dioxide1_0.txt`, `dry_weather_river/River1_0.txt`, `far_from_sea_level/Sea_level_rise1_0.txt`, `fog_bow/Fog1_0.txt`
  - `airborne_fraction/Airborne_fraction1.txt`:
```text
Airborne fraction - Wikipedia Jump to content Main menu Main menu move to sidebar hide Navigation Main pageContentsCurrent eventsRandom articleAbout WikipediaContact usDonate Contribute HelpLearn to editCommunity portalR…
```
  - `airborne_fraction/Carbon_dioxide1_0.txt`:
```text
Carbon dioxide - Wikipedia Jump to content Main menu Main menu move to sidebar hide Navigation Main pageContentsCurrent eventsRandom articleAbout WikipediaContact usDonate Contribute HelpLearn to editCommunity portalRece…
```
- cụm size 12: `mass_of_earth/air_mass1_324.txt`, `mass_of_earth/air_mass1_640.txt`, `mass_of_earth/air_mass1_666.txt`, `mass_of_earth/air_mass2_68.txt`, `mass_of_earth/air_mass2_81.txt`
  - `mass_of_earth/air_mass1_324.txt`:
```text
<span class="c-IconButton c-IconButton--tiny toggle expandCollapseIcon c-IconButton--no-ripple c-IconButton--arrowDropDown" aria-expanded="false" role="button" tabindex="0"></span>
```
  - `mass_of_earth/air_mass1_640.txt`:
```text
<span class="c-IconButton c-IconButton--tiny toggle expandCollapseIcon c-IconButton--no-ripple c-IconButton--arrowDropDown" aria-expanded="false" role="button" tabindex="0"></span>
```
- cụm size 10: `acidity_of_rock/List_of_acid_rock_artists5_6.txt`, `arid_area/Earth_rainfall_climatology5_20.txt`, `below_treeline/Montane_ecosystems5_22.txt`, `continental_drift/Drifting_(motorsport)5_9.txt`, `dry_weather_river/River5_9.txt`
  - `acidity_of_rock/List_of_acid_rock_artists5_6.txt`:
```text
under the Creative Commons Attribution-ShareAlike License 4.0; additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Found…
```
  - `arid_area/Earth_rainfall_climatology5_20.txt`:
```text
additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization. Privacy policy About Wi…
```
- cụm size 9: `acidity_of_rock/List_of_acid_rock_artists3_0.txt`, `always_daytime/Daytime4_0.txt`, `far_from_sea_level/Sea_level_rise2_3.txt`, `karst/Jagged_Mountain4_0.txt`, `life_on_mars/Life_on_Mars_(British_TV_series)2_2.txt`
  - `acidity_of_rock/List_of_acid_rock_artists3_0.txt`:
```text
Add links ArticleTalk English ReadEditView history Tools Tools move to sidebar hide Actions ReadEditView history General What links hereRelated changesUpload fileSpecial pagesPermanent linkPage informationCite this pageG…
```
  - `always_daytime/Daytime4_0.txt`:
```text
ReadEditView history Tools Tools move to sidebar hide Actions ReadEditView history General What links hereRelated changesUpload fileSpecial pagesPermanent linkPage informationCite this pageGet shortened URLDownload QR co…
```
- cụm size 9: `mass_of_earth/air_mass1_461.txt`, `mass_of_earth/air_mass1_658.txt`, `mass_of_earth/air_mass2_47.txt`, `mass_of_earth/air_mass3_1016.txt`, `mass_of_earth/air_mass3_832.txt`
  - `mass_of_earth/air_mass1_461.txt`:
```text
<li class="ajax-node-opener type-volume shut"> <div class="header-container rightFlushed flex flex-nowrap flex-align-start"> <div class="flex-1 flex flex-row">
```
  - `mass_of_earth/air_mass1_658.txt`:
```text
</li> <li class="ajax-node-opener type-volume shut"> <div class="header-container rightFlushed flex flex-nowrap flex-align-start"> <div class="flex-1 flex flex
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

- `44_turn_1`: In auroras, have they ever been seen as far south as the Caribbean during big solar storms?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 63

- `1_turn_2`: Is it the constant westerly wind shear down there that stops these storms from even getting started?
- `1_turn_5`: Is it that those strong winds up high just blow the storms apart before they can stack up?
- `1_turn_6`: What happens if those upper-level winds ease up for a while—could storms actually get going then?
- `7_turn_2`: Is that because water holds onto heat longer than land does?
- `7_turn_4`: Is there a pattern to when the coldest day hits in different places, or does it really jump around?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 16

- `1_turn_3`: Oh, and what about those African easterly waves—does not having them down there make a big difference too?
- `1_turn_7`: Oh, did satellites actually help spot and track Catarina when it formed down there?
- `7_turn_3`: Oh, and does the warmest day show up later in places near the ocean because of that lag too?
- `7_turn_5`: What about humidity—does that make winters feel even colder near the ocean, or does it help at all?
- `13_turn_3`: Why doesn’t the wave’s frequency change as it moves into shallow water?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 31

- `1_turn_5` (cos=0.0)
  - trước: Do you think climate change could actually make hurricanes more likely down there in the future?
  - sau: Is it that those strong winds up high just blow the storms apart before they can stack up?
- `7_turn_2` (cos=0.0)
  - trước: In seasonal weather, why is the coldest time of year weeks after the shortest day?
  - sau: Is that because water holds onto heat longer than land does?
- `7_turn_5` (cos=0.0)
  - trước: Is there a pattern to when the coldest day hits in different places, or does it really jump around?
  - sau: What about humidity—does that make winters feel even colder near the ocean, or does it help at all?
- `7_turn_6` (cos=0.0)
  - trước: What about humidity—does that make winters feel even colder near the ocean, or does it help at all?
  - sau: Is that why places like Western Europe get their coldest days way after the solstice compared to somewhere inland?
- `8_turn_4` (cos=0.0)
  - trước: Is there an easy way to turn those calcium tablets into calcium oxide safely at home?
  - sau: Is there any real downside to just using regular sand instead of pure silicon dioxide for this?

## D. Gold / qrels

### ✅ Gold mồ côi (doc không có trong corpus)
- Không phát hiện.

### ✅ qrels qid không khớp turn nào
- Không phát hiện.

### ✅ Gold inline (benchmark) ≠ qrels
- Không phát hiện.

### ✅ Turn không có gold
- Không phát hiện.

### ❌ Gold doc có lỗi nội dung nghiêm trọng — 16

- `shape_of_waves/Wave_shoaling3.txt` ['repetitive']
```text
part3 ------------------- Physics[edit] When waves enter shallow water they slow down. Under stationary conditions, the wave length is reduced. The energy flux must remain constant and the reduction i…
```
- `shape_of_waves/Wave_shoaling4.txt` ['repetitive']
```text
part4 ------------------- Water wave refraction[edit] Following Phillips (1977) and Mei (1989), denote the phase of a wave ray as S = S ( x , t ) , 0 ≤ S < 2 π {\displaystyle S=S(\mathbf {x} ,t),\qqua…
```
- `shape_of_waves/Dispersion_%28water_waves%292.txt` ['repetitive']
```text
part2 ------------------- Frequency dispersion for surface gravity waves[edit] This section is about frequency dispersion for waves on a fluid layer forced by gravity, and according to linear theory. …
```
- `interpolating_wind_speed/Wind_gradient4.txt` ['repetitive']
```text
part4 ------------------- Implications[edit] Engineering[edit] The design of buildings must account for wind loads, and these are affected by wind gradient. The respective gradient levels, usually ass…
```
- `methane_clathrates/BF001445042.txt` ['boilerplate']
```text
Skip to main content Log in Menu Find a journal Publish with us Track your research Search Cart Home Climatic Change Article Role of methane clathrates in past and future climates Published: June 1990…
```

### ❌ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng) — 1

- gold ['colder_winter_after_solstice/Seasonal_lag1.txt'] ↔ bản sao ['colder_march/Seasonal_lag1.txt']

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 6

- `9_turn_9` (standalone) gold=['start_of_a_season/Growing_season1.txt']: Do you think farming schedules had anything to do with how people picked the start of summer here?
- `20_turn_2` (standalone) gold=['ocean_continent_divergent_boundary/Triple_junction4.txt']: What actually happens when a rift starts right at the edge of a continent next to the ocean?
- `53_turn_3` (pronoun) gold=['mariana_trench/Oceanic_trench1.txt']: Is it just the lack of sediment, or do other things help keep it so deep too?
- `53_turn_4` (standalone) gold=['mariana_trench/Oceanic_trench1.txt']: I wonder if the way the Pacific Plate dives under the Mariana Plate changes how deep it gets?
- `96_turn_3` (pronoun) gold=['airborne_fraction/Airborne_fraction4.txt']: Is that 40% actually pretty typical compared to what scientists see in real-world data?

### ❌ Bằng chứng nằm muộn (> 1500 ký tự) — 52

- `1_turn_4` offset=49450c gold=`hurricanes_in_the_southern_Atlantic_basin/Tropical_cyclone1.txt`
  - query: Do you think climate change could actually make hurricanes more likely down there in the future?
  - bằng chứng: As climate change is warming ocean temperatures, there is potentially more of this fuel available.
- `61_turn_2` offset=26297c gold=`difference_in_climate_change/ripple_effects_population_and_coastal_regions4.txt`
  - query: Would having so many people living by the coast now make the effects of rapid warming way worse than back then?
  - bằng chứng: They also provide food, building materials, shoreline protection, and many indirect benefits for people living near them.
- `1_turn_1` offset=22504c gold=`hurricanes_in_the_southern_Atlantic_basin/Tropical_cyclone1.txt`
  - query: In southern Atlantic storms, what made the 2004 Brazilian hurricane such a rare event?
  - bằng chứng: Within the Southern Hemisphere, it is either called a hurricane, tropical cyclone or a severe tropical cyclone, depending on if it is located within the South A…
- `9_turn_1` offset=13408c gold=`start_of_a_season/Season3.txt`
  - query: In seasonal calendars, how do earlier summer starts in Celtic and Chinese traditions shape their Midsummer festivals?
  - bằng chứng: On the Celtic calendar, the start of the seasons corresponds to four Pagan agricultural festivals - the traditional first day of winter is 1 November (Samhain, …
- `9_turn_3` offset=13408c gold=`start_of_a_season/Season3.txt`
  - query: Is that why meteorologists start summer on June 1 instead of waiting for the solstice?
  - bằng chứng: On the Celtic calendar, the start of the seasons corresponds to four Pagan agricultural festivals - the traditional first day of winter is 1 November (Samhain, …

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 28

- `8_turn_5` OOV=['crush', 'figuring']: Any tips on figuring out how much of those magnesium tablets to crush up for the mix?
- `33_turn_5` OOV=['sicker', 'stricter']: Did all that extra pollution back then actually make people sicker, and is that what pushed for stricter air rules later?
- `69_turn_3` OOV=['blend', 'hmm']: Hmm, did people actually draw a line between Archaeozoic and Archean, or did those just kind of blend together over time?
- `8_turn_4` OOV=['downside']: Is there any real downside to just using regular sand instead of pure silicon dioxide for this?
- `8_turn_6` OOV=['sitting']: What happens if the calcium oxide just turns back into calcium carbonate while it’s sitting around?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 4

*nguyên nhân: {'lexical_gap (overlap<0.2)': 3, 'ranking/distractor': 1}*

- `9_turn_9` ti=8 ctx=standalone overlap=0.0: Do you think farming schedules had anything to do with how people picked the start of summer here?
  - gold ['start_of_a_season/Growing_season1.txt'] | top3 ['start_of_a_season/Season3.txt', 'colder_winter_after_solstice/Seasonal_lag1.txt', 'arid_area/K_C3_B6ppen_climate_classification2.txt']
- `53_turn_3` ti=2 ctx=pronoun overlap=0.0: Is it just the lack of sediment, or do other things help keep it so deep too?
  - gold ['mariana_trench/Oceanic_trench1.txt'] | top3 ['artificial_river/Soil_conditioner3.txt', 'authigenic_zeolites/om2.txt', 'north_pole_rotation/spin_speed5_66.txt']
- `53_turn_4` ti=3 ctx=standalone overlap=0.0: I wonder if the way the Pacific Plate dives under the Mariana Plate changes how deep it gets?
  - gold ['mariana_trench/Oceanic_trench1.txt'] | top3 ['ocean_continent_divergent_boundary/Triple_junction5.txt', 'shape_of_waves/Wave_shoaling1.txt', 'ocean_continent_divergent_boundary/Triple_junction4.txt']
- `69_turn_1` ti=0 ctx=standalone overlap=0.444: In geology, how did 'Azoic' come to mean a lifeless period, and how does that connect to 'Archaeozic'?
  - gold ['Archaeozoic_vs_Archean/Archean4.txt'] | top3 ['acidity_of_rock/igrockclassif_htm1.txt', 'shape_of_waves/Wave_shoaling2.txt', 'shape_of_waves/Wave_shoaling3.txt']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.