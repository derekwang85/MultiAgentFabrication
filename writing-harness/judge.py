#!/usr/bin/env python3
"""
derekwritting-judge — 写作评测循环（Judge Loop）评分脚本

用途：
  1. LLM as Judge：把稿件交给 LLM，按 10 维 rubric 评分
  2. Best-of-N：生成 N 份候选，取最高分
  3. 门禁阈值检查：风格五维 <35/50 或 rubric 均值 <3.5/5 → FAIL

用法：
  python3 judge.py <input.md>              # 单篇评分（需 ANTHROPIC_API_KEY 或 LLM 通道）
  python3 judge.py --list                  # 列出 benchmark 样例
  python3 judge.py --selfcheck <file.md>   # 离线自检模式（无 API，人工打分）

Benchmark 回归：
  修改 prompt/skill 后运行 `python3 judge.py evals/cases/*.md` 对比分数，
  确保"写得好"的标准可回归、可对比、不退化。

依赖：仅标准库 + 可选 requests（若配置了 LLM API 通道）。
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------
# 配置：LLM 通道（按需填写）
# 支持环境变量：DEREKW_LLM_API / DEREKW_LLM_KEY / DEREKW_LLM_MODEL
# 若未配置，脚本进入 offline 模式，输出 rubric 表供人工打分。
# ---------------------------------------------------------------
LLM_API = os.environ.get("DEREKW_LLM_API", "")
LLM_KEY = os.environ.get("DEREKW_LLM_KEY", "")
LLM_MODEL = os.environ.get("DEREKW_LLM_MODEL", "")

# 10 维 rubric（与 methodology/06-judge-loop.md 一致）
RUBRIC_DIMS = [
    ("Clarity of Purpose", "目标明显且全程对齐"),
    ("Audience Specificity", "写给特定读者特定需求"),
    ("Point of View", "清晰可信的判断"),
    ("Specificity", "细节/约束/例子丰富"),
    ("Insight Density", "多个真正锐化认知的观察"),
    ("Structural Focus", "强调得当、节奏清晰"),
    ("Voice Credibility", "像真实作者有意图地说话"),
    ("Reader Usefulness", "帮读者行动/决策/理解"),
    ("Trustworthiness", "校准、可信、有界"),
    ("Memorability", "有留存的句子"),
]

# 风格五维（stop-slop 门禁 G1，每维 1-10，阈值 35/50）
STYLE_DIMS = ["Directness", "Rhythm", "Trust", "Authenticity", "Density"]

# 门禁阈值
GATE_STYLE_MIN = 35  # 风格五维总分阈值 /50
GATE_RUBRIC_MEAN = 3.5  # rubric 均值阈值 /5


def read_text(path: Path) -> str:
    if not path.exists():
        print(f"[ERROR] 文件不存在: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def extract_scores(text: str) -> dict:
    """从 LLM 返回文本中提取维度分数。格式：`维度: 分数` 一行一个。"""
    scores = {}
    for dim, _ in RUBRIC_DIMS + [(d, "") for d in STYLE_DIMS]:
        m = re.search(rf"{re.escape(dim)}\s*[:：]\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
        if m:
            scores[dim] = float(m.group(1))
    return scores


def call_llm(prompt: str) -> str:
    """调用配置的 LLM 通道。默认尝试 OpenAI 兼容端点；未配置返回空串（offline）。"""
    if not (LLM_API and LLM_KEY):
        return ""
    try:
        import requests  # 延迟导入，保持核心零依赖

        resp = requests.post(
            LLM_API,
            headers={"Authorization": f"Bearer {LLM_KEY}"},
            json={
                "model": LLM_MODEL or "gpt-4o",
                "messages": [
                    {"role": "system", "content": "你是严格的写作评审，只输出分数，不解释过程。"},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.0,
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] LLM 调用失败: {e}", file=sys.stderr)
        return ""


def build_prompt(text: str) -> str:
    dims_line = "\n".join(f"- {d}: 1-5 分（{desc}）" for d, desc in RUBRIC_DIMS)
    style_line = "\n".join(f"- {d}: 1-10 分" for d in STYLE_DIMS)
    return (
        "对以下稿件进行写作评审。严格按下列维度打分，每个维度单独一行输出 `维度: 分数`，"
        "不要解释过程。\n\n"
        f"Rubric 维度（1-5 分）：\n{dims_line}\n\n"
        f"风格维度（1-10 分）：\n{style_line}\n\n"
        "===== 稿件开始 =====\n"
        f"{text}\n"
        "===== 稿件结束 =====\n"
    )


def judge(text: str) -> dict:
    """执行评分。返回 {rubric: {dim: score}, style: {...}, gates: {...}}"""
    result = {"rubric": {}, "style": {}, "gates": {}, "offline": True}
    prompt = build_prompt(text)
    resp = call_llm(prompt)
    if not resp:
        print("[INFO] 未配置 LLM 通道，进入离线模式——输出 rubric 表，请人工打分。")
        for d, desc in RUBRIC_DIMS:
            print(f"  - {d} (1-5): {desc}")
        print("\n[INFO] 离线模式无法自动评分。请用 --selfcheck 或配置 DEREKW_LLM_API/KEY。")
        result["offline"] = True
        return result

    scores = extract_scores(resp)
    result["offline"] = False
    for d, _ in RUBRIC_DIMS:
        result["rubric"][d] = scores.get(d)
    for d in STYLE_DIMS:
        result["style"][d] = scores.get(d)

    # 门禁判断
    style_vals = [v for v in result["style"].values() if v is not None]
    rubric_vals = [v for v in result["rubric"].values() if v is not None]
    style_total = sum(style_vals)
    rubric_mean = sum(rubric_vals) / len(rubric_vals) if rubric_vals else 0
    result["gates"] = {
        "style_total": style_total,
        "style_pass": style_total >= GATE_STYLE_MIN,
        "rubric_mean": round(rubric_mean, 2),
        "rubric_pass": rubric_mean >= GATE_RUBRIC_MEAN,
    }
    return result


def report(result: dict, name: str = "") -> int:
    if result.get("offline"):
        return 1
    title = f" 评审报告: {name}" if name else "评审报告"
    print(f"\n=== {title} ===")
    for d, v in result["rubric"].items():
        print(f"  rubric  {d:<24} {v}")
    for d, v in result["style"].items():
        print(f"  style   {d:<24} {v}")
    g = result["gates"]
    print(f"\n  风格总分 {g['style_total']}/50  → {'PASS' if g['style_pass'] else 'FAIL'}")
    print(f"  rubric 均值 {g['rubric_mean']}/5 → {'PASS' if g['rubric_pass'] else 'FAIL'}")
    return 0 if (g["style_pass"] and g["rubric_pass"]) else 1


def main():
    ap = argparse.ArgumentParser(description="derekwritting judge loop")
    ap.add_argument("files", nargs="*", help="输入 .md 稿件")
    ap.add_argument("--list", action="store_true", help="列出 benchmark 样例")
    ap.add_argument("--selfcheck", metavar="FILE", help="离线自检：给出 rubric 表供人工打分")
    args = ap.parse_args()

    evals_dir = Path(__file__).parent / "cases"

    if args.list:
        for p in sorted(evals_dir.glob("*.md")):
            print(f"  {p.name}")
        return 0

    if args.selfcheck:
        text = read_text(Path(args.selfcheck))
        judge(text)
        return 0

    if not args.files:
        print("用法: python3 judge.py <input.md> | --list | --selfcheck <file.md>")
        return 1

    rc = 0
    for f in args.files:
        text = read_text(Path(f))
        result = judge(text)
        rc = max(rc, report(result, name=Path(f).name))
    return rc


if __name__ == "__main__":
    sys.exit(main())
