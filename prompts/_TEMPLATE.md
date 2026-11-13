---
title: Tên ngắn gọn của prompt
description: Một câu nói rõ KHI NÀO thì dùng prompt này. Câu này cũng là thứ Claude đọc để tự quyết định có dùng skill hay không.
tags: [tu-khoa-1, tu-khoa-2]
skill: true
---

# Vai trò
Bạn là ...

# Nhiệm vụ
... Chỗ nào thay đổi theo từng lần thì viết {{ten_du_an}}.

{{bang_tich}}

# Cách làm
1. ...
2. ...

# Kiểm tra trước khi giao
- ...

```bang-tich
# Bảng 1: Thông tin chung
ten_du_an | Tên dự án | chữ | VD: River Collection
loai | Loại hồ sơ | một | Kiến trúc, Cảnh quan, Nội thất

# Bảng 2: Giữ nguyên và tránh
tranh | Tránh | nhiều | Tự đổi số liệu, Bỏ sót trang, Giải thích dài
```

<!--
GHI CHÚ (file bắt đầu bằng _ nên trang và skill đều bỏ qua file này)

Phần đầu file (giữa hai dòng ---):
  title        bắt buộc  Tên hiện trong danh sách
  description  bắt buộc  Khi nào dùng; dùng luôn làm mô tả của skill
  tags         không     Để tìm kiếm
  skill        không     true = sinh thành skill cho Claude

Khối ```bang-tich (trang hiện thành các bảng ô tích):
  # Bảng 1: Tên bảng                              -> tiêu đề một nhóm ô
  ten_bien | Nhãn | kiểu | lựa chọn A, B, C       -> một ô
  kiểu: một (chọn một) / nhiều (chọn nhiều) / chữ (gõ một dòng) / đoạn (gõ nhiều dòng)
  Bản tiếng Anh: one / many / text / paragraph.

{{bang_tich}}  chỗ trang chèn danh sách người dùng đã tích (không có thì thêm vào cuối).
{{ten_bien}}   thay đúng giá trị vào chỗ đó. Mọi {{ten_bien}} phải có trong khối bang-tich,
               nếu không trang báo "mâu thuẫn" và không cho lưu.
-->
