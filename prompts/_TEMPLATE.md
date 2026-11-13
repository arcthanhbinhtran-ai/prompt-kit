---
title: Tên ngắn gọn của prompt
description: Một câu mô tả khi nào thì dùng prompt này. Câu này cũng là thứ Claude đọc để tự quyết định có dùng hay không.
tags: [tu-khoa-1, tu-khoa-2]
skill: true
ngay: [Hôm nay, Theo ngày trên khung tên]
---

# Tên prompt

Viết nội dung prompt ở đây bằng Markdown bình thường.

Muốn có chỗ điền biến thì dùng dấu ngoặc nhọn đôi:

- Dự án: {{ten_du_an}}
- Ngày: {{ngay}}

Công cụ web sẽ tự nhận ra `{{ten_du_an}}`, hiện ô nhập, và thay giá trị vào khi ghép prompt.

Muốn chỗ điền hiện thành **ô tích** chọn nhanh thì khai báo các lựa chọn ở phần đầu file, dùng đúng tên biến
(xem dòng `ngay: [...]` ở trên). Người dùng vẫn gõ thêm được ở ô "Khác…".

## Ghi chú về frontmatter

| Khoá | Bắt buộc | Ý nghĩa |
|---|---|---|
| `title` | có | Tên hiển thị trong danh sách |
| `description` | có | Mô tả ngắn; dùng luôn làm `description` của skill |
| `tags` | không | Để lọc/tìm kiếm |
| `skill` | không | `true` thì file này được sinh thành skill cho Claude; `false` hoặc bỏ trống thì chỉ dùng trong web |
| `<ten_bien>` | không | Danh sách lựa chọn `[A, B, C]` cho chỗ `{{ten_bien}}` — trang hiện thành ô tích, skill ghi kèm để Claude hỏi đúng |
