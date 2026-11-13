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

        index.append({
            "file": fn,
            "name": name,
            "title": title,
            "description": desc,
            "tags": tags,
            "skill": bool(meta.get("skill", False)),
            "variables": sorted(set(re.findall(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", body))),
        })

        if not meta.get("skill"):
            continue

        d = os.path.join(SKILLS, name)
        os.makedirs(d, exist_ok=True)
        front = "---\nname: %s\ndescription: %s\n---\n\n" % (
            name, desc.replace("\n", " ").strip())
        # Chỗ cần điền + lựa chọn quen dùng (khoá trùng tên biến trong frontmatter)
        tail = ""
        vs = sorted(set(re.findall(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", body)))
        if vs:
            lines = []
            for v in vs:
                opts = meta.get(v)
                if isinstance(opts, list) and opts:
                    lines.append("- `{{%s}}`: thường chọn một trong: %s" % (v, ", ".join(opts)))
                else:
                    lines.append("- `{{%s}}`" % v)
            tail = ("\n## Chỗ cần hỏi người dùng\n\n"
                    "Nếu người dùng chưa nói rõ, hỏi trước khi làm:\n\n" + "\n".join(lines) + "\n")
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
