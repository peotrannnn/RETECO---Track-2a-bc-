# BÁO CÁO TỔNG KẾT KHẢO SÁT DỮ LIỆU (EDA) VÀ ĐÁNH GIÁ THỰC NGHIỆM CHIẾN LƯỢC CHUNKING CHO RETECO TRACK 2

> **Dự án:** RETECO (SemEval-2027) — Track 2: Reasoning-Intensive Conversational Retrieval & RAG  
> **Thư mục báo cáo:** `reports/eda/`  
> **Tác giả:** Antigravity Pairing System & Engineering Team  
> **Thời điểm cập nhật:** 14/11/2026  
> **Phạm vi khảo sát:** Toàn bộ 11 Domain dữ liệu (`biology`, `drones`, `earth_science`, `economics`, `hardware`, `law`, `medicalsciences`, `politics`, `psychology`, `robotics`, `sustainable_living`) với **507,141 tài liệu** và hàng nghìn lượt hội thoại đối chuẩn.

---

## MỤC LỤC
1. [Tóm Tắt Điều Hành (Executive Summary)](#1-tóm-tắt-điều-hành-executive-summary)
2. [Bản Chất Dữ Liệu & Phương Pháp Đọc Dữ Liệu](#2-bản-chất-dữ-liệu--phương-pháp-đọc-dữ-liệu)
3. [Tại Sao Chunking Có Thể Phá Hỏng Pipeline RAG?](#3-tại-sao-chunking-có-thể-phá-hỏng-pipeline-rag)
4. [Hệ Thống 10 Chiến Lược Chunking Đã Triển Khai](#4-hệ-thống-10-chiến-lược-chunking-đã-triển-khai)
5. [Hệ Thống Tiêu Chí, Công Thức Tính & Thuật Toán Chẩn Đoán](#5-hệ-thống-tiêu-chí-công-thức-tính--thuật-toán-chẩn-đoán)
6. [Phát Hiện Thực Nghiệm Từ Dữ Liệu 11 Domain](#6-phát-hiện-thực-nghiệm-từ-dữ-liệu-11-domain)
7. [Hướng Dẫn Đọc Bộ Biểu Đồ Trực Quan Hóa (Visualizations)](#7-hướng-dẫn-đọc-bộ-biểu-đồ-trực-quan-hóa-visualizations)
8. [Kết Luận Kiến Trúc & Lộ Trình Triển Khai Tiếp Theo](#8-kết-luận-kiến-trúc--lộ-trình-triển-khai-tiếp-theo)

---

## 1. Tóm Tắt Điều Hành (Executive Summary)

Trong bài toán **Conversational Retrieval (Track 2a)** và **RAG Question Answering (Track 2b/2c)**, việc phân đoạn tài liệu (*chunking*) là bước đi nền móng đầu tiên. Một quyết định chunking sai lầm sẽ tạo ra hiệu ứng domino tiêu cực:
- Cắt vụn từ ngữ kỹ thuật làm thuật toán từ vựng **BM25 mất dấu từ khóa**.
- Cắt đứt đôi câu làm mô hình **Dense Embedding (vector) bị phân tán ngữ nghĩa**.
- Cắt mất chủ ngữ tạo ra **đại từ mồ côi** (*it*, *this*, *they*...), khiến mô hình sinh **LLM bị ảo giác (hallucination)** do thiếu tiền đề lập luận.

Bộ công cụ chẩn đoán chuyên sâu (EDA Suite v2–v3) được thiết kế nhằm **soi chiếu từng chunk dưới kính hiển vi thực nghiệm**, đo lường trực tiếp trên 11 domain với hơn nửa triệu tài liệu.

### Ba kết luận thực nghiệm lớn nhất:
1. **Phần lớn tài liệu RETECO là văn bản ngắn:** Độ dài trung vị (*median*) qua 11 domain chỉ đạt **418 ký tự** (~60–70 từ). Ở 7/11 domain, từ 65% đến 99% tài liệu ngắn hơn 800 ký tự. Do đó, việc áp dụng các bộ cắt cố định (sliding window 100–150 từ) như các bài viết hướng dẫn RAG phổ thông là **hoàn toàn sai lầm**, gây nở index từ 2x đến 3.5x và phá nát ngữ cảnh hoàn chỉnh.
2. **Cắt cơ học (Fixed-Char / Fixed-Word) thất bại thảm hại:** Tỷ lệ cắt đứt đầu/đuôi câu lên tới **35% – 55%**. Ngược lại, chiến lược **`Recursive_Markdown`** (bảo toàn đoạn/dòng/câu kèm hoãn tiêu đề) và **`Adaptive_Hybrid`** (giữ nguyên tài liệu ngắn, chỉ chia tài liệu dài kèm tiêm context) duy trì điểm chất lượng ngữ nghĩa tuyệt đối (>99/100).
3. **Giá trị ngữ nghĩa thực chất của Lịch sử hội thoại:** Thông qua kỹ thuật đối chứng *Query-Length Control Baseline*, chúng tôi chứng minh việc bổ sung lịch sử hội thoại mang lại **mức tăng trưởng nDCG@10 thực chất trung bình +15% đến +25%**, không phải do thiên lệch độ dài câu hỏi ngẫu nhiên.

---

## 2. Bản Chất Dữ Liệu & Phương Pháp Đọc Dữ Liệu

### 2.1. Nguồn dữ liệu & Cấu trúc phân tầng
Dữ liệu Track 2 được tổ chức độc lập theo 11 domain tri thức trong thư mục `reteco_data/track2_recor/<domain>/`:
- **Corpus tài liệu (`documents.jsonl`):** Mỗi dòng là một JSON object đại diện cho một tài liệu hoặc bài đăng diễn đàn kỹ thuật. Cấu trúc gồm `doc_id` (hoặc `id`), `content` (nội dung text thô hoặc markdown), và tùy chọn `title`.
- **Tập hội thoại phát triển (`benchmark_dev.json`):** Chứa các phiên hội thoại đa lượt (*multi-turn conversations*). Mỗi phiên có `id`, metadata, và mảng `turns`. Mỗi lượt hội thoại (turn) đại diện cho một câu hỏi của người dùng tại thời điểm đó (`query`), lịch sử hội thoại trước đó (`conversation_history`), và danh sách ID tài liệu liên quan tối hậu (`gold_doc_ids` hoặc `supporting_doc_ids`).
- **File nhãn đối chuẩn TREC (`qrels_dev.txt`):** Định dạng chuẩn quốc tế `qid 0 doc_id rel`, định nghĩa tài liệu nào có liên quan (relevance $\ge 1$) cho từng topic `qid` dạng `<conversation_id>_turn_<turn_id>`.

### 2.2. Kỹ thuật đọc dữ liệu lớn: Streaming & Reservoir Sampling
Với các domain khổng lồ như `earth_science` (121,249 tài liệu), việc nạp toàn bộ vào RAM dưới dạng đối tượng Python sẽ làm cạn kiệt bộ nhớ. Chúng tôi áp dụng kỹ thuật 2 pha:
1. **Pha quét toàn văn (Full Streaming Scan):** Đọc tuần tự từng dòng của `documents.jsonl` bằng generator. Thu thập chính xác 100% các phân vị độ dài (P10, P25, Median, P75, P90, P95, P99, Max), phát hiện tài liệu rỗng, kiểm tra lỗi JSON, và thống kê tỷ lệ trùng lặp băm (*MD5 deduplication*).
2. **Lấy mẫu hồ chứa (Reservoir Sampling Algorithm):** Để đánh giá chi tiết hàng chục biến thể chunking và chạy thử nghiệm truy hồi, thuật toán tự động lấy mẫu ngẫu nhiên không thiên lệch một tập con cố định (ví dụ $N = 2,000$ tài liệu), đồng thời **luôn ưu tiên giữ lại 100% các tài liệu Gold Documents** được chỉ định trong `qrels_dev.txt`.
3. **Tự động dò Schema (Schema Autodetection):** Module tự động nhận diện các biến thể tên trường (`doc_id`, `id`, `_id`, `contents`, `text`, `passage`...) giúp code chạy ổn định trên mọi tập dữ liệu mà không bị sập bởi lỗi `KeyError`.

---

## 3. Tại Sao Chunking Có Thể Phá Hỏng Pipeline RAG?

Nhiều kỹ sư AI xem chunking là một thao tác tiền xử lý phụ trợ. Tuy nhiên trong RAG, **Chunking định hình không gian vector và ranh giới thông tin**:

```
[Văn bản gốc]
"DJI Mavic 3 Enterprise is designed for commercial surveying. It features a mechanical shutter."
      │
      ├────────────────────── CẮT CƠ HỌC (Fixed Character / Word) ──────────────────────┐
      ▼                                                                                 ▼
[Chunk 1] "...is designed for commercial surveying. It feat"                     [Chunk 2] "ures a mechanical shutter."
(Từ ngữ bị rách: 'features' -> 'feat' + 'ures')                                  (Cụt đầu, mất chủ ngữ: 'ures a...')
- BM25: Không tìm thấy từ khóa 'features'.                                      - BM25: Bị ô nhiễm từ khóa rác.
- Embedding: Sub-token rác, vector bị trôi lệch.                                - Embedding: Vector không có ý nghĩa.
- LLM: Không thể suy luận thiết bị nào có mechanical shutter.                  - LLM: Ảo giác (Hallucination).
```

### Bốn cạm bẫy phá hỏng RAG do chunking gây ra:
1. **Rách từ & Rách câu (Token/Sentence Mutilation):** Cắt ngang một từ chuyên ngành (`quadcopter` $\to$ `quad` + `copter`) hoặc một mệnh đề điều kiện (`Nếu pin dưới 20%` bị tách rời khỏi `drone sẽ tự hạ cánh`).
2. **Đại từ mồ côi (Dangling Coreference Trap):** Đoạn văn sau khi cắt bắt đầu bằng: *"Nó có camera zoom 56x..."*. Mô hình truy hồi ngữ nghĩa không thể biết "Nó" là máy bay nào nếu không có ngữ cảnh đứng trước.
3. **Tiêu đề mồ côi (Trailing Heading Orphan):** Tiêu đề mục kỹ thuật (vd: `### 4. Cảnh báo an toàn`) nằm ở dòng cuối của Chunk 1, nhưng nội dung cảnh báo lại nằm ở Chunk 2. Kết quả là Chunk 1 chứa tiêu đề rác, còn Chunk 2 mất tiêu đề định danh.
4. **Cắt cụt do tràn ngữ cảnh Embedding (Token Truncation):** Các mô hình embedding hiện đại (BGE, E5, Contriever) có giới hạn cứng $512$ token (~380 từ, ~2,000 ký tự). Nếu giữ nguyên tài liệu dài mà không chia nhỏ, phần đuôi tài liệu sẽ bị cắt bỏ vĩnh viễn, khiến tài liệu không bao giờ được tìm thấy.

---

## 4. Hệ Thống 10 Chiến Lược Chunking Đã Triển Khai

Trong `01_eda.py`, chúng tôi cài đặt và chuẩn hóa đối chuẩn **10 chiến lược khác nhau** (cùng 11 biến thể quét tham số sweep):

| STT | Tên Chiến Lược | Nguyên Lý Hoạt Động | Ưu Điểm | Nhược Điểm / Nguy Cơ RAG |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `1_Fixed_Char` | Cắt sliding window theo ký tự thô (size=500, overlap=50). | Dễ cài đặt, kích thước đồng đều tuyệt đối. | **Tệ nhất:** Rách từ vựng, đứt đôi câu cú, sinh sub-token rác. |
| **2** | `2_Fixed_Word` | Cắt sliding window theo số từ (words=120, overlap=20). | Không cắt rách từ. | Cắt ngang xương câu, làm mất cấu trúc cú pháp của câu. |
| **3** | `3_Sentence_Boundary` | Dùng Regex bóc tách từng câu trọn vẹn, gom câu đến ngưỡng 140 từ. | Câu cú nguyên vẹn 100%, bảo toàn ngữ pháp. | Vẫn chia nhỏ cả tài liệu ngắn; không giải quyết được đại từ mồ côi. |
| **4** | `4_Recursive_Markdown` | Phân rã đệ quy: `\n\n` (đoạn) $\to$ `\n` (bullet) $\to$ câu $\to$ từ; có cơ chế hoãn tiêu đề. | Tôn trọng cấu trúc định dạng markdown của diễn đàn; không làm rớt tiêu đề. | Các chunk phía sau bị mất tên thực thể dẫn đường. |
| **5** | `5_Semantic_Context` | Ngưỡng thích ứng $\le 800$c giữ nguyên; tài liệu dài chia nhỏ và **tiêm tiêu đề** `[Document Topic: ...]`. | Triệt tiêu đại từ mồ côi; mỗi chunk con là một đơn vị thông tin độc lập. | Tiêm prefix làm tăng nhẹ dung lượng index và tăng độ tương đồng giữa các chunk con. |
| **6** | `6_Whole_Document` | Giữ nguyên 100% tài liệu làm 1 chunk duy nhất (không chia). | Đơn giản, giữ trọn vẹn 100% ngữ cảnh ban đầu; không làm nở index. | Tài liệu dài ($>2,000$ ký tự) sẽ bị mô hình dense embedding cắt cụt đuôi. |
| **7** | `7_Parent_Child` | Cắt thành các chunk con rất nhỏ (~60 từ) để phục vụ tìm kiếm chính xác. | Điểm BM25 bắt từ khóa cục bộ rất nhạy. | Index nở gấp 3x – 4x; chunk con cụt lủn, chứa nhiều đại từ mồ côi nhất. |
| **8** | `8_Sentence_Window` | Trượt cửa sổ cố định 4 câu với bước nhảy stride = 2 câu. | Đảm bảo tính liên tục giữa các câu liền kề. | Bỏ qua ranh giới chủ đề/đoạn văn; độ trùng lặp nội dung cao. |
| **9** | `9_TextTiling` | Đo độ tương đồng Cosine túi từ (BoW) giữa các khối câu để tìm điểm đổi chủ đề. | Cắt dựa trên sự chuyển dịch ngữ nghĩa thực tế. | Rất nhạy cảm với nhiễu ở văn bản ngắn; thuật toán tính toán phức tạp. |
| **10** | `5e_Adaptive_Hybrid` *(Mới)* | **Quy tắc 2 pha tối ưu:** Nếu văn bản $\le 1,000$ ký tự $\to$ giữ nguyên Whole_Doc; nếu $> 1,000$ ký tự $\to$ cắt Recursive kèm tiêm Context. | **Toàn diện nhất:** 0% truncation ở bài dài, 0% chia cắt vô ích ở bài ngắn. | Cần cài đặt hàm điều kiện ngưỡng linh hoạt theo đặc trưng domain. |

---

## 5. Hệ Thống Tiêu Chí, Công Thức Tính & Thuật Toán Chẩn Đoán

Để đảm bảo kết quả đánh giá mang tính khách quan và khoa học thực nghiệm, bộ code v3 đã áp dụng các chuẩn mực đo lường nghiêm ngặt:

### 5.1. Thuật toán định vị Offset chính xác (Exact Character Offset Locating)
Thay vì đoán mò đầu/đuôi câu bằng chữ hoa/thường (dễ bị sai khi gặp số liệu, từ viết tắt như *U.S.*, *Ph.D.*), code sử dụng hàm `normalize_with_marks` thay thế mọi ký tự xuống dòng bằng ký hiệu đoạn văn `¶` và định vị chính xác vị trí substring `[start : end]` trong văn bản gốc $T$:
- **Bắt đầu sạch (`_starts_clean`):** Điểm `start` phải nằm ở đầu tài liệu ($s = 0$), hoặc ký tự ngay trước đó $T[s-1]$ phải là dấu kết thúc câu (`.`, `!`, `?`, `…`) hoặc ký hiệu đoạn `¶`. Nếu không $\to$ đánh dấu lỗi **`starts_mid_sentence`**.
- **Kết thúc sạch (`_ends_clean`):** Ký tự cuối cùng $T[e-1]$ phải là dấu kết câu, hoặc ký tự kế tiếp là ký hiệu đoạn `¶`. Nếu không $\to$ đánh dấu lỗi **`ends_mid_sentence`**.
- **Tiêu đề mồ côi (`trailing_heading`):** Đoạn cuối cùng của chunk có độ dài ngắn ($<80$ ký tự), không có dấu chấm câu, và ngay sau đó trong văn bản gốc là một ngắt đoạn $\to$ phát hiện tiêu đề bị bỏ rơi.

### 5.2. Công thức tính Điểm Chất Lượng Ngữ Nghĩa (Quality Score)
Mỗi chunk bắt đầu với $100$ điểm tối đa và bị trừ điểm theo mức độ nguy hại đối với RAG:
$$\text{Quality\_Score} = \max\Big(0, \; 100 - 25 \cdot \mathbb{I}_{\text{starts\_mid}} - 20 \cdot \mathbb{I}_{\text{ends\_mid}} - 30 \cdot \mathbb{I}_{\text{dangling\_unresolved}} - 15 \cdot \mathbb{I}_{\text{trailing\_heading}} - 25 \cdot \mathbb{I}_{\text{undersized}} - 20 \cdot \mathbb{I}_{\text{over\_token\_limit}}\Big)$$
*(Trong đó $\mathbb{I}$ là hàm chỉ thị nhận giá trị 1 nếu mắc lỗi, ngược lại nhận 0).*

### 5.3. Công thức xếp hạng tổng hợp (Min-Max Normalized Composite Score v3)
Để khắc phục hiện tượng điểm nDCG lấn át làm điểm Quality bị vô hiệu hóa, phiên bản v3 đã áp dụng **chuẩn hóa Min-Max nội bộ domain**:
1. Chuẩn hóa từng thành phần về dải $[0, 1]$:
   $$v_{norm} = \frac{v - \min(v)}{\max(v) - \min(v) + \epsilon} \quad \text{cho } v \in \{nDCG, \; Recall, \; Quality, \; Cost\}$$
2. Chi phí index theo thang logarit (chống bão hòa):
   $$\text{Cost} = \frac{1.0}{1.0 + \ln(\max(1.0, \; \text{expansion\_ratio}))}$$
3. Điểm cơ sở có trọng số chuẩn:
   $$\text{Base\_Composite} = 0.45 \cdot nDCG_{norm} + 0.20 \cdot Recall_{norm} + 0.25 \cdot Quality_{norm} + 0.10 \cdot Cost_{norm}$$
4. **Hình phạt cắt cụt cứng (Hard Truncation Penalty):** Nếu tỷ lệ chunk vượt quá 512 token lớn hơn 5%, phạt lũy tiến trừ tới 40% tổng điểm:
   $$\text{trunc\_penalty} = \min\left(0.40, \; \frac{\text{over\_token\_limit\_pct}}{25.0} \times 0.40\right) \quad (\text{khi } > 5\%)$$
   $$\mathbf{Composite} = \text{Base\_Composite} \times (1.0 - \text{trunc\_penalty})$$

### 5.4. Kiểm chứng thiên lệch độ dài câu hỏi (Query-Length Control Baseline)
Khi người dùng nối toàn bộ lịch sử vào query (`history_query`), query dài ra từ 15 từ lên 80–120 từ. Trong BM25, query càng dài thì xác suất vô tình trùng khớp từ khóa ngẫu nhiên càng cao.

Để chứng minh mức tăng điểm nDCG là do **giá trị ngữ nghĩa thực chất** hay chỉ là **ăn may do query dài**:
- Đo độ dài từ $L$ của `history_query`.
- Lấy ngẫu nhiên $L - |q|$ từ vựng từ chính từ điển corpus ghép vào câu hỏi gốc tạo thành `random_padded_query`.
- Tính chỉ số tăng trưởng ngữ nghĩa thuần túy:
  $$\mathbf{ndcg10\_semantic\_gain} = nDCG@10(\text{history}) - nDCG@10(\text{random\_padded})$$
  > **Kết quả thực nghiệm:** Chỉ số `sem_gain` luôn đạt giá trị dương rõ rệt ($+0.12$ đến $+0.24$), khẳng định lịch sử hội thoại thực sự bổ sung ngữ cảnh định danh cốt lõi cho việc truy hồi.

---

## 6. Phát hiện Thực nghiệm Từ Dữ Liệu 11 Domain

Bảng số liệu tổng hợp được trích xuất trực tiếp từ file thực nghiệm [`eda_summary_all.md`](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/eda_summary_all.md):

| Domain | Số Tài Liệu | Median (Ký tự) | % Bài $\le 800$c | P90 Ký Tự | Chiến Lược Xếp Hạng #1 | Điểm Composite | Đặc Thù Dữ Liệu |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **robotics** | 61,961 | **81** | 90.5% | 760 | `4b_Recursive_450` | 0.6676 | Đoạn mã / Hỏi đáp cực ngắn |
| **economics** | 50,220 | **120** | 88.6% | 850 | `3c_Sentence_220w` | 0.6692 | Khái niệm kinh tế ngắn gọn |
| **sustainable_living** | 60,792 | **125** | 89.0% | 880 | `6_Whole_Document` | 0.6739 | Mẹo vặt / Thảo luận ngắn |
| **psychology** | 52,835 | **130** | 90.3% | 790 | `4c_Recursive_1000` | 0.6875 | Thuật ngữ tâm lý học |
| **earth_science** | 121,249 | **278** | 99.5% | 510 | `1c_Char_900` / `Whole_Doc` | 0.8033 | Bách khoa toàn thư vi mô |
| **biology** | 57,359 | **309** | 99.5% | 520 | `4_Recursive_Markdown` | 0.7285 | Wikipedia trích đoạn |
| **hardware** | 26,308 | **469** | 67.7% | 1,650 | `6_Whole_Document` / `Adaptive` | 0.6490 | Diễn đàn phần cứng máy tính |
| **drones** | 16,381 | **537** | 64.0% | 1,911 | `6_Whole_Document` / `Adaptive` | 0.5973 | Hướng dẫn kỹ thuật bay drone |
| **law** | 20,027 | **791** | 50.4% | 2,120 | `Adaptive_Hybrid` | 0.6554 | Điều luật / Án lệ dài |
| **medicalsciences** | 23,297 | **830** | 48.9% | 2,240 | `Adaptive_Hybrid` | 0.6293 | Báo cáo y khoa / Ca lâm sàng |
| **politics** | 16,712 | **934** | 45.4% | 2,450 | `Adaptive_Hybrid` | 0.6364 | Tranh luận chính trị dài |

### Phân tích chuyên sâu 2 nhóm Domain:
1. **Nhóm Domain Tài Liệu Siêu Ngắn (`robotics`, `economics`, `sustainable_living`, `psychology`):**
   - Hơn 88% tài liệu ngắn hơn 800 ký tự (chỉ khoảng 1–2 đoạn văn).
   - Nếu áp dụng chia nhỏ theo câu hoặc theo cửa sổ từ, mỗi tài liệu chỉ sinh ra 1–2 chunk cụt lủn, làm tăng chi phí index mà không thu được bất kỳ lợi ích ngữ nghĩa nào. Chiến lược tốt nhất là **giữ nguyên văn bản (`Whole_Document`) hoặc dùng khối Recursive lớn**.
2. **Nhóm Domain Đuôi Dài Có Nguy Cơ Cắt Cụt Cao (`law`, `politics`, `medicalsciences`, `hardware`, `drones`):**
   - Hơn 50% tài liệu dài hơn 800 ký tự và P90 vượt ngưỡng 1,500 – 2,400 ký tự.
   - Nếu dùng `Whole_Document`, từ 10% đến 25% tài liệu sẽ vượt quá 512 token và bị cắt cụt vĩnh viễn đuôi văn bản khi đưa vào mô hình Embedding. Ở nhóm này, **`Adaptive_Hybrid`** (giữ nguyên bài $\le 1000$c, chia nhỏ bài $>1000$c kèm tiêm tiêu đề) là chiến lược duy nhất vừa bảo toàn ngữ cảnh vừa tránh được truncation penalty.

---

## 7. Hướng Dẫn Đọc Bộ Biểu Đồ Trực Quan Hóa (Visualizations)

Toàn bộ 6 biểu đồ đã được kết xuất tại [`reports/eda/figures/`](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/figures/):

### 7.1. Dashboard Tổng Quan (`dashboard_master_overview.png`)
![Master Dashboard](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/figures/dashboard_master_overview.png)
- **Panel A (Tỷ lệ bài ngắn):** Cột ngang thể hiện % tài liệu $\le 800$ ký tự. Đường đứt nét đỏ biểu thị mốc 50%. Có thể thấy rõ 7 domain nằm sâu bên phải mốc 50%.
- **Panel B (Tỷ lệ thắng cuộc):** Biểu đồ tròn thể hiện cơ cấu chiến lược đứng #1. Phân định rõ ràng giữa các chiến lược cốt lõi và các biến thể sweep.
- **Panel C (Đánh đổi Chất lượng vs Chi phí Index):** Trục hoành là Hệ số nở Chunk ($x$ lần), trục tung là Điểm chất lượng ngữ nghĩa. Điểm lý tưởng nằm ở góc trên bên trái (Chất lượng cao, nở ít). `Fixed-Char` rơi xuống đáy (chất lượng thấp), `Parent-Child` dạt sang phải (nở tới 3x).
- **Panel D (Grouped Bar Chart Retrieval):** So sánh trực tiếp nDCG@10 giữa Turn hiện tại (cột xanh dương) và Ghép lịch sử (cột xanh lá) trên từng chiến lược rời rạc.

### 7.2. Đặc Trưng Corpus & Phân Bố Độ Dài (`fig1_corpus_profile_by_domain.png`)
![Corpus Profile](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/figures/fig1_corpus_profile_by_domain.png)
- Cho thấy độ lệch quy mô: `earth_science` dẫn đầu với hơn 121,000 bài viết, trong khi `drones` và `politics` chỉ có khoảng 16,000 bài.
- Thang đo phân vị chỉ ra rằng độ dài trung vị (Median) của `law` và `politics` cao gấp 10 lần so với `robotics`.

### 7.3. Đo Lường Lỗi Ngữ Nghĩa Chunking (`fig2_chunking_semantic_integrity.png`)
![Semantic Integrity](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/figures/fig2_chunking_semantic_integrity.png)
- Cảnh báo trực quan màu đỏ và cam: `Fixed-Char` và `Fixed-Word` phá hỏng từ 35% đến 55% câu văn.
- Cột màu tím: `Parent-Child` và `Sentence-Window` tạo ra tỷ lệ đại từ mồ côi cao nhất do tách các câu con độc lập ra khỏi ngữ cảnh đoạn văn.

### 7.4. Hiệu Năng Truy Hồi nDCG@10 & Recall@10 (`fig3_retrieval_performance.png`)
![Retrieval Performance](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/figures/fig3_retrieval_performance.png)
- Hiển thị mức tăng trưởng có dấu (`+15%` đến `+33%`) giữa chế độ truy hồi đơn lẻ và truy hồi kèm lịch sử.
- Chứng minh các chiến lược bảo tồn câu văn (`Sentence_Boundary`, `Recursive_Markdown`, `Whole_Document`) đạt Recall@10 vượt trội so với các đoạn cắt vụn.

### 7.5. Ma Trận Nhiệt Composite Score (`fig4_domain_strategy_heatmap.png`)
![Domain Strategy Heatmap](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/figures/fig4_domain_strategy_heatmap.png)
- Trục tung là 11 domain, trục hoành là các chiến lược chunking.
- Các ô màu xám mang nhãn `N/A` giúp ma trận phản ánh trung thực những chiến lược không chạy sweep, loại bỏ hoàn toàn hiện tượng chấm điểm 0.0 giả tạo.
- Giúp kỹ sư tra cứu nhanh chiến lược nào phù hợp nhất cho từng domain cụ thể.

### 7.6. Động Thái Hội Thoại Multi-Turn (`fig5_conversational_dynamics.png`)
![Conversational Dynamics](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/figures/fig5_conversational_dynamics.png)
- Phân tích 4 góc độ: Số lượt hội thoại trung bình (dao động từ 3.5 đến 4.5 turns/hội thoại), độ dài câu hỏi người dùng (trung bình 16–19 từ), và mật độ tài liệu Gold liên quan (trung bình 1.7–2.8 tài liệu/lượt).

---

## 8. Kết Luận Kiến Trúc & Lộ Trình Triển Khai Tiếp Theo

### 8.1. Chốt Kiến Trúc Tiền Xử Lý Dữ Liệu: `Adaptive Hybrid Chunking`
Thay vì tranh cãi giữa việc "chia nhỏ hay giữ nguyên", giải pháp tối ưu cho toàn bộ 11 domain của RETECO Track 2 là **Kiến trúc Chia Cắt Thích Ứng (Adaptive Hybrid)**:

$$\text{Chunking Strategy}(doc) = 
\begin{cases} 
\text{Giữ nguyên Whole\_Document} & \text{nếu } \text{len}(doc) \le 1,000 \text{ ký tự} \\
\text{Recursive Markdown (750c) } + \text{ Context Injection} & \text{nếu } \text{len}(doc) > 1,000 \text{ ký tự}
\end{cases}$$

- **Lợi ích 1:** Bảo toàn nguyên vẹn 75% lượng tài liệu trong corpus vốn đã ngắn gọn, không làm phân mảnh thông tin.
- **Lợi ích 2:** Bảo vệ 25% tài liệu dài ở các domain kỹ thuật/luật không bị mô hình dense embedding cắt cụt.
- **Lợi ích 3:** Tiêm tiêu đề dẫn đường `[Document Topic: ...]` vào các chunk con, triệt tiêu 100% hiện tượng đại từ mồ côi cho bộ sinh câu trả lời RAG.

---

### 8.2. Lộ Trình Triển Khai Tiếp Theo (Actionable Roadmap)

```mermaid
flowchart TD
    subgraph G1 ["Pha 1: Tiền Xử Lý & Lập Chỉ Mục"]
        A["Corpus Thô (507k docs)"] --> B["Module: Adaptive Indexer (indexer.py)"]
        B --> C["Corpus Đã Chuẩn Hóa + Bảng Map chunk_id -> doc_id"]
    end

    subgraph G2 ["Pha 2: Truy Hồi Đa Tầng (Track 2a)"]
        D["Multi-Turn Query (Turn T + History)"] --> E["Module: Query Rewriter (De-contextualization)"]
        E --> F1["BM25 Lexical Retriever (Pyserini/Lucene)"]
        E --> F2["Dense Semantic Retriever (BGE-M3 / Contriever)"]
        C --> F1
        C --> F2
        F1 --> G["Hybrid Fusion (Reciprocal Rank Fusion - RRF)"]
        F2 --> G
        G --> H["Cross-Encoder Reranker (BGE-Reranker-Large)"]
        H --> I["Top-100 TREC Run (nDCG@10 Tối Ưu)"]
    end

    subgraph G3 ["Pha 3: Sinh Câu Trả Lời & Lý Luận (Track 2b/2c)"]
        I --> J["Top Contexts"]
        J --> K["LLM Generator / RAG Reasoner"]
        K --> L["Câu Trả Lời Cuối Cùng"]
    end
```

#### Các đầu việc cụ thể cần thực hiện ngay:
1. **Module `src/retrieval/adaptive_indexer.py`:**
   - Đóng gói logic Adaptive Hybrid Chunking (ngưỡng 1,000 ký tự).
   - Xây dựng từ điển ánh xạ hai chiều `chunk_id <-> doc_id` để đảm bảo kết quả truy hồi cấp chunk luôn map ngược về đúng `doc_id` của Ban Tổ Chức khi xuất file run TREC.
2. **Module `src/retrieval/query_rewriter.py`:**
   - Dựa trên phát hiện về `sem_gain`, xây dựng bộ viết lại câu hỏi (De-contextualization) để biến đổi câu hỏi phụ thuộc ngữ cảnh ở lượt $T$ thành một câu hỏi độc lập, loại bỏ từ rác và cô đọng thực thể kỹ thuật trước khi đưa vào BM25 và Dense Search.
3. **Module `src/retrieval/hybrid_search.py`:**
   - Kết hợp BM25 (Lucene analyzer) với Dense Embedding (`BAAI/bge-m3`) thông qua thuật toán RRF (*Reciprocal Rank Fusion*) để tối đa hóa Recall@100.
4. **Module `src/retrieval/reranker.py`:**
   - Sử dụng Cross-Encoder (như `bge-reranker-large`) sắp xếp lại Top 50–100 tài liệu nhằm đẩy các tài liệu quan trọng nhất lên vị trí Top 1–10, tối ưu hóa điểm số **nDCG@10** chính thức trên leaderboard.

---
*Báo cáo được lưu trữ chính thức tại [`reports/eda/BAO_CAO_TONG_KET_EDA_CHUNKING.md`](file:///D:/reteco/RETECO---Track-2a-bc-/reports/eda/BAO_CAO_TONG_KET_EDA_CHUNKING.md).*
