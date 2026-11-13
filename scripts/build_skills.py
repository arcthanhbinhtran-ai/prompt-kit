#!/usr/bin/env python3
"""Sinh skill cho Claude từ thư mục prompts/.

Mỗi file prompts/<ten>.md có frontmatter `skill: true` sẽ trở thành
plugins/prompt-kit/skills/<ten>/SKILL.md

Chạy:  python3 scripts/build_skills.py
"""
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS = os.path.join(ROOT, "prompts")
SKILLS = os.path.join(ROOT, "plugins", "prompt-kit", "skills")
INDEX = os.path.join(ROOT, "docs", "index.json")


def parse_front_matter(text):
    """Trả về (dict metadata, phần thân). Parser tối giản, đủ cho khoá: giá trị."""
    meta, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            elif v.lower() in ("true", "false"):
                v = v.lower() == "true"
            meta[k.strip()] = v
    return meta, body


def slugify(name):
    s = re.sub(r"[^a-zA-Z0-9-]+", "-", name.strip().lower()).strip("-")
    return s or "prompt"


FORM_RE = re.compile(r"(`{3,})bang-tich[^\n]*\n(.*?)\n?\1", re.S)
KINDS = {"một": "mot", "mot": "mot", "nhiều": "nhieu", "nhieu": "nhieu",
         "chữ": "chu", "chu": "chu", "đoạn": "doan", "doan": "doan",
         "one": "mot", "many": "nhieu", "text": "chu", "paragraph": "doan"}


def parse_form(body):
    """Tách khối ```bang-tich ra khỏi thân prompt. Trả về (danh sách ô, thân còn lại)."""
    m = FORM_RE.search(body)
    if not m:
        return [], body
    out = []
    for raw in m.group(2).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            out.append({"group": line.lstrip("#").strip()})
            continue
        c = [s.strip() for s in line.split("|")]
        if not re.match(r"^[a-zA-Z0-9_]+$", c[0]) or c[0] == "bang_tich":
            continue
        c += [""] * (4 - len(c))
        kind = KINDS.get(c[2].lower()) or ("nhieu" if c[3] else "chu")
        opts = [s.strip() for s in c[3].split(",") if s.strip()] if kind in ("mot", "nhieu") else []
        out.append({"var": c[0], "label": c[1] or c[0], "kind": kind, "opts": opts,
                    "hint": "" if opts else c[3]})
    return out, (body[:m.start()] + body[m.end():])


def main():
    if not os.path.isdir(PROMPTS):
        sys.exit("Khong tim thay thu muc prompts/")

    if os.path.isdir(SKILLS):
        shutil.rmtree(SKILLS)
    os.makedirs(SKILLS, exist_ok=True)

    index, made = [], 0
    for fn in sorted(os.listdir(PROMPTS)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        path = os.path.join(PROMPTS, fn)
        with open(path, encoding="utf-8") as f:
            meta, body = parse_front_matter(f.read())

        name = slugify(meta.get("name") or os.path.splitext(fn)[0])
        title = meta.get("title") or name
        desc = meta.get("description") or title
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]

        form, body = parse_form(body)
        vs = sorted(set(re.findall(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", body)) - {"bang_tich"})
        names = [x["var"] for x in form if x.get("var")]
        index.append({
            "file": fn,
            "name": name,
            "title": title,
            "description": desc,
            "tags": tags,
            "skill": bool(meta.get("skill", False)),
            "variables": names + [v for v in vs if v not in names],
        })

        if not meta.get("skill"):
            continue

        d = os.path.join(SKILLS, name)
        os.makedirs(d, exist_ok=True)
        front = "---\nname: %s\ndescription: %s\n---\n\n" % (
            name, desc.replace("\n", " ").strip())
        # Chỗ cần hỏi: lấy từ khối bang-tich, rồi các {{bien}} còn lại (lựa chọn khai ở frontmatter)
        lines = []
        for x in form:
            if "group" in x:
                lines.append("\n**%s**\n" % x["group"])
                continue
            if x["opts"]:
                how = "chọn một trong" if x["kind"] == "mot" else "chọn một hoặc nhiều trong"
                lines.append("- %s: %s: %s" % (x["label"], how, ", ".join(x["opts"])))
            else:
                lines.append("- %s%s" % (x["label"], (" (" + x["hint"] + ")") if x["hint"] else ""))
        for v in vs:
            if v in names:
                continue
            opts = meta.get(v)
            if isinstance(opts, list) and opts:
                lines.append("- `{{%s}}`: thường chọn một trong: %s" % (v, ", ".join(opts)))
            else:
                lines.append("- `{{%s}}`" % v)
        tail = ""
        if lines:
            tail = ("\n## Chỗ cần hỏi người dùng\n\n"
                    "Nếu người dùng chưa nói rõ, hỏi trước khi làm:\n" + "\n".join(lines).rstrip() + "\n")
        body = re.sub(r"\{\{\s*bang_tich\s*\}\}", "(Các lựa chọn của người dùng — xem mục \"Chỗ cần hỏi người dùng\" ở cuối.)", body)
        body = re.sub(r"\n{3,}", "\n\n", body)
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(front + body.strip() + "\n" + tail)
        made += 1

    os.makedirs(os.path.dirname(INDEX), exist_ok=True)
    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"prompts": index}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("Da sinh %d skill / %d prompt." % (made, len(index)))


if __name__ == "__main__":
    main()
