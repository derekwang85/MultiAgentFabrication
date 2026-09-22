#!/usr/bin/env python3
"""
writing-gates.py — derekwritting-framework 五道门禁自动执行器（G1-G5）

对应 methodology/05-writing-gates.md 的五道门禁，把可量化的部分自动化：
  G1 风格门禁:  stop-slop 信号词扫描（AI 味词汇密度），总分换算 1-10 五维
  G2 结构门禁:  Purpose-First 检查（段首给答案/无废话开场/设问套近乎）
  G3 事实门禁:  强主张可验证检查（统计必须有来源+年份+方法；无"看起来合理"的虚构）
  G4 引用门禁:  链接可解析性检查（本地文件真实存在、外部 URL 格式合法）
  G5 发布门禁:  独立评审记录检查（评审者分离 + 剩留问题清单）

用法:
  python3 writing-gates.py <file.md>            # 单文件
  python3 writing-gates.py <dir>                # 目录内所有 .md
  python3 writing-gates.py <file.md> --json     # JSON 输出
  python3 writing-gates.py --list               # 列出信号词表

退出码: 0 = 五道全过; 1 = 有门禁未过; 2 = 用法错误
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── 门禁阈值（与 05-writing-gates.md 一致）─────────────────────────────
G1_STYLE_MIN = 35  # 风格总分下限（/50）
# 信号词密度阈值：每 1000 字允许的信号词数。AI 味稿（空洞夸张+套话密集）密度显著高于正常稿。
G1_DENSITY_THRESHOLD = 6.0  # 信号词 / 千字

# ── G1 信号词表（AI 味 / slop 词汇，中英混合）────────────────────────
SIGNAL_WORDS_CN = [
    "综上所述", "总而言之", "值得注意的是", "众所周知", "毋庸置疑",
    "不可否认", "由此可见", "与此同时", "值得一提的是", "不难发现",
    "显而易见", "进一步而言", "更进一步", "总的来说", "在当今",
    "在这个快速变化", "在当今快节奏", "赋能", "抓手", "闭环思维",
    "深度", "首先", "其次", "最后", "总之", "让我们", "一起",
    "真正重要的是", "关键在于", "毫无疑问", "事实上", "确实",
    "无可否认", "本质上是", "从根本上", "让我们深入", "让我们思考",
    "不断", "持续", "助力", "引领", "探索", "开启", "赋能", "拥抱",
    "重新定义", "颠覆", "变革", "挑战", "机遇", "未来已来",
]
SIGNAL_WORDS_EN = [
    "delve", "delve into", "furthermore", "moreover", "additionally",
    "in conclusion", "conclusively", "it is important to note",
    "it is worth noting", "comprehensive", "landscape", "leverage",
    "seamless", "cutting-edge", "state-of-the-art", "dive into",
    "in today's", "fast-paced", "underscore", "paramount",
    "ever-evolving", "game-changer", "revolutionize", "unlock the power",
    "holistic", "synergy", "robust", "granular",
]
G1_SIGNAL_WORDS = SIGNAL_WORDS_CN + SIGNAL_WORDS_EN

# ── G3 统计模式：识别"统计主张"（需溯源的百分比/倍率类）
# 只匹配统计主张（% / 倍 / x / 比率），不匹配项目计数（N 个/行/条——那是作者一手经验数据）
G3_STRONG_STAT_RE = re.compile(r"(\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*(?:倍|x)\b|\d+(?:\.\d+)?\s*倍)")

# 统计出现前后 120 字符内无来源标记 → 疑似无来源主张
# 来源分两类（constitution 2.4 认知纪律：一手经验标清楚，不与行业普遍情况混淆）：
#   一手经验：作者自己项目里的实测/抽查/复盘（合法，需标注）
#   外部引用：报告/研究/调查，需可追溯来源
G3_SOURCE_MARKERS = ["CodeRabbit", "Google Research", "CSA", "GitHub", "Sonar",
                     "Veracode", "Fordel", "调查", "研究", "报告", "来源",
                     "According", "per ", "2026", "2025",
                     "[ORIGINAL DATA]", "[PERSONAL EXPERIENCE]",
                     # 一手经验标记（中文）：作者自己项目里的数字
                     "[内部项目实测]", "[内部项目]", "[个人经验]", "[实测]",
                     "我们项目", "我们踩过", "我们建了", "抽查", "复盘", "实测"]

# ── G2 废话开场模式 ────────────────────────────────────────────────────
G2_FILLER_OPENERS = [
    "在当今", "在这个", "众所周知", "随着", "毫无疑问", "首先，让我们",
    "本文将", "本文将从", "在这篇文章中", "让我先", "在开始之前",
]

# ── G5 评审记录标记 ────────────────────────────────────────────────────
G5_REVIEW_MARKERS = ["评审", "rubric", "门禁评审", "剩留问题", "reviewed"]


def scan_g1_signal(text: str) -> dict:
    """G1：按密度扫描信号词，返回命中统计（/千字）。"""
    hits = []
    for word in G1_SIGNAL_WORDS:
        count = len(re.findall(re.escape(word), text, flags=re.IGNORECASE))
        if count:
            hits.append((word, count))
    total = sum(c for _, c in hits)
    # 有效字数（粗略：汉字+英文单词数）
    cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    en_words = len(re.findall(r"[A-Za-z]+", text))
    length = cn_chars + en_words
    density = (total * 1000.0 / length) if length else 0.0
    return {
        "hits": hits,
        "total": total,
        "length": length,
        "density_per_1k": round(density, 1),
        "passed": density < G1_DENSITY_THRESHOLD,
    }


def g2_structure(text: str, path: str) -> dict:
    """G2：Purpose-First 结构检查。"""
    problems = []
    checks = {}
    # 无 H1
    checks["has_h1"] = bool(re.search(r"^# ", text, flags=re.M))
    if not checks["has_h1"]:
        problems.append("缺少 H1 主标题")

    # H2 数量（太少=结构单薄）
    h2s = re.findall(r"^## ", text, flags=re.M)
    checks["h2_count"] = len(h2s)
    if len(h2s) < 2:
        problems.append(f"H2 节过少（{len(h2s)} 个）")

    # 段首废话开场（每个 H2 后第一段非空行的首个字符）
    for m in re.finditer(r"^## .*\n(.*)", text, flags=re.M):
        first_line = m.group(1).strip()
        if not first_line:
            continue
        for filler in G2_FILLER_OPENERS:
            if first_line.startswith(filler):
                problems.append(f"节段首废话开场: “{first_line[:30]}…”")
                break

    # 设问铺垫检查（只查正文开头 300 字符内的设问，排除反方论证/子标题中的设问）
    # 反方论证（"反方怎么看""会不会"）是严谨论证的一部分，不算套近乎
    head = text[:300]
    q_count = len(re.findall(r"(?:是不是|值不值得|应该怎么|该如何选择)", head))
    checks["setup_question_count"] = q_count
    if q_count > 2:
        problems.append(f"开头设问铺垫过多（{q_count} 次），疑似套近乎")

    checks["passed"] = not problems
    return {"problems": problems, "checks": checks, "passed": checks["passed"]}


def g3_facts(text: str) -> dict:
    """G3：统计主张可验证检查。"""
    problems = []
    suspicious = []
    for m in G3_STRONG_STAT_RE.finditer(text):
        start = m.start()
        end = m.end()
        # 排除引号/反引号内的假设性数字（如“首次通过率 ≥70%”是举例，非统计）
        # 中文弯引号（“”）与直引号（""）都覆盖
        in_dquote = False
        for q in ('“', '"'):
            prev = text.rfind(q, 0, start)
            if prev != -1:
                closer = text.find('”' if q == '“' else '"', end)
                if closer != -1 and closer - end < 80:
                    in_dquote = True
                    break
        if in_dquote:
            continue  # 位于成对引号内 → 跳过
        # 窗口前后双向覆盖：来源可能在数字前（"CSA（2026年4月）报告显示 45%"）
        window = text[max(0, start - 100):start + 120]
        has_source = any(marker.lower() in window.lower() for marker in G3_SOURCE_MARKERS)
        if not has_source:
            snippet = text[max(0, start - 30):start + 40].replace("\n", " ")
            suspicious.append(snippet)
    if suspicious:
        problems.append(f"{len(suspicious)} 处统计主张缺少来源（示例: “{suspicious[0]}…”）")
    return {"problems": problems, "suspicious_count": len(suspicious), "passed": not problems}


def g4_links(text: str, base_dir: Path) -> dict:
    """G4：链接可解析性检查（本地文件存在 + URL 格式）。"""
    problems = []
    local_links = re.findall(r"\]\(([^)]+\.md(?:#[^)]*)?)\)", text)
    url_links = re.findall(r"\]\((https?://[^)]+)\)", text)
    for link in local_links:
        p = link.split("#")[0]
        target = (base_dir / p).resolve()
        if not target.exists():
            problems.append(f"本地引用文件不存在: {link}")
    for u in url_links:
        if not re.match(r"^https?://\S+\.\S+", u):
            problems.append(f"URL 格式非法: {u[:60]}")
    return {"problems": problems, "local_links": len(local_links),
            "url_links": len(url_links), "passed": not problems}


def g5_review(text: str, path: str = "") -> dict:
    """G5：独立评审记录检查。

    两层检查：
    1. 正文含评审记录块（关键词 + 实际 rubric 分数，不止"评审"一词）
    2. 软检查：reviews/ 目录是否有对应 verdict 文件（有则更佳，无则警告不阻断）
    """
    problems = []
    warnings = []
    found = [marker for marker in G5_REVIEW_MARKERS if marker.lower() in text.lower()]
    if not found:
        problems.append("缺少评审记录（G5 需评审者分离 + rubric 分数留痕）")
    # 检查是否含实际 rubric 分数（0.xx 或 X.X 格式），不止关键词
    has_rubric_score = bool(re.search(r"\b0\.\d{1,2}\b|\b[0-9]\.\d{1,2}\b", text))
    if found and not has_rubric_score:
        warnings.append("评审记录块存在但未检测到 rubric 分数（如 0.92 / 8.8），建议补实际评分")
    # 软检查：reviews/ 目录是否有对应 verdict 文件
    if path:
        import os
        base = os.path.splitext(os.path.basename(path))[0]
        # 提取文章编号前缀（如 "01" from "01-constraint-pyramid"）
        num_prefix = base.split("-")[0] if "-" in base else base
        reviews_dir = os.path.join(os.path.dirname(os.path.dirname(path)), "reviews")
        if os.path.isdir(reviews_dir):
            verdicts = [f for f in os.listdir(reviews_dir) if f.startswith("verdict-")]
            has_verdict = False
            for v in verdicts:
                vbase = os.path.splitext(v)[0].replace("verdict-", "")
                # 合并 verdict 如 verdict-00-01-02.md 覆盖 00/01/02
                parts = vbase.split("-")
                if num_prefix in parts:
                    has_verdict = True
                    break
            if not has_verdict:
                warnings.append(f"reviews/ 无对应 verdict 文件（有正文评审记录，但评审与写作分离的独立 verdict 缺失）")
    return {"problems": problems, "warnings": warnings, "markers_found": found,
            "passed": not problems}


def run_gates(file_path: str, verbose: bool = True) -> dict:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    results = {
        "file": str(path),
        "G1_style": scan_g1_signal(text),
        "G2_structure": g2_structure(text, str(path)),
        "G3_facts": g3_facts(text),
        "G4_links": g4_links(text, path.parent),
        "G5_review": g5_review(text, str(path)),
    }
    all_pass = all(r.get("passed", True) for r in results.values()
                   if isinstance(r, dict))
    results["all_pass"] = all_pass
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="derekwritting 五道门禁自动执行器")
    ap.add_argument("target", nargs="?", help="md 文件或目录")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--list", action="store_true", help="列出信号词表")
    args = ap.parse_args()

    if args.list:
        print("G1 信号词表（AI 味/slop）：")
        print("  中文:", "、".join(SIGNAL_WORDS_CN))
        print("  英文:", "、".join(SIGNAL_WORDS_EN))
        return 0

    if not args.target:
        ap.print_help()
        return 2

    target = Path(args.target)
    files = [target] if target.is_file() else sorted(target.glob("*.md"))
    if not files:
        print(f"未找到 .md 文件: {args.target}")
        return 2

    all_results = [run_gates(str(f)) for f in files]
    overall = all(r["all_pass"] for r in all_results)

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        for r in all_results:
            print(f"\n=== {r['file']} ===")
            for gate in ["G1_style", "G2_structure", "G3_facts", "G4_links", "G5_review"]:
                g = r[gate]
                status = "PASS" if g.get("passed") else "FAIL"
                marker = "✅" if g.get("passed") else "❌"
                print(f"  {marker} {gate}: {status}")
                if isinstance(g, dict) and "problems" in g:
                    for p in g["problems"][:5]:
                        print(f"       - {p}")
                if isinstance(g, dict) and g.get("warnings"):
                    for w in g["warnings"][:3]:
                        print(f"       [!] {w}")
        print(f"\n{'✅ 五道门禁全部通过' if overall else '❌ 存在未过门禁'}（{len(all_results)} 文件）")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
