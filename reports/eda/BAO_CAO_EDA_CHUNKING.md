# BÁO CÁO TỔNG KẾT EDA & CHUNKING
## RETECO – TRACK 2 | Phiên bản v3

**Ngày tạo:** 14/11/2026  
**Phạm vi:** 11 domain, 507.141 tài liệu  
**Nguồn số liệu:** `eda_summary_all.md`, `visualization_report.md`, `eda_metrics_*.json`

---

## 1. Mục tiêu thực nghiệm

Trong Retrieval Track 2, hệ thống cần tìm đúng tài liệu dựa trên câu hỏi của người dùng, kể cả khi cuộc hội thoại có nhiều lượt.

Trước khi tìm kiếm, tài liệu thường được chia thành những đoạn nhỏ gọi là *chunk*. Cách chia ảnh hưởng trực tiếp đến chất lượng retrieval:

- Chunk quá nhỏ có thể làm mất ngữ cảnh, khiến câu hoặc đại từ không còn ý nghĩa khi đứng riêng.
- Chunk quá lớn có thể chứa quá nhiều nội dung và vượt giới hạn token của mô hình embedding.
- Cách chia không phù hợp có thể làm vỡ từ khóa hoặc cấu trúc mà BM25 cần để tìm kiếm.

**Mục tiêu của thực nghiệm** là tìm chiến lược chunking phù hợp cho từng domain, thay vì mặc định sử dụng một cấu hình duy nhất cho toàn bộ dữ liệu.

### Phạm vi

- 11 domain: biology, drones, earth_science, economics, hardware, law, medicalsciences, politics, psychology, robotics và sustainable_living.
- Tổng cộng **507.141 tài liệu**.
- 9 chiến lược chunking chính và 12 biến thể tinh chỉnh tham số, tổng cộng 21 cấu hình.
- Đánh giá retrieval bằng BM25 trên corpus thử nghiệm gồm gold documents và khoảng 10.000 distractor documents.

---

## 2. Dữ liệu và cách xử lý

### 2.1. Cấu trúc dữ liệu đầu vào

Mỗi domain có ba thành phần chính:

| Tệp | Nội dung |
|---|---|
| `documents.jsonl` | Danh sách tài liệu, gồm document ID, nội dung và tiêu đề |
| `benchmark_dev.json` | Các cuộc hội thoại dùng cho tập phát triển, bao gồm query và gold document IDs |
| `qrels_dev.txt` | Nhãn liên quan của tài liệu theo định dạng TREC |

### 2.2. Cách đọc dữ liệu

Vì corpus có hơn 507.000 tài liệu, việc nạp toàn bộ dữ liệu vào RAM có thể tiêu tốn nhiều bộ nhớ. Thay vào đó, thực nghiệm sử dụng quy trình sau:

1. **Streaming:** Đọc lần lượt từng dòng để thống kê toàn bộ tài liệu, bao gồm Median, P90 và P99.
2. **Reservoir sampling:** Lấy mẫu ngẫu nhiên 2.000 tài liệu để đánh giá chất lượng chunk.
3. **Ưu tiên gold documents:** Giữ lại toàn bộ tài liệu được đánh dấu là gold để bảo đảm quá trình đo retrieval có đủ tài liệu mục tiêu.

Cách làm này giúp thống kê độ dài trên toàn bộ corpus mà không cần nạp tất cả tài liệu vào RAM. Phần lấy mẫu được dùng cho các bước đánh giá cần kiểm tra nội dung chunk.

---

## 3. Các chiến lược chunking được thử nghiệm

Thực nghiệm sử dụng 9 chiến lược chính. Có thể hiểu chúng qua cách chúng quyết định vị trí cắt văn bản.

| Chiến lược | Cách hoạt động | Ưu điểm | Hạn chế |
|---|---|---|---|
| **Fixed Character** | Cắt theo số ký tự cố định | Đơn giản, nhanh | Có thể cắt giữa từ hoặc câu |
| **Fixed Word** | Cắt theo số từ cố định | Không cắt giữa từ | Có thể cắt ngang câu |
| **Sentence Boundary** | Cắt tại ranh giới câu | Giữ nguyên câu | Có thể chia nhỏ tài liệu ngắn |
| **Recursive Markdown** | Ưu tiên chia theo đoạn, dòng, câu rồi đến từ | Tôn trọng cấu trúc văn bản | Chunk sau có thể thiếu tên thực thể hoặc ngữ cảnh trước đó |
| **Semantic Context** | Kết hợp Recursive Chunking và prefix ngữ cảnh | Hạn chế chunk bị mất ngữ cảnh | Prefix lặp có thể tạo nội dung gần trùng lặp |
| **Whole Document** | Giữ nguyên tài liệu, không chia | Giữ được ngữ cảnh đầy đủ | Có nguy cơ vượt giới hạn token |
| **Parent-Child** | Tạo các chunk con nhỏ để truy hồi | Có thể tìm trúng đoạn cụ thể | Chunk con quá ngắn dễ mất ngữ cảnh |
| **Sentence Window** | Tạo cửa sổ gồm nhiều câu có phần chồng lấn | Giữ thêm ngữ cảnh xung quanh | Không nhất thiết tuân theo ranh giới đoạn |
| **TextTiling** | Cắt tại các điểm chuyển chủ đề | Có khả năng chia theo mạch nội dung | Nhạy với nhiễu khi văn bản ngắn |

### 3.1. Các tham số mặc định

| Chiến lược | Cấu hình mặc định |
|---|---|
| Fixed Character | `size=500`, `overlap=50` |
| Fixed Word | `words=120`, `overlap=20` |
| Sentence Boundary | `max_words=140`, overlap 1 câu |
| Recursive Markdown | `max_chars=650`, `min_chars=150` |
| Semantic Context | `threshold=800`, `max_chars=650` |
| Whole Document | Không chia |
| Parent-Child | `child_words=60` |
| Sentence Window | `window=4`, `stride=2` |
| TextTiling | `block=3`, `k=0.5` |

### 3.2. Các biến thể tinh chỉnh

Ngoài cấu hình mặc định, thực nghiệm thay đổi một số tham số để kiểm tra liệu kích thước chunk khác có đem lại kết quả tốt hơn hay không.

| Nhóm | Các biến thể được thử |
|---|---|
| Fixed Character | Kích thước 300 và 900 ký tự |
| Sentence Boundary | Tối đa 80 và 220 từ |
| Recursive Markdown | Tối đa 450, 1.000 và 250 ký tự |
| Semantic Context | Threshold 1.200 và 500; thêm biến thể prefix cho mọi chunk; thêm cấu hình Adaptive Hybrid |
| Sentence Window | Window 6, stride 3 |

Như vậy, tổng cộng có 9 chiến lược gốc và 12 biến thể tham số.

---

## 4. Phương pháp đánh giá

Để lựa chọn chiến lược phù hợp, thực nghiệm xem xét ba khía cạnh: chất lượng bản thân chunk, hiệu quả tìm kiếm và chi phí phát sinh khi lập chỉ mục.

### 4.1. Chất lượng chunk

Mỗi chunk bắt đầu với 100 điểm. Điểm sẽ bị trừ nếu phát hiện các vấn đề sau:

| Lỗi | Điểm trừ | Ý nghĩa |
|---|---:|---|
| `starts_mid_sentence` | -25 | Chunk bắt đầu ở giữa câu |
| `ends_mid_sentence` | -20 | Chunk kết thúc ở giữa câu |
| `dangling_pronoun_unresolved` | -30 | Chunk bắt đầu bằng đại từ như “it”, “this”, “they” nhưng không có prefix giải thích |
| `dangling_pronoun_mitigated_by_prefix` | -8 | Chunk vẫn bắt đầu bằng đại từ nhưng đã có prefix chủ đề (từ 3 từ trở lên) bổ sung |
| `starts_with_connector` | -10 | Chunk bắt đầu bằng từ nối (ví dụ “however”, “and”), tức là tiếp nối ý của chunk trước |
| `trailing_heading_orphan` | -15 | Chunk kết thúc bằng một heading ngắn, không có nội dung đi kèm |
| `undersized` | -25 | Chunk ngắn hơn 80 ký tự, trừ trường hợp whole document |
| `over_embedding_token_limit` | -20 | Chunk vượt giới hạn 512 token theo ước lượng |
| `oversized_chars` | -10 | Chunk dài hơn 1.500 ký tự nhưng chưa vượt 512 token (không cộng dồn với lỗi vượt token) |

Công thức tính:

```text
Quality = max(0, 100 - tổng điểm bị trừ)
```

Việc kiểm tra vị trí chunk dựa trên offset trong văn bản gốc, thay vì suy đoán dựa vào chữ hoa hoặc chữ thường. Nhờ đó, hệ thống có thể kiểm tra chính xác ký tự đứng trước và sau mỗi chunk.

### 4.2. Hiệu quả retrieval

Retrieval được đánh giá bằng BM25 thuần Python trên corpus thử nghiệm gồm:

- Các gold documents được xác định từ qrels.
- Khoảng 10.000 distractor documents được lấy từ corpus.

Ba cách tạo query được so sánh:

| Chế độ | Nội dung query | Mục đích |
|---|---|---|
| **Single** | Chỉ câu hỏi hiện tại | Làm baseline khi không sử dụng lịch sử hội thoại |
| **History** | Lịch sử hội thoại kết hợp câu hỏi hiện tại | Đánh giá lợi ích của ngữ cảnh hội thoại |
| **Random Padded** | Câu hỏi hiện tại cộng thêm số từ ngẫu nhiên tương đương độ dài history | Kiểm tra ảnh hưởng đơn thuần của việc query dài hơn |

Các chỉ số retrieval được sử dụng gồm:

- **nDCG@10:** Đánh giá chất lượng thứ tự xếp hạng của 10 kết quả đầu.
- **Recall@10:** Đánh giá khả năng tìm được tài liệu liên quan trong 10 kết quả đầu.
- **MRR@10:** Đánh giá vị trí xuất hiện của kết quả liên quan đầu tiên.

### 4.3. Vì sao cần Random Padded?

Khi nối lịch sử hội thoại vào query, câu truy vấn sẽ dài hơn. Vì vậy, nếu chỉ so sánh Single và History, chúng ta chưa thể khẳng định kết quả tốt hơn là nhờ ngữ nghĩa hay chỉ vì query có thêm từ.

Random Padded được dùng làm baseline kiểm soát vấn đề này.

Ví dụ minh họa (câu hỏi chỉ để dễ hình dung; các con số nDCG là **trung bình của chiến lược Sentence Boundary trên 11 domain**, không phải điểm của riêng một câu hỏi):

| Chế độ | Ví dụ query | nDCG |
|---|---|---:|
| Single | “How does it fly?” | 0.2599 |
| History | “What is a drone? How does it fly?” | 0.3714 |
| Random Padded | Câu hỏi ban đầu cộng thêm các từ ngẫu nhiên | 0.2364 |

Chênh lệch ngữ nghĩa được tính bằng:

```text
Δ Semantic = nDCG(History) - nDCG(Random Padded)
           = 0.3714 - 0.2364
           = +0.1350
```

History cho kết quả cao hơn rõ rệt so với Random Padded. Điều này cho thấy phần lịch sử hội thoại cung cấp thông tin có ích cho truy vấn, thay vì chỉ làm query dài hơn.

### 4.4. Composite Score

Để kết hợp các tiêu chí thành một điểm tổng hợp, báo cáo sử dụng Composite Score v3.

**Bước 1 – Chuẩn hóa min-max trong từng domain**

```text
v_norm = (v - min) / (max - min)
```

Việc chuẩn hóa được thực hiện riêng trong từng domain cho các thành phần nDCG hiệu dụng, Recall, Quality và Cost.

Lý do là các chỉ số có thang điểm và mức biến thiên khác nhau. Nếu không chuẩn hóa, chỉ số có phạm vi lớn hơn có thể chi phối điểm tổng hợp.

**Bước 2 – Tính điểm Cost**

```text
Cost = 1 / (1 + ln(expansion_ratio))
```

Trong đó `expansion_ratio` thể hiện mức độ dữ liệu tăng lên sau khi chunking.

Ví dụ:

| Expansion ratio | Cost |
|---:|---:|
| 1x | 1.00 |
| 2x | 0.59 |
| 4x | 0.42 |

Expansion càng lớn thì điểm Cost càng thấp.

**Bước 3 – Tính nDCG hiệu dụng**

```text
nDCG_eff = nDCG_single + max(0, Δ Semantic)

Δ Semantic = nDCG_history - nDCG_random_padded
```

Chỉ phần lợi ích ngữ nghĩa dương được cộng thêm vào nDCG Single.

**Bước 4 – Tính điểm tổng hợp trước khi phạt**

```text
Base = 0.45 × nDCG_eff
     + 0.20 × Recall
     + 0.25 × Quality
     + 0.10 × Cost
```

**Bước 5 – Áp dụng Truncation Penalty**

Truncation Penalty được dùng để giảm điểm của chiến lược tạo ra quá nhiều chunk vượt giới hạn 512 token.

| Tỷ lệ chunk vượt giới hạn | Mức phạt |
|---|---:|
| ≤ 5% | 0% |
| Từ trên 5% đến 25% | Tăng tuyến tính từ 0% đến 40% |
| > 25% | 40% |

Công thức cuối cùng:

```text
Composite = Base × (1 - penalty)
```

**Lưu ý:** Composite Score được chuẩn hóa trong từng domain. Vì vậy, chỉ nên dùng điểm này để so sánh các chiến lược trong cùng một domain, không dùng để kết luận domain nào tốt hơn domain khác.

### 4.5. Các ngưỡng cấu hình quan trọng

| Tham số | Giá trị | Ý nghĩa |
|---|---:|---|
| `EMBED_TOKEN_LIMIT` | 512 | Giới hạn token embedding |
| `TOKEN_PER_WORD` | 1.35 | Hệ số ước lượng token trên mỗi từ |
| `UNDERSIZED_CHARS` | 80 | Ngưỡng chunk quá ngắn |
| Trọng số nDCG | 0.45 | Tỷ trọng trong Composite |
| Trọng số Recall | 0.20 | Tỷ trọng trong Composite |
| Trọng số Quality | 0.25 | Tỷ trọng trong Composite |
| Trọng số Cost | 0.10 | Tỷ trọng trong Composite |
| `TRUNC_PENALTY_START` | 5% | Ngưỡng bắt đầu phạt |
| `TRUNC_PENALTY_MAX` | 0.40 | Mức phạt tối đa |
| `MIN_VOCAB_FOR_PAD` | 500 | Ngưỡng vocab tối thiểu để bật Random Padded |

---

## 5. Kết quả thực nghiệm

### 5.1. Tổng quan corpus

Thực nghiệm được tiến hành trên 507.141 tài liệu thuộc 11 domain.

| Chỉ số | Kết quả |
|---|---:|
| Tổng số tài liệu | **507.141** |
| Median ký tự trung bình của 11 domain | **418,5** |
| Domain có Median thấp nhất | Robotics – 81 ký tự |
| Domain có Median cao nhất | Politics – 934 ký tự |
| Số domain có P90 > 1.500 ký tự | 5/11 |
| Số domain có P90 ≤ 1.500 ký tự | 6/11 |

Median cho biết độ dài nằm ở giữa phân phối tài liệu. Tuy nhiên, chỉ nhìn Median là chưa đủ: hai domain có Median gần nhau vẫn có thể có phân phối độ dài và cấu trúc nội dung rất khác nhau.

### 5.2. Chiến lược tốt nhất theo từng domain

Bảng dưới đây tổng hợp chiến lược có Composite Score cao nhất trong từng domain.

| Domain | Số tài liệu | Median | Tỷ lệ tài liệu ≤ 800 ký tự | Chiến lược tốt nhất | Composite |
|---|---:|---:|---:|---|---:|
| Biology | 57.359 | 309 | 99,48% | `4_Recursive_Markdown` | 0.9598 |
| Drones | 16.381 | 537 | 64,01% | `6_Whole_Document` | 0.9334 |
| Earth Science | 121.249 | 278 | 99,46% | `3_Sentence_Boundary` | 0.9280 |
| Economics | 50.220 | 120 | 88,56% | `5b_Semantic_thr1200_max900` | 0.9104 |
| Hardware | 26.308 | 469 | 67,72% | `6_Whole_Document` | **0.9914** |
| Law | 20.027 | 791 | 50,44% | `5b_Semantic_thr1200_max900` | 0.9046 |
| Medical Sciences | 23.297 | 830 | 48,85% | `4c_Recursive_1000` | 0.9506 |
| Politics | 16.712 | 934 | 45,38% | `3c_Sentence_220w` | 0.9619 |
| Psychology | 52.835 | 130 | 90,34% | `4c_Recursive_1000` | 0.9286 |
| Robotics | 61.961 | 81 | 90,53% | `5d_Semantic_prefix_all` | 0.9524 |
| Sustainable Living | 60.792 | 125 | 88,99% | `6_Whole_Document` | 0.9210 |

Có thể thấy không có một phương pháp nào chiến thắng ở tất cả domain. Ngay cả những domain có độ dài tài liệu tương tự nhau cũng có thể cần cách chia khác nhau.

### 5.3. Tần suất chiến lược chiến thắng

| Chiến lược | Số domain chiến thắng | Tỷ lệ | Domain |
|---|---:|---:|---|
| `6_Whole_Document` | 3 | 27,3% | Drones, Hardware, Sustainable Living |
| `5b_Semantic_thr1200_max900` | 2 | 18,2% | Economics, Law |
| `4c_Recursive_1000` | 2 | 18,2% | Medical Sciences, Psychology |
| `4_Recursive_Markdown` | 1 | 9,1% | Biology |
| `3_Sentence_Boundary` | 1 | 9,1% | Earth Science |
| `3c_Sentence_220w` | 1 | 9,1% | Politics |
| `5d_Semantic_prefix_all` | 1 | 9,1% | Robotics |

Ba nhận xét chính:

1. **Không có chiến lược vạn năng:** Có 7 cấu hình khác nhau chiến thắng trên 11 domain.
2. **Tham số mặc định chưa tối ưu:** 6/11 domain chiến thắng nhờ các biến thể đã tinh chỉnh tham số (Economics, Law, Medical Sciences, Politics, Psychology, Robotics). 5/11 domain còn lại thắng bằng chiến lược gốc (Biology, Drones, Earth Science, Hardware, Sustainable Living).
3. **Adaptive Hybrid chưa đạt kỳ vọng:** `5e_Adaptive_Hybrid` không chiến thắng domain nào trong phiên bản thực nghiệm v3.

### 5.4. Kết quả kiểm soát Length Bias

Đây là một trong những phát hiện quan trọng nhất của thực nghiệm.

Kết quả nDCG@10 trung bình trên 11 domain:

| Chế độ | nDCG@10 | So với Single |
|---|---:|---:|
| Single | 0.2554 | Baseline |
| History | 0.3545 | Tăng 38,8% |
| Random Padded | 0.2330 | Thấp hơn Single |

Chênh lệch ngữ nghĩa:

```text
Δ Semantic = 0.3545 - 0.2330
           = +0.1215
```

Diễn giải:

- Nếu History chỉ giúp tăng độ dài query, kết quả History và Random Padded được kỳ vọng sẽ gần nhau.
- Nhưng thực tế, History đạt 0.3545, cao hơn đáng kể so với Random Padded ở mức 0.2330.
- Vì vậy, phần lịch sử hội thoại có đóng góp ngữ nghĩa thực sự cho quá trình truy xuất.

Kết quả này cung cấp căn cứ định lượng để tiếp tục phát triển **Query Rewriter**, tức thành phần sử dụng ngữ cảnh hội thoại để viết lại câu truy vấn rõ ràng và đầy đủ hơn.

### 5.5. So sánh hiệu quả của một số chiến lược chính

| Chiến lược | nDCG Single | nDCG History | Δ Semantic | nDCG hiệu dụng |
|---|---:|---:|---:|---:|
| Sentence Boundary | 0.2599 | 0.3714 | +0.1350 | **0.3949** |
| Semantic Context | 0.2708 | 0.3644 | +0.1150 | 0.3857 |
| Recursive Markdown | 0.2684 | 0.3574 | +0.1123 | 0.3808 |
| Whole Document | 0.2323 | 0.3546 | **+0.1435** | 0.3758 |
| Parent-Child | 0.2562 | 0.3446 | +0.1075 | 0.3637 |

Những điểm đáng chú ý:

- **Sentence Boundary** có nDCG hiệu dụng cao nhất trong nhóm chiến lược được so sánh.
- **Whole Document** có mức tăng ngữ nghĩa từ History cao nhất, với Δ Semantic = +0.1435.
- **Parent-Child** có nDCG hiệu dụng thấp nhất trong nhóm này. Một khả năng được nêu trong báo cáo là chunk con 60 từ quá ngắn và làm mất ngữ cảnh.

Cần phân biệt hai kết quả: chiến lược có nDCG hiệu dụng cao nhất trên bảng so sánh tổng thể không nhất thiết là chiến lược có Composite Score cao nhất ở mọi domain.

---

## 6. Phân tích và quy luật theo độ dài tài liệu

### 6.1. Cấu hình phù hợp theo nhóm domain

| Nhóm | Domain đại diện | Chiến lược/cấu hình tốt | Gợi ý |
|---|---|---|---|
| Rất ngắn | Robotics – Median 81 | Semantic Context + Prefix All | Bổ sung prefix cho cả chunk đầu |
| Ngắn | Economics – 120; Psychology – 130 | Semantic threshold 1.200 hoặc Recursive max 1.000 | Giữ chunk lớn, tránh chia vụn |
| Trung bình | Drones – 537; Hardware – 469 | Whole Document | Giữ nguyên nếu không gây truncation |
| Trung bình, có cấu trúc | Biology – 309 | Recursive Markdown | Tôn trọng cấu trúc đoạn và tiêu đề |
| Trung bình, ít cấu trúc | Earth Science – 278 | Sentence Boundary | Chia theo ranh giới câu |
| Dài | Law – 791; Medical Sciences – 830 | Semantic hoặc Recursive với tham số lớn | Tăng kích thước chunk |
| Rất dài | Politics – 934 | Sentence Boundary, 220 từ | Cho phép mỗi chunk chứa nhiều câu hơn |

Đây là các cấu hình rút ra từ những domain đã thử nghiệm, không phải quy tắc chắc chắn đúng cho mọi bộ dữ liệu mới.

### 6.2. Quy luật về kích thước chunk

Từ ba domain dài có chiến lược chiến thắng sử dụng tham số lớn, báo cáo rút ra một quy luật tham khảo:

```text
max_chunk_size ≈ median_document_length × 1.0–1.5
```

Kiểm tra trên các domain:

| Domain | Median | Cấu hình thắng | Kích thước tối đa | Tỷ lệ so với Median |
|---|---:|---|---:|---:|
| Politics | 934 ký tự | Sentence 220 từ | Khoảng 1.320 ký tự | 1,41x |
| Medical Sciences | 830 ký tự | Recursive 1.000 | 1.000 ký tự | 1,20x |
| Law | 791 ký tự | Semantic 1.200 | 1.200 ký tự | 1,52x |

Điều này gợi ý rằng với domain dài, việc tăng kích thước chunk có thể giúp giữ được nhiều ngữ cảnh hơn. Tuy nhiên, cần kiểm tra thêm tỷ lệ vượt giới hạn token để tránh tạo ra chunk quá lớn.

### 6.3. Vì sao các domain ngắn có kết quả khác nhau?

Economics, Psychology và Sustainable Living có Median khá gần nhau, lần lượt là 120, 130 và 125 ký tự. Tuy nhiên, chiến lược tốt nhất của chúng lại khác nhau:

- **Economics:** Semantic Context với threshold 1.200. Median thấp nhưng vẫn có một phần tài liệu dài hơn đáng kể.
- **Psychology:** Recursive với max 1.000, phù hợp với đặc điểm cấu trúc đoạn được ghi nhận trong báo cáo.
- **Sustainable Living:** Whole Document, do phân phối độ dài được mô tả là có P90 thấp và ít tài liệu ở đuôi dài.

Điều này cho thấy Median không thể đại diện cho toàn bộ phân phối độ dài. Khi lựa chọn chunking, cần xem thêm P90 và cấu trúc tài liệu.

---

## 7. Giới hạn của thực nghiệm

### 7.1. Những gì kết quả hiện tại hỗ trợ

- So sánh các chiến lược chunking trong cùng một domain bằng Composite đã chuẩn hóa nội domain.
- Đánh giá chất lượng chunk dựa trên offset thực tế trong văn bản.
- Kiểm tra lợi ích của History có đối chứng Random Padded để hạn chế ảnh hưởng của độ dài query.

### 7.2. Những gì chưa được kiểm chứng đầy đủ

1. **Chỉ sử dụng BM25:** Chưa đánh giá đầy đủ với dense retriever như BGE hoặc E5.
2. **Token mới được ước lượng:** Số token được tính gần đúng bằng số từ nhân 1,35, chưa đo bằng tokenizer thật của model embedding.
3. **Corpus retrieval còn giới hạn:** Tập thử nghiệm sử dụng khoảng 10.000 distractor documents, chưa phải toàn bộ corpus.
4. **Chưa đánh giá chất lượng câu trả lời cuối:** Chưa đo trực tiếp ảnh hưởng của chunking đến chất lượng câu trả lời do LLM tạo ra trong Track 2b/2c.
5. **Composite chỉ có ý nghĩa nội domain:** Không thể dùng điểm Composite để xếp hạng chất lượng giữa các domain khác nhau.

### 7.3. Các bước cần xác minh trước production

- Chạy lại với dense retriever thực tế, chẳng hạn BGE-M3 hoặc Contriever.
- Đo số token bằng tokenizer thật của mô hình embedding.
- Mở rộng corpus retrieval lên khoảng 20–50% corpus thực tế.
- Kiểm tra trực quan khoảng 20–30 chunk có chất lượng thấp nhất của mỗi chiến lược thông qua các file `chunk_inspection_*.md`.

---

## 8. Kết luận và đề xuất triển khai

### 8.1. Ba kết luận chính

**1. Không có chiến lược chunking phù hợp cho mọi domain.**  
Có 7 cấu hình khác nhau chiến thắng trên 11 domain. Vì vậy, việc lựa chọn cần dựa trên đặc điểm của từng nhóm dữ liệu.

**2. History mang lại lợi ích ngữ nghĩa cho retrieval.**  
nDCG@10 tăng từ 0.2554 lên 0.3545 khi sử dụng History. Sau khi đối chiếu với Random Padded, Δ Semantic đạt +0.1215. Đây là căn cứ để phát triển Query Rewriter.

**3. Tham số mặc định chưa tối ưu.**  
Có 6/11 domain đạt kết quả tốt nhất với các biến thể đã tinh chỉnh. Do đó, hệ thống nên có khả năng điều chỉnh tham số theo đặc điểm domain.

### 8.2. Hướng lựa chọn chunking

Kết quả v3 không ủng hộ việc mặc định sử dụng `5e_Adaptive_Hybrid`, vì cấu hình này không chiến thắng domain nào.

Thay vào đó, có thể triển khai quy trình lựa chọn dựa trên thống kê của domain:

1. Tính Median và P90 của độ dài tài liệu.
2. Xác định đặc điểm cấu trúc văn bản.
3. Chọn một số chiến lược phù hợp để thử nghiệm.
4. Tinh chỉnh kích thước chunk và threshold.
5. Kiểm tra Quality, retrieval metrics và tỷ lệ vượt 512 token.
6. Chọn cấu hình có kết quả tốt nhất trong domain đó.

Ví dụ logic tham khảo:

```python
def adaptive_chunking(doc_text, doc_median):
    length = len(doc_text)

    if doc_median <= 100:
        return semantic_context(
            doc_text,
            threshold=800,
            max_chars=650,
            prefix_all=True
        )

    elif doc_median <= 200:
        if length > 1000:
            return recursive_structure(
                doc_text,
                max_chars=1000
            )
        return whole_document(doc_text)

    elif doc_median <= 550:
        if length <= 800:
            return whole_document(doc_text)
        return recursive_structure(
            doc_text,
            max_chars=650
        )

    else:
        return semantic_context(
            doc_text,
            threshold=1200,
            max_chars=900
        )
```

Đây là logic minh họa dựa trên kết quả thực nghiệm, cần được kiểm thử thêm trước khi sử dụng chính thức. Đặc biệt, báo cáo hiện tại chưa xác lập một nhánh riêng cho khoảng Median từ 550 đến 750 ký tự.

### 8.3. Checklist trước khi triển khai

- [ ] Phân loại domain dựa trên Median và P90.
- [ ] Tinh chỉnh `max_chunk_size` theo phân phối độ dài tài liệu.
- [ ] Kiểm tra trường hợp chunk thiếu ngữ cảnh hoặc có đại từ mồ côi.
- [ ] Bật `prefix_all=True` ở domain phù hợp, chẳng hạn Robotics.
- [ ] Kiểm tra `over_token_limit_pct`, mục tiêu dưới 5%.
- [ ] Đánh giá lại bằng dense retriever.
- [ ] Kiểm tra trực quan các chunk có điểm Quality thấp.

### 8.4. Lộ trình tiếp theo

```text
Pha 1: Preprocessing
    Đã hoàn thành
        ↓
Pha 2: Retrieval – Track 2a
    - Query Rewriter, dựa trên kết quả Δ Semantic
    - Hybrid Search: BM25 + Dense Retrieval
    - Reranker: BGE-Reranker-Large
        ↓
Pha 3: RAG – Track 2b/2c
    - Sử dụng LLM Generator
    - Truy xuất chunk từ hệ thống adaptive indexing
```

---

## 9. Bảng tra cứu nhanh

| Domain | Median | Chiến lược tốt nhất | Composite |
|---|---:|---|---:|
| Biology | 309 | `4_Recursive_Markdown` | 0.9598 |
| Drones | 537 | `6_Whole_Document` | 0.9334 |
| Earth Science | 278 | `3_Sentence_Boundary` | 0.9280 |
| Economics | 120 | `5b_Semantic_thr1200_max900` | 0.9104 |
| Hardware | 469 | `6_Whole_Document` | 0.9914 |
| Law | 791 | `5b_Semantic_thr1200_max900` | 0.9046 |
| Medical Sciences | 830 | `4c_Recursive_1000` | 0.9506 |
| Politics | 934 | `3c_Sentence_220w` | 0.9619 |
| Psychology | 130 | `4c_Recursive_1000` | 0.9286 |
| Robotics | 81 | `5d_Semantic_prefix_all` | 0.9524 |
| Sustainable Living | 125 | `6_Whole_Document` | 0.9210 |

**Tóm tắt:** Trên 507.141 tài liệu thuộc 11 domain, không có một chiến lược chunking nào chiến thắng áp đảo. Kết quả cho thấy cần lựa chọn chiến lược và tham số dựa trên độ dài, phân phối và cấu trúc của từng domain. Đồng thời, History mang lại lợi ích ngữ nghĩa có thể đo lường được cho retrieval, tạo cơ sở để phát triển Query Rewriter ở giai đoạn tiếp theo.

---

## Phụ lục: Hình ảnh nên chèn vào báo cáo

Có thể bổ sung các hình sau để người đọc dễ theo dõi kết quả:

| Vị trí đề xuất | Hình ảnh | Nội dung minh họa |
|---|---|---|
| Sau mục 5.1 | `fig1_corpus_profile_by_domain.png` | Phân phối độ dài tài liệu theo domain |
| Sau mục 5.3 | `dashboard_master_overview.png` | Tổng quan các chiến lược chiến thắng |
| Sau mục 5.4 | `fig3_retrieval_performance.png` | So sánh Single, History và Random Padded |
| Sau mục 5.5 | `fig2_chunking_semantic_integrity.png` | Chất lượng và tính toàn vẹn ngữ nghĩa của chunk |
| Sau mục 6.1 | `fig4_domain_strategy_heatmap.png` | Bản đồ chiến lược phù hợp theo domain |
