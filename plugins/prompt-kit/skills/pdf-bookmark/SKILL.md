---
name: pdf-bookmark
description: Dùng khi cần tạo, đặt lại hoặc đổi tên bookmark cho file PDF hồ sơ bản vẽ nhiều trang (kiến trúc, cảnh quan, MEP, hạ tầng).
---

# Hướng dẫn tạo bookmark cho hồ sơ bản vẽ PDF

Tài liệu này mô tả quy trình đã dùng cho hồ sơ *River Collection – Kiến trúc cảnh quan*,
để AI (hoặc người) lặp lại cho các hồ sơ bản vẽ khác có cùng kiểu khung tên.

---

## 1. Nguyên tắc chung

1. **Không sửa nội dung bản vẽ.** Bookmark chỉ là lớp điều hướng; mã hiệu đặt trong tên
   bookmark không ghi đè ô *Drawing No.* trên khung tên, trừ khi người dùng yêu cầu rõ.
2. **Mọi trang đều phải có bookmark.** Không bỏ sót trang nào, kể cả bìa và trang phân mục.
3. **Tên bookmark phải tự giải thích** khi đọc rời khỏi bản vẽ: có số trang, mã hiệu, tên bản vẽ.

## 2. Định dạng tên bookmark

```
<số trang 2 chữ số> | <MÃ HIỆU> – <Tên bản vẽ>
```

Ví dụ:

```
01 | BÌA
02 | PHẦN CẢNH QUAN            <- mục cha, in đậm, không có mã
06 | CQ.004 – Mặt đứng EL 00
25 | E.001 – Bảng thống kê vật tư tủ điện cảnh quan
```

Quy ước:

- Số trang là **số trang thật trong file PDF**, không phải số trang in trên bản vẽ.
- Dấu phân cách: ` | ` giữa số trang và mã, ` – ` (en dash) giữa mã và tên.
- Tên bản vẽ viết kiểu câu (chữ đầu hoa), không VIẾT HOA TOÀN BỘ.
- Mục cha (tên phần hồ sơ) viết HOA TOÀN BỘ và in đậm (`bold=True`).

## 3. Cấu trúc cây

Hai cấp là đủ:

```
01 | BÌA                       (cấp 0, không có con)
02 | PHẦN CẢNH QUAN            (cấp 0, in đậm)
  03 | CQ.001 – ...            (cấp 1)
  ...
22 | PHẦN CHIẾU SÁNG
  ...
32 | PHẦN NƯỚC
  ...
36 | PHẦN HẠ TẦNG
  ...
```

- Mỗi **trang bìa phân mục** (trang chỉ có chữ "PHẦN ..." trong khung tên) trở thành
  mục cha, và trỏ tới chính trang đó.
- Các bản vẽ nằm sau nó, cho tới trang bìa phân mục kế tiếp, là con của nó.
- Trang 1 là **BÌA** của cả hồ sơ – không gọi là "phối cảnh" dù hình nền là ảnh phối cảnh.

## 4. Cách lấy mã hiệu và tên bản vẽ

Đọc text từng trang (`pypdf`, `page.extract_text()`), rồi:

1. **Mã hiệu**: regex theo các tiền tố có trong hồ sơ, ví dụ
   `r'(?:CQ|MEP|HT|E)\.\d+'`. Thường chỉ xuất hiện đúng 1 lần, trong ô *Drawing No.*
2. **Tên bản vẽ**: nằm ngay trước mã hiệu trong luồng text của khung tên, sau
   `CÔNG TY TNHH ...` (tên đơn vị thiết kế). Mẫu text khung tên thường là:

   ```
   THIẾT KẾ / DESIGNER
   <Tên đơn vị thiết kế>
   <Hạng mục trong khung>        <- đôi khi lặp
   <TÊN BẢN VẼ>
   <MÃ HIỆU>
   <Tên dự án>
   <Hạng mục>
   <Địa chỉ>
   ```

   Nên in 500–700 ký tự quanh chuỗi `Giám Đốc- Director` để đọc và đối chiếu bằng mắt,
   vì thứ tự text có thể đảo tuỳ trang.
3. **Trang không có mã**: thường là các trang phụ lục (bảng thống kê, sơ đồ nguyên lý).

## 5. Xử lý mã thiếu hoặc trùng

- **Trùng mã** (nhiều trang cùng `CQ.013`): thêm hậu tố chữ thường theo thứ tự trang —
  `CQ.013a`, `CQ.013b`, `CQ.013c`, `CQ.013d`.
- **Thiếu mã**: đặt mã tạm theo nhóm hạng mục, đánh số liên tục từ `001`:
  - phần điện → `E.001`, `E.002`, …
  - phần hạ tầng → tiếp nối mã sẵn có (`HT.001` đã có ⇒ trang sau là `HT.002`)
- Luôn **báo lại cho người dùng** danh sách mã tự đặt, vì đó là suy luận chứ không phải
  dữ liệu có sẵn trong bản vẽ.

## 6. Ghi chú trạng thái

Nếu có trang vừa được thay/cập nhật, ghi chú ngắn trong ngoặc ở cuối tên bookmark:

```
06 | CQ.004 – Mặt đứng EL 00  (logo mới)
```

Chỉ giữ ghi chú này trong bản bàn giao đang rà soát; bản phát hành chính thức thì bỏ đi.

## 7. Script mẫu

```python
import pypdf

src = 'ho-so.pdf'
w = pypdf.PdfWriter(clone_from=src)

# xoá outline cũ nếu ghi đè lên chính file đó
try:
    del w._root_object['/Outlines']
except KeyError:
    pass

tree = [
    # (tên phần, trang bìa phần, [(trang, mã, tên bản vẽ), ...])
    ("PHẦN CẢNH QUAN", 2, [
        (3, "CQ.001", "Hoạ đồ vị trí"),
        (4, "CQ.002", "Sơ đồ định vị khu vực thi công"),
    ]),
]

w.add_outline_item("01 | BÌA", 0, bold=True)
for name, pg, kids in tree:
    parent = w.add_outline_item("%02d | %s" % (pg, name), pg - 1, bold=True)
    for p, code, title in kids:
        w.add_outline_item("%02d | %s – %s" % (p, code, title), p - 1, parent=parent)

w.page_mode = "/UseOutlines"   # mở file là hiện sẵn khung bookmark
w.write(src)
```

Lưu ý kỹ thuật:

- `add_outline_item` nhận **chỉ số trang từ 0**, nên luôn truyền `page - 1`.
- `w.page_mode = "/UseOutlines"` để người nhận mở ra thấy ngay cây bookmark.
- Ghi đè lên chính file nguồn chỉ an toàn khi đã `clone_from=src` (đọc hết vào bộ nhớ trước).

## 8. Kiểm tra lại sau khi ghi

```python
r = pypdf.PdfReader(src)
def show(o, d=0):
    for x in o:
        if isinstance(x, list):
            show(x, d + 1)
        else:
            print('  ' * d + x.title, '->', r.get_destination_page_number(x) + 1)
show(r.outline)
```

Đối chiếu: số trang in ra phải khớp với số thứ tự ở đầu tên bookmark, và tổng số
bookmark lá phải bằng tổng số trang trừ các trang bìa phân mục.
