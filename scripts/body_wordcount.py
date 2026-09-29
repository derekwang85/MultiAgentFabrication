#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
body_wordcount.py — 出版正文量纲检查（去掉「清单」+「评审」后剩多少字）。

用途：全系列"扩正文到真3000"的量纲硬门禁。现有 writing-gates.py 的 G1-G5 / E1-E6
没有绝对字数判定，本工具补上这一道：把公开发表时会被剥掉的 section 截掉后，
量中文正文的汉字数 / 英文正文的词数。

判定阈值（写死，供批内回归）：
  CN 正文汉字数 >= 2800
  EN 正文词数   >= 1900

用法（在项目根目录）：
  python scripts/body_wordcount.py articles/06-minority.zh.md
  python scripts/body_wordcount.py articles/en/06-minority.en.md
  python scripts/body_wordcount.py --all      # 全量回归 13 CN + 12 EN
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 各语言会被剥掉的 section 起始标记（命中即截断，之后的都算剥除段）。
# EN 历史变体用词/大小写不一致（Checklist/checklist、Attached/Appendix），
# 用大小写不敏感 + 词形兼容的正则截断，避免把附录字数误算进正文。
CN_STRIP_MARKERS = ["## 第一天就能用的清单", "## 附：门禁评审记录"]
EN_STRIP_PATTERNS = [
    r"^##\s+A\s+[Cc]hecklist\s+you\s+can\s+use\s+on\s+day\s+one",
    r"^##\s+(?:[Aa]ppendix|[Aa]ttached)\s*:",
]

CN_MIN = 2800
EN_MIN = 1900


def _find_first_strip(text: str, kind: str) -> int:
    """返回第一个剥离标记的偏移；未命中则返回 len(text)。"""
    if kind == "en":
        best = len(text)
        for pat in EN_STRIP_PATTERNS:
            m = re.search(pat, text, re.M)
            if m and m.start() < best:
                best = m.start()
        return best
    # cn：字面量，中文不涉及大小写变体
    best = len(text)
    for m in CN_STRIP_MARKERS:
        idx = text.find(m)
        if idx != -1 and idx < best:
            best = idx
    return best


def truncate_body(text: str, kind: str):
    """从第一个剥离标记处截断，返回仅含发布正文（含标题与开篇引言块）的文本。"""
    return text[:_find_first_strip(text, kind)]


def count_cn(text: str) -> int:
    """统计 CJK 汉字数（不含 CJK 标点、不含 ASCII 数字字母）。"""
    # 去掉 markdown 语法记号，避免污染；保留汉字
    body = re.sub(r"[#>*`|\[\]()\-]", "", truncate_body(text, "cn"))
    han = re.findall(r"[\u4e00-\u9fff]", body)
    return len(han)


def count_en(text: str) -> int:
    """统计 英文/ASCII 单词数（含数字串计为词），去掉代码块行与引用下的 URL 干扰需可读化处理。"""
    body = truncate_body(text, "en")
    # 去掉 markdown 记号与行内代码反引号内容、括号内注释，再分词
    body = re.sub(r"`[^`]*`", " ", body)
    body = re.sub(r"[#>*|\[\]()_]", " ", body)
    words = re.findall(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*", body)
    return len(words)


def classify(text: str):
    if "第一天就能用的清单" in text or "附：门禁评审记录" in text:
        return "cn"
    if "A checklist" in text or "Attached: gate review" in text:
        return "en"
    # 回退：按文件名
    return None


def check_one(path):
    text = path.read_text(encoding="utf-8")
    kind = classify(text)
    if path.suffix.lower() != ".md":
        return None
    if kind is None:
        if path.name == "00-prologue.md":
            kind = "cn"
        else:
            kind = "cn"
    if "en" in path.parts and path.name.endswith(".en.md"):
        kind = "en"
    if kind == "cn":
        n = count_cn(text)
        status = "PASS" if n >= CN_MIN else "FAIL"
        return (path.name, f"CN 汉字 {n:4d}  (阈值 >= {CN_MIN})  {status}")
    else:
        n = count_en(text)
        status = "PASS" if n >= EN_MIN else "FAIL"
        return (path.name, f"EN 词    {n:4d}  (阈值 >= {EN_MIN})  {status}")


def run_all():
    cn_files = sorted((ROOT / "articles").glob("*.md"))
    en_files = sorted((ROOT / "articles" / "en").glob("*.en.md"))
    rows = []
    for f in cn_files + en_files:
        r = check_one(f)
        if r:
            rows.append(r)
    fails = [name for name, _ in rows if "FAIL" in _]
    for name, line in rows:
        print(f"{name:<32} {line}")
    print("-" * 60)
    print(f"合计 {len(rows)} 篇 ｜ 达标 {len(rows) - len(fails)} ｜ 未达标 {len(fails)}")
    if fails:
        print("FAIL 列表:", ", ".join(fails))
        sys.exit(1)
    print("量纲门禁：全部通过")


def main():
    args = sys.argv[1:]
    if not args or "--all" in args:
        run_all()
        return
    for a in args:
        p = Path(a)
        if not p.is_absolute():
            p = ROOT / p
        r = check_one(p)
        if r:
            print(r[1])
        else:
            print(f"跳过（非 md）: {a}")


if __name__ == "__main__":
    main()