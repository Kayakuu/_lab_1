# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Em thấy khi để Temperature thấp như 0.0 hay 0.5 thì AI trả lời rất ổn định, câu chữ gọn gàng nhưng máy móc. Khi tăng lên 1.0 thì câu chữ bắt đầu có sáng tạo và đa dạng hơn, còn lên đến 1.5 thì AI bắt đầu trả lời bay bổng, thỉnh thoảng dùng từ hơi lạ hoặc trả lời không mạch lạc lắm.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Em sẽ chọn mức thấp, khoảng 0.0 đến 0.2. Vì làm chatbot hỗ trợ khách hàng thì quan trọng nhất là phải đưa ra thông tin chính xác, đúng chính sách của công ty chứ không cần AI tự sáng tạo hay nói chuyện quá lan man dễ gây hiểu lầm.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tính toán nhanh thì GPT-4o đắt hơn con mini tầm gần 17 lần (khoảng 16.6 lần). Với quy mô 10.000 người dùng thì con số chênh lệch này là cực kỳ lớn về mặt kinh tế.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> Dùng GPT-4o sẽ xứng đáng khi mình cần AI giải quyết các bài toán logic khó, viết code hay phân tích dữ liệu chuyên sâu cần độ thông minh cao. Còn với những việc đơn giản như phân loại ý kiến khách hàng hay chatbot hỏi đáp thông tin cơ bản thì dùng GPT-4o-mini sẽ tốt hơn vì vừa rẻ vừa phản hồi nhanh.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Theo em thì Streaming cực kỳ quan trọng khi AI phải trả lời những câu dài, ví dụ như viết bài luận hay hướng dẫn code. Việc để chữ hiện ra dần dần giúp người dùng cảm thấy AI đang làm việc và đỡ sốt ruột hơn là chờ cả chục giây mới thấy kết quả. Còn non-streaming thì thích hợp cho những tác vụ chạy ngầm hoặc khi AI chỉ cần trả lời rất ngắn gọn (như "Đúng" hoặc "Sai") thì hiện ra luôn một lúc sẽ gọn hơn.

---

## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ (phong cách sinh viên)
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
