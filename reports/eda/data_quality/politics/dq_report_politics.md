# Báo cáo chất lượng dữ liệu — domain `politics`

*Tạo lúc 2026-11-21T09:07:08 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 91.9 🟢** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 95.5 | 🟢 |
| content | 0.25 | 94.8 | 🟢 |
| conversation | 0.15 | 92.3 | 🟢 |
| gold | 0.25 | 82.7 | 🟡 |
| link | 0.15 | 97.2 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| gold | % turn gold inline ≠ qrels | 5.56 | 2 | 11.12 |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 7.69 | 1 | 7.69 |
| gold | % cặp gold mồ côi (doc không có trong corpus) | 2.07 | 3 | 6.21 |
| integrity | % doc có mojibake | 1.39 | 2 | 2.78 |
| link | % turn gold không chia sẻ từ nào với query | 1.85 | 1.5 | 2.78 |
| integrity | % doc có ký tự điều khiển | 0.87 | 2 | 1.74 |
| content | % nghi không phải tiếng Anh | 3.42 | 0.5 | 1.71 |
| content | % boilerplate | 2.9 | 0.3 | 0.87 |
| content | % doc quá ngắn | 1.5 | 0.5 | 0.75 |
| content | % lặp bất thường | 1.33 | 0.5 | 0.67 |
| content | % ký hiệu lạ/URL nặng | 1.56 | 0.4 | 0.62 |
| content | % gần trùng (ngoài trùng chính xác) | 0.35 | 0.7 | 0.24 |

## 2. Khuyến nghị

- **[medium]** 1.39% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 1.5%.
- **[low]** 3.42% doc nghi không phải tiếng Anh.
- **[low]** Có email/SĐT trong corpus -> cân nhắc ẩn danh.
- **[high]** 63.41% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 1 hội thoại có đại từ/liên từ ở turn đầu.
- **[high]** 3 cặp gold trỏ tới doc KHÔNG có trong corpus.
- **[high]** 3 turn có gold inline KHÁC qrels.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **16,712** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 1.39% | ký tự điều khiển 0.87% | HTML/entity sót 0.28%
- Benchmark: 13 hội thoại | schema=`qa_pair` | vai trò {'user': 54, 'assistant': 54} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 54/54
- qrels: 142 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 142} | qid 54

## 4. Chất lượng nội dung

- Ký tự: min=24 p25=347.0 **median=934.0** mean=1097.6 p75=1825.0 p90=2176.0 p99=2939.0 max=18601 | outlier dài (>6259.0c): 0.07%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 39.89% / 45.38% / 66.44% / 99.61%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 6.5% |
| 101-300 | 15.05% |
| 301-650 | 18.34% |
| 651-800 | 5.49% |
| 801-1500 | 21.06% |
| 1501-3000 | 33.17% |
| 3001-6000 | 0.32% |
| >6000 | 0.08% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 251 | 1.5% |
| mojibake | lỗi encoding (mojibake) | 232 | 1.39% |
| control_chars | ký tự điều khiển | 145 | 0.87% |
| html_residue | HTML/entity còn sót | 46 | 0.28% |
| boilerplate | boilerplate/menu/footer | 484 | 2.9% |
| url_heavy | URL chiếm >25% nội dung | 117 | 0.7% |
| symbol_heavy | ký hiệu lạ >30% | 144 | 0.86% |
| repetitive | lặp từ/dòng bất thường | 222 | 1.33% |
| non_english | nghi không phải tiếng Anh | 571 | 3.42% |
| pii_email | chứa email | 142 | 0.85% |
| pii_phone | chứa số điện thoại | 210 | 1.26% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 2106 | 12.6% |
| starts_lower | bắt đầu bằng chữ thường | 239 | 1.43% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **9.88%**
- Trùng chính xác: 0 doc dư (0.0%), 0 nhóm
- Gần trùng: 54 cụm | doc dư gần-trùng ngoài trùng chính xác 58 (0.35%) | cụm lớn nhất 4
- Từ vựng (mẫu 10,028 doc): 52,295 từ | hapax 42.76% | Zipf -0.921 | s(15569), u(3978), state(3915), government(3732), more(3681), may(3559), 1(3202), states(3196), also(3136), other(3102), all(3089), new(3057), law(2859), these(2679), israel(2564)

## 5. Hội thoại

- **13** hội thoại, **54** turn | turn/hội thoại: mean 4.15 (min 3, max 6) | query: mean 18.6 từ, median 19.0, p95 22.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 28 | 51.85% |
| pronoun | 25 | 46.3% |
| connector | 1 | 1.85% |
| short_ellipsis | 0 | 0% |

→ **63.41%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 1 (7.69%)
- Chuyển chủ đề: {'weak': 24.39, 'shift': 19.51, 'on_topic': 56.1} | hội thoại nhảy chủ đề ≥50% turn: 23.08%

**Loại câu hỏi:** statement_other 46.3%, yes_no 42.59%, what 5.56%, how 5.56%

## 6. Gold / qrels

- Nguồn gold: {'inline': 54} | qrels được dùng để eval: False
- Gold/turn: mean 2.69, max 7
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **3** cặp (2.07%), 1 doc
- qrels: khớp 54/54 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **3** turn
- Doc chưa từng là gold: 16,649/16,712 (99.62%) | Gini 0.2753
- Độ dài gold vs corpus (median): 1074.0 vs 934.0 (tỷ lệ 1.15x)
- Gold có lỗi nghiêm trọng: 0.0% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.312** (có history: 0.267) | overlap=0: 1.85% | <20%: 14.81% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.336, 'pronoun': 0.287, 'connector': 0.267}
- OOV: 1.85% (TB 0.14%)
- **Vị trí bằng chứng** (54 mẫu): {'0-20%': 37.04, '20-40%': 25.93, '40-60%': 14.81, '60-80%': 12.96, '80-100%': 9.26} | median offset 262c | sau 650c: 22.22% | sau 512 token: 0.0%

## 8. BM25 baseline

- 54 query | 63 gold + 200 nhiễu
- nDCG@10 single/history = 0.6319/0.7709 | Recall@10 = 0.74/0.9102

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 13 | 0.7222 | 0.7222 | 0.8231 | 0.8231 |
| 2 | 13 | 0.6086 | 0.8826 | 0.7308 | 0.978 |
| 3 | 13 | 0.5564 | 0.7018 | 0.674 | 0.9286 |
| 4 | 9 | 0.5778 | 0.7966 | 0.6667 | 0.9444 |
| 5+ | 6 | 0.731 | 0.7459 | 0.8333 | 0.8611 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 1 | 0.6934 | 0.525 | 1.0 | 1.0 |
| pronoun | 25 | 0.5412 | 0.8175 | 0.6505 | 0.9286 |
| standalone | 28 | 0.7106 | 0.7381 | 0.8107 | 0.8906 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 3 | 0.7941 | 0.9071 | 0.8333 | 0.8889 |
| statement_other | 25 | 0.7259 | 0.7267 | 0.8109 | 0.868 |
| what | 3 | 0.5397 | 0.9277 | 0.7778 | 1.0 |
| yes_no | 23 | 0.5205 | 0.7809 | 0.646 | 0.9472 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 13 | 0.7222 | 0.7222 | 0.8231 | 0.8231 |
| on_topic | 23 | 0.6237 | 0.7746 | 0.6957 | 0.9079 |
| shift | 8 | 0.5791 | 0.8571 | 0.7292 | 1.0 |
| weak | 10 | 0.5754 | 0.7569 | 0.7429 | 0.9571 |

- Turn khó: **1** (1.85%) — {'lexical_gap (overlap<0.2)': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 159 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 251

**`politics_ex_91249_neg_106`** (24 ký tự)
```text
۔^@�Z�� t��Gj_wD�Ad�!
```
**`politics_ex_91249_neg_67`** (35 ký tự)
```text
L-A0^��� �� �� �=�%]� �jO�\��.
```
**`politics_ex_93264_neg_67`** (42 ký tự)
```text
Biden Nicaragua v. Germany South Africa v.
```
**`politics_ex_88512_google_neg_11`** (48 ký tự)
```text
Photo: GAVRIIL GRIGOROV/SPUTNIK/AFP/Getty Images
```
**`politics_ex_88512_google_neg_164`** (34 ký tự)
```text
Yevgeniya Gaber and Graeme P. Herd
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 232

**`politics_ex_88512_neg_49`** (1786 ký tự)
```text
In this context, limited nuclear use as a means of coercion may appear less outlandish. A nuclear weapon imparts four effects upon its target area: thermal radiation; blast; nuclear radiation; and a nuclear electromagnet…
```
**`politics_ex_88512_neg_51`** (1981 ký tự)
```text
One possibility is that if Russia cannot fully reconstitute the conventional military power that it is expending in Ukraine, it will become increasingly reliant on its nonstrategic nuclear arsenal and could lower its nuc…
```
**`politics_ex_88849_neg_12`** (1954 ký tự)
```text
Not because the courts believe the Administration is prohibited by law from issuing new regulations or rescinding or modifying existing ones, but because courts have found that the Administration has short-circuited the …
```
**`politics_ex_88849_neg_13`** (1957 ký tự)
```text
Because of my Catholic upbringing and background, I personally disagree with those who advocate unrestricted birth control and abortions. That wouldnât stop me from following the law as laid down by a higher court, alt…
```
**`politics_ex_88912_neg_10`** (1964 ký tự)
```text
'DEARG LE FEARG' | Derry Girls and Peaky Blinders star joins tens of thousands on Irish language rights protest | Media Archive | An Dream Dearg Media Archive 'DEARG LE FEARG' | Derry Girls and Peaky Blinders star joins …
```

### ❌ `control_chars` — ký tự điều khiển — 145

**`politics_ex_91249_neg_0`** (6529 ký tự)
```text
%PDF-1.3 %���� 323 0 obj << /Linearized 1 /O 325 /H [ 1101 464 ] /L 441116 /E 162066 /N 100 /T 434537 >> endobj xref 323 32 0000000016 00000 n 0000000991 00000 n 0000001565 00000 n 0000001723 00000 n 0000002001 00000 n 0…
```
**`politics_ex_91249_neg_1`** (1726 ký tự)
```text
�_ ��yxg)˔z���çL�U���*�u�Sk�Se�O4?׸�c����.� �  �� R� ߁��-��2�5������ ��S�>ӣV����d�`r��n~��Y�&�+`��;�A4�� ���A9� =�-� t� � l�`;��~p���� �Gp | ��[`L��`<� "A � YA�+��Cb(��R�,� *�T�2B-� �ꇆ�…
```
**`politics_ex_91249_neg_10`** (2069 ký tự)
```text
����̡�o5�ծ��?�b &7ΫWէ���z��s�I;0Q4&G ����^�d��.щ���[*QN"�q:#|ŝ0R6��k��_��&�LsaB��2��0�͉G*�;���m o�]����g� ��������/��e�S��)섈�Ί������͟�-��E �U��}���!�Nc�^G�"�9��;���Yh ��2��j���5�|8�td��U���#{��;�R{q|�…
```
**`politics_ex_91249_neg_100`** (2682 ký tự)
```text
�p4Mq�e ��B���]�MV�( GS�di���+��RE��}V˷���W��ת1�������R<[�ڇYN��x�m�a�U�l���r:t�t}� ���@���s�����d�.�Ժ�  a7���MN� �$r��P*!ac���Uc��2P ����T�Seg��� �E��η��\ !]D*t�Y��3�2>��8<~�y\gy^I�Z�uv~p�)��C t<���� …
```
**`politics_ex_91249_neg_101`** (2286 ký tự)
```text
��y�aM?������V��:�v; T��#��?�; |�� �uI�E��tB�8��� �r��� MEM��5����^��}��=���~K ˘�wI�I h��yjB'��b� �5�t��T�� �7�\�`�Pku y�ָ ��[П �J�:��u���� P��'22��!�B l��`��� �c��F�H@��=-��Z��˂ �M�2�7�nCS2�|��AR� �…
```

### ❌ `html_residue` — HTML/entity còn sót — 46

**`politics_ex_91249_neg_114`** (1525 ký tự)
```text
��K<��LJ�tVe��J����x9�=-G�:r��#��>)�<��$���4Dݖc�k_�3�] ����趟@%1d��1�Ў���K��"� g��+��*���Sb�{�}'��9�k�Ғu���� ]9�� �+Q)fG7�(�\���u�ҥ�GW�9` U�Z�(�(�Y�r8�<�{e��o`�� |�N�y� 8g�z��� ��>�w^$ ײ�� ���sq$6@ 1…
```
**`politics_ex_91249_neg_12`** (2960 ký tự)
```text
��'3~.��4�1p��j� �6'uz:���}P�/��A(����{��U��;/�rR��΋%���Ҭe�O�-+X m�6e�Y�=�4<a�f�N̎�6�ǎLM��X [o\�]1�|q�2"6�(Q�Lq�2%6٨R*�5�oc��ͱ=�^�͘���8C5%#1CT � 25=�"�W�v��PU�"Ѕd ���h4 �m�4�'��ĳpނ[�܍y�-c�K� f G �A 4�…
```
**`politics_ex_91249_neg_129`** (3192 ký tự)
```text
��+ 駒�-{��EL���1�� 6>xe �x؃��,���ٹ��Զ�w,Ԫ<��|���� �gS��cM]�UJ� ��G��\�7�c�6������[Y� �Tt�I�}l�œ��"!��~k@� 6��5"YL �g�n�+M�Z[oE# KXd<��Q�<ڷg���u��� �(��vL�� �~ �<x,����"���� j.����&�r*��!<��L�ؑ�Ȧ[�^…
```
**`politics_ex_91249_neg_132`** (3549 ký tự)
```text
><�W��g%��C�_��*?~+�p�?"[�S%���:��h���,6� �\�ȶ����:�ȳ��(�E�b�k�T��!K�$q� ���^�E7>��>��1���\|��1�����Ǻk�n>��;��=���z�E(�/=z�f=5G�%ۺr�v��Xg�D���?� ��$z]}3V޾J��j+�~��89bv��z4��5@J5RN~P ��O_�U?��P&�tyB��4k…
```
**`politics_ex_91249_neg_137`** (5322 ký tự)
```text
�f��b�NΩ�}�5��m ���&��ɚ꿉� ���B�V+�z �l���*.�7�ojr@�@?�tMd�R\N�>�7��z0�� w���0�V^~�l�0g��N�@�ďȨ��J6y�?XX;��":�gщ�����{�n k�F�u2�l��?��� ���H�[J� 5xz�!\3 �v�Hh��U_�y��,R�)|�m�t�R?�����|�FEԈY����0�K-=�B��…
```

### ❌ `boilerplate` — boilerplate/menu/footer — 484

**`politics_ex_88512_neg_0`** (1955 ký tự)
```text
Russia’s Nuclear Weapons | Congress.gov | Library of Congress skip to main content Citation Subscribe Share/Save Site Feedback Home > CRS Products (Library of Congress) > IF12672 Russia’s Nuclear Weapons CRS PRODUCT (LIB…
```
**`politics_ex_88512_neg_36`** (1555 ký tự)
```text
Myths and misconceptions around Russian military intent | Myth 6: ‘Russia’s nuclear threats are real and should be taken literally’ 42 captures 23 Aug 2022 - 21 Sep 2025 Apr MAY Jun 18 2024 2025 2026 success fail About t…
```
**`politics_ex_88512_neg_52`** (694 ký tự)
```text
Projects Closed The Red Team Project: Understanding the Enemy The Red Team project seeks to provide in-depth analysis of the military forces of adversaries and competitors View online chevron-right keywords Topics C4ISR …
```
**`politics_ex_88512_neg_53`** (1933 ký tự)
```text
Strengthening the Nuclear Taboo in the Midst of Russia's War on Ukraine | Arms Control Association Skip to main content Create new account Reset your password "No one can solve this problem alone, but together we can cha…
```
**`politics_ex_88512_neg_64`** (1906 ký tự)
```text
Why Russia Keeps Rattling the Nuclear Saber Skip to main content Why Russia Keeps Rattling the Nuclear Saber Photo: Alexander Zemlianichenko Jr/Xinhua/Getty Images Commentary by Heather Williams Published May 20, 2024 Re…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 117

**`politics_ex_88512_neg_28`** (1949 ký tự)
```text
Schelling, The Strategy of Conflict (Cambridge, UK: Cambridge University Press, 1980). 17 RIA Novosti, “ Олег Сыромолотов: среди беженцев с Украины могут быть террористы [Oleg Syromolotov: there may be terrorists among r…
```
**`politics_ex_88512_neg_29`** (2001 ký tự)
```text
24 Dmitry Medvedev, “ Результаты решений Верховного главнокомандующего от, 21 September 2022 [Results of the decisions of the Supreme Commander-in-Chief of 21 September 2022],” Telegram (Post), updated September 22, 2022…
```
**`politics_ex_88512_neg_30`** (1968 ký tự)
```text
31 The Kremlin, “Signing of treaties on accession of Donetsk and Lugansk people’s republics and Zaporozhye and Kherson regions to Russia,” President of Russia, September 30, 2022, http://en.kremlin.ru/events/president/ne…
```
**`politics_ex_88512_neg_31`** (1827 ký tự)
```text
39 William Alberque, “Russia is unlikely to use nuclear weapons in Ukraine,” IISS Analysis , October 10, 2022, https://www.iiss.org/blogs/analysis/2022/10/russia-is-unlikely-to-use-nuclear-weapons-in-ukraine ; Brian Mich…
```
**`politics_ex_88512_neg_33`** (1653 ký tự)
```text
25, 2022.” 51 “‘Response should be devastating’ if Russia uses nuclear weapons, Polish foreign minister says,” NBC News , September 27, 2022, https://www.nbcnews.com/video/-response-should-be-devastating-if-russia-uses-n…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 144

**`politics_ex_91249_neg_1`** (1726 ký tự)
```text
�_ ��yxg)˔z���çL�U���*�u�Sk�Se�O4?׸�c����.� �  �� R� ߁��-��2�5������ ��S�>ӣV����d�`r��n~��Y�&�+`��;�A4�� ���A9� =�-� t� � l�`;��~p���� �Gp | ��[`L��`<� "A � YA�+��Cb(��R�,� *�T�2B-� �ꇆ�…
```
**`politics_ex_91249_neg_10`** (2069 ký tự)
```text
����̡�o5�ծ��?�b &7ΫWէ���z��s�I;0Q4&G ����^�d��.щ���[*QN"�q:#|ŝ0R6��k��_��&�LsaB��2��0�͉G*�;���m o�]����g� ��������/��e�S��)섈�Ί������͟�-��E �U��}���!�Nc�^G�"�9��;���Yh ��2��j���5�|8�td��U���#{��;�R{q|�…
```
**`politics_ex_91249_neg_100`** (2682 ký tự)
```text
�p4Mq�e ��B���]�MV�( GS�di���+��RE��}V˷���W��ת1�������R<[�ڇYN��x�m�a�U�l���r:t�t}� ���@���s�����d�.�Ժ�  a7���MN� �$r��P*!ac���Uc��2P ����T�Seg��� �E��η��\ !]D*t�Y��3�2>��8<~�y\gy^I�Z�uv~p�)��C t<���� …
```
**`politics_ex_91249_neg_101`** (2286 ký tự)
```text
��y�aM?������V��:�v; T��#��?�; |�� �uI�E��tB�8��� �r��� MEM��5����^��}��=���~K ˘�wI�I h��yjB'��b� �5�t��T�� �7�\�`�Pku y�ָ ��[П �J�:��u���� P��'22��!�B l��`��� �c��F�H@��=-��Z��˂ �M�2�7�nCS2�|��AR� �…
```
**`politics_ex_91249_neg_102`** (5395 ký tự)
```text
;K!��a�c�2��,��.���W�F]�����M�����]�I��C��6R�I g�>�4���1� s�Ǿm-MW��l�§I|�m`��x��wϳ}ƻ��W#}�qqXc4^�x�����$�=�#č�l��UF����1t��7�mg���e �M$=LY�]�le/�.��lG�Rl0�E|2ޭUW;�i��/�� �SHm�;��W�{��^���2E�'e �(9�f'�…
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 222

**`politics_ex_88698_neg_28`** (1954 ký tự)
```text
[ 196 ] [ better source needed ] Following the armistice, both Israel and Syria sought to take advantage of the territorial ambiguities left in place by the 1949 agreement. This resulted in an evolving tactical situation…
```
**`politics_ex_88698_neg_58`** (1975 ký tự)
```text
Institute for the Study of Diplomacy, Edmund A. Walsh School of Foreign Service, Georgetown University. p. 12. ISBN 978-0-934742-11-5 . ^ a b Taylor & Francis Group (2003). The Europa World Year Book 2003 . Europa World …
```
**`politics_ex_88698_neg_61`** (1993 ký tự)
```text
^ a b Edgar S. Marshall. Israel: current issues and historical background . Nova Publishers, 2002. pg. 35. ISBN 978-1-59033-325-9 . ^ Garfinkle, Adam (1998). "History and Peace: Revisiting two Zionist myths". Israel Affa…
```
**`politics_ex_89068_neg_12`** (1112 ký tự)
```text
Furthermore, that would risk the same ire Macron’s penultimate government suffered when he used this constitutional clause to push through everything from budgets to pension reforms. Since then, 49:3 has become a byword …
```
**`politics_ex_89068_neg_22`** (1985 ký tự)
```text
^ "Matignon: Macron "test" Cazeneuve and Bertrand, the Beaudet surprise emerges" . TV5 Monde (in French). 2 September 2024 . Retrieved 5 September 2024 . . ^ "Nouveau Premier ministre: Michel Barnier, nouvelle "piste sér…
```

### ❌ `non_english` — nghi không phải tiếng Anh — 571

**`politics_ex_88912_neg_8`** (2100 ký tự)
```text
External links [ edit ] Official website v t e Irish language History Proto-Indo-European Proto-Celtic Insular Celtic Proto-Goidelic Primitive Irish Old Irish Middle Irish Early Modern Irish Modern Irish Sociolinguistics…
```
**`politics_ex_88912_neg_9`** (1312 ký tự)
```text
Uí Néill , Clan Colla , Clan Donald , Uí Mháine , etc) Dalcassians (incl. Déisi ) Eóganachta Érainn (incl. Dál Riata , Corcu Loígde , Dál Fiatach , etc) Laigin Ulaid (incl. Dál nAraidi , Conmaicne , and Cíarraige ) Ulste…
```
**`politics_ex_89068_neg_13`** (1840 ký tự)
```text
cache:https://www.eurasiareview.com/05122024-french-left-and-far-right-bring-down-barnier-government/ - Google Suche Links zur Barrierefreiheit Zu den Hauptinhalten springen Hilfe zur Barrierefreiheit Feedback zur Barrie…
```
**`politics_ex_89068_neg_14`** (601 ký tự)
```text
Alle ablehnen Alle akzeptieren Weitere Optionen Datenschutz · Nutzungsbedingungen Filter und Themen KI‑Modus Alle Bilder Videos Kurze Videos Bücher Web Mehr Looking for results in English? Change to English Weiter auf De…
```
**`politics_ex_89068_neg_22`** (1985 ký tự)
```text
^ "Matignon: Macron "test" Cazeneuve and Bertrand, the Beaudet surprise emerges" . TV5 Monde (in French). 2 September 2024 . Retrieved 5 September 2024 . . ^ "Nouveau Premier ministre: Michel Barnier, nouvelle "piste sér…
```

### ❌ `pii_email` — chứa email — 142

**`politics_ex_88512_neg_51`** (1981 ký tự)
```text
One possibility is that if Russia cannot fully reconstitute the conventional military power that it is expending in Ukraine, it will become increasingly reliant on its nonstrategic nuclear arsenal and could lower its nuc…
```
**`politics_ex_89587_neg_0`** (1994 ký tự)
```text
GAO-05-478, Elections: Additional Data Could Help State and Local Elections Officials Maintain Accurate Voter Registration Lists This is the accessible text file for GAO report number GAO-05-478 entitled 'Elections: Addi…
```
**`politics_ex_89587_neg_2`** (1630 ký tự)
```text
Michigan has had a statewide list since 1998, and officials believe it is near HAVA compliant. California election officials are still considering how to meet these HAVA requirements, and in New York, legislation was pas…
```
**`politics_ex_89587_neg_61`** (1843 ký tự)
```text
Despite resource shortages in the federal courts and the fact that most juror are screened by local and state courts, the AOUSC Director acknowledged the public interest in ensuring that non-citizens are not afforded the…
```
**`politics_ex_89587_neg_86`** (458 ký tự)
```text
20548: To order by Phone: Voice: (202) 512-6000: TDD: (202) 512-2537: Fax: (202) 512-6061: To Report Fraud, Waste, and Abuse in Federal Programs: Contact: Web site: www.gao.gov/fraudnet/fraudnet.htm E-mail: fraudnet@gao.…
```

### ❌ `pii_phone` — chứa số điện thoại — 210

**`politics_ex_88512_neg_36`** (1555 ký tự)
```text
Myths and misconceptions around Russian military intent | Myth 6: ‘Russia’s nuclear threats are real and should be taken literally’ 42 captures 23 Aug 2022 - 21 Sep 2025 Apr MAY Jun 18 2024 2025 2026 success fail About t…
```
**`politics_ex_88698_neg_46`** (1944 ký tự)
```text
170 ISBN 978-0-8010-0010-2 ^ a b HaReuveni, Immanuel (1999). Lexicon of the Land of Israel (in Hebrew). Miskal – Yedioth Ahronoth Books and Chemed Books. pp. 662–663 ISBN 978-965-448-413-8 . ^ a b Vitto, Fanny, Ancient S…
```
**`politics_ex_88698_neg_49`** (1973 ký tự)
```text
The Jewish presence probably dated back to the mid second century BCE, and most likely increased after the Hasmonean conquest of the region during the reign of Alexander Jannaeus. Itureans were among the earliest settler…
```
**`politics_ex_88698_neg_53`** (1961 ký tự)
```text
ISBN 978-965-223-863-4 . ^ a b c d e Gil-Har, Yitzhak (1981). "Separation of Trans-Jordan from Palestine". The Jerusalem Cathedra , ed. Lee Levine, Yad Yitzhak Ben-Zvi and Wayne State University , Jerusalem, p. 306. ^ Si…
```
**`politics_ex_88698_neg_55`** (1961 ký tự)
```text
The main item on the agenda was the threat posed by Israel's diversion of water … The preamble to its decision stated: "The establishment of Israel is the basic threat that the Arab nation in its entirety has agreed to f…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 2,106

**`politics_ex_88512_doc_6`** (583 ký tự)
```text
A wide range of experienced analysts outside Russia have concluded that, as opposed to threatened use for coercion or military advantage, Russia's nuclear weapons would only actually be used in extremis. This view holds …
```
**`politics_ex_89909_doc_0`** (2663 ký tự)
```text
The Big Country/Small Country Problem Most of the open-border discussion is framed within the context of wealthy countries opening up their borders to migrants from poorer countries. Moreover, many of these wealthy count…
```
**`politics_ex_90729_doc_1`** (1724 ký tự)
```text
"Natural Resource Relevant Assets" means the sites, reserves, and deposits in the territory of Ukraine of aluminum, antimony, arsenic, barite, beryllium, bismuth, cerium, cesium, chromium, cobalt, copper, dysprosium, erb…
```
**`politics_ex_90729_doc_6`** (1307 ký tự)
```text
This framework is reminiscent of the colonial arrangement that the United States imposed on Iraq, after invading the country in an illegal war of aggression in 2003 and overthrowing its government. The US central bank, t…
```
**`politics_ex_91144_doc_2`** (594 ký tự)
```text
Andrew Martin, Ph.D. "For motivation purposes, I think, obviously, a commitment to a cause is important but also being embedded in networks with like-minded individuals who can—you might go to a protest with, who can mak…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 239

**`politics_ex_88512_neg_62`** (1723 ký tự)
```text
and European states begin to supply Ukraine with weapons that can strike deeper into Russian territory, into Russian-controlled Ukrainian territory of Crimea, or into Belarusian territory, such as advanced fighter aircra…
```
**`politics_ex_88698_neg_75`** (4109 ký tự)
```text
v t e Israeli and Palestinian border crossings and checkpoints Crossings between Israel and other countries Mutually-recognised borders / demarcation lines Egypt Egypt–Israel barrier Taba Border Crossing Nitzana Border C…
```
**`politics_ex_88912_neg_12`** (1106 ký tự)
```text
âWe have had no action, nothing concrete in terms of dates, in terms of any legislation coming through. Weâre bringing this to the streets.â He said the mass turnout was representative of the anger felt towards the…
```
**`politics_ex_89068_neg_13`** (1840 ký tự)
```text
cache:https://www.eurasiareview.com/05122024-french-left-and-far-right-bring-down-barnier-government/ - Google Suche Links zur Barrierefreiheit Zu den Hauptinhalten springen Hilfe zur Barrierefreiheit Feedback zur Barrie…
```
**`politics_ex_89575_neg_57`** (1530 ký tự)
```text
general election offers one of the most tempting targets for cyber-attack in the history of the Internet, whether the attacker’s motive is overtly political or simply self-aggrandizement.” [16] One of the most serious pr…
```

### ✅ Trùng chính xác
- Không phát hiện.

### ❌ Gần trùng (khác nhau chút ít) — 58

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 4: `politics_ex_93305_google_neg_24`, `politics_ex_93305_google_neg_28`, `politics_ex_93305_google_neg_41`, `politics_ex_93305_google_neg_49`
  - `politics_ex_93305_google_neg_24`:
```text
Link to this speech In context Individually (Citation: HL Deb, 3 July 2025, c944)
```
  - `politics_ex_93305_google_neg_28`:
```text
Link to this speech In context Individually (Citation: HL Deb, 3 July 2025, c945)
```
- cụm size 3: `politics_ex_91112_google_neg_230`, `politics_ex_91112_google_neg_383`, `politics_ex_93729_google_neg_46`
  - `politics_ex_91112_google_neg_230`:
```text
Official websites use .gov A .gov website belongs to an official government organization in the United States. Secure .gov websites use HTTPS A lock (LockA locked padlock) or https:// means you’ve safely connected to the…
```
  - `politics_ex_91112_google_neg_383`:
```text
Official websites use .gov A .gov website belongs to an official government organization in the United States. Secure .gov websites use HTTPS A lock ( Lock Locked padlock ) or https:// means you’ve safely connected to th…
```
- cụm size 3: `politics_ex_93394_google_neg_532`, `politics_ex_93394_google_neg_533`, `politics_ex_93394_google_neg_534`
  - `politics_ex_93394_google_neg_532`:
```text
Appreciation to the Admins of this page, Thank you. Both HSV-1 and HSV-2 can be painful and cause discomfort to the individual suffering from it. Once you suffer from herpes, there are a lot of medications and dietary su…
```
  - `politics_ex_93394_google_neg_533`:
```text
Appreciation to the Admins of this page, Thank you. Both HSV-1 and HSV-2 can be painful and cause discomfort to the individual suffering from it. Once you suffer from herpes, there are a lot of medications and dietary su…
```
- cụm size 2: `politics_ex_89994_doc_0`, `politics_ex_89994_doc_1`
  - `politics_ex_89994_doc_0`:
```text
Trump can't reverse Biden's pardons Legal experts agreed that nothing in the Constitution or the law permits pardons to be reversed. "Pardons are final and irrevocable," Kalt said. In an 1869 ruling, a federal court wrot…
```
  - `politics_ex_89994_doc_1`:
```text
Legal experts agreed that nothing in the Constitution or the law permits pardons to be reversed. "Pardons are final and irrevocable," Kalt said. In an 1869 ruling, a federal court wrote: "The law undoubtedly is, that whe…
```
- cụm size 2: `politics_ex_88698_neg_83`, `politics_ex_89563_neg_18`
  - `politics_ex_88698_neg_83`:
```text
Please join The Times of Israel Community to comment and enjoy other Community benefits Only ToI Community members can comment below articles Or Continue with close popup Check your email We sent an email to you at . It …
```
  - `politics_ex_89563_neg_18`:
```text
Log in here close popup Sign in or Join The Times of Israel Community Paying ToI Community members are invited to comment on articles Or Continue with By joining you agree to the terms and conditions back close popup Reg…
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

- `ex_93260_turn_1`: In Eisenhower's elections, why didn't he win by a bigger margin like Harding or Nixon, even though he was so popular?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 25

- `ex_93260_turn_4`: Is that why those other guys got such massive wins—because the country was going through something huge at the time?
- `ex_93094_turn_2`: Was Vietnam really that different from other wars in terms of press access?
- `ex_93094_turn_4`: I'm curious—was that total media blackout really unusual compared to how the US handled press in other wars?
- `ex_93094_turn_5`: I wonder if the way they used press pools back then kind of set the pattern for later wars?
- `ex_93094_turn_6`: Is it usually the top military leaders who decide how much the press gets to see during a war?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 1

- `ex_88512_turn_3`: But if these diplomatic moves don't really change Russia's nuclear thinking, why bother pushing China at all?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 8

- `ex_93260_turn_4` (cos=0.0)
  - trước: I’m curious—did the South sticking with the Democrats back then make it harder for Eisenhower to run up bigger numbers?
  - sau: Is that why those other guys got such massive wins—because the country was going through something huge at the time?
- `ex_93260_turn_5` (cos=0.0)
  - trước: Is that why those other guys got such massive wins—because the country was going through something huge at the time?
  - sau: I wonder if people back then just wouldn’t vote outside their party, even for someone like Eisenhower?
- `ex_93094_turn_4` (cos=0.0)
  - trước: Do you think the danger on the ground kept a lot of reporters away, even if they technically had access?
  - sau: I'm curious—was that total media blackout really unusual compared to how the US handled press in other wars?
- `ex_91586_turn_2` (cos=0.0)
  - trước: In recent resource deals, how have mineral agreements helped countries stand up to outside pressure or avoid sanctions?
  - sau: Is it clear if having US troops around those resources actually made things safer long-term for Iraq or Afghanistan?
- `ex_90619_turn_4` (cos=0.0)
  - trước: I’m curious—couldn’t they just tweak the main pension rules for tough jobs instead of having separate schemes?
  - sau: Do those old reasons for special pensions still shape how they work today?

## D. Gold / qrels

### ❌ Gold mồ côi (doc không có trong corpus) — 3

- `ex_88512_turn_1` → `politics_ex_88512_doc_3`
- `ex_88512_turn_3` → `politics_ex_88512_doc_3`
- `ex_88512_turn_4` → `politics_ex_88512_doc_3`

### ✅ qrels qid không khớp turn nào
- Không phát hiện.

### ❌ Gold inline (benchmark) ≠ qrels — 3

- `ex_88512_turn_1`: chỉ có ở inline ['politics_ex_88512_doc_3'] | chỉ có ở qrels []
- `ex_88512_turn_3`: chỉ có ở inline ['politics_ex_88512_doc_3'] | chỉ có ở qrels []
- `ex_88512_turn_4`: chỉ có ở inline ['politics_ex_88512_doc_3'] | chỉ có ở qrels []

### ✅ Turn không có gold
- Không phát hiện.

### ✅ Gold doc có lỗi nội dung nghiêm trọng
- Không phát hiện.

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 1

- `ex_90155_turn_2` (pronoun) gold=['politics_ex_90155_doc_0']: Is that basically a safeguard so parliament can't just kick out a president for any reason they want?

### ✅ Bằng chứng nằm muộn (> 1500 ký tự)
- Không phát hiện.

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 1

- `ex_90243_turn_3` OOV=['bundling']: Does bundling everything like that change how much money HMOs actually get from Medicare compared to the regular system?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 1

*nguyên nhân: {'lexical_gap (overlap<0.2)': 1}*

- `ex_91586_turn_1` ti=0 ctx=standalone overlap=0.154: In recent resource deals, how have mineral agreements helped countries stand up to outside pressure or avoid sanctions?
  - gold ['politics_ex_91586_doc_4'] | top3 ['politics_ex_90729_doc_1', 'politics_ex_91207_google_neg_42', 'politics_ex_90729_neg_75']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.