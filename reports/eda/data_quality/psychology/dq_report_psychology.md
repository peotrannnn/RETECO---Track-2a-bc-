# Báo cáo chất lượng dữ liệu — domain `psychology`

*Tạo lúc 2026-11-21T09:07:21 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 84.7 🟡** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 99.5 | 🟢 |
| content | 0.25 | 50.6 | 🔴 |
| conversation | 0.15 | 92.0 | 🟢 |
| gold | 0.25 | 98.2 | 🟢 |
| link | 0.15 | 92.1 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| content | % trùng chính xác | 17.18 | 1.0 | 17.18 |
| content | % doc quá ngắn | 29.4 | 0.5 | 14.7 |
| content | % ký hiệu lạ/URL nặng | 20.57 | 0.4 | 8.23 |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 8.0 | 1 | 8.0 |
| link | % turn gold không chia sẻ từ nào với query | 5.05 | 1.5 | 7.57 |
| content | % nghi không phải tiếng Anh | 13.51 | 0.5 | 6.75 |
| gold | % gold có lỗi nội dung nghiêm trọng | 3.53 | 0.5 | 1.76 |
| content | % gần trùng (ngoài trùng chính xác) | 1.4 | 0.7 | 0.98 |
| content | % boilerplate | 2.66 | 0.3 | 0.8 |
| content | % lặp bất thường | 1.27 | 0.5 | 0.64 |
| integrity | % doc có mojibake | 0.23 | 2 | 0.46 |
| link | % OOV trung bình của query | 1.22 | 0.3 | 0.37 |

## 2. Khuyến nghị

- **[medium]** 0.23% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 29.4%.
- **[medium]** Trùng chính xác 17.18%.
- **[medium]** Gần trùng 1.4% (MinHash).
- **[low]** 13.51% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 78.38% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 2 hội thoại có đại từ/liên từ ở turn đầu.
- **[medium]** 5.05% turn gold KHÔNG chia sẻ từ nào với query.
- **[medium]** Bằng chứng nằm sau 650 ký tự ở 47.96% gold.
- **[medium]** Bằng chứng nằm sau ~512 token ở 18.37% gold.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **52,835** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.23% | ký tự điều khiển 0.01% | HTML/entity sót 0.05%
- Benchmark: 25 hội thoại | schema=`qa_pair` | vai trò {'user': 99, 'assistant': 99} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 99/99
- qrels: 191 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 191} | qid 99

## 4. Chất lượng nội dung

- Ký tự: min=3 p25=37.0 **median=130.0** mean=384.4 p75=341.0 p90=775.0 p99=3832.0 max=226941 | outlier dài (>1253.0c): 5.33%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 87.25% / 90.34% / 95.87% / 98.5%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 42.98% |
| 101-300 | 28.85% |
| 301-650 | 15.42% |
| 651-800 | 3.09% |
| 801-1500 | 5.53% |
| 1501-3000 | 2.64% |
| 3001-6000 | 1.01% |
| >6000 | 0.48% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 15536 | 29.4% |
| mojibake | lỗi encoding (mojibake) | 123 | 0.23% |
| control_chars | ký tự điều khiển | 5 | 0.01% |
| html_residue | HTML/entity còn sót | 27 | 0.05% |
| boilerplate | boilerplate/menu/footer | 1408 | 2.66% |
| url_heavy | URL chiếm >25% nội dung | 9922 | 18.78% |
| symbol_heavy | ký hiệu lạ >30% | 948 | 1.79% |
| repetitive | lặp từ/dòng bất thường | 673 | 1.27% |
| non_english | nghi không phải tiếng Anh | 7138 | 13.51% |
| pii_email | chứa email | 165 | 0.31% |
| pii_phone | chứa số điện thoại | 482 | 0.91% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 2545 | 4.82% |
| starts_lower | bắt đầu bằng chữ thường | 930 | 1.76% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **55.14%**
- Trùng chính xác: 9,079 doc dư (17.18%), 3136 nhóm
- Gần trùng: 446 cụm | doc dư gần-trùng ngoài trùng chính xác 194 (1.4%) | cụm lớn nhất 67
- Từ vựng (mẫu 10,074 doc): 39,096 từ | hapax 41.06% | Zipf -0.929 | wiki(9009), https(6812), com(3423), org(3034), www(2848), doi(2769), identifier(2614), 10(2445), s(2315), 1(1949), scholar(1460), 2(1359), edit(1343), wikipedia(1318), google(1247)

## 5. Hội thoại

- **25** hội thoại, **99** turn | turn/hội thoại: mean 3.96 (min 3, max 6) | query: mean 16.8 từ, median 17.0, p95 22.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 41 | 41.41% |
| pronoun | 54 | 54.55% |
| connector | 4 | 4.04% |
| short_ellipsis | 0 | 0% |

→ **78.38%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 2 (8.0%)
- Chuyển chủ đề: {'weak': 31.08, 'on_topic': 36.49, 'shift': 32.43} | hội thoại nhảy chủ đề ≥50% turn: 36.0%

**Loại câu hỏi:** statement_other 46.46%, yes_no 37.37%, what 7.07%, how 6.06%, wh_other 2.02%, why 1.01%

## 6. Gold / qrels

- Nguồn gold: {'inline': 99} | qrels được dùng để eval: False
- Gold/turn: mean 1.93, max 12
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 99/99 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 52,750/52,835 (99.84%) | Gini 0.3321
- Độ dài gold vs corpus (median): 2106.0 vs 130.0 (tỷ lệ 16.2x)
- Gold có lỗi nghiêm trọng: 3.53% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.319** (có history: 0.318) | overlap=0: 5.05% | <20%: 27.27% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.316, 'pronoun': 0.327, 'connector': 0.231}
- OOV: 11.11% (TB 1.22%)
- **Vị trí bằng chứng** (98 mẫu): {'0-20%': 37.76, '20-40%': 7.14, '40-60%': 22.45, '60-80%': 19.39, '80-100%': 13.27} | median offset 604c | sau 650c: 47.96% | sau 512 token: 18.37%

## 8. BM25 baseline

- 99 query | 85 gold + 200 nhiễu
- nDCG@10 single/history = 0.5427/0.7472 | Recall@10 = 0.6913/0.8799

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 25 | 0.4989 | 0.4919 | 0.7417 | 0.7217 |
| 2 | 25 | 0.5425 | 0.8563 | 0.6733 | 0.9533 |
| 3 | 25 | 0.589 | 0.7763 | 0.66 | 0.9117 |
| 4 | 14 | 0.5723 | 0.8159 | 0.7286 | 0.927 |
| 5+ | 10 | 0.4955 | 0.944 | 0.6367 | 0.9467 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 4 | 0.2893 | 1.0 | 0.5833 | 1.0 |
| pronoun | 54 | 0.6226 | 0.8414 | 0.729 | 0.9536 |
| standalone | 41 | 0.4622 | 0.5985 | 0.6522 | 0.7711 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 6 | 0.5594 | 0.7616 | 0.6667 | 0.875 |
| statement_other | 46 | 0.4727 | 0.6499 | 0.719 | 0.8141 |
| wh_other | 2 | 0.6173 | 0.8357 | 0.6667 | 0.8333 |
| what | 7 | 0.3889 | 0.6911 | 0.4524 | 0.8333 |
| why | 1 | 0.4693 | 1.0 | 0.3333 | 1.0 |
| yes_no | 37 | 0.6542 | 0.8649 | 0.7171 | 0.9706 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 25 | 0.4989 | 0.4919 | 0.7417 | 0.7217 |
| on_topic | 27 | 0.6744 | 0.8142 | 0.7852 | 0.8994 |
| shift | 24 | 0.4688 | 0.8252 | 0.5625 | 0.9253 |
| weak | 23 | 0.5129 | 0.8648 | 0.6609 | 0.9816 |

- Turn khó: **4** (4.04%) — {'lexical_gap (overlap<0.2)': 3, 'ranking/distractor': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 234 | 0 (0.0%) | 0 (0.0%) | 1 (0.44%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 15,536

**`Kohlberg/1468223012756_100.txt`** (13 ký tự)
```text
Pages 122-143
```
**`Kohlberg/1468223012756_104.txt`** (42 ký tự)
```text
Robert Lockie Ratio Equity before ‘Equity’
```
**`Kohlberg/1468223012756_107.txt`** (16 ký tự)
```text
Wiley Home Page
```
**`Kohlberg/1468223012756_72.txt`** (46 ký tự)
```text
the parcels had been stolen by a UPS employee.
```
**`Kohlberg/1468223012756_98.txt`** (17 ký tự)
```text
Volume86, Issue1
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 123

**`analysis_paralysis/unfinishedtasks_42.txt`** (436 ký tự)
```text
[ â¨ Better Thinking ](https://nesslabs.com/topic/thinking) [ ð§ Healthy Mind ](https://nesslabs.com/topic/mental-health) [ âð¬ Meaningful Living ](https://nesslabs.com/topic/life) [ ð¨ Purposeful Creativity ](ht…
```
**`analysis_paralysis/unfinishedtasks_44.txt`** (84 ký tự)
```text
Ness Labs Â© 2022. [ All rights reserved ](https://nesslabs.com/copyright- notice) .
```
**`bandwagon/votingpoliticalparty_9.txt`** (53 ký tự)
```text
[ EspaÃ±ol ](/es/votar-partido-de-registro-electoral)
```
**`confirmation_bias/indexhtml_1.txt`** (90 ký tự)
```text
[ EspaÃ±ol ](/spanish/) | [ Other Languages ](https://wwwn.cdc.gov/pubs/other-languages/)
```
**`confirmation_bias/indexhtml_69.txt`** (1390 ký tự)
```text
* [ EspaÃ±ol ](https://www.cdc.gov/other/language-assistance.html#Spanish "Spanish") * [ ç¹é«ä¸­æ ](https://www.cdc.gov/other/language-assistance.html#Chinese "Chinese") * [ Tiáº¿ng Viá»t ](https://www.cdc.gov/other…
```

### ❌ `control_chars` — ký tự điều khiển — 5

**`active_learning/WilliamsLombrozoRehderpdf_4.txt`** (3522 ký tự)
```text
Discovered differences between categories (from explicit reports) Theme Features 62% 43% 28% 10% Color Features 37% 57% 45% 70% Classification test accuracy Theme Features 0.83 0.74 0.70 0.60 Color Features 0.78 0.83 0.8…
```
**`active_learning/WilliamsLombrozoRehderpdf_5.txt`** (3787 ký tự)
```text
condition more often reported theme features as a difference between categories than those in the classify condition, whether the pattern was reliable, 2 (1) = 4.04, p < 0.05, or misleading, 2 (1) = 9.79, p < 0.05. Par…
```
**`active_learning/WilliamsLombrozoRehderpdf_6.txt`** (3555 ký tự)
```text
monitoring, identifying gaps in knowledge, or motivation and attention. A prompt to explain could have made participants attend more to their errors, justify individual categorizations by appeal to the salient and object…
```
**`active_learning/WilliamsLombrozoRehderpdf_7.txt`** (2554 ký tự)
```text
   !        !              !      !    Other interesting directions for future research include the role of explanation in generating…
```
**`recurrent_synapes/2B004pdf_2.txt`** (4117 ký tự)
```text
[26] g(fijk(t)) = fijk(t)  1 + α N min(K,k X +N/2) k0=max(0,k−N/2) (fijk0 ) 2   β (4) where K is the total number of feature maps in the current layer. Note that in the denominator in (4) the sum runs over N feature …
```

### ❌ `html_residue` — HTML/entity còn sót — 27

**`dopamine/endorphinsthebrainsnaturalpainreliever_7.txt`** (2642 ký tự)
```text
How to release endorphins You can increase your body’s endorphin release by engaging in these activities: * **[ Exercise ](/mind-and-mood/the-no-drug-approach-to-mild-depression) . ** A moderately intense pace, whether y…
```
**`cause_effect/reversecausality_1.txt`** (9860 ký tự)
```text
When you evaluate a scenario and conclude that one factor affects another, it’s important to consider the possibility of reverse causation. This phenomenon describes the process of variable Y influencing variable X inste…
```
**`confirmation_bias/understandingpsychosis_73.txt`** (109 ký tự)
```text
[ Funding & Grant News ](/funding/opportunities-announcements/funding-grant- news "Funding &amp; Grant News")
```
**`illogical_things/strikethroughhowtrumpovertonwindowextremenormal_15.txt`** (749 ký tự)
```text
[ Bird flu jumped to cows, then to a human. Should we be worried? ](https://www.vox.com/health/24118152/explain-it-to-me-bird-flu-human-case- texas-chickens-cows-animal-agriculture) By [ Benji Jones ](https://www.vox.com…
```
**`illusion_control/rhetoricalstrategieslist_6.txt`** (55 ký tự)
```text
&nbsp; Share: Is this article helpful? Related Articles
```

### ❌ `boilerplate` — boilerplate/menu/footer — 1,408

**`dopamine/dopaminethepathwaytopleasure_6.txt`** (953 ký tự)
```text
_Dopamine can provide an intense feeling of reward._ [ Dopamine ](/blog/dopamine-fasting-misunderstanding-science-spawns-a- maladaptive-fad-2020022618917) is most notably involved in helping us feel pleasure as part of t…
```
**`dopamine/endorphinsthebrainsnaturalpainreliever_7.txt`** (2642 ký tự)
```text
How to release endorphins You can increase your body’s endorphin release by engaging in these activities: * **[ Exercise ](/mind-and-mood/the-no-drug-approach-to-mild-depression) . ** A moderately intense pace, whether y…
```
**`cause_effect/reversecausality_1.txt`** (9860 ký tự)
```text
When you evaluate a scenario and conclude that one factor affects another, it’s important to consider the possibility of reverse causation. This phenomenon describes the process of variable Y influencing variable X inste…
```
**`fmri_tms/pnas1522551113_2.txt`** (2259 ký tự)
```text
Vol. 113 | No. 21 Significance Abstract Results SI Materials and Methods Discussion SI Results Materials and Methods Acknowledgments Supporting Information References Information & Authors Metrics & Citations View Option…
```
**`synes/home_1.txt`** (1817 ký tự)
```text
What is Synesthesia? Synesthesia (British spelling synaesthesia) is a rare trait that gives rise to a type of 'merging of sensations'. Some synaesthetes see colours when they hear music, for example. For other synaesthet…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 9,922

**`confirmation_bias/cphpg861448p6298338_7.txt`** (198 ký tự)
```text
[ Confirmation Bias ](https://en.wikipedia.org/wiki/List_of_cognitive_biases) is the tendency to search for, interpret, focus on and remember information in a way that confirms one's preconceptions.
```
**`dopamine/oxytocinthelovehormone_5.txt`** (515 ký tự)
```text
Oxytocin can help us bond with loved ones and can be released through touch, music, and exercise. June 13, 2023 * Reviewed by [ Howard E. LeWine, MD ](https://www.health.harvard.edu/authors/howard-lewine-md) , Chief Medi…
```
**`illogical_things/strikethroughhowtrumpovertonwindowextremenormal_7.txt`** (2718 ký tự)
```text
**Share** All sharing options for: How Trump makes extreme things look normal * [ Reddit ](https://reddit.com/submit?title=How+Trump+makes+extreme+things+look+normal&url=https%3A%2F%2Fwww.vox.com%2F2017%2F12%2F21%2F16806…
```
**`Kohlberg/LawrenceKohlberg27sstagesofmoraldevelopment_2.txt`** (4538 ký tự)
```text
Lawrence Kohlberg's stages of moral development 19 languages * [ Afrikaans ](https://af.wikipedia.org/wiki/Stadiums_van_morele_ontwikkeling_van_die_mens "Stadiums van morele ontwikkeling van die mens – Afrikaans") * [ ال…
```
**`Kohlberg/reasoningmoral_105.txt`** (857 ký tự)
```text
> ![sep man icon](../../symbols/sepman-icon.jpg) | [ How to cite this entry > ](https://plato.stanford.edu/cgi- > bin/encyclopedia/archinfo.cgi?entry=reasoning-moral) . > ---|--- > ![sep man icon](../../symbols/sepman-ic…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 948

**`Kohlberg/reasoningmoral_11.txt`** (5 ký tự)
```text
* * *
```
**`active_learning/howpowerpointpresentationshelpstudentszfd5h1y418_17.txt`** (5 ký tự)
```text
* * *
```
**`active_learning/howpowerpointpresentationshelpstudentszfd5h1y418_6.txt`** (5 ký tự)
```text
* * *
```
**`active_learning/howpowerpointpresentationshelpstudentszfd5h1y418_8.txt`** (5 ký tự)
```text
* * *
```
**`already_dream/mg24632841000whydoesfallingindreamshappen_48.txt`** (12 ký tự)
```text
#### Health
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 673

**`personality_disorder/Personalitydisorder_135.txt`** (4344 ký tự)
```text
DSM-IV-TR Personality disorders from the perspective of the five-factor model of general personality functioning [47] : 1723 (including previous DSM revisions) Factors | PPD | SzPD | StPD | ASPD | BPD | HPD | NPD | AvPD …
```
**`social_facilitation/Socialfacilitation_29.txt`** (276 ký tự)
```text
the effects on performance commonly attributed to competition are actually due to performance goals. Competition prompts either performance-approach goals, which are what facilitate performance improvements, or performan…
```
**`Kohlberg/reasoningmoral_109.txt`** (573 ký tự)
```text
[ agency: shared ](../shared-agency/) | [ intentionality: collective ](../collective-intentionality/) | [ moral dilemmas ](../moral-dilemmas/) | [ moral particularism ](../moral-particularism/) | [ moral particularism: a…
```
**`Kohlberg/reasoningmoral_117.txt`** (336 ký tự)
```text
* [ Editorial Information ](../../info.html) * [ About the SEP ](../../about.html) * [ Editorial Board ](../../board.html) * [ How to Cite the SEP ](../../cite.html) * [ Special Characters ](../../special-characters.html…
```
**`Kohlberg/reasoningmoral_119.txt`** (193 ký tự)
```text
* [ Support the SEP ](../../support/) * [ PDFs for SEP Friends ](../../support/friends.html) * [ Make a Donation ](../../support/donate.html) * [ SEPIA for Libraries ](../../support/sepia.html)
```

### ❌ `non_english` — nghi không phải tiếng Anh — 7,138

**`personality_disorder/Personalitydisorder_135.txt`** (4344 ký tự)
```text
DSM-IV-TR Personality disorders from the perspective of the five-factor model of general personality functioning [47] : 1723 (including previous DSM revisions) Factors | PPD | SzPD | StPD | ASPD | BPD | HPD | NPD | AvPD …
```
**`fmri_tms/pnas1522551113_22.txt`** (374 ký tự)
```text
Crossref PubMed Google Scholar 11 JM Fuster, SL Bressler, Cognit activation: A mechanism enabling temporal integration in working memory. Trends Cogn Sci 16, 207–218 (2012). Go to reference Crossref PubMed Google Scholar…
```
**`Kohlberg/LawrenceKohlberg27sstagesofmoraldevelopment_1.txt`** (807 ký tự)
```text
Contents move to sidebar hide * (Top) * 1 Stages Toggle Stages subsection * 1.1 Pre-conventional * 1.2 Conventional * 1.3 Post-conventional * 1.4 Further stages * 2 Theoretical assumptions (philosophy) Toggle Theoretical…
```
**`Kohlberg/LawrenceKohlberg27sstagesofmoraldevelopment_14.txt`** (146 ký tự)
```text
Critiques [ [ edit ](/w/index.php?title=Lawrence_Kohlberg%27s_stages_of_moral_development&action=edit&section=9 "Edit section: Critiques") ]
```
**`Kohlberg/LawrenceKohlberg27sstagesofmoraldevelopment_2.txt`** (4538 ký tự)
```text
Lawrence Kohlberg's stages of moral development 19 languages * [ Afrikaans ](https://af.wikipedia.org/wiki/Stadiums_van_morele_ontwikkeling_van_die_mens "Stadiums van morele ontwikkeling van die mens – Afrikaans") * [ ال…
```

### ❌ `pii_email` — chứa email — 165

**`methodology/osopdf_0.txt`** (5400 ký tự)
```text
1 Running Head: OPEN SCIENCE AND REFORM Open Science and Reform Practices in Organizational Behavior Research over Time (2011 to 2019) Elizabeth R. Tenney University of Utah Elaine Costa University of Utah Aurélien Allar…
```
**`chick_vision/jexbiopdf_1.txt`** (3191 ký tự)
```text
accurately. Chicks have four types of single-cone photoreceptor sensitive to ultraviolet, short-, medium- or long-wavelength light. To establish how these receptors are used for colour vision, stimuli were designed to be…
```
**`positive_negative_reinforce/behavan000020003pdf_0.txt`** (4508 ký tự)
```text
The Behavior Analyst 2005, 28, 85-98 No. 2 (Fall) Positive and Negative Reinforcement: Should the Distinction Be Preserved? Alan Baron University of Wisconsin-Milwaukee Mark Galizio University of North Carolina at Wilmin…
```
**`active_learning/WilliamsLombrozoRehderpdf_0.txt`** (3858 ký tự)
```text
Why does explaining help learning? Insight from an explanation impairment effect Joseph Jay Williams (joseph_williams@berkeley.edu) Tania Lombrozo (lombrozo@berkeley.edu) Department of Psychology, University of Californi…
```
**`active_learning/activelearning_10.txt`** (220 ký tự)
```text
Contact University Office Plaza, Suite 400 2221 University Ave SE Minneapolis , MN 55414 United States [ 612-625-3041 ](tel:612-625-3041) [ cei@umn.edu ](mailto:cei@umn.edu) [ Request Consultation ](/node/891)
```

### ❌ `pii_phone` — chứa số điện thoại — 482

**`emotion_definition/S2352250X17300106via3Dihub_2.txt`** (3361 ký tự)
```text
Highlights • Internal bodily signals impact behaviour and emotions. • Interoception is dissociable along objective, subjective and metacognitive psychological dimensions. • Alignment of interoceptive dimensions can predi…
```
**`chick_vision/jexbiopdf_11.txt`** (2200 ký tự)
```text
−0.5(q +l qs)]/ √(3/2) L=M -0.8 0 0.8 -0.5 0 0.5 1 L L=M S 0 0.05 0.1 0.15 0.05 0.1 RB T1 T2 T3 T4 T5 500 510 520 530 550 560 570 580 590 600 630 Greenish Reddish Bluish M x y A B 2958 Avian ultraviolet and yellow There …
```
**`chick_vision/jexbiopdf_2.txt`** (2572 ký tự)
```text
provoked much interest, and it is clear that the ultraviolet cone signal is used for mate choice and for finding prey (Bennett et al., 1996, 1997; Burkhardt, 1996; Andersson and Amundsen, 1997; Church et al., 1998). Deri…
```
**`Kohlberg/LawrenceKohlberg27sstagesofmoraldevelopment_23.txt`** (18970 ký tự)
```text
References [ [ edit ](/w/index.php?title=Lawrence_Kohlberg%27s_stages_of_moral_development&action=edit&section=18 "Edit section: References") ] 1. ^ _**a** _ _**b** _ _**c** _ Crain, William C. (1985). [ _Theories of Dev…
```
**`active_learning/activelearning_10.txt`** (220 ký tự)
```text
Contact University Office Plaza, Suite 400 2221 University Ave SE Minneapolis , MN 55414 United States [ 612-625-3041 ](tel:612-625-3041) [ cei@umn.edu ](mailto:cei@umn.edu) [ Request Consultation ](/node/891)
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 2,545

**`meg/Magnetoencephalography_5.txt`** (1702 ký tự)
```text
The basis of the MEG signal [ [ edit ](/w/index.php?title=Magnetoencephalography&action=edit&section=2 "Edit section: The basis of the MEG signal") ] [ Synchronized neuronal currents ](/wiki/Neural_synchronization "Neura…
```
**`basking/Baskinginreflectedglory_5.txt`** (3666 ký tự)
```text
Major theoretical approaches [ [ edit ](/w/index.php?title=Basking_in_reflected_glory&action=edit&section=2 "Edit section: Major theoretical approaches") ] Although Cialdini's studies introduced the concept of BIRGing to…
```
**`dopamine/dopaminethepathwaytopleasure_6.txt`** (953 ký tự)
```text
_Dopamine can provide an intense feeling of reward._ [ Dopamine ](/blog/dopamine-fasting-misunderstanding-science-spawns-a- maladaptive-fad-2020022618917) is most notably involved in helping us feel pleasure as part of t…
```
**`dopamine/dopaminethepathwaytopleasure_7.txt`** (1573 ký tự)
```text
**Where is dopamine produced?** Neurons in the region at the base of the brain produce dopamine in a two-step process. First, the amino acid tyrosine is converted into another amino acid, called L-dopa. Then L-dopa under…
```
**`dopamine/endorphinsthebrainsnaturalpainreliever_7.txt`** (2642 ký tự)
```text
How to release endorphins You can increase your body’s endorphin release by engaging in these activities: * **[ Exercise ](/mind-and-mood/the-no-drug-approach-to-mild-depression) . ** A moderately intense pace, whether y…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 930

**`hot_cold/Hotcoldempathygap_3.txt`** (4617 ký tự)
```text
sitelinks- wikipedia "Edit interlanguage links") * [ Article ](/wiki/Hot-cold_empathy_gap "View the content page \[c\]") * [ Talk ](/wiki/Talk:Hot-cold_empathy_gap "Discuss improvements to the content page \[t\]") Englis…
```
**`basking/Baskinginreflectedglory_3.txt`** (5199 ký tự)
```text
sitelinks-wikipedia "Edit interlanguage links") * [ Article ](/wiki/Basking_in_reflected_glory "View the content page \[c\]") * [ Talk ](/wiki/Talk:Basking_in_reflected_glory "Discuss improvements to the content page \[t…
```
**`gene_express/Geneexpression_38.txt`** (693 ký tự)
```text
mRNA-protein correlation [ [ edit ](/w/index.php?title=Gene_expression&action=edit&section=24 "Edit section: mRNA-protein correlation") ] While transcription directly reflects gene expression, the copy number of mRNA mol…
```
**`finger_motion/Basalganglia_3.txt`** (10850 ký tự)
```text
sitelinks-wikipedia "Edit interlanguage links") * [ Article ](/wiki/Basal_ganglia "View the content page \[c\]") * [ Talk ](/wiki/Talk:Basal_ganglia "Discuss improvements to the content page \[t\]") English * [ Read ](/w…
```
**`methodology/osopdf_3.txt`** (6271 ký tự)
```text
period examined. Pre-registration We found 18 instances of authors claiming to use pre-registration, representing 0.8% of published studies across these four journals (see Figure 2 and Table 2), and 14 of the instances w…
```

### ❌ Trùng chính xác — 9,079

*3136 nhóm*

- nhóm: `anthropo/full_18.txt`, `anthropo/full_35.txt`, `anthropo/full_45.txt`, `causality_illusion/full_18.txt`, `causality_illusion/full_35.txt`, `causality_illusion/full_45.txt`
```text
[ Articles ](//www.frontiersin.org/journals/psychology/articles) [ Research Topics ](//www.frontiersin.org/journals/psychology/research-topics) [ Editorial Board ](//www.frontiersin.org/journals/psychology/editors)
```
- nhóm: `aphasia/typesreadingdisability_24.txt`, `aphasia/whatdysgraphia_24.txt`
```text
Browse our library of evidence-based teaching strategies, learn more about using classroom texts, find out what whole-child literacy instruction looks like, and dive deeper into comprehension, content area literacy, writ…
```
- nhóm: `change_belief/Listofcognitivebiases_235.txt`, `pareidolia/Mereexposureeffect_125.txt`
```text
| Researchers |
```
- nhóm: `confirmation_bias/paranoia_99.txt`, `gay_genetic/genesandgenetics_147.txt`
```text
* #### Health topics
```
- nhóm: `illusion_control/planningfallacy_130.txt`, `pareidolia/mereexposureeffect_121.txt`
```text
##### Why it happens
```

### ❌ Gần trùng (khác nhau chút ít) — 194

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 67: `surgeon_son/buresearchriddlerevealsthedepthofgenderbias_103.txt`, `surgeon_son/buresearchriddlerevealsthedepthofgenderbias_107.txt`, `surgeon_son/buresearchriddlerevealsthedepthofgenderbias_111.txt`, `surgeon_son/buresearchriddlerevealsthedepthofgenderbias_124.txt`, `surgeon_son/buresearchriddlerevealsthedepthofgenderbias_147.txt`
  - `surgeon_son/buresearchriddlerevealsthedepthofgenderbias_103.txt`:
```text
[ Link ](https://www.bu.edu/articles/2014/bu-research-riddle-reveals-the- depth-of-gender-bias/#comment-7663992)
```
  - `surgeon_son/buresearchriddlerevealsthedepthofgenderbias_107.txt`:
```text
[ Link ](https://www.bu.edu/articles/2014/bu-research-riddle-reveals-the- depth-of-gender-bias/#comment-7679121)
```
- cụm size 15: `anthropo/TheLastLionWinstonSpencerChurchill_82.txt`, `basiler_membrane/Frequency_165.txt`, `basking/JamesCleverly_403.txt`, `change_belief/Listofcognitivebiases_249.txt`, `divergent_norm/Gestaltpsychology_188.txt`
  - `anthropo/TheLastLionWinstonSpencerChurchill_82.txt`:
```text
* [ Privacy policy ](https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Privacy_policy) * [ About Wikipedia ](/wiki/Wikipedia:About) * [ Disclaimers ](/wiki/Wikipedia:General_disclaimer) * [ Contact Wikipedi…
```
  - `basiler_membrane/Frequency_165.txt`:
```text
* [ Privacy policy ](https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Privacy_policy) * [ About Wikipedia ](/wiki/Wikipedia:About) * [ Disclaimers ](/wiki/Wikipedia:General_disclaimer) * [ Contact Wikipedi…
```
- cụm size 13: `anthropo/Zoomorphism_0.txt`, `bandwagon/Bandwagoneffect_0.txt`, `finger_motion/Motorcontrol_0.txt`, `meg/Magnetoencephalography_0.txt`, `meg/Shuntinginhibition_0.txt`
  - `anthropo/Zoomorphism_0.txt`:
```text
Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events …
```
  - `bandwagon/Bandwagoneffect_0.txt`:
```text
Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events …
```
- cụm size 11: `anthropo/TheLastLionWinstonSpencerChurchill_81.txt`, `basiler_membrane/Frequency_164.txt`, `causality_illusion/2018Torontovanattack_151.txt`, `fmri/DerekJonesmusician_104.txt`, `gene_express/Expressionmathematics_126.txt`
  - `anthropo/TheLastLionWinstonSpencerChurchill_81.txt`:
```text
* This page was last edited on 26 March 2024, at 04:24 (UTC) . * Text is available under the [ Creative Commons Attribution-ShareAlike License 4.0 ](//en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attribut…
```
  - `basiler_membrane/Frequency_164.txt`:
```text
* This page was last edited on 12 March 2024, at 19:06 (UTC) . * Text is available under the [ Creative Commons Attribution-ShareAlike License 4.0 ](//en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attribut…
```
- cụm size 10: `Kohlberg/LawrenceKohlberg27sstagesofmoraldevelopment_27.txt`, `bandwagon/Bandwagoneffect_35.txt`, `cosine_similarity/Similaritymeasure_29.txt`, `finger_motion/Basalganglia_29.txt`, `horn_effect/Horneffect_17.txt`
  - `Kohlberg/LawrenceKohlberg27sstagesofmoraldevelopment_27.txt`:
```text
/en.wikipedia.org) * [ Cookie statement ](https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Cookie_statement) * [ Mobile view ](//en.m.wikipedia.org/w/index.php?title=Lawrence_Kohlberg%27s_stages_of_moral_d…
```
  - `bandwagon/Bandwagoneffect_35.txt`:
```text
/en.wikipedia.org) * [ Cookie statement ](https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Cookie_statement) * [ Mobile view ](//en.m.wikipedia.org/w/index.php?title=Bandwagon_effect&mobileaction=toggle_vi…
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

- `31_turn_1`: In split-brain patients, can they still play piano pieces they learned before surgery?
- `77_turn_1`: In workplace feedback, what does it mean when criticism is sandwiched between positive comments?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 54

- `0_turn_2`: Are there certain mental habits that make us more likely to change our minds for no real reason?
- `2_turn_2`: What happens if you only use one wavelength—does it just blur the two types together?
- `2_turn_4`: Does that make it tricky to compare results between different people or sessions?
- `6_turn_2`: Is that why our bodies react physically when we feel strong emotions?
- `6_turn_3`: How does the brain actually send those signals to speed up your heart when you’re scared?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 4

- `31_turn_4`: Then how do their brains handle seeing both lines of music at once when they're playing?
- `33_turn_6`: Oh, does Wikipedia talk about how this plays out in friendships or close relationships?
- `74_turn_5`: Why do psychologists joke about wanting what neuroscientists have?
- `88_turn_4`: Oh, and when people actually see those vote counts or poll numbers, does that make them more likely to go with the majority?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 24

- `2_turn_4` (cos=0.0)
  - trước: I wonder if using two wavelengths also helps deal with how light scatters differently through brain tissue?
  - sau: Does that make it tricky to compare results between different people or sessions?
- `6_turn_3` (cos=0.0)
  - trước: Is that why our bodies react physically when we feel strong emotions?
  - sau: How does the brain actually send those signals to speed up your heart when you’re scared?
- `14_turn_2` (cos=0.0)
  - trước: In personality disorders, how does looking at traits instead of strict categories change how we see opposites like histr…
  - sau: Would seeing these as points on a spectrum make it clearer how opposite their attention needs really are?
- `14_turn_3` (cos=0.0)
  - trước: Would seeing these as points on a spectrum make it clearer how opposite their attention needs really are?
  - sau: Is it harder to spot someone who wants to be unnoticed if we use those broader trait systems?
- `23_turn_4` (cos=0.0)
  - trước: Is it different when people use animal traits for objects or gods instead of for other people?
  - sau: How do you actually tell when something’s zoomorphism versus anthropomorphism?

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

- `confirmation_bias/cphpg861448p6298338_7.txt` ['url_heavy']
```text
[ Confirmation Bias ](https://en.wikipedia.org/wiki/List_of_cognitive_biases) is the tendency to search for, interpret, focus on and remember information in a way that confirms one's preconceptions.
```
- `personality_disorder/Personalitydisorder_135.txt` ['repetitive', 'non_english']
```text
DSM-IV-TR Personality disorders from the perspective of the five-factor model of general personality functioning [47] : 1723 (including previous DSM revisions) Factors | PPD | SzPD | StPD | ASPD | BPD…
```
- `synes/home_1.txt` ['boilerplate']
```text
What is Synesthesia? Synesthesia (British spelling synaesthesia) is a rare trait that gives rise to a type of 'merging of sensations'. Some synaesthetes see colours when they hear music, for example. …
```

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 5

- `14_turn_2` (pronoun) gold=['personality_disorder/Personalitydisorder_135.txt']: Would seeing these as points on a spectrum make it clearer how opposite their attention needs really are?
- `14_turn_3` (pronoun) gold=['personality_disorder/Personalitydisorder_135.txt']: Is it harder to spot someone who wants to be unnoticed if we use those broader trait systems?
- `24_turn_2` (pronoun) gold=['delusion/communicatingpsychosisaspx_25.txt']: Does avoiding arguments like that actually make people more open to getting help?
- `33_turn_5` (standalone) gold=['pygmalion/Pygmalioneffect_3.txt']: I’m curious—could always expecting the best from someone actually change how your relationship develops over time?
- `39_turn_2` (pronoun) gold=['thought_terminate/Chaoticitinerancy_34.txt']: What actually makes those lingering neuron patterns finally stop so we can think about something else?

### ❌ Bằng chứng nằm muộn (> 1500 ký tự) — 33

- `57_turn_2` offset=42250c gold=`revenge_multi/annurevpsych010418103305pdf_1.txt`
  - query: What happens when that urge for revenge spills over into group decisions or politics?
  - bằng chứng: People take revenge for several reasons, including (a) because they feel angry over a perceived norm violation, (b) because they see revenge as a means of resto…
- `57_turn_3` offset=42250c gold=`revenge_multi/annurevpsych010418103305pdf_1.txt`
  - query: Is there actual evidence that wanting revenge helped humans survive or stay safe in the past?
  - bằng chứng: People take revenge for several reasons, including (a) because they feel angry over a perceived norm violation, (b) because they see revenge as a means of resto…
- `57_turn_6` offset=35329c gold=`revenge_multi/annurevpsych010418103305pdf_1.txt`
  - query: Is it the feeling that something’s unfair that really pushes people to want revenge, more than just being angry?
  - bằng chứng: Honor-based revenge represents another example of this potential spiral dynamic: People commit honor-based vengeance because of intense cultural norms in honor …
- `57_turn_1` offset=23577c gold=`revenge_multi/annurevpsych010418103305pdf_1.txt`
  - query: In understanding revenge, how can looking at biology, psychology, and culture together help explain why people seek it?
  - bằng chứng: Perceptions of entitativity may also help explain the conditions under which individuals may seek revenge on behalf of people within their social groups (Choi e…
- `57_turn_4` offset=9908c gold=`revenge_multi/annurevpsych010418103305pdf_1.txt`
  - query: I wonder if growing up in different cultures actually changes how likely someone is to want revenge?
  - bằng chứng: This explains why employees in organizations are more likely to seek revenge when they are higher up the chain of command than the offending party (Aquino et al…

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 11

- `15_turn_3` OOV=['sst', 'vip']: How exactly does a neuron start making something like Sst or Vip in the first place?
- `15_turn_1` OOV=['sst']: In brain imaging studies, how do scientists use things like GFP to spot Sst-expressing neurons?
- `15_turn_2` OOV=['sst']: Wait, when they say a neuron is Sst-expressing, are they talking about the actual protein, the mRNA, or just a label?
- `23_turn_2` OOV=['legends']: Are there times in history when people used animal traits for humans more than for gods or legends?
- `36_turn_1` OOV=['xq28']: In sexual orientation, is there real evidence that genetics, like the Xq28 region, play a role in being gay?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 4

*nguyên nhân: {'lexical_gap (overlap<0.2)': 3, 'ranking/distractor': 1}*

- `39_turn_2` ti=1 ctx=pronoun overlap=0.0: What actually makes those lingering neuron patterns finally stop so we can think about something else?
  - gold ['thought_terminate/Chaoticitinerancy_34.txt'] | top3 ['psycho_neuro/neuroscience_13.txt', 'burnout/thetelltalesignsofburnoutdoyouhavethem_3.txt', 'herd_mentality/runningandjogging_11.txt']
- `0_turn_1` ti=0 ctx=standalone overlap=0.083: In belief formation, can our confidence in something shift even if we don't get new information?
  - gold ['confirmation_bias/cphpg861448p6298338_7.txt', 'confirmation_bias/cphpg861448p6298338_8.txt'] | top3 ['thought_terminate/Chaoticitinerancy_41.txt', 'russell/27181_19.txt', 'russell/27181_27.txt']
- `39_turn_1` ti=0 ctx=standalone overlap=0.167: In brain activity, what keeps our thoughts from getting stuck and helps us shift to new ones?
  - gold ['thought_terminate/Chaoticitinerancy_12.txt', 'thought_terminate/Chaoticitinerancy_13.txt', 'thought_terminate/Chaoticitinerancy_38.txt'] | top3 ['russell/27181_27.txt', 'overthinking/overthinkingcanbedetrimentalhumanperformance_32.txt', 'sandwich_technique/25792_0.txt']
- `49_turn_1` ti=0 ctx=standalone overlap=0.2: In psychology, what's the term for thinking a solution was obvious after you already know the answer?
  - gold ['hindsight_bias/Hindsightbias_3.txt'] | top3 ['psycho_neuro/neuroscience_12.txt', 'meg/megsignalmodelingusingrecurrentneuralnetworks_12.txt', 'psycho_neuro/neuroscience_11.txt']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ❌ Split `train`: gold doc dùng chung với dev — 1

- `confirmation_bias/cphpg861448p6298338_8.txt`