# RETECO — chạy Track 2

Hướng dẫn này dùng cấu trúc mã nguồn hiện tại trong `src/` và dữ liệu Track 2
trong `reteco_data/track2_recor/`. Các lệnh bên dưới chạy từ thư mục gốc repo.

Track 2 là **conversational retrieval**: mỗi turn là một truy vấn, với topic ID
theo dạng `<conversation_id>_turn_<turn_id>`. Baseline hiện có đánh giá sub-track
**2a**; nó tạo danh sách tài liệu truy hồi, không sinh câu trả lời cho 2b/2c.

## 1. Chuẩn bị môi trường

Cần Python 3.13 trở lên và [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
```

Repo đã có dữ liệu tại `reteco_data/`. Nếu bạn chưa tải dữ liệu, chạy:

```bash
uv run --with huggingface-hub hf download DataScience-UIBK/RETECO-SemEval2027 \
    --repo-type dataset --local-dir reteco_data
```

Mỗi domain Track 2 có corpus đầy đủ dùng chung cho train và dev; benchmark và
qrels được chia theo toàn bộ conversation.

## 2. Chạy baseline nhanh

Pure-Python BM25 không cần JDK. Chạy thử một domain trên dev:

```bash
uv run python src/starter_kit/run_release.py \
    --data reteco_data \
    --out runs/track2 \
    --split dev \
    --track1 \
    --track2 drones
```

`--track1` để trống là có chủ ý: repo dữ liệu này chỉ có Track 2, còn runner
dùng chung cho cả hai track. Thay `drones` bằng domain muốn chạy, hoặc liệt kê
nhiều domain sau `--track2`. Các domain hiện có:

```text
biology drones earth_science economics hardware law medicalsciences
politics psychology robotics sustainable_living
```

Để chạy tất cả domain Track 2 trên dev, dùng:

```bash
uv run python src/starter_kit/run_release.py \
    --data reteco_data \
    --out runs/track2 \
    --split dev \
    --track1 \
    --track2 biology drones earth_science economics hardware law medicalsciences \
        politics psychology robotics sustainable_living
```

Đổi `--split dev` thành `--split train` để chạy train. Baseline thử nghiệm này
chạy cả hai cách tạo truy vấn:

- `current`: chỉ dùng câu hỏi của turn hiện tại.
- `history`: thêm lịch sử hội thoại của turn vào câu hỏi.

Kết quả nằm trong `runs/track2/track2/<domain>/`, gồm các run
`2a_current_<split>.txt`, `2a_history_<split>.txt`; file tổng hợp điểm là
`runs/track2/baseline_<split>.json`. Điểm chính thức được báo cáo là **nDCG@10**.

## 3. Chạy baseline official

Baseline official dùng cùng phương pháp BM25 như các benchmark upstream: Lucene
analyzer, `gensim` `LuceneBM25Model` (`k1=0.9`, `b=0.4`) và `pytrec_eval`.
`uv sync` cài các thư viện Python cần thiết; phần này cần JDK (khuyến nghị JDK
21) cho Pyserini.

Trên Linux, đặt đường dẫn JDK trước khi chạy:

```bash
export JAVA_HOME=/path/to/jdk
export JVM_PATH="$JAVA_HOME/lib/server/libjvm.so"
```

Ví dụ chạy cả train và dev cho một domain:

```bash
uv run python src/starter_kit/official_baseline.py \
    --data reteco_data \
    --out baselines_official \
    --track1 \
    --track2 drones \
    --splits train dev
```

Chạy tất cả domain: đặt danh sách domain như ở trên sau `--track2`. Kết quả gồm
run TREC cho từng sub-track/split tại
`baselines_official/track2_recor/<domain>/` và bảng tổng hợp tại
`baselines_official/summary.json`. Dữ liệu corpus được lập chỉ mục một lần cho
mỗi domain; các kết quả đã lưu có thể được tái sử dụng khi chạy lại.

## 4. Chấm điểm và kiểm tra run

Ví dụ chấm run pure-Python cho domain `drones` trên dev:

```bash
uv run python src/utilities/scorer.py \
    --track 2 \
    --run runs/track2/track2/drones/2a_current_dev.txt \
    --qrels reteco_data/track2_recor/drones/qrels_dev.txt
```

Kiểm tra định dạng TREC và ID tài liệu trong corpus trước khi nộp:

```bash
uv run python src/utilities/format_checker.py \
    runs/track2/track2/drones/2a_current_dev.txt \
    --qrels reteco_data/track2_recor/drones/qrels_dev.txt \
    --corpus reteco_data/track2_recor/drones/documents.jsonl \
    --doc-key doc_id
```

Run cần có sáu cột theo định dạng `qid Q0 docid rank score tag`. Chỉ nộp run
trên tập test theo hướng dẫn của ban tổ chức; qrels train/dev trong repo chỉ
dùng để phát triển và đánh giá offline.

## 5. Cấu trúc liên quan

```text
src/
  starter_kit/
    run_release.py        # chạy pure-Python baseline và scorer trên release
    bm25_baseline.py      # sinh run TREC cho một track/domain
    official_baseline.py  # baseline Lucene BM25 + pytrec_eval
  utilities/
    scorer.py             # chấm nDCG@10 và phân tích theo vị trí turn
    format_checker.py     # kiểm tra định dạng run

reteco_data/
  track2_recor/<domain>/
    documents.jsonl       # corpus: doc_id, content
    benchmark_train.json  # hội thoại/turns để phát triển
    benchmark_dev.json    # hội thoại/turns để đánh giá held-out
    qrels_train.txt
    qrels_dev.txt
```
