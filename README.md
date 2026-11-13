# Prompt Kit

Kho prompt cá nhân, dùng được ở mọi máy. Một repo GitHub duy nhất làm hai việc:

1. **Web** — trang chọn / sắp xếp / điền biến / ghép prompt, mở bằng link, không cần cài gì.
2. **Plugin cho Claude** — mỗi prompt thành một "skill", máy mới chỉ cần cài plugin là Claude tự biết dùng.

Thêm một file `.md` vào `prompts/` là cả hai nơi đều có ngay.

---

## Cấu trúc

```
prompts/                  <- KHO PROMPT. Chỉ cần quan tâm thư mục này.
  _TEMPLATE.md            <- mẫu, file bắt đầu bằng _ sẽ bị bỏ qua
  pdf-bookmark.md
docs/
  index.html              <- giao diện web (GitHub Pages phục vụ từ đây)
  index.json              <- danh mục prompt, máy tự sinh
plugins/prompt-kit/
  skills/<ten>/SKILL.md   <- máy tự sinh từ prompts/, đừng sửa tay
scripts/build_skills.py   <- script sinh skill
.github/workflows/        <- tự chạy script mỗi khi prompts/ thay đổi
combos.json               <- các bộ ghép đã lưu
```

## Định dạng một file prompt

```markdown
---
title: Tạo bookmark cho hồ sơ bản vẽ PDF
description: Dùng khi cần tạo hoặc đặt lại bookmark cho PDF hồ sơ bản vẽ nhiều trang.
tags: [pdf, ban-ve, bookmark]
skill: true
---

Nội dung prompt… có thể chèn biến {{ten_du_an}}, {{ngay}}.
```

- `description` chính là câu Claude đọc để quyết định có dùng skill này không — viết rõ "dùng khi nào".
- `skill: false` thì prompt chỉ hiện trên web, không thành skill.
- `{{bien}}` sẽ thành ô nhập trên web.

---

## Dựng repo lần đầu

```bash
cd prompt-kit
git init -b main
git add .
git commit -m "feat: khoi tao prompt kit"

gh repo create prompt-kit --public --source=. --push
# hoặc tạo repo trên github.com rồi:
# git remote add origin https://github.com/<ten-cua-anh>/prompt-kit.git
# git push -u origin main
```

Bật giao diện web: **Settings → Pages → Source: Deploy from a branch → `main` / `/docs` → Save**.
Sau 1–2 phút trang chạy tại `https://<ten-cua-anh>.github.io/prompt-kit/`.

Trang tự đoán owner/repo từ chính URL GitHub Pages, nên mở là dùng được ngay (chế độ chỉ đọc).

## Dùng web

| Việc | Cách làm |
|---|---|
| Chọn prompt | Tick vào danh sách bên trái |
| Đổi thứ tự khi ghép | Kéo thả các thẻ bên phải |
| Điền biến | Các ô `{{…}}` hiện ra bên dưới |
| Lấy kết quả | **Sao chép prompt** hoặc **Tải .md** |
| Lưu bộ hay dùng | **Lưu bộ** → đặt tên → lần sau chọn ở ô "Bộ đã lưu" |
| Thêm / sửa / xoá prompt | **+ Prompt mới**, hoặc bấm ✎ ở từng dòng |

Thêm / xoá / lưu bộ là ghi thẳng vào repo, nên cần **token**:

1. GitHub → Settings → Developer settings → **Fine-grained tokens** → Generate new token
2. Repository access: chỉ chọn repo `prompt-kit`
3. Permissions → Repository permissions → **Contents: Read and write**
4. Dán token vào **Cài đặt** trên trang web

Token chỉ nằm trong `localStorage` của trình duyệt đó, không bị commit đi đâu. Máy lạ thì
dùng chế độ chỉ đọc (vẫn chọn, ghép, copy bình thường), hoặc bấm **Xoá token** trước khi rời máy.

## Dùng trong Claude (Cowork / Claude Code)

Ở máy bất kỳ:

```
/plugin marketplace add <ten-cua-anh>/prompt-kit
/plugin install prompt-kit@prompt-kit
```

Xong. Claude đọc `description` của từng skill và tự dùng đúng quy trình khi anh nhắc tới
công việc tương ứng — không phải copy-paste prompt nữa.

Cập nhật về sau: `git pull` ở repo, hoặc chạy lại lệnh marketplace để lấy bản mới.

## Khi sửa prompt bằng tay (không qua web)

```bash
# sửa / thêm file trong prompts/ rồi:
python3 scripts/build_skills.py     # sinh lại skills + docs/index.json
git add -A && git commit -m "docs: cap nhat prompt" && git push
```

Nếu quên chạy script cũng không sao — GitHub Actions trong repo tự chạy lại và commit giúp.

## Quy ước đặt tên file

- chữ thường, không dấu, nối bằng `-`: `dat-ma-ban-ve.md`
- tên file chính là tên skill, nên đặt theo việc cần làm, không theo dự án
