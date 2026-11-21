# Báo cáo chất lượng dữ liệu — domain `drones`

*Tạo lúc 2026-11-21T09:05:21 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 97.0 🟢** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 99.3 | 🟢 |
| content | 0.25 | 93.9 | 🟢 |
| conversation | 0.15 | 90.9 | 🟢 |
| gold | 0.25 | 100.0 | 🟢 |
| link | 0.15 | 99.9 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 9.09 | 1 | 9.09 |
| content | % nghi không phải tiếng Anh | 6.72 | 0.5 | 3.36 |
| content | % doc quá ngắn | 2.03 | 0.5 | 1.01 |
| integrity | % doc có mojibake | 0.35 | 2 | 0.7 |
| content | % boilerplate | 2.19 | 0.3 | 0.66 |
| content | % gần trùng (ngoài trùng chính xác) | 0.58 | 0.7 | 0.41 |
| content | % lặp bất thường | 0.5 | 0.5 | 0.25 |
| content | % ký hiệu lạ/URL nặng | 0.63 | 0.4 | 0.25 |
| link | % OOV trung bình của query | 0.46 | 0.3 | 0.14 |
| content | % chứa PII (email/phone) | 0.84 | 0.1 | 0.08 |
| content | % HTML sót | 0.07 | 0.4 | 0.03 |

## 2. Khuyến nghị

- **[medium]** 0.35% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 2.03%.
- **[low]** 6.72% doc nghi không phải tiếng Anh.
- **[high]** 59.26% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 1 hội thoại có đại từ/liên từ ở turn đầu.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **16,381** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.35% | ký tự điều khiển 0.0% | HTML/entity sót 0.07%
- Benchmark: 11 hội thoại | schema=`qa_pair` | vai trò {'user': 38, 'assistant': 38} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 38/38
- qrels: 107 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 107} | qid 38

## 4. Chất lượng nội dung

- Ký tự: min=30 p25=240.0 **median=537.0** mean=772.0 p75=1113.0 p90=1911.0 p99=2754.0 max=13156 | outlier dài (>3732.0c): 0.01%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 56.71% / 64.01% / 83.4% / 99.98%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 7.68% |
| 101-300 | 23.36% |
| 301-650 | 25.67% |
| 651-800 | 7.31% |
| 801-1500 | 19.39% |
| 1501-3000 | 16.58% |
| 3001-6000 | 0.01% |
| >6000 | 0.01% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 333 | 2.03% |
| mojibake | lỗi encoding (mojibake) | 58 | 0.35% |
| control_chars | ký tự điều khiển | 0 | 0.0% |
| html_residue | HTML/entity còn sót | 12 | 0.07% |
| boilerplate | boilerplate/menu/footer | 359 | 2.19% |
| url_heavy | URL chiếm >25% nội dung | 103 | 0.63% |
| symbol_heavy | ký hiệu lạ >30% | 0 | 0.0% |
| repetitive | lặp từ/dòng bất thường | 82 | 0.5% |
| non_english | nghi không phải tiếng Anh | 1101 | 6.72% |
| pii_email | chứa email | 64 | 0.39% |
| pii_phone | chứa số điện thoại | 74 | 0.45% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 2688 | 16.41% |
| starts_lower | bắt đầu bằng chữ thường | 194 | 1.18% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **11.68%**
- Trùng chính xác: 0 doc dư (0.0%), 0 nhóm
- Gần trùng: 76 cụm | doc dư gần-trùng ngoài trùng chính xác 94 (0.58%) | cụm lớn nhất 5
- Từ vựng (mẫu 10,020 doc): 37,703 từ | hapax 41.76% | Zipf -0.971 | drone(7081), s(6942), flight(4673), battery(4109), 2(3786), 1(3486), drones(3424), more(3325), use(3193), 3(3023), dji(2746), power(2615), also(2506), aircraft(2381), these(2350)

## 5. Hội thoại

- **11** hội thoại, **38** turn | turn/hội thoại: mean 3.45 (min 3, max 5) | query: mean 18.9 từ, median 19.0, p95 24.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 22 | 57.89% |
| pronoun | 13 | 34.21% |
| connector | 3 | 7.89% |
| short_ellipsis | 0 | 0% |

→ **59.26%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 1 (9.09%)
- Chuyển chủ đề: {'on_topic': 51.85, 'shift': 14.81, 'weak': 33.33} | hội thoại nhảy chủ đề ≥50% turn: 18.18%

**Loại câu hỏi:** yes_no 39.47%, statement_other 36.84%, what 15.79%, why 5.26%, how 2.63%

## 6. Gold / qrels

- Nguồn gold: {'inline': 38} | qrels được dùng để eval: False
- Gold/turn: mean 2.82, max 7
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 38/38 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 16,333/16,381 (99.71%) | Gini 0.2124
- Độ dài gold vs corpus (median): 899.0 vs 537.0 (tỷ lệ 1.67x)
- Gold có lỗi nghiêm trọng: 0.0% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.345** (có history: 0.323) | overlap=0: 0.0% | <20%: 18.42% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.395, 'pronoun': 0.288, 'connector': 0.225}
- OOV: 5.26% (TB 0.46%)
- **Vị trí bằng chứng** (38 mẫu): {'0-20%': 39.47, '20-40%': 7.89, '40-60%': 15.79, '60-80%': 26.32, '80-100%': 10.53} | median offset 314c | sau 650c: 23.68% | sau 512 token: 0.0%

## 8. BM25 baseline

- 38 query | 48 gold + 200 nhiễu
- nDCG@10 single/history = 0.5684/0.7634 | Recall@10 = 0.6905/0.8848

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 11 | 0.7737 | 0.772 | 0.9455 | 0.9455 |
| 2 | 11 | 0.5308 | 0.7386 | 0.647 | 0.8909 |
| 3 | 11 | 0.5079 | 0.7704 | 0.5883 | 0.8338 |
| 4 | 4 | 0.4153 | 0.7298 | 0.5625 | 0.8125 |
| 5+ | 1 | 0.0 | 1.0 | 0.0 | 1.0 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 3 | 0.2276 | 0.5837 | 0.4167 | 0.6667 |
| pronoun | 13 | 0.4091 | 0.7072 | 0.5106 | 0.8209 |
| standalone | 22 | 0.7089 | 0.8211 | 0.8341 | 0.9523 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 1 | 1.0 | 0.9747 | 1.0 | 1.0 |
| statement_other | 14 | 0.682 | 0.7275 | 0.8321 | 0.9036 |
| what | 6 | 0.5494 | 0.8633 | 0.6583 | 0.9667 |
| why | 2 | 0.3414 | 0.7569 | 0.625 | 0.75 |
| yes_no | 15 | 0.4714 | 0.7438 | 0.5592 | 0.8448 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 11 | 0.7737 | 0.772 | 0.9455 | 0.9455 |
| on_topic | 14 | 0.3984 | 0.6743 | 0.4884 | 0.7837 |
| shift | 4 | 0.4207 | 0.7562 | 0.5625 | 0.875 |
| weak | 9 | 0.6474 | 0.8948 | 0.75 | 0.9722 |

- Turn khó: **0** (0.0%) — {}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 104 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 333

**`Drones_ex_3025_neg_10`** (37 ký tự)
```text
Simply login or create a free account
```
**`drones_ex_2188_google_neg_258`** (31 ký tự)
```text
New cameras, Camcorder and DSLR
```
**`drones_ex_2188_google_neg_346`** (30 ký tự)
```text
Sample footage is coming soon!
```
**`drones_ex_2188_google_neg_6`** (39 ký tự)
```text
Skyzone SKY04X Pro FPV Goggles (analog)
```
**`drones_ex_2209_google_neg_104`** (49 ký tự)
```text
Start typing to see products you are looking for.
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 58

**`Drones_ex_2188_neg_10`** (1908 ký tự)
```text
The waypoint's altitude is also shown above the waypoint marker on the map. Speed : The speed at which the aircraft will travel from this waypoint to the next. By default the aircraft will use the mission's cruising spee…
```
**`Drones_ex_2188_neg_11`** (1929 ký tự)
```text
For "Interpolate" to work, the previous or next waypoint need to be set to "Interpolate" as well. Litchi will then automatically adjust the gimbal pitch angle to start and end at the specified angles, and smoothly transi…
```
**`Drones_ex_2188_neg_12`** (1914 ký tự)
```text
If the aircraft is already pointing West before starting this action, it will not rotate at all. Tilt Camera : The gimbal will move to the specified angle (tilt). The valid value range is +0Â° to -90Â° (look down). Panor…
```
**`Drones_ex_2188_neg_2`** (1914 ký tự)
```text
If there are any, close them Start your drone and remote controller if you are using one, and let them initialize for a few seconds Connect the remote controller to the mobile device using a cable. For Wi-Fi based drones…
```
**`Drones_ex_2188_neg_29`** (1940 ký tự)
```text
Panorama Settings : Tap to bring up the Panorama settings window (details below). Panorama Database : Tap to show the Panorama Database which lists all your panoramas (iOS only - details below). Auto Pano : Tap to start …
```

### ✅ `control_chars` — ký tự điều khiển
- Không phát hiện.

### ❌ `html_residue` — HTML/entity còn sót — 12

**`Drones_ex_2523_neg_20`** (1068 ký tự)
```text
You can use a belt sander ,drum sander or router to trim the ends to a perfect radius, plus or minus a few thousanths of an inch or tenths of a millimeter. B.E. The good engineer does not need to memorize every formula; …
```
**`Drones_ex_2685_neg_2`** (1767 ký tự)
```text
You should see something like this <?xml version="1.0" encoding="UTF-8"?> <kml xmlns="http://www.opengis.net/kml/2.2"> <Document xmlns=""> <name>Mapping1</name> <open>1</open> <ExtendedData xmlns:mis="www.dji.com"> <mis:…
```
**`Drones_ex_2685_neg_3`** (1258 ký tự)
```text
<?xml version="1.0" encoding="utf-8" ?> <kml xmlns="http://www.opengis.net/kml/2.2"> <Document id="root_doc"> <Schema name="DouglasTotalArea" id="DouglasTotalArea"> <SimpleField name="id" type="float"></SimpleField> </Sc…
```
**`Drones_ex_2915_neg_11`** (1696 ký tự)
```text
BU-1006: Cost of Mobile and Renewable Power BU-1007: Net Calorific Value BU-1008: Working towards Sustainability BU-1009: Battery Paradox - Afterword Information BU-1101: Glossary BU-1102: Abbreviations BU-1103: Bibliogr…
```
**`Drones_ex_2915_neg_9`** (1703 ký tự)
```text
BU-603: How to Calibrate a “Smart” Battery BU-603a: Calibrating SMBus Batteries with Impedance Tracking BU-604: How to Process Data from a “Smart” Battery Testing and Calibrating Smart Batteries From Birth to Retirement …
```

### ❌ `boilerplate` — boilerplate/menu/footer — 359

**`Drones_ex_2188_neg_37`** (1933 ký tự)
```text
This token is a secure way to associate your flight logs with your account when they are uploaded to Airdata UAV. Info Click here to learn more about how to setup Airdata UAV with Litchi. Airdata UAV Automatic Sync : Whe…
```
**`Drones_ex_2188_neg_49`** (780 ký tự)
```text
Started by jarimy Today at 11:55 AM Replies: 2 Photo and Video Showcase The FCC ban on all foreign made UAS and UAS "critical components" Started by anotherlab Today at 10:25 AM Replies: 12 News Members online Dmonwai Pr…
```
**`Drones_ex_2188_neg_50`** (1898 ký tự)
```text
All DJI Goggles Reviewed With Features, Specs And Drone Compatibility - DroneZon Skip to content This DJI Goggles review covers the features, specifications of the original DJI Goggle, the Racing Edition (RE) and the DJI…
```
**`Drones_ex_2188_neg_58`** (630 ký tự)
```text
0.5A Output: 5V,3A ; 9V,2A；12V,1.5A External power supplied required using an input voltage of 7.4 - 17.6v. More Information On DJI Goggles If you require further information, here is the link to the DJI Goggles page. Wi…
```
**`Drones_ex_2209_neg_0`** (1909 ký tự)
```text
You need to download the DJI Fly app from DJI's website - DroneDJ Skip to main content Feature DJI Fly App UPDATED: Latest DJI Fly Android app only available from DJI’s website, not the Play Store Josh | Jan 27 2021 - 8:…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 103

**`Drones_ex_2232_neg_0`** (336 ký tự)
```text
Wayback Machine 14 captures 29 Nov 2020 - 29 May 2025 Jun JUL Aug 17 2023 2024 2025 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - http://web.archive.org/…
```
**`Drones_ex_2466_neg_11`** (325 ký tự)
```text
Wayback Machine 3 captures 24 Oct 2020 - 21 Jan 2025 Dec JAN Feb 21 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - https://web.archive.org/…
```
**`Drones_ex_2466_neg_13`** (462 ký tự)
```text
The Archive Team Panic Downloads are full pulldowns of currently extant websites, meant to serve as emergency backups for needed sites that are in danger of closing, or which will be missed dearly if suddenly lost due to…
```
**`Drones_ex_2582_neg_3`** (1152 ký tự)
```text
Get started on your BVLOS approval Article sources: https://www.faa.gov/uas/media/Part_107_Summary.pdf https://www.law.cornell.edu/cfr/text/14/107.31 https://www.law.cornell.edu/cfr/text/14/107.35 https://jrupprechtlaw.c…
```
**`Drones_ex_2752_neg_45`** (458 ký tự)
```text
The Archive Team Panic Downloads are full pulldowns of currently extant websites, meant to serve as emergency backups for needed sites that are in danger of closing, or which will be missed dearly if suddenly lost due to…
```

### ✅ `symbol_heavy` — ký hiệu lạ >30%
- Không phát hiện.

### ❌ `repetitive` — lặp từ/dòng bất thường — 82

**`Drones_ex_2240_neg_11`** (1962 ký tự)
```text
Last edited: Dec 24, 2020 Repaid1 Well-Known Member Joined Mar 27, 2020 Messages 1,834 Reactions 1,897 Age 61 Location US, SC ekoslav said: I've seen other non-DJI related USB to serial adapters before. When they have no…
```
**`Drones_ex_2276_neg_10`** (1860 ký tự)
```text
[ 9 ] Bernoulli's principle [ edit ] To compute the disk loading using Bernoulli's principle , we assume the pressure in the slipstream far downstream is equal to the starting pressure p 0 {\displaystyle p_{0}} , which i…
```
**`Drones_ex_2357_neg_7`** (1916 ký tự)
```text
Last edited: May 18, 2020 R Ronny St. Well-Known Member Joined Apr 21, 2020 Messages 537 Reactions 380 Age 66 Location Broechem, Belgium Think I found a practical one: Irfanview portable so that you do not have to instal…
```
**`Drones_ex_2466_neg_8`** (1850 ký tự)
```text
If for some reason activation has failed and the ESC is not regarded as a valid BLHeli_32 unit, the ESC will beep like this upon powerup, before the normal operation beep sequence starts: In this case the ESC will only a…
```
**`Drones_ex_2523_neg_12`** (1974 ký tự)
```text
Fan [ edit ] Like any other fan, propeller or rotor, a ducted fan is characterised by the number of blades. The Rhein Flugzeugbau (RFB) SG 85 had three blades, while the Dowty Rotol Ducted Propulsor had seven. [ 3 ] [ 4 …
```

### ❌ `non_english` — nghi không phải tiếng Anh — 1,101

**`drones_ex_2357_doc_1`** (881 ký tự)
```text
Make : DJI Speed X : +0.00 Speed Y : +0.10 Speed Z : -0.10 Pitch : -5.90 Yaw : -13.60 Roll : +1.90 Camera Pitch : -15.50 Camera Yaw : -13.70 Camera Roll : +0.00 Flashpix Version : 0010 Color Space : sRGB Exif Image Width…
```
**`drones_ex_2357_doc_2`** (259 ký tự)
```text
About : DJI Meta Data Format : image/jpg Absolute Altitude : +42.63 Relative Altitude : +48.70 Gimbal Roll Degree : +0.00 Gimbal Yaw Degree : -13.70 Gimbal Pitch Degree : -15.50 Flight Roll Degree : +1.90 Flight Yaw Degr…
```
**`drones_ex_2357_doc_3`** (162 ký tự)
```text
GPS Altitude : 42.6 m Above Sea Level GPS Latitude : 51 deg 27' 42.93" N GPS Longitude : 0 deg 39' 35.44" W GPS Position : 51 deg 27' 42.93" N, 0 deg 39' 35.44" W
```
**`Drones_ex_2188_neg_57`** (1946 ký tự)
```text
DJI Goggles DJI Goggles RE DJI Digital FPV System Weight 995 grams (35 ounces) 1002 grams (35.35 ounces) 420 grams (14.81 ounces) Dimensions Goggles: 195×155×110 mm Headband(Folded): 255×205×92 mm DJI Goggles RE Body: 19…
```
**`Drones_ex_2232_neg_0`** (336 ký tự)
```text
Wayback Machine 14 captures 29 Nov 2020 - 29 May 2025 Jun JUL Aug 17 2023 2024 2025 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - http://web.archive.org/…
```

### ❌ `pii_email` — chứa email — 64

**`Drones_ex_2240_neg_34`** (1994 ký tự)
```text
SimuDrone - Drone Simulator - Apps on Google Play play_arrow Trailer SimuDrone - Drone Simulator Akkuzu Games In-app purchases 3.8 star 2.24K reviews info 100K+ Downloads PEGI 3 info Install Share Add to wishlist play_ar…
```
**`Drones_ex_2240_neg_35`** (739 ký tự)
```text
5 people found this review helpful See all reviews *You can now switch flight modes between Cine, Normal, and Sport using the DJI Remote Controller. *Mode 4 has been added to the joystick modes. flag Flag as inappropriat…
```
**`Drones_ex_2566_neg_22`** (1845 ký tự)
```text
It also describes the agency's incremental implementation approach for the exception and how individuals can operate recreational unmanned aircraft (commonly referred to as drones) today under the exception. FOR FURTHER …
```
**`Drones_ex_2566_neg_7`** (1984 ký tự)
```text
We highlight over ten industries where drone adoption is growing in our Drone Jobs Guide . 10 CHAPTER How Much Money Can I Make With an FAA Drone License? The drone industry is still relatively young, which can make it c…
```
**`Drones_ex_2582_neg_22`** (1507 ký tự)
```text
“ Practice Quiz Next Lesson © Copyright 2024 | Flightpath107 | All Rights Reserved Custom UX/UI & Web Design for Nature Tech Ventures by WildTECH Page load link Course Login E: hello@flightpath107.com CURRICULUM Section …
```

### ❌ `pii_phone` — chứa số điện thoại — 74

**`Drones_ex_2232_neg_0`** (336 ký tự)
```text
Wayback Machine 14 captures 29 Nov 2020 - 29 May 2025 Jun JUL Aug 17 2023 2024 2025 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - http://web.archive.org/…
```
**`Drones_ex_2232_neg_1`** (1957 ký tự)
```text
Wayback Machine 26 captures 03 Feb 2021 - 15 Oct 2025 Sep OCT Nov 15 2024 2025 2026 success fail About this capture COLLECTED BY Organization: Archive Team Formed in 2009, the Archive Team (not to be confused with the ar…
```
**`Drones_ex_2357_neg_3`** (13156 ký tự)
```text
The following is the raw output from a Mavic Pro JPG: MacBook:~ *******$ exiftool /Users/*******/Pictures/DJI_0060.JPG ExifTool Version Number : 10.53 File Name : DJI_0060.JPG Directory : /Users/*******/Pictures File Siz…
```
**`Drones_ex_2466_neg_11`** (325 ký tự)
```text
Wayback Machine 3 captures 24 Oct 2020 - 21 Jan 2025 Dec JAN Feb 21 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Save Page Now Outlinks TIMESTAMPS The Wayback Machine - https://web.archive.org/…
```
**`Drones_ex_2466_neg_12`** (1956 ký tự)
```text
Wayback Machine 3 captures 24 Jan 2022 - 30 Mar 2024 Feb MAR Apr 30 2023 2024 2025 success fail About this capture COLLECTED BY Organization: Archive Team Formed in 2009, the Archive Team (not to be confused with the arc…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 2,688

**`drones_ex_2195_doc_2`** (1008 ký tự)
```text
The pitch is a measure of how far the propeller would move forwards in one revolution if it were treated as a screw and screwed into some solid material. Although the measure of pitch treats the propeller as if it were a…
```
**`drones_ex_2212_doc_0`** (406 ký tự)
```text
R/C System These are example connections. Please setup Aileron, Elevator, Throttle, Rudder channels on your TX first, and choose o n e 2 positions switch/channel ( 3 positions switch with GPS) as control mode switch, the…
```
**`drones_ex_2212_doc_3`** (353 ký tự)
```text
I am using a DJI NAZA M LITE with a FS-IA6B CH1: Aileron on Naza CH2: Elevator on Naza CH3: Throttle on Naza CH4: Rudder on Naza CH5: U on Naza (for flight modes) CH6: X2 on Naza (for IOC) You can later upgrade to a FS-I…
```
**`drones_ex_2232_doc_1`** (639 ký tự)
```text
Noise depends on the oversampling and filter settings selected. The stated values were determined in a controlled pressure environment and are based on the average standard deviation of 32 consecutive measurement points …
```
**`drones_ex_2276_doc_1`** (574 ký tự)
```text
The elemental thrust of this blade element can thus be written as $$ΔT=L\cos(φ)≈L=1/2ρV_1^2C_LcB.dr$$ where $ρ$ is the air density, $c$ is the blade chord and small angle approximations are used for $φ$. The area generat…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 194

**`drones_ex_2492_doc_2`** (163 ký tự)
```text
get the best drive for your multirotor! ✓ fast & reliable simulation - no more guessing ✓ most comprehensive motor database ☆ over 1 million calculations per month
```
**`drones_ex_2523_doc_6`** (1034 ký tự)
```text
there is a lot going on here. Short answer is that a ducted fan (what you have pictured) can produce a lot more thrust (experiments from one paper say twice as much) than an open rotor of the same size. The big thing tha…
```
**`drones_ex_2752_doc_1`** (962 ký tự)
```text
why closed loop speed control? Typical drone electronic speed controllers (ESCs) are not actually speed controllers - rather, they handle commutation: switching of the applied current between the (usually 3) phases of th…
```
**`Drones_ex_2271_neg_15`** (1979 ký tự)
```text
bidirectionnal DSHOT makes the quad to flips at starts, so I gave up on it after many hours of trying stuff. But just by changing the motors setting to timing =20, frenquency=36 and betaflight 4.2 stock, except dmin =off…
```
**`Drones_ex_2271_neg_19`** (1158 ký tự)
```text
viewed_cookie_policy 11 months The cookie is set by the GDPR Cookie Consent plugin and is used to store whether or not user has consented to the use of cookies. It does not store any personal data. Functional Functional …
```

### ✅ Trùng chính xác
- Không phát hiện.

### ❌ Gần trùng (khác nhau chút ít) — 94

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 5: `Drones_ex_2492_neg_21`, `Drones_ex_2707_neg_11`, `Drones_ex_2707_neg_48`, `Drones_ex_2811_neg_67`, `Drones_ex_3025_neg_2`
  - `Drones_ex_2492_neg_21`:
```text
Cookie Duration Description cookielawinfo-checkbox-analytics 11 months This cookie is set by GDPR Cookie Consent plugin. The cookie is used to store the user consent for the cookies in the category "Analytics". cookielaw…
```
  - `Drones_ex_2707_neg_11`:
```text
These cookies ensure basic functionalities and security features of the website, anonymously. Cookie Duration Description cookielawinfo-checkbox-analytics 11 months This cookie is set by GDPR Cookie Consent plugin. The c…
```
- cụm size 4: `Drones_ex_2707_neg_27`, `Drones_ex_2728_neg_14`, `Drones_ex_2782_neg_37`, `Drones_ex_2787_neg_11`
  - `Drones_ex_2707_neg_27`:
```text
These cookies will be stored in your browser only with your consent. You also have the option to opt-out of these cookies. But opting out of some of these cookies may affect your browsing experience. Necessary Necessary …
```
  - `Drones_ex_2728_neg_14`:
```text
We also use third-party cookies that help us analyze and understand how you use this website. These cookies will be stored in your browser only with your consent. You also have the option to opt-out of these cookies. But…
```
- cụm size 4: `drones_ex_2188_google_neg_105`, `drones_ex_2324_google_neg_519`, `drones_ex_2782_google_neg_281`, `drones_ex_2927_google_neg_97`
  - `drones_ex_2188_google_neg_105`:
```text
Parts and AccessoriesOpen submenu Autel RoboticsOpen submenu Mavic 2 Enterprise Advanced Matrice 200 Series V2 Phantom 4 Multispectral Commercial Drone Packages Drones in the Government Sector Drone Mapping & Surveying P…
```
  - `drones_ex_2324_google_neg_519`:
```text
Parts and AccessoriesOpen submenu Autel RoboticsOpen submenu Mavic 2 Enterprise Advanced Matrice 200 Series V2 Phantom 4 Multispectral Commercial Drone Packages Drones in the Government Sector Drone Mapping & Surveying P…
```
- cụm size 4: `drones_ex_2545_google_neg_435`, `drones_ex_2545_google_neg_438`, `drones_ex_2545_google_neg_440`, `drones_ex_2545_google_neg_442`
  - `drones_ex_2545_google_neg_435`:
```text
NOTE: we are using affiliate links for some of the shops listed – any money raised goes back into funding our events and equipment! These links may be out of date and we recommend shopping around for the best deals.
```
  - `drones_ex_2545_google_neg_438`:
```text
BBB Ant Parts CAD Files NOTE: we are using affiliate links for some of the shops listed – any money raised goes back into funding our events and equipment! These links may be out of date and we recommend shopping around …
```
- cụm size 3: `Drones_ex_2232_neg_1`, `Drones_ex_2466_neg_12`, `Drones_ex_2752_neg_44`
  - `Drones_ex_2232_neg_1`:
```text
Wayback Machine 26 captures 03 Feb 2021 - 15 Oct 2025 Sep OCT Nov 15 2024 2025 2026 success fail About this capture COLLECTED BY Organization: Archive Team Formed in 2009, the Archive Team (not to be confused with the ar…
```
  - `Drones_ex_2466_neg_12`:
```text
Wayback Machine 3 captures 24 Jan 2022 - 30 Mar 2024 Feb MAR Apr 30 2023 2024 2025 success fail About this capture COLLECTED BY Organization: Archive Team Formed in 2009, the Archive Team (not to be confused with the arc…
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

- `ex_2545_turn_1`: In battery setups, is it risky to connect LiPo and Li-ion batteries in series if their specs are slightly different?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 13

- `ex_2927_turn_2`: Does adding that multispectral sensor change how accurate the maps are, or is it basically the same as the 3E for surveying?
- `ex_2927_turn_3`: Is there any difference in how easy it is to use either drone once you add things like RTK or extra batteries?
- `ex_2779_turn_3`: Is there ever a situation where you'd want to charge a cell above 4.2 volts, or is that always risky?
- `ex_2752_turn_3`: Is it normal for the RPM to lag behind the throttle input when I change it quickly?
- `ex_2662_turn_2`: Is that why it feels trickier for beginners to land with Betaflight than with, say, a DJI drone?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 3

- `ex_2662_turn_4`: Why don’t Betaflight drones have that kind of automatic landing help built in?
- `ex_2324_turn_3`: Why do you think so many beginners end up picking the Mini Series over those cheaper options?
- `ex_2324_turn_4`: And when it comes to wind or sand, do these Minis actually hold up better than the cheaper drones?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 4

- `ex_2927_turn_3` (cos=0.0)
  - trước: Does adding that multispectral sensor change how accurate the maps are, or is it basically the same as the 3E for survey…
  - sau: Is there any difference in how easy it is to use either drone once you add things like RTK or extra batteries?
- `ex_2662_turn_3` (cos=0.0)
  - trước: Is that why it feels trickier for beginners to land with Betaflight than with, say, a DJI drone?
  - sau: What actually happens if you just disarm right before touching down—is that safer, or could it mess things up?
- `ex_2662_turn_4` (cos=0.0)
  - trước: What actually happens if you just disarm right before touching down—is that safer, or could it mess things up?
  - sau: Why don’t Betaflight drones have that kind of automatic landing help built in?
- `ex_2324_turn_3` (cos=0.0)
  - trước: Is it really worth paying more for the pro drones if I'm just starting out?
  - sau: Why do you think so many beginners end up picking the Mini Series over those cheaper options?

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

### ✅ Query không chia sẻ từ nào với gold
- Không phát hiện.

### ✅ Bằng chứng nằm muộn (> 1500 ký tự)
- Không phát hiện.

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 2

- `ex_2324_turn_4` OOV=['minis']: And when it comes to wind or sand, do these Minis actually hold up better than the cheaper drones?
- `ex_2324_turn_5` OOV=['minis']: Is there a big difference in how smooth and sharp the videos look between these Minis and other brands at this price?

## F. Turn khó với BM25 (recall@10 = 0)

### ✅ Turn khó
- Không phát hiện.

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.