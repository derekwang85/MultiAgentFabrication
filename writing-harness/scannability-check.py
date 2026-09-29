#!/usr/bin/env python3
"""
scannability-check.py — derekwritting-framework 英文可扫读性自动检测

英文长文的一个主要风险是"读得动但扫不动"：段落堆成一堵墙、句子一个回车连一句、
小节标题含糊到无法当目录用、被动语态把动作倒装。这个脚本把可扫读性拆成
可机器判定的指标，输出分维分数与问题清单，供门禁或人工评审参考。

检测项（均可配置阈值）:
  C1 段落长度   超过 max_sentences 句的段落偏长（默认 4 句）
  C2 句子长度   超过 max_words 词的句子偏长（默认 32 词）
  C3 小节链     小节标题少于 min_sections 个，或标题空/过短，扫读无纲
  C4 列表密度   应使用列表的"步骤枚举"却写成长段落（启发式: 段落内出现 "first/second/1)" 等)
  C5 被动语态   被动句占比过高（英文特有: be + past participle）
  C6 弱化/允诺词 每千词出现频率过高（延续 G1 的 en 信号，覆盖可扫读弱化词）

用法:
  python3 scannability-check.py <file.md>
  python3 scannability-check.py <file.md> --json     # JSON 输出
  python3 scannability-check.py <dir>                # 目录内所有 .md

退出码: 0 = 通过; 1 = 存在偏弱项; 2 = 用法错误
"""
import argparse
import json
import re
import sys
from pathlib import Path

# ── 可扫读性阈值 ──────────────────────────────────────────────────────
MAX_SENTENCES_PER_PARAGRAPH = 4    # C1
MAX_WORDS_PER_SENTENCE = 32        # C2
MIN_SECTIONS = 2                   # C3
MAX_PASSIVE_RATIO = 0.3            # C5: 被动句占句子总数上限
MAX_WEAKENER_PER_1K = 4.0          # C6

# C6 弱化词（英文信号，延续 writing-gates.py 的 en 风格）
WEAKENERS = [
    "quite", "very", "really", "just", "basically", "simply",
    "actually", "obviously", "clearly", "of course", "it is worth noting",
    "it is important to note", "delve", "furthermore", "additionally",
]
# C4 提示应使用列表的行内枚举模式
LIST_HINT_RE = re.compile(r"\b(first|second|third|then|next)\b|^\s*\d+[).]", re.IGNORECASE)
# C1 识别"列表块"：无序(-/*)、有序(1.) 与任务清单项，均视为可扫读结构而非长段落
LIST_BLOCK_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s", re.MULTILINE)


def split_sentences_en(text: str) -> list[str]:
    """粗粒度切句：英文按句号/问号/叹号，中文按句号/问号，保留下标。"""
    return [s.strip() for s in re.split(r"(?<=[.!?。！？])\s+", text) if s.strip()]


def word_count_en(sentence: str) -> int:
    return len(re.findall(r"[A-Za-z]+", sentence))


def split_paragraphs(text: str) -> list[str]:
    """按空行或单个换行分成段落块（保留有意义的多行文字）。"""
    blocks = re.split(r"\n\s*\n", text)
    return [b for b in blocks if len(b.strip()) > 0]


def check_paragraph_length(text: str) -> dict:
    problems = []
    paragraphs = split_paragraphs(text)
    long_ones = []
    for p in paragraphs:
        # 跳过标题行 / 列表块 / 代码块外壳（列表即可扫读结构，不计为长段落）
        if re.match(r"^#{1,6}\s", p) or LIST_BLOCK_RE.match(p) or p.lstrip().startswith(("`",)):
            continue
        sents = split_sentences_en(p)
        if len(sents) > MAX_SENTENCES_PER_PARAGRAPH:
            long_ones.append((len(sents), p[:70].replace("\n", " ")))
    for count, head in long_ones:
        problems.append(f"段落偏长（{count} 句）: “{head}…”")
    return {"ok_len": len(long_ones), "count": len(long_ones),
            "passed": len(long_ones) == 0, "problems": problems[:6]}


def check_sentence_length(text: str) -> dict:
    problems = []
    sentences = split_sentences_en(text)
    long_ones = []
    total = len(sentences)
    for s in sentences:
        if re.match(r"^#{1,6}\s", s):  # 跳过标题单行
            continue
        wc = word_count_en(s)
        if wc > MAX_WORDS_PER_SENTENCE:
            long_ones.append((wc, s[:80]))
    for wc, head in long_ones:
        problems.append(f"句子偏长（{wc} 词）: “{head}…”")
    ratio = (len(long_ones) / total) if total else 0.0
    return {"long_count": len(long_ones), "sentence_count": total,
            "long_ratio": round(ratio, 3), "passed": len(long_ones) <= max(1, int(total * 0.15)),
            "problems": problems[:6]}


def check_sections(text: str) -> dict:
    problems = []
    h2 = re.findall(r"^##\s+(.+)", text, flags=re.M)
    bad = [h for h in h2 if word_count_en(h) < 2 and not re.search(r"[\u4e00-\u9fff]", h)]
    if not h2:
        problems.append("无二级小节，扫读者无法按标题跳读")
    elif len(h2) < MIN_SECTIONS:
        problems.append(f"二级小节过少（{len(h2)} 个）")
    if bad:
        problems.append(f"{len(bad)} 个小节标题过于简短，无法当纲目扫读")
    return {"h2_count": len(h2), "passed": bool(h2) and len(h2) >= MIN_SECTIONS and not bad,
            "problems": problems}


def check_list_density(text: str) -> dict:
    """启发式：发现连续枚举语气却未用列表。"""
    problems = []
    paragraphs = split_paragraphs(text)
    for p in paragraphs:
        if re.match(r"^#{1,6}\s", p):
            continue
        lines = [l for l in p.splitlines() if l.strip()]
        if len(lines) == 1 and LIST_HINT_RE.search(p):
            problems.append(f"疑似应改用列表的枚举段落: “{p[:70]}…”")
    return {"count": len(problems), "passed": len(problems) <= 1, "problems": problems[:5]}


def check_passive(text: str) -> dict:
    """被动语态检测（英文: be 动词 + 过去分词，排除 be-be/I am 等）。"""
    sentences = split_sentences_en(text)
    passive = 0
    checked = 0
    for s in sentences:
        words = re.findall(r"[A-Za-z]+", s)
        if len(words) < 4:
            continue
        checked += 1
        # 粗判：\b(am|is|are|was|were|been|being)\b + <gap> + 常见过去分词
        if re.search(r"\b(am|is|are|was|were|been|being)\s+\w+(?:ed|en|t)\b", s, re.IGNORECASE):
            passive += 1
    ratio = (passive / checked) if checked else 0.0
    passed = ratio <= MAX_PASSIVE_RATIO
    note = "" if passed else f"被动语态偏多（{passive}/{checked} 句，占比 {ratio:.0%}）"
    return {"passive": passive, "checked": checked, "ratio": round(ratio, 3),
            "passed": passed, "problems": [note] if note else []}


def check_weakeners(text: str) -> dict:
    hits = []
    for w in WEAKENERS:
        c = len(re.findall(re.escape(w), text, flags=re.IGNORECASE))
        if c:
            hits.append((w, c))
    total = sum(c for _, c in hits)
    words = len(re.findall(r"[A-Za-z]+", text))
    density = (total * 1000.0 / words) if words else 0.0
    return {"hits": hits, "total": total, "word_count": words,
            "density_per_1k": round(density, 1),
            "passed": density < MAX_WEAKENER_PER_1K}


def run_check(file_path: str) -> dict:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    checks = {
        "C1_paragraph_length": check_paragraph_length(text),
        "C2_sentence_length": check_sentence_length(text),
        "C3_sections": check_sections(text),
        "C4_list_density": check_list_density(text),
        "C5_passive": check_passive(text),
        "C6_weakeners": check_weakeners(text),
    }
    # 三项硬指标通过则整体通过（C1/C2/C3 为主，C4-C6 为提示）
    hard = [checks["C1_paragraph_length"]["passed"],
            checks["C2_sentence_length"]["passed"],
            checks["C3_sections"]["passed"]]
    return {"file": str(path), "checks": checks,
            "all_pass": all(hard),
            "hard_summary": "核心可扫读性通过" if all(hard) else "核心可扫读性需加强"}


def main() -> int:
    ap = argparse.ArgumentParser(description="derekwritting 英文可扫读性检测")
    ap.add_argument("target", nargs="?", help="md 文件或目录")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--list", action="store_true", help="列出弱化词表")
    args = ap.parse_args()

    if args.list:
        print("C6 弱化/允诺词表：", "、".join(WEAKENERS))
        return 0
    if not args.target:
        ap.print_help()
        return 2

    target = Path(args.target)
    files = [target] if target.is_file() else sorted(target.glob("*.md"))
    if not files:
        print(f"未找到 .md 文件: {args.target}")
        return 2

    results = [run_check(str(f)) for f in files]
    overall = all(r["all_pass"] for r in results)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        order = ["C1_paragraph_length", "C2_sentence_length", "C3_sections",
                 "C4_list_density", "C5_passive", "C6_weakeners"]
        for r in results:
            print(f"\n=== {r['file']} ===")
            print(f"  {r['all_pass'] and '✅' or '❌'} {r['hard_summary']}")
            for c in order:
                ch = r["checks"][c]
                status = "PASS" if ch.get("passed") else "CHECK"
                marker = "✅" if ch.get("passed") else "⚠️"
                print(f"  {marker} {c}: {status}")
                for p in ch.get("problems", [])[:3]:
                    print(f"       - {p}")
        print(f"\n{'✅ 全部文件可扫读性通过' if overall else '❌ 存在需加强的可扫读性项'}（{len(results)} 文件）")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())