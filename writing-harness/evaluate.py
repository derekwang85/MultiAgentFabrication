#!/usr/bin/env python3
"""evaluate.py — AI Harness 系列文章评估体系的可执行工具。

数据源：writing-harness/evaluation-scoreboard.json
规则（见 writing-harness/EVALUATION.md）：
  新文章写作水平必须超过前序文章平均分（基准线）。
  每次新文或重写录入后，自动重算滚动平均，作为下一篇的目标。

用法：
  python evaluate.py --list                 # 打印分数板与前序平均分
  python evaluate.py --next [--exclude key] # 打印下一篇目标分；--exclude 剔除仍待入库的当前篇目，
                                            # 使基准严格等于“前 N-1 篇累计均分”
  python evaluate.py --recalib              # 逐篇回放前序累计均分，审计历史基线是否存在滞后
  python evaluate.py --record articles/XX.md --score 8.7 [--breakthrough 维度] [--note 注]
                                            # 录入新文章，重算均分，校验是否达标
  python evaluate.py --update articles/XX.md [--score 8.8] [--breakthrough ...] [--note ...]
                                            # 更新既有文章（记录历史）
  python evaluate.py --check                # 校验数据源结构与规则一致性
"""

import argparse
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SCOREBOARD = os.path.join(HERE, "evaluation-scoreboard.json")

VALID_DIMS = ["遣词造句", "经典案例", "名言名句引用"]


def now_str():
    return date.today().isoformat()


def load():
    with open(SCOREBOARD, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(SCOREBOARD, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[写盘] {SCOREBOARD}")


def average(articles):
    if not articles:
        return 0.0
    return round(sum(a["score"] for a in articles) / len(articles), 2)


def exclude_key(articles, exclude):
    """返回剔除指定篇目后的文章列表；exclude 为空字符串时原样返回。

    exclude 支持篇目 key、文件名、相对路径三种写法（与 find 口径一致）。
    未命中时给出提示但不报错——避免录入顺序干扰。
    """
    if not exclude:
        return articles
    arts = [a for a in articles if not (
        a["key"] == exclude
        or a["file"] == exclude
        or os.path.basename(a["file"]) == exclude
    )]
    if len(arts) == len(articles):
        print(f"[提示] --exclude '{exclude}' 未匹配任何篇目，按全量计算。")
    return arts


def find(articles, key):
    for a in articles:
        if a["key"] == key or a["file"] == key or os.path.basename(a["file"]) == key:
            return a
    return None


def rule_check(new_score, avg):
    # 主导规则：每篇锁定 9.5-9.9 目标带；相对前序均分采用“不低于”（>=）而非“严格大于”（>）。
    # 若超过 9.9 上沿，视为越界告警（宽松通过但提示）。
    ok = new_score >= avg
    status = "PASS" if ok else "FAIL"
    over_band = new_score > 9.9
    band_note = "，越上沿告警" if over_band else ""
    print(f"  判定：分数 {new_score} 对基准 {avg} -> {status}（须不低于）{band_note}")
    return ok


def cmd_list(data):
    arts = data["articles"]
    print("=== AI Harness 文章评估分数板 ===")
    h = "篇目", "分数", "状态", "日期"
    print(f"{h[0]:<28}{h[1]:<8}{h[2]:<10}{h[3]}")
    print("-" * 70)
    for a in arts:
        print(f"{a['title'] + ' (' + a['key'] + ')':<30}{str(a['score']):<8}{a['status']:<12}{a['date']}")
    avg = average(arts)
    print("-" * 70)
    print(f"前序文章平均分（基准线）：{avg}")
    print(f"下篇目标分：锁定 9.5-9.9 带，向带内上沿递进；且不低于前均 {avg}")


def cmd_next(data, args):
    arts = exclude_key(data["articles"], getattr(args, "exclude", "") or "")
    avg = average(arts)
    print(f"基准口径：{'剔除 --exclude 篇目后' if args.exclude else '全部已入库篇目'}的累计均分")
    print(f"前序平均分（基准线）：{avg:.2f}")
    print(f"下一篇目标分：锁定 9.5-9.9 目标带，向 9.9 收敛；相对前均 {avg:.2f} 采用不低于（>=）")
    print("突破维度（至少标注 1 项）：" + " / ".join(VALID_DIMS))


def cmd_recalib(data):
    """重算校准：按“每篇评分 > 其前序累计均分”逐篇回放验证口径。

    严格按分数板当前顺序逐篇累计，输出每一篇被录入时的正确基准与判定，
    用于审计历史是否存在基线滞后（如第 9 篇仍以第 7 篇后的 8.55 为基准）。
    """
    arts = data["articles"]
    print("--- 重算校准：前序累计均分回放 ---")
    print(f"{'篇目':<30}{'评分':<8}{'前序累计均分':<12}{'判定'}")
    print("-" * 66)
    cum = 0.0
    for i, a in enumerate(arts):
        if i == 0:
            base_prev = 0.0
        else:
            base_prev = round(cum / i, 2)
        ok = a["score"] > base_prev
        status = "PASS" if ok else "FAIL"
        print(f"{a['key']:<30}{str(a['score']):<8}{str(base_prev):<12}{status}（须>{base_prev}）")
        cum += a["score"]
    final_avg = round(cum / len(arts), 2)
    print("-" * 66)
    print(f"最终累计平均分：{final_avg}")
    print("注：首篇无前序，基准记 0.0；序号按分数板当前顺序。")


def cmd_record(data, args):
    arts = data["articles"]
    target_key = os.path.splitext(os.path.basename(args.target))[0]
    if find(arts, target_key):
        print(f"[错误] {args.target} 已存在。新增请用 --record，修改用 --update。")
        sys.exit(1)
    if args.score < 0 or args.score > data["system"]["scale_max"]:
        print(f"[错误] 分数须在 0 ~ {data['system']['scale_max']} 之间。")
        sys.exit(1)
    print("--- 录入前检查 ---")
    avg = average(arts)
    rule_check(args.score, avg)
    arts.append({
        "key": target_key,
        "title": args.title or target_key,
        "file": args.target,
        "score": args.score,
        "status": "样稿待审",
        "date": args.date or now_str(),
        "breakthrough": args.breakthrough or "",
        "note": args.note or "",
    })
    arts.sort(key=lambda a: a["key"])
    new_avg = average(arts)
    data["updated"] = now_str()
    save(data)
    print(f"\n--- 已录入 {args.target}，分数 {args.score} ---")
    print(f"新平均分（含本篇）：{new_avg}（仅含历史篇目时为基准线）")


def cmd_update(data, args):
    arts = data["articles"]
    target_key = os.path.splitext(os.path.basename(args.target))[0]
    a = find(arts, target_key)
    if not a:
        print(f"[错误] 未找到 {args.target}。请用完整路径或篇目 key。")
        sys.exit(1)
    prev = a["score"]
    if args.score is not None:
        if args.score < 0 or args.score > data["system"]["scale_max"]:
            print(f"[错误] 分数须在 0 ~ {data['system']['scale_max']} 之间。")
            sys.exit(1)
        if "score_history" not in a:
            a["score_history"] = []
        a["score_history"].append([str(prev), a["date"], a.get("note", "")])
        a["score"] = args.score
        a["date"] = now_str()
    if args.breakthrough:
        a["breakthrough"] = args.breakthrough
    if args.note:
        a["note"] = args.note
    if not (args.score is None and args.breakthrough is None and args.note is None):
        a["status"] = "样稿待审" if args.status is None else args.status
        print(f"--- 已更新 {args.target} ：{prev} -> {a['score']} ---")
        # 重算均分（全部已评篇目）
        avg = average(arts)
        print(f"重写后基准线更新：{prev:.2f} 变化后，当前全部文章平均 = {avg}")
        if args.score is not None:
            rule_check(args.score, avg)
        data["updated"] = now_str()
        save(data)
    else:
        print("[提示] 未提供任何变更字段，跳过。")


def ratchet_failures(data):
    """逐篇回放棘轮规则：每篇评分须严格大于其前序累计均分。
    返回 [(key, score, baseline_at_that_point), ...] 的失败列表。
    用于审计历史基线漂移（如序章升级后，早期篇目可能对新基线不达标）。
    """
    arts = data["articles"]
    failures = []
    cum = 0.0
    for i, a in enumerate(arts):
        if i == 0:
            base_prev = 0.0
        else:
            base_prev = round(cum / i, 2)
        if not (a["score"] >= base_prev):  # 主导规则：不低于前序均分
            failures.append((a["key"], a["score"], base_prev))
        cum += a["score"]
    return failures


def cmd_check(data):
    arts = data["articles"]
    errs = []
    avg = average(arts)
    print(f"--- 数据源校验（{SCOREBOARD}）---")
    print(f"系统分制：0 ~ {data['system']['scale_max']}")
    print(f"文章数：{len(arts)}，平均分：{avg}")
    for a in arts:
        if not (0 <= a["score"] <= data["system"]["scale_max"]):
            errs.append(f"  [{a['key']}] 分数越界 {a['score']}")
        if not a.get("breakthrough"):
            errs.append(f"  [{a['key']}] 缺少突破维度注记（breakthrough）")
    # 棘轮一致性校验（P0-1）：早期篇目可能因后续篇目升级导致基线漂移
    ratchet_fails = ratchet_failures(data)
    if ratchet_fails:
        print("\n--- 棘轮一致性校验（ratchet）---")
        for key, score, base in ratchet_fails:
            print(f"  [{key}] 评分 {score} <= 当前前序基线 {base}（基线漂移，需复核或重写提分）")
    if errs:
        print("\n发现问题：")
        for e in errs:
            print(e)
        sys.exit(1)
    if ratchet_fails:
        print("\n[棘轮警告] 以下篇目对当前基线不再达标（非阻断，但需关注）：")
        print("棘轮规则：每篇须严格大于其前序累计均分。基线漂移说明早期篇目")
        print("在后续篇目升级后可能不再达标——建议重写提分或在 score_history 记录打分时基线。")
        # 棘轮警告不 exit(1)，只警告——基线漂移是历史合规但当前需复核，不是数据错误
    else:
        print("校验通过（含棘轮一致性）。")

    # 门禁脚本完整性校验（P2-12）：harness-sync.json 记录门禁脚本的 md5，
    # 防止门禁被悄悄修改放水。修改门禁脚本后须同步更新 harness-sync.json。
    import hashlib
    sync_path = os.path.join(HERE, "harness-sync.json")
    if os.path.exists(sync_path):
        import json as _json
        sync = _json.load(open(sync_path, "r", encoding="utf-8"))
        sync_warns = []
        for fpath, expected_md5 in sync.items():
            if fpath.startswith("_"):
                continue
            full = os.path.join(os.path.dirname(HERE), fpath)
            if os.path.exists(full):
                actual = hashlib.md5(open(full, "rb").read()).hexdigest()
                if actual != expected_md5:
                    sync_warns.append(f"  [{fpath}] md5 不匹配（期望 {expected_md5[:8]}...，实际 {actual[:8]}...）")
        if sync_warns:
            print("\n--- 门禁脚本完整性校验（harness-sync.json）---")
            for w in sync_warns:
                print(w)
            print("（门禁脚本已修改但 harness-sync.json 未同步——修改后请更新 md5）")
        else:
            print("门禁脚本完整性：harness-sync.json 校验通过。")


def cmd_verify_doc(data):
    """校验 JSON 分数板与 docs/article-evaluation-system.md 人类可读表的一致性。

    检查每个文章的 score 在 JSON 和 markdown 表中是否一致（同一行），
    报告不匹配的篇目（单一事实来源是 JSON，markdown 应同步）。
    """
    import re
    doc_path = os.path.join(os.path.dirname(HERE), "docs", "article-evaluation-system.md")
    if not os.path.exists(doc_path):
        print(f"[错误] 找不到 {doc_path}")
        sys.exit(1)
    doc_lines = open(doc_path, "r", encoding="utf-8").readlines()
    arts = data["articles"]
    mismatches = []
    checked = 0
    for a in arts:
        key = a["key"]
        score = str(a["score"])
        fname = a["file"].replace("articles/", "")
        # 在 markdown 中搜索包含 key 或文件名的行，检查同行是否有分数
        found = False
        for line in doc_lines:
            if key in line or fname in line:
                # 检查同行是否有该分数（允许 ** 包裹、→ 前缀等格式）
                if re.search(r"\b" + re.escape(score) + r"\b", line):
                    found = True
                    break
        if found:
            checked += 1
        else:
            # 搜索 key 是否在文档中出现
            doc_text = "".join(doc_lines)
            if key in doc_text or fname in doc_text:
                mismatches.append((key, score, "篇目在文档中出现但同行分数不匹配"))
            else:
                mismatches.append((key, score, "篇目在文档中未找到"))
    print("--- 文档一致性校验（JSON vs docs/article-evaluation-system.md）---")
    print(f"JSON 文章数：{len(arts)}，文档匹配：{checked}，不匹配：{len(mismatches)}")
    if mismatches:
        print("不一致项：")
        for key, score, reason in mismatches:
            print(f"  [{key}] JSON 分数 {score} — {reason}")
        print("（JSON 是唯一真值，请同步 docs/article-evaluation-system.md）")
    else:
        print("一致。")
    return len(mismatches) == 0


def main():
    parser = argparse.ArgumentParser(description="AI Harness 系列文章评估工具")
    parser.add_argument("--list", action="store_true", help="打印分数板与前序平均分")
    parser.add_argument("--next", action="store_true", help="打印下一篇目标分")
    parser.add_argument("--exclude", dest="exclude", help="计算基准时剔除的篇目（key/文件名/路径），用于‘写第 N 篇时按前 N-1 篇累计’")
    parser.add_argument("--recalib", action="store_true", help="重算校准：逐篇回放前序累计均分并复核判定")
    parser.add_argument("--record", dest="target", help="录入新文章的文件路径")
    parser.add_argument("--update", dest="update_target", help="更新既有文章的文件路径")
    parser.add_argument("--score", type=float, help="分数")
    parser.add_argument("--breakthrough", help="突破维度注记（自由文本，建议含一个规范维度：遣词造句 / 经典案例 / 名言名句引用）")
    parser.add_argument("--note", help="评分注记")
    parser.add_argument("--title", help="标题（record 时）")
    parser.add_argument("--date", help="日期 YYYY-MM-DD")
    parser.add_argument("--status", help="状态")
    parser.add_argument("--check", action="store_true", help="校验数据源（含棘轮一致性）")
    parser.add_argument("--verify-doc", action="store_true", help="校验 JSON 分数板与 docs/article-evaluation-system.md 人类可读表的一致性")
    args = parser.parse_args()

    if not os.path.exists(SCOREBOARD):
        print(f"[错误] 找不到分数板：{SCOREBOARD}")
        sys.exit(1)

    data = load()
    if args.list:
        cmd_list(data)
    elif args.next:
        cmd_next(data, args)
    elif args.recalib:
        cmd_recalib(data)
    elif args.check:
        cmd_check(data)
    elif args.verify_doc:
        ok = cmd_verify_doc(data)
        if not ok:
            sys.exit(1)
    elif args.target:
        cmd_record(data, args)
    elif args.update_target:
        args.target = args.update_target
        cmd_update(data, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()