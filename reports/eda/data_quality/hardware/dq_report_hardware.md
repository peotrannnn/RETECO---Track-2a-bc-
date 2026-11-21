# Báo cáo chất lượng dữ liệu — domain `hardware`

*Tạo lúc 2026-11-21T09:05:59 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 95.3 🟢** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 98.3 | 🟢 |
| content | 0.25 | 93.7 | 🟢 |
| conversation | 0.15 | 85.7 | 🟢 |
| gold | 0.25 | 99.0 | 🟢 |
| link | 0.15 | 97.2 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 14.29 | 1 | 14.29 |
| content | % nghi không phải tiếng Anh | 7.15 | 0.5 | 3.58 |
| link | % turn gold không chia sẻ từ nào với query | 1.72 | 1.5 | 2.58 |
| integrity | % doc có mojibake | 0.87 | 2 | 1.74 |
| content | % doc quá ngắn | 2.14 | 0.5 | 1.07 |
| gold | % gold có lỗi nội dung nghiêm trọng | 1.92 | 0.5 | 0.96 |
| content | % boilerplate | 2.2 | 0.3 | 0.66 |
| content | % lặp bất thường | 0.75 | 0.5 | 0.38 |
| content | % gần trùng (ngoài trùng chính xác) | 0.48 | 0.7 | 0.34 |
| link | % OOV trung bình của query | 0.58 | 0.3 | 0.17 |
| content | % ký hiệu lạ/URL nặng | 0.35 | 0.4 | 0.14 |
| content | % chứa PII (email/phone) | 0.88 | 0.1 | 0.09 |

## 2. Khuyến nghị

- **[medium]** 0.87% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 2.14%.
- **[low]** 7.15% doc nghi không phải tiếng Anh.
- **[high]** 47.73% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 2 hội thoại có đại từ/liên từ ở turn đầu.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **26,308** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.87% | ký tự điều khiển 0.0% | HTML/entity sót 0.04%
- Benchmark: 14 hội thoại | schema=`qa_pair` | vai trò {'user': 58, 'assistant': 58} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 58/58
- qrels: 114 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 114} | qid 58

## 4. Chất lượng nội dung

- Ký tự: min=30 p25=196.0 **median=469.0** mean=711.3 p75=1021.0 p90=1842.0 p99=2761.0 max=8385 | outlier dài (>3496.0c): 0.02%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 61.16% / 67.72% / 85.02% / 99.96%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 9.83% |
| 101-300 | 26.5% |
| 301-650 | 24.82% |
| 651-800 | 6.56% |
| 801-1500 | 17.31% |
| 1501-3000 | 14.93% |
| 3001-6000 | 0.03% |
| >6000 | 0.01% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 564 | 2.14% |
| mojibake | lỗi encoding (mojibake) | 230 | 0.87% |
| control_chars | ký tự điều khiển | 0 | 0.0% |
| html_residue | HTML/entity còn sót | 10 | 0.04% |
| boilerplate | boilerplate/menu/footer | 579 | 2.2% |
| url_heavy | URL chiếm >25% nội dung | 93 | 0.35% |
| symbol_heavy | ký hiệu lạ >30% | 1 | 0.0% |
| repetitive | lặp từ/dòng bất thường | 197 | 0.75% |
| non_english | nghi không phải tiếng Anh | 1880 | 7.15% |
| pii_email | chứa email | 94 | 0.36% |
| pii_phone | chứa số điện thoại | 138 | 0.52% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 4016 | 15.27% |
| starts_lower | bắt đầu bằng chữ thường | 445 | 1.69% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **12.98%**
- Trùng chính xác: 0 doc dư (0.0%), 0 nhóm
- Gần trùng: 82 cụm | doc dư gần-trùng ngoài trùng chính xác 94 (0.48%) | cụm lớn nhất 11
- Từ vựng (mẫu 10,024 doc): 36,890 từ | hapax 41.69% | Zipf -1.014 | s(7241), 2(3902), more(3775), performance(3564), use(3229), 1(3170), up(3050), data(3039), all(2833), t(2822), power(2523), 5(2487), also(2424), one(2421), 3(2281)

## 5. Hội thoại

- **14** hội thoại, **58** turn | turn/hội thoại: mean 4.14 (min 3, max 9) | query: mean 19.6 từ, median 20.0, p95 24.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 37 | 63.79% |
| pronoun | 17 | 29.31% |
| connector | 4 | 6.9% |
| short_ellipsis | 0 | 0% |

→ **47.73%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 2 (14.29%)
- Chuyển chủ đề: {'on_topic': 38.64, 'weak': 38.64, 'shift': 22.73} | hội thoại nhảy chủ đề ≥50% turn: 21.43%

**Loại câu hỏi:** yes_no 50.0%, statement_other 37.93%, what 6.9%, how 5.17%

## 6. Gold / qrels

- Nguồn gold: {'inline': 58} | qrels được dùng để eval: False
- Gold/turn: mean 1.97, max 4
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 58/58 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 26,256/26,308 (99.8%) | Gini 0.2824
- Độ dài gold vs corpus (median): 866.0 vs 469.0 (tỷ lệ 1.85x)
- Gold có lỗi nghiêm trọng: 1.92% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.309** (có history: 0.269) | overlap=0: 1.72% | <20%: 29.31% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.33, 'pronoun': 0.249, 'connector': 0.369}
- OOV: 6.9% (TB 0.58%)
- **Vị trí bằng chứng** (58 mẫu): {'0-20%': 20.69, '20-40%': 36.21, '40-60%': 12.07, '60-80%': 20.69, '80-100%': 10.34} | median offset 370c | sau 650c: 20.69% | sau 512 token: 0.0%

## 8. BM25 baseline

- 58 query | 52 gold + 200 nhiễu
- nDCG@10 single/history = 0.5367/0.66 | Recall@10 = 0.6121/0.7802

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 14 | 0.7316 | 0.7316 | 0.8036 | 0.8036 |
| 2 | 14 | 0.5327 | 0.7806 | 0.5774 | 0.9226 |
| 3 | 14 | 0.587 | 0.6131 | 0.7143 | 0.7083 |
| 4 | 8 | 0.4413 | 0.6233 | 0.5 | 0.75 |
| 5+ | 8 | 0.2102 | 0.4422 | 0.2708 | 0.6458 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 4 | 0.7193 | 0.55 | 0.75 | 0.8125 |
| pronoun | 17 | 0.4146 | 0.573 | 0.5392 | 0.6961 |
| standalone | 37 | 0.5731 | 0.7118 | 0.6306 | 0.8153 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 3 | 0.0645 | 0.4968 | 0.1667 | 0.8333 |
| statement_other | 22 | 0.6526 | 0.6851 | 0.7159 | 0.7955 |
| what | 4 | 0.5714 | 0.7217 | 0.625 | 0.875 |
| yes_no | 29 | 0.4929 | 0.6492 | 0.5776 | 0.75 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 14 | 0.7316 | 0.7316 | 0.8036 | 0.8036 |
| on_topic | 17 | 0.4482 | 0.6804 | 0.4902 | 0.7843 |
| shift | 10 | 0.4621 | 0.5774 | 0.525 | 0.725 |
| weak | 17 | 0.5086 | 0.6291 | 0.6275 | 0.7892 |

- Turn khó: **7** (12.07%) — {'lexical_gap (overlap<0.2)': 6, 'context_dependent': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 130 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

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

### ❌ `too_short` — quá ngắn (<50 ký tự) — 564

**`hardware_ex_18936_neg_3`** (30 ký tự)
```text
Your request has been sent. Ok
```
**`hardware_ex_10266_google_neg_0`** (46 ký tự)
```text
Applications & Use Cases, Products, Technology
```
**`hardware_ex_10266_google_neg_147`** (32 ký tự)
```text
Joined: Mon Jan 15, 2024 9:47 am
```
**`hardware_ex_10266_google_neg_199`** (34 ký tự)
```text
Financial Services Fraud Detection
```
**`hardware_ex_10266_google_neg_253`** (41 ký tự)
```text
Latest Version of Classic via Adobe Cloud
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 230

**`hardware_ex_18378_neg_0`** (993 ký tự)
```text
VRAM requirements table Hereâs a comparison of VRAM requirements for different model sizes and fine-tuning techniques: Method Precision 7B 13B 30B 70B 110B Full 16 67GB 125GB 288GB 672GB 1056GB LoRA 16 15GB 28GB 63GB 1…
```
**`hardware_ex_18378_neg_13`** (1969 ký tự)
```text
For example, QLoRA enables fine-tuning of a 13B model on a single RTX 4090, which would be impossible with traditional methods. When all is said and done, here's how those values might shake out for a number of different…
```
**`hardware_ex_8728_neg_12`** (1989 ký tự)
```text
Orange Pi Zero 2W V1.1 Pin Definition Product display Top View Bottom View Hardware Parameters CPU Allwinner H618 Quad-Core Cortex-A53 Processor 1.5GHz GPU Mali G31 MP2 - Support OpenGL ES 1.0/2.0/3.2, OpenCL 2.0, Vulkan…
```
**`hardware_ex_8728_neg_13`** (1840 ký tự)
```text
How to Integrate Touchscreen Displays with Your Android Board | Android Board Touchscreen technology has become an essential component in modern embedded systems, especially for devices running Android on Single Board Co…
```
**`hardware_ex_8728_neg_14`** (1935 ký tự)
```text
For projects where Android SBC vs Linux SBC decision-making is still pending, you can explore Android SBC vs Linux SBC to understand which environment better suits your display needs. 3. Hardware Connection Steps a) Disp…
```

### ✅ `control_chars` — ký tự điều khiển
- Không phát hiện.

### ❌ `html_residue` — HTML/entity còn sót — 10

**`hardware_ex_11067_neg_23`** (1724 ký tự)
```text
Most Common Desktop Screen Resolutions Worldwide According to StatCounter's March 2025 data , the most used desktop screen resolutions worldwide are: 1920x1080 (24.09%) 1536x864 (10.79%) 1366x768 (10.49%) 1280x720 (5.38%…
```
**`hardware_ex_11412_neg_27`** (1967 ký tự)
```text
You can set your browser to block or alert you about these cookies, but some parts of the site will not then work.sage Name Provider Purpose Expires Type __cfduid eneba.com Cookie associated with sites using CloudFlare, …
```
**`hardware_ex_11067_google_neg_750`** (527 ký tự)
```text
Fixed a regression in 13.6.1 where a malformed URI would crash Cypress. Fixes #28521. Fixed a regression in 12.4.0 where erroneous <br> tags were displaying in error messages in the Command Log making them less readable.…
```
**`hardware_ex_15902_google_neg_190`** (419 ký tự)
```text
Star 0 (0) You must be signed in to star a gist Fork 0 (0) You must be signed in to fork a gist Embed Select an option Embed Embed this gist in your website. Share Copy sharable link for this gist. Clone via HTTPS Clone …
```
**`hardware_ex_18576_google_neg_504`** (462 ký tự)
```text
https://shop.udoo.org/udoo-bolt-v8.html The Rolls Royce of single-board computers, comparing this to the Raspberry Pi, is almost an insult to the Bolt. This is a full desktop machine crammed onto a tiny board, powerful e…
```

### ❌ `boilerplate` — boilerplate/menu/footer — 579

**`hardwarerecs_ex_18350_doc_2`** (800 ký tự)
```text
So, this is similar to backwards compatibility of say a Gen4 drive being put into a Gen3 slot and just reducing the BW of the drive. However, U.2 won't work in a U.3 position even though the connector is the same. So, if…
```
**`hardwarerecs_ex_18995_doc_1`** (1405 ký tự)
```text
How to get a cheap Mac for coding Sometimes, as much as you would love to own the best and most powerful Mac, the budget just won't stretch above £1,000/$1,000. Maybe that is more than you are willing (or able) to pay. L…
```
**`hardware_ex_10150_neg_12`** (1858 ký tự)
```text
PC power supply ratings: 80 Plus Platinum vs Gold vs Bronze vs White | PCWorld News All News Accessories Business Entertainment Gaming Laptops Mobile Monitors PCs & Components Security Smart Home Security Software Storag…
```
**`hardware_ex_10150_neg_8`** (542 ký tự)
```text
Latest: BFG-9000 Today at 5:37 PM Android & Chrome OS Moderators online Share this page Facebook X Bluesky LinkedIn Reddit Tumblr WhatsApp Email Share Link COMPANY Space.com is part of Future plc, an international media …
```
**`hardware_ex_10266_neg_1`** (1996 ký tự)
```text
NVMe vs SATA SSD: What's the Difference? | Beebom Skip to content Home > Tech > NVMe vs SATA SSD: What’s the Difference? NVMe vs SATA SSD: What’s the Difference? Beebom Staff Updated: October 15, 2025 Comments 2 Share Co…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 93

**`hardwarerecs_ex_18853_doc_2`** (341 ký tự)
```text
You may refer to Question # 6, FAQ about IEEE 1588 at http://www.intel.com/content/dam/www/public/us/en/documents/faqs/ieee1588-faq.pdf http://www.intel.com/content/dam/www/public/us/en/documents/faqs/ieee1588-faq.pdf. A…
```
**`hardwarerecs_ex_18995_doc_1`** (1405 ký tự)
```text
How to get a cheap Mac for coding Sometimes, as much as you would love to own the best and most powerful Mac, the budget just won't stretch above £1,000/$1,000. Maybe that is more than you are willing (or able) to pay. L…
```
**`hardware_ex_18350_neg_12`** (1953 ký tự)
```text
8TB U.2 Gen3 - $400 - https://www.amazon.com/dp/B0C6B2PGMC/?tag=snbforums-20 8TB U.2 Gen4 - $500 - https://www.amazon.com/dp/B0B7Y4TFJR/?tag=snbforums-20 16TB U.2 Gen4 - $1000 - https://www.amazon.com/dp/B0C6BR89C2/?tag=…
```
**`hardware_ex_18574_neg_4`** (327 ký tự)
```text
Wayback Machine 52 captures 20 Jul 2023 - 28 Oct 2025 Sep OCT Nov 28 2024 2025 2026 success fail About this capture COLLECTED BY Collection: Save Page Now TIMESTAMPS The Wayback Machine - https://web.archive.org/web/2025…
```
**`hardware_ex_19156_neg_7`** (1787 ký tự)
```text
Below are some very detailed notes on exactly what I tried / learned ez Share file and directory URLs List photos http://ezshare.card/photo ? http://ezshare.card/photo?vtype=0&fdir=100CANON&ftype=0&devw=320&devh=356&fold…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 1

**`hardware_ex_18576_google_neg_318`** (81 ký tự)
```text
ä½ æ­£å¨ä½¿ç¨æ§çæ¬æµè§å¨ãè¯·åçº§æµè§å¨ä»¥è·å¾æ´å¥½çä½éªã
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 197

**`hardware_ex_10150_neg_12`** (1858 ký tự)
```text
PC power supply ratings: 80 Plus Platinum vs Gold vs Bronze vs White | PCWorld News All News Accessories Business Entertainment Gaming Laptops Mobile Monitors PCs & Components Security Smart Home Security Software Storag…
```
**`hardware_ex_10150_neg_6`** (1965 ký tự)
```text
PCPartPicker part list / Price breakdown by merchant CPU: AMD - Ryzen 5 1400 3.2GHz Quad-Core Processor ($156.48 @ OutletPC) Motherboard: ASRock - AB350M Micro ATX AM4 Motherboard ($59.99 @ Newegg) Memory: Team - Vulcan …
```
**`hardware_ex_10543_neg_100`** (1950 ký tự)
```text
Only Audio, Visual (including 4K) Editing and CG. Reply Akshat Verma November 17, 2019 For motherboard, go with the Master and for graphics card, go with the GTX 1660 Ti as it is almost as fast as the RTX 2060 and costs …
```
**`hardware_ex_10543_neg_106`** (1996 ký tự)
```text
Reply Dominiek November 25, 2019 Thanks for comment, i will go for rtx 2060 super, there are different one, is MSI GeForce RTX 2060 Super Gaming X 8GB a good one? Greetings Dominiek Reply Akshat Verma November 25, 2019 Y…
```
**`hardware_ex_10543_neg_115`** (1986 ký tự)
```text
I work with premiere pro CC 2020 and the card is NOT for gaming! Thank you very much if you can help me for a decision. Greetings Reply Akshat Verma January 7, 2020 Hello, I think RX 580 8GB should be able to do the job …
```

### ❌ `non_english` — nghi không phải tiếng Anh — 1,880

**`hardwarerecs_ex_11349_doc_3`** (777 ký tự)
```text
Supermicro A2SDi-4C-HLN4F-O Motherboard Mini-ITX Embedded Intel Atom Processor C3558 4-Core Denverton Supports up to 256GB ECC DDR4-2133 in 4 DIMM slots 4 GbE LAN and up to 8 SATA3 ports via SoC Flexible I/O M.2 PCIe 3.0…
```
**`hardwarerecs_ex_18574_doc_4`** (786 ký tự)
```text
Standard Ports - 1x USB-A (USB 5Gbps / USB 3.2 Gen 1) - 1x USB-A (USB 5Gbps / USB 3.2 Gen 1), Always On - 1x USB-C® (USB 10Gbps / USB 3.2 Gen 2), with USB PD 3.0 - 2x Thunderbolt™ 4 / USB4® 40Gbps (support data transfer …
```
**`hardwarerecs_ex_18576_doc_0`** (1305 ký tự)
```text
Rock Pi 4C preliminary specifications: SoC – Rockchip RK3399 big.LITTLE hexa-core processor with 2x Arm Cortex-A72 @ up to 1.8 GHz, 4x Cortex-A53 @ up to 1.4 GHz, a Mali-T864 GPU with support OpenGL ES1.1/2.0/3.0/3.1, Op…
```
**`hardwarerecs_ex_18939_doc_0`** (302 ký tự)
```text
Capacity1 64GB 128GB 256GB Size and Weight2 Width: 2.65 inches (67.3 mm) Height: 5.45 inches (138.4 mm) Depth: 0.29 inch (7.3 mm) Weight: 5.22 ounces (148 grams) Display Retina HD display 4.7-inch (diagonal) widescreen L…
```
**`hardwarerecs_ex_18939_doc_3`** (438 ký tự)
```text
Body Dimensions 138.4 x 67.3 x 7.3 mm (5.45 x 2.65 x 0.29 in) Weight 148 g (5.22 oz) Build Glass front (Corning-made glass), glass back (Corning-made glass), aluminum frame SIM Nano-SIM IP67 dust/water resistant (up to 1…
```

### ❌ `pii_email` — chứa email — 94

**`hardware_ex_10543_neg_35`** (2001 ký tự)
```text
Thank you for supporting the work I put into this site!) Related Posts About The Author Akshat Verma I am a PC Gamer and a Hardware Enthusiast. I love Graphics Cards and I have been digging them since GeForce 3 series. I…
```
**`hardware_ex_11067_neg_27`** (1214 ký tự)
```text
Follow on: LinkedIn Send email: greg@designrush.com Latest Updates Related to Website Development view all Trends | Website Development Top 10 Bug Tracking Tools for Web Development Teams in 2026 By Sergio Oliveira | 1 m…
```
**`hardware_ex_18337_neg_10`** (2985 ký tự)
```text
Summary Manufacturer: HP Manufacturer part number (MPN): 3302fdw Product Family: Cartridge People SKU: 43525 What's in the Box Box Contents: HP Color LaserJet Pro MFP 3302fdw Black Starter Toner Cartridge (600 Pages) CMY…
```
**`hardware_ex_18576_neg_65`** (1855 ký tự)
```text
Specification: Rockchip RK3588 SOC — High-Performance 8nm AI & 8K Platform Brand Xilinx / AMD IC Type Field-Programmable Gate Array Related Products ESPRESSIF ESP32-C6 Wi-Fi 6 IoT SoC – RISC-V, BLE 5.3, Zigbee/Thread Quo…
```
**`hardware_ex_19220_neg_0`** (1870 ký tự)
```text
DSI 42U - 1442 G2 My Account | 0 items 855.374.7225 855.DSI.RACK DSI NEW PRODUCTS REFURBISHED PRODUCTS POLICIES ACCESSORIES SERVER RACKS Menu DSI 42U - 1442 G2 DSI 1442 G2 Call for Price The DSI 1442 G2 offers 4 compartm…
```

### ❌ `pii_phone` — chứa số điện thoại — 138

**`hardware_ex_10543_neg_121`** (1917 ký tự)
```text
– Motherboard: Asus TUF GAMING X570-PLUS (WI-FI) ($245) – RAM: Corsair Vengeance LPX 32GB (2x16GB) 3200MHz DDR4 Or Crucial Ballistix Sport LT 32GB (2x16GB) 3200 MHz DDR4 CL16 (~$200) Q#4 – Both cost almost the same, any …
```
**`hardware_ex_10543_neg_54`** (2000 ký tự)
```text
However, for video editing you do need a better processor (core i7 or Ryzen 7) and more RAM (16GB preferably). Reply Sanjay Khemka May 10, 2019 My motherboard is showing PCI e × 16 Gen 2.x = 1 Motherboard support DDR 3 a…
```
**`hardware_ex_10543_neg_60`** (1896 ký tự)
```text
https://www.newegg.com/gold-steel-asus-tuf-gaming-tuf505du-eb74-gaming-entertainment/p/N82E16834235196?Description=Asus%20tuf505du-eb74&cm_re=Asus_tuf505du-eb74-_-34-235-196-_-Product Any thoughts are appreciated. The go…
```
**`hardware_ex_13449_neg_12`** (2417 ký tự)
```text
Max system memory size Dell Latitude 7400 32 GB Dell XPS 13 9310 32 GB Specs Comparison Key Differences Availability Exterior Display Ports Internal Specs Connectivity Battery Software Camera & Audio Misc Key Features Co…
```
**`hardware_ex_13449_neg_15`** (2442 ký tự)
```text
Dell Latitude 7400 Price Dell Latitude 7400 Laptop, 14.0 inches FHD (1920 x 1080) Touchscreen, Intel Core 8th Gen i7-8665U, 16GB RAM, 256GB SSD, Windows 11 (Renewed) By Dell $264.89 See at Amazon Dell 65W USB-C Laptop Ch…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 4,016

**`hardwarerecs_ex_11349_doc_3`** (777 ký tự)
```text
Supermicro A2SDi-4C-HLN4F-O Motherboard Mini-ITX Embedded Intel Atom Processor C3558 4-Core Denverton Supports up to 256GB ECC DDR4-2133 in 4 DIMM slots 4 GbE LAN and up to 8 SATA3 ports via SoC Flexible I/O M.2 PCIe 3.0…
```
**`hardwarerecs_ex_11412_doc_4`** (1464 ký tự)
```text
I could use a remote PC via NVIDIA Gamestream and Moonlight like a gaming-enabled remote desktop. When on a trip, I could leave my heavy gaming laptop home, and connect to it with my lightweigh fanless laptop, and game o…
```
**`hardwarerecs_ex_15902_doc_1`** (905 ký tự)
```text
MacOS only allow for AMD GPU in eGPU enclosures but OSs like Windows or Linux work fine with NVIDIA. No. Because Apple only supports AMD GPU's, and doesn't make any others available to the host OS to be virtualized (it's…
```
**`hardwarerecs_ex_16133_doc_2`** (628 ký tự)
```text
Why is it so difficult to find a good MP3 player with a 3.5 mm jack output and SD card slot? I don't want to spend $4000 on something like that. I'm just looking for something to listen to music without needing Bluetooth…
```
**`hardwarerecs_ex_18350_doc_3`** (1046 ký tự)
```text
The Multi-Size M.2 NVMe to U.2 (SFF-8639) 2.5" SSD converter/adapter converts an M.2 NVMe module into a U.2 2.5" drive form factor with a thickness of 9.5mm. The casing dimension and U.2 interface are on the same locatio…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 445

**`hardwarerecs_ex_18640_doc_0`** (421 ký tự)
```text
a***k (4)- Feedback left by buyer. Past 6 months Verified purchase Seller kept in contact with me when there was an issue with the GPU, never leaving me wondering what happened. The GPU is a workhorse and handles AI task…
```
**`hardwarerecs_ex_18939_doc_1`** (1018 ký tự)
```text
iPhone SE explained If you're a thrifty consumer in the market for a second hand iPhone, you're probably aware of the iPhone Special Edition. These are more affordable iPhones which feature the body of an older model and…
```
**`hardwarerecs_ex_18939_doc_2`** (542 ký tự)
```text
iOS 26: Which iPhones are compatible with the new iOS update? iPhones from the iPhone 11, iPhone SE (second generation) and up (roughly, those released in 2017 or later) will be able to upgrade to iOS 26, which was relea…
```
**`hardwarerecs_ex_9549_doc_5`** (1162 ký tự)
```text
thank you for the excellent explanation. Not new to Ubiquiti and firewall rules but very interested in using the VLAN model you provided to segment IoT devices. I plan to deploy a Dream Machine Pro with a 16 port POE swi…
```
**`hardware_ex_10543_neg_159`** (1890 ký tự)
```text
i7 4770, Asus Z87 Pro Mobo, 32 Gb Kingston 1333mhz ram, 650W Be Quiet Dark Power Pro , Samsung 850 Pro SSD. No GPU. Is it beneficial if i would do only a small (second hand) upgrade and buy a z97 mobo and put an m2 ssd (…
```

### ✅ Trùng chính xác
- Không phát hiện.

### ❌ Gần trùng (khác nhau chút ít) — 94

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*

- cụm size 11: `hardware_ex_9102_google_neg_186`, `hardware_ex_9102_google_neg_187`, `hardware_ex_9102_google_neg_188`, `hardware_ex_9102_google_neg_189`, `hardware_ex_9102_google_neg_191`
  - `hardware_ex_9102_google_neg_186`:
```text
Below is a listing of all our reviews, roundups and evaluations published in 2023.
```
  - `hardware_ex_9102_google_neg_187`:
```text
Below is a listing of all our reviews, roundups and evaluations published in 2022.
```
- cụm size 3: `hardware_ex_18640_neg_0`, `hardware_ex_8476_neg_0`, `hardware_ex_8476_neg_2`
  - `hardware_ex_18640_neg_0`:
```text
cache:https://www.jawa.gg/product/93414/nvidia-p102-100-mn102p-2sdn-p6d-10-gb-mining-gpu-gtx-1080-ti-equivalent - Google Suche Links zur Barrierefreiheit Zu den Hauptinhalten springen Hilfe zur Barrierefreiheit Feedback …
```
  - `hardware_ex_8476_neg_0`:
```text
cache:https://www.dell.com/community/Storage-Drives-Media/How-to-setup-Dell-Inspiron-7720-such-that-the-mSATA-speed-is/td-p/4229943 - Google Suche Links zur Barrierefreiheit Zu den Hauptinhalten springen Hilfe zur Barrie…
```
- cụm size 3: `hardware_ex_18576_google_neg_101`, `hardware_ex_18576_google_neg_96`, `hardware_ex_18576_google_neg_97`
  - `hardware_ex_18576_google_neg_101`:
```text
The VMware virtual machine is great for those occasions where SBC performance just isn't enough. Run one of these on any x86_64 PC/server and still get the same great DietPi features and experience.
```
  - `hardware_ex_18576_google_neg_96`:
```text
The Hyper-V virtual machine is great for those occasions where SBC performance just isn't enough. Run one of these on any x86_64 PC/server and still get the same great DietPi features and experience.
```
- cụm size 3: `hardware_ex_19043_google_neg_781`, `hardware_ex_19043_google_neg_796`, `hardware_ex_19043_google_neg_804`
  - `hardware_ex_19043_google_neg_781`:
```text
Tableau Prep is Unicode-enabled and compatible with data stored in any language. The user interface and supporting documentation are in English (US), English (UK), French (France), French (Canada), German, Italian, Spani…
```
  - `hardware_ex_19043_google_neg_796`:
```text
Tableau Mobile is Unicode-enabled and compatible with data stored in any language. The user interface and supporting documentation are in English (US), English (UK), French (France), French (Canada), German, Italian, Spa…
```
- cụm size 2: `hardwarerecs_ex_15312_doc_1`, `hardware_ex_15312_neg_2`
  - `hardwarerecs_ex_15312_doc_1`:
```text
If you're a PC gamer, you likely use a discrete graphics card. Even if it's not one of the very best graphics cards, a modern discrete GPU should perform much better than any integrated graphics. And if you're using inte…
```
  - `hardware_ex_15312_neg_2`:
```text
Intel K vs KF for Gaming If you’re a PC gamer, you likely use a discrete graphics card. Even if it’s not one of the very best graphics cards , a modern discrete GPU should perform much better than any integrated graphics…
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

- `ex_18337_turn_1`: For home office printers, is it easy to connect both with a cable and over WiFi for more flexibility?
- `ex_15078_turn_1`: In laptop RAM upgrades, is it okay to mix different brands or speeds, or should I match my current module for best results?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 17

- `ex_19234_turn_3`: Would it just be easier to get a selfie stick that's made for Android phones instead of messing with adapters?
- `ex_18640_turn_4`: How easy is it to actually find one of these cards for under $100?
- `ex_18337_turn_4`: Is it quick enough to do at least 23 pages a minute in both color and black?
- `ex_15902_turn_2`: Is that extra power from the eGPU actually noticeable for CADD stuff in the VM, or does Fusion kind of bottleneck it?
- `ex_15430_turn_2`: Is it easier to set up the system with the 5600G before I get a graphics card?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 4

- `ex_19103_turn_3`: And having an app—does that actually make it easier to track your weight or spot changes over time?
- `ex_18337_turn_2`: Oh, and does it let you print straight from your phone, like with AirPrint or Bluetooth?
- `ex_18337_turn_3`: Oh, does it come with an automatic feeder for scanning a bunch of pages at once, and can it scan both sides?
- `ex_11412_turn_4`: Oh, and can you actually stream stuff like emulators or VR games through Steam, or does it only work with regular PC games?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 10

- `ex_19103_turn_3` (cos=0.0)
  - trước: What happens if the scale’s feet aren’t all on the same tile—does that throw things off too?
  - sau: And having an app—does that actually make it easier to track your weight or spot changes over time?
- `ex_18978_turn_2` (cos=0.0)
  - trước: In choosing a laptop for Linux, how many external monitors can you realistically run at once, and are there GPU issues t…
  - sau: Do you actually need adapters for both screens, or does it come with enough ports built in?
- `ex_18978_turn_3` (cos=0.0)
  - trước: Do you actually need adapters for both screens, or does it come with enough ports built in?
  - sau: Have you heard if the T480 plays nice with Linux when you’re plugging in two monitors?
- `ex_18337_turn_2` (cos=0.0)
  - trước: For home office printers, is it easy to connect both with a cable and over WiFi for more flexibility?
  - sau: Oh, and does it let you print straight from your phone, like with AirPrint or Bluetooth?
- `ex_17938_turn_2` (cos=0.0)
  - trước: Regarding old computers, how much faster would everyday tasks and light video editing feel if I swapped the hard drive f…
  - sau: Do you think bumping the RAM up to 16GB would actually stop it from freezing like that?

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

- `hardwarerecs_ex_9583_doc_3` ['non_english']
```text
DHCP | • DHCP Server• DHCPv6 PD Server (only in Standalone Mode) • DHCP Options Customization• DHCP Address Reservation• Multi-IP Interfaces• Multi-Net DHCP NAT | • One-to-One NAT• Multi-Net NAT• Port…
```

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 1

- `ex_15078_turn_3` (pronoun) gold=['hardwarerecs_ex_15078_doc_1']: Is there an easy way to tell which way the RAM stick should go in, or could I mess that up?

### ✅ Bằng chứng nằm muộn (> 1500 ký tự)
- Không phát hiện.

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 4

- `ex_17938_turn_3` OOV=['xubuntu']: Would something like Xubuntu or another lightweight Linux run better on that old hardware, even with more RAM?
- `ex_15902_turn_1` OOV=['cadd']: In using an eGPU with VMware Fusion, does turning on 'Prefer External GPU' actually help with CADD software performance in a Windows VM?
- `ex_15902_turn_2` OOV=['cadd']: Is that extra power from the eGPU actually noticeable for CADD stuff in the VM, or does Fusion kind of bottleneck it?
- `ex_15902_turn_3` OOV=['cadd']: Do you have to plug in the eGPU before starting up the VM for it to actually help with CADD work?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 7

*nguyên nhân: {'lexical_gap (overlap<0.2)': 6, 'context_dependent': 1}*

- `ex_15078_turn_3` ti=2 ctx=pronoun overlap=0.0: Is there an easy way to tell which way the RAM stick should go in, or could I mess that up?
  - gold ['hardwarerecs_ex_15078_doc_1'] | top3 ['hardware_ex_10543_neg_122', 'hardware_ex_19220_google_neg_391', 'hardwarerecs_ex_17938_doc_3']
- `ex_15078_turn_7` ti=6 ctx=pronoun overlap=0.067: Would bumping it up to 32 GB actually speed things up a lot with heavy apps, especially since mine has an AMD chip?
  - gold ['hardwarerecs_ex_15078_doc_2'] | top3 ['hardware_ex_19167_google_neg_185', 'hardwarerecs_ex_13449_doc_0', 'hardware_ex_16177_google_neg_270']
- `ex_15430_turn_4` ti=3 ctx=standalone overlap=0.071: Can you actually run extra monitors off the 5600G’s graphics once you add a GPU, or does it switch over completely?
  - gold ['hardwarerecs_ex_15430_doc_1'] | top3 ['hardwarerecs_ex_15430_doc_2', 'hardwarerecs_ex_15430_doc_4', 'hardware_ex_19156_google_neg_405']
- `ex_15078_turn_9` ti=8 ctx=pronoun overlap=0.083: Is it a big deal if the voltage on the new RAM isn’t exactly the same as my current one?
  - gold ['hardwarerecs_ex_15078_doc_3'] | top3 ['hardware_ex_8728_google_neg_480', 'hardware_ex_9549_neg_16', 'hardwarerecs_ex_17938_doc_0']
- `ex_19043_turn_1` ti=0 ctx=standalone overlap=0.154: In planning a CPU and motherboard upgrade, what features should I check to make sure everything works well and is future-proof?
  - gold ['hardwarerecs_ex_19043_doc_3'] | top3 ['hardware_ex_18880_google_neg_373', 'hardware_ex_19167_google_neg_405', 'hardwarerecs_ex_15078_doc_0']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.