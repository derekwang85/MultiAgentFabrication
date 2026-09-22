#!/usr/bin/env python3
"""
writing-gates-en.py — derekwritting-evolution-en 六道英文门禁自动执行器（E1-E6）

对应 writing-harness/EVALUATION-EN.md。它管"这篇英文像不像 native 工程师写的"，是
中文版 writing-gates.py（G1-G5）的英文专属版，专注英文读者最敏感的四类问题：
  E1 slop 门禁:  英文 AI 味词/slop 扫描（密度），harness 品牌词豁免但要求首次定义
  E2 translationese 门禁:  中式英语句式检测（according to my opinion / perform an analysis 等）
  E3 first-screen 门禁:  首屏亮牌检查（开头 3 句内给出"问题+读者+主张"）
  E4 evidence 门禁:  强主张可验证检查（统计需来源标记，如 [ORIGINAL DATA] / 年份 / 出处）
  E5 localization 门禁:  素材本地化检查（中文典故残留、Drucker 伪名言拦截）
  E6 review 门禁:  独立母语评审记录检查（英语母语审校 + 剩留问题留痕）

用法:
  python writing-gates-en.py <file.md>            # 单文件
  python writing-gates-en.py <dir>                # 目录内所有 .en.md
  python writing-gates-en.py <file.md> --json     # JSON 输出
  python writing-gates-en.py --list               # 列出信号词表

退出码: 0 = 六道全过; 1 = 有门禁未过; 2 = 用法错误
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── 门禁阈值 ──────────────────────────────────────────────
E1_DENSITY_THRESHOLD = 4.0   # slop 词密度 / 千词（英文稿阈值略低于中英混合稿）
E1_HARNESS_DEF_WINDOW = 600  # harness 品牌词必须在开头 600 词内出现明确定义（steer/restrain/约束）

# ── E1 slop 词表（英文 AI 味，来自手册 S3.1；比 writing-gates.py 的英文清单更全）──
SLOP_WORDS = [
    # 标志性动词
    "delve", "delve into", "leverage", "utilize", "navigate", "unlock",
    "streamline", "harness the power", "dive into", "circle back", "touch base",
    # 空泛修饰
    "comprehensive", "robust", "seamless", "cutting-edge", "state-of-the-art",
    "groundbreaking", "revolutionary", "innovative", "game-changer", "holistic",
    "ever-evolving", "fast-paced",
    # 陈词滥调比喻/名词
    "tapestry", "in the realm of", "landscape", "paradigm-shift", "ecosystem",
    "empower", "granular", "synergy", "paramount", "underscore", "holistic",
    # 清嗓子开头
    "in today's", "in an era defined", "in this ever", "it is important to note",
    "it is worth noting", "notably", "in conclusion", "furthermore", "moreover",
    "additionally",
    # 滥用连接/口头承诺
    "that being said", "great question", "feel free to", "i hope this helps",
    "let's dive", "in summary", "to summarize",
]
# 硬豁免：harness 作为品牌词出现（不含 "harness the power" 这类 slop 用法）
BRAND_SLOPS = {"harness"}

# ── E2 translationese 中式英语句式 ──
TRANSLATIONESE = [
    "according to my opinion", "based on my opinion", "in my opinion, i",
    "according to me", "perform an analysis of", "do an analysis of",
    "make a progress", "make a discussion", "we will now discuss",
    "let us now", "this paper will", "this blog will", "as we all know",
    "we can see that", "i very like", "more and more people",
    "with the development of", "the reason is because", "regarding the",
    "as is well-known", "it goes without saying",
]
# 空泛加强词 + 无数字（"significantly improve" 而没有可指认数字）
WEAK_BOOSTERS = ["significantly", "greatly", "dramatically", "highly", "extremely", "tremendously", "vastly"]
# 中文标点残留（全角，说明直接粘贴中文）
CN_PUNCT = ["，", "。", "：", "；", "（", "）", "“", "”", "《", "》", "！", "？", "、"]
CN_CHAR_RE = re.compile(r"[\u4e00-\u9fff]")

# ── E3 empty-opener / 首屏 ──
E3_META_OPENERS = [
    "welcome to", "in this essay", "in this article", "in this post", "this essay will",
    "this article will", "i wanted to share", "today i", "let me take you", "have you ever",
]

# ── E4 强主张 / 统计模式 ──
E4_STRONG_STAT_RE = re.compile(r"(\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*(?:x|×)\b|\d+(?:\.\d+)?\s*倍|\b\d+(?:\.\d+)?\s*(?:ms|s|sec|minutes|hours|days)\b)")
E4_SOURCE_MARKERS = [
    "[ORIGINAL DATA]", "[PERSONAL EXPERIENCE]", "according to", "as of", "in " + "20", "report",
    "study", "survey", "benchmark", "measur", "git", "commit", "log", "repo", "github", "README",
]

# ── E5 本地化残留（中文典故直译 / 伪名言）──
E5_CN_ALLUSION = ["qi", "tcm", "sun tzu", "zhongyi", "将功", "船长又", "按摩鱼", "抛砖引玉"]
# 伪名言拦截（Drucker 没有说过的）
E5_FAKE_QUOTES = [
    "what gets measured gets managed",
    "you can't manage what you don't measure",
    "if you can't measure it, you can't manage it",
]

# ── E6 评审留痕 ──
E6_REVIEW_MARKERS = ["reviewed by", "native", "english", "rubric", "remaining issues", "剩留", "native review", "mother tongue"]

# ── 阈值辅助 ──
BRAND_DEF_WORDS = ["steer", "restrain", "constraint", "fence", "bound", "limit", "tame", "taming", "驾驭", "约束"]


def english_word_count(text: str) -> int:
    """英文词数（对英文稿的密度分母）。"""
    return len(re.findall(r"[A-Za-z']+", text))


def e1_slop(text: str) -> dict:
    """E1：slop 词密度 + harness 首次定义检查。"""
    hits = []
    lowered = text.lower()
    for word in SLOP_WORDS:
        if word in BRAND_SLOPS:
            continue
        count = len(re.findall(re.escape(word), lowered))
        if count:
            hits.append((word, count))
    total = sum(c for _, c in hits)
    words = english_word_count(text)
    density = (total * 1000.0 / words) if words else 0.0

    # harness 品牌词：全文需有"至少一处"显式定义（steer/restrain/constraint/tame 等）。
    # 允许开篇以钩子提一次（native 惯例），只要后文在 E1_HARNESS_DEF_WINDOW 词内给出定义即算通过。
    prob = []
    harness_hits = [m.start() for m in re.finditer(r"\bharness(?!es)\b", lowered)]
    any_defined = False
    for pos in harness_hits:
        window = text[max(0, pos - 150):pos + 250]
        if any(w in window.lower() for w in BRAND_DEF_WORDS):
            any_defined = True
            break
    if harness_hits and not any_defined:
        prob.append("harness 品牌词出现但全文无任意一处定义（steer/restrain/constraint/tame/fence 等），需在后文显式定义")
    if density >= E1_DENSITY_THRESHOLD:
        prob.append(f"slop 词密度 {density:.1f}/千词 ≥ 阈值 {E1_DENSITY_THRESHOLD}（示例: {hits[0][0]}）")
    return {
        "hits": hits, "total": total, "word_count": words,
        "density_per_1k": round(density, 1), "harness_defined": any_defined,
        "problems": prob, "passed": not prob,
    }


def e2_translationese(text: str) -> dict:
    """E2：中式英语句式/中文标点残留。"""
    prob, details = [], []
    lowered = text.lower()
    for phrase in TRANSLATIONESE:
        if phrase in lowered:
            details.append(phrase)
    # 中文标点残留（英文稿不应有全角标点）
    for p in CN_PUNCT:
        if p in text:
            details.append(f"中文标点 {p}")
    # 弱加强词：出现在句子中且后 40 词内无数字 → 空泛
    for boost in WEAK_BOOSTERS:
        for m in re.finditer(rf"\b{boost}\b", lowered):
            window = text[m.end():m.end() + 60]
            if not re.search(r"\d", window):
                details.append(f"空泛加强词 {boost}")
                break  # 每词记一次即可
    if details:
        prob.append(f"发现翻译腔/中文残留: {', '.join(details[:6])}")
    return {"problems": prob, "details": details[:10], "passed": not prob}


def e3_first_screen(text: str) -> dict:
    """E3：首屏亮牌。开头不空泛（不以"本文将"清嗓子），且前 60 词内有主动语态的具体主张。"""
    prob = []
    head = re.sub(r"^#.*\n", "", text, flags=re.M).strip()
    lowered_head = head[:400].lower()
    for opener in E3_META_OPENERS:
        if lowered_head.startswith(opener):
            prob.append(f"清嗓子开头: '{opener}' — 第一屏未直接亮主张")
            break
    # 主动语态检测：前 60 词内先出现"可作主语的具象名词（抽出动词前的实词）"，再命中一个强主动动词。
    # 刻意不用硬编码主语白名单——native 开篇"a roomful of the world's best programmers admitted…"同样成立。
    first_3 = " ".join(head.split()[:60])
    strong_verbs = [
        "admitted|found|built|hit|learned|discovered|noticed|realized|wrote|shipped|tamed|flipped|changed",
        "showed|revealed|proved|broke|exploded|collapsed|slipped|blew",
    ]
    # 命中任意强动词，且其前有名词性主体（动词前 2~8 词内存在非介词开头的实词群）
    def agent_before_verb(m):
        pre = first_3[: m.start()]
        pre_words = re.findall(r"[A-Za-z']+", pre)
        if not pre_words:
            return False
        # 若主语是 "There is/are"、"It is" 等存在句/形式主语则不算具象主张
        if re.search(r"\b(there|it)\s+(is|are|was|were)$", pre, re.IGNORECASE):
            return False
        tail = pre_words[-4:]  # 动词前最近 4 个词里应含名词性主体
        return any(re.search(r"'s$|\b[A-Z]", w) or len(w) > 3 for w in tail)
    m = re.search(r"\b(" + "|".join(strong_verbs) + r")\b", first_3, re.IGNORECASE)
    has_active_verb = bool(m) and agent_before_verb(m)
    if not has_active_verb:
        prob.append("首屏 60 词内缺少主动语态主张（读者不知道这是谁、对谁、主张什么）")
    return {"problems": prob, "checks": {"has_active_claim": has_active_verb}, "passed": not prob}


def e4_evidence(text: str) -> dict:
    """E4：强主张可验证。统计/数据类出现但无来源标记 → 疑点。"""
    suspicious, prob = [], []
    for m in E4_STRONG_STAT_RE.finditer(text):
        start, end = m.start(), m.end()
        # 跳过引号内举例
        ctx = text[max(0, start - 120):start]
        if any(x in ctx[-30:] for x in ("“", '"', "e.g.", "like")):
            continue
        window = text[max(0, start - 100):start + 120]
        has_src = any(mk.lower() in window.lower() for mk in E4_SOURCE_MARKERS)
        if not has_src:
            snippet = text[max(0, start - 30):end + 40].replace("\n", " ")
            suspicious.append(snippet)
    if suspicious:
        prob.append(f"{len(suspicious)} 处数据/强主张缺来源（示例: '{suspicious[0][:60]}…'）")
    return {"problems": prob, "suspicious_count": len(suspicious), "passed": not prob}


def e5_localization(text: str) -> dict:
    """E5：素材本地化 + 伪名言拦截。"""
    prob, details = [], []
    lowered = text.lower()
    for quote in E5_FAKE_QUOTES:
        if quote in lowered:
            details.append(f"⚠ 伪名言拦截: '{quote}' — Drucker 从未说过，需替换为可考引文或改论证")
    for al in E5_CN_ALLUSION:
        if al in lowered:
            details.append(f"中文典故可能残留直译: '{al}'")
    # 中文汉字残留（英文稿不应出现的中文主体）
    cn_chars = CN_CHAR_RE.findall(text)
    if len(cn_chars) > 3:
        details.append(f"出现 {len(cn_chars)} 个中文字符（可能未本地化）")
    if details:
        prob.append("; ".join(details[:6]))
    return {"problems": prob, "details": details[:8], "passed": not prob}


def e6_review(text: str) -> dict:
    """E6：独立母语评审留痕。"""
    found = [m for m in E6_REVIEW_MARKERS if m.lower() in text.lower()]
    prob = []
    if not found:
        prob.append("缺少独立母语评审留痕（需包含 reviewed by native / English / rubric / remaining issues）")
    return {"problems": prob, "markers_found": found, "passed": not prob}


def run_gates(file_path: str) -> dict:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    results = {
        "file": str(path),
        "E1_slop": e1_slop(text),
        "E2_translationese": e2_translationese(text),
        "E3_first_screen": e3_first_screen(text),
        "E4_evidence": e4_evidence(text),
        "E5_localization": e5_localization(text),
        "E6_review": e6_review(text),
    }
    results["all_pass"] = all(r.get("passed", True) for r in results.values() if isinstance(r, dict))
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="derekwritting-evolution-en 六道英文门禁执行器")
    ap.add_argument("target", nargs="?", help="md 文件或目录")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--list", action="store_true", help="列出 slop 词表")
    args = ap.parse_args()

    if args.list:
        print("E1 slop 词表（英文 AI 味）：")
        print("  ", "、".join(sorted(set(SLOP_WORDS))))
        print("\nE2 translationese 句式（中文直译）：")
        print("  ", "、".join(TRANSLATIONESE))
        return 0

    if not args.target:
        ap.print_help()
        return 2

    target = Path(args.target)
    files = [target] if target.is_file() else sorted(target.glob("*.en.md"))
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
            for gate in ["E1_slop", "E2_translationese", "E3_first_screen", "E4_evidence", "E5_localization", "E6_review"]:
                g = r[gate]
                status = "PASS" if g.get("passed") else "FAIL"
                print(f"  {'✅' if g.get('passed') else '❌'} {gate}: {status}")
                for p in g.get("problems", [])[:5]:
                    print(f"       - {p}")
        print(f"\n{'✅ 六道英文门禁全部通过' if overall else '❌ 存在未过门禁'}（{len(all_results)} 文件）")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())