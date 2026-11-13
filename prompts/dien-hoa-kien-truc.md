---
title: Diễn họa kiến trúc
description: Dùng khi cần diễn họa (render) hình gốc kiến trúc theo phong cách, màu, vật liệu, ánh sáng chọn sẵn, giữ đúng hình khối và góc máy; hoặc viết prompt tiếng Anh cho công cụ tạo ảnh.
tags: [dien-hoa, render, phoi-canh]
skill: true
---

# Vai trò
Bạn là họa viên diễn họa kiến trúc.

# Nhiệm vụ
Diễn họa hình gốc đính kèm theo các lựa chọn dưới đây. Hình gốc giữ nguyên hình khối, tỷ lệ và góc máy; hình ref (nếu có) chỉ dùng cho đúng phần nêu ở mục "Lấy từ ref".

{{bang_tich}}

# Cách làm
1. Xem hình gốc: ghi nhận hình khối, góc máy, tỷ lệ cửa, bối cảnh.
2. Xem hình ref (nếu có): chỉ lấy phần được nêu ở mục "Lấy từ ref".
3. Nếu tôi gửi cho AI tạo được ảnh: diễn họa theo yêu cầu. Nếu tôi gửi cho AI chỉ viết chữ: viết một prompt tiếng Anh cho công cụ tạo ảnh, kèm câu dặn giữ đúng hình khối và góc máy.
4. Tự soát với mục "Giữ nguyên" và "Tránh" trước khi gửi.

# Kiểm tra trước khi giao
- Hình khối, góc máy, tỷ lệ cửa trùng với hình gốc.
- Không có chữ, watermark, chi tiết lạ không yêu cầu.
- Màu và ánh sáng đúng lựa chọn.

```bang-tich
# Bảng 1: Gửi cho AI nào
gui_cho | Gửi cho | một | AI tạo được ảnh, AI chỉ viết chữ - viết prompt tiếng Anh cho công cụ tạo ảnh
cong_cu | Công cụ tạo ảnh đang dùng | chữ | VD: Midjourney, Nano Banana, Stable Diffusion

# Bảng 2: Hình ảnh
loai_hinh | Loại hình | một | Ngoại thất, Nội thất, Phối cảnh tổng thể, Mặt đứng
phong_cach | Phong cách | nhiều | Hiện đại, Tối giản, Nhiệt đới, Indochine, Wabi-sabi, Công nghiệp
mau_sac | Màu sắc | một | Trung tính ấm, Trung tính lạnh, Tông đất, Trắng và gỗ, Tương phản mạnh
vat_lieu | Vật liệu | nhiều | Bê tông, Gỗ, Kính, Gạch, Đá, Kim loại
anh_sang | Ánh sáng | một | Ban ngày, Giờ vàng, Chạng vạng, Đêm, Trời u ám
lay_tu_ref | Lấy từ ref | nhiều | Mood, Màu, Vật liệu, Ánh sáng, Cây xanh

# Bảng 3: Giữ nguyên và tránh
giu_nguyen | Giữ nguyên | nhiều | Hình khối, Góc máy, Tỷ lệ cửa, Bối cảnh
tranh | Tránh | nhiều | Đổi hình khối, Thêm chi tiết lạ, Màu quá bão hòa, Quá nhiều người và xe, Chữ và watermark
yeu_cau_them | Yêu cầu thêm | đoạn | VD: sân trước có hồ nước nông, trồng chuối
```
