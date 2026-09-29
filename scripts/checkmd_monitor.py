# -*- coding: utf-8 -*-
"""
checkmd_monitor.py
==================
MD 文件变化后台监控器（写作经验沉淀流水线的"检测 + 总结"段）。

用途
----
被 TRAE 自定义命令 /checkmd <project> <timer> <duration> 调用，针对
一个指定文件夹（默认 <project>/publish）内的 .md 文件做周期性变化检测：
每 <timer> 分钟一次，持续 <duration> 天，窗口结束自动退出。

对每次检测到的变化（新增 / 修改 / 删除），脚本生成两样产物：
  1) 一份"变化总结报告"（面向人的阅读稿）；
  2) 一份"写作技巧落库草稿" `.draft.md`（遵循项目 wiki 四段结构）。
两者都写到"待确认区"，**不会**直接写入 `wiki/concepts/`——落库需要 HITL
人工确认（对齐项目 wiki 元规约 AGENTS.md §六失败安全：AI 只产出草稿，
定稿写入必须人工确认）。

设计原则（对齐用户规则）
--------------------
- 纯标准库，零第三方依赖：对项目非侵入。
- "持续 duration 天自动停止"由脚本内部持有到期时间控制，而非 cron
  （cron 只能表达无限期周期，无法表达一次性窗口）。
- 会话状态 JSON（快照 + 到期），脚本中断可续跑；也可通过删除会话文件
  或提前 -k 来安全停止。
- 幂等：重复执行同一周期不会重复写草稿（用 hash 快照去重）。

用法
----
检查 publish 目录，每 30 分钟一次、持续 3 天（后台常驻）：
    python scripts/checkmd_monitor.py --interval 30 --duration 3 --once=0

只检查一次（便于测试 / 用 Schedule cron 手动调）：
    python scripts/checkmd_monitor.py --interval 30 --duration 3 --once

参数
----
--project     项目根目录（绝对路径）。默认当前工作目录。
--target-html <project>/publish 是默认发布正文目录；如需改传相对或绝对路径。
--interval    检查间隔（分钟），默认 30。
--duration    持续天数，默认 3。到期后脚本自动退出。
--once        只检查一个周期后退出（不循环）。
--session-dir 会话状态与待确认产物存放目录。默认 <project>/.checkmd/<会话名>。
--name        会话名，用于隔离多次监控任务。默认 "mdwatch"。
--dry-run     只检测与报告，不写任何草稿文件（用于验证/演练）。
--check       快速自检：验证目标目录可读、参数合法，立即退出。
"""
import argparse
import hashlib
import json
import os
import sys
import time
import datetime as dt

# ---------------------------------------------------------------------------
# 常量与默认
# ---------------------------------------------------------------------------
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NOCHANGE = 0


def _log(msg):
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[checkmd {ts}] {msg}"
    # 同时写控制台与会话日志（会话日志由调用方落盘）
    print(line, flush=True)


def sha256_of(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except OSError:
        return None
    return h.hexdigest()


def md_files_under(root):
    """递归收集 root 下所有 .md/.markdown 文件（绝对路径）。跳过隐藏目录。"""
    result = []
    if not os.path.isdir(root):
        return result
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith((".md", ".markdown")):
                result.append(os.path.join(dirpath, fn))
    result.sort()
    return result


def fingerprint(files):
    """为每个文件生成 sha256+mtime 指纹；返回 {abs_path: {hash, mtime}}。"""
    snap = {}
    for p in files:
        hs = sha256_of(p)
        if hs is None:
            continue
        try:
            mt = os.path.getmtime(p)
        except OSError:
            mt = 0.0
        snap[p] = {"hash": hs, "mtime": mt}
    return snap


def diff_snapshot(before, after):
    """对比快照，返回 (added[], modified[], deleted[])。"""
    b_keys = set(before)
    a_keys = set(after)
    added = sorted(a_keys - b_keys)
    deleted = sorted(b_keys - a_keys)
    modified = []
    for k in sorted(a_keys & b_keys):
        if before[k]["hash"] != after[k]["hash"]:
            modified.append(k)
    return added, modified, deleted


def extract_insight(path):
    """从一篇 MD 里粗略提取可能的写作技巧信号，产出结构化行。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        text = ""
    if not text:
        return {"length": 0, "headlines": [], "units": 0}
    lines = text.splitlines()
    headlines = [l.strip().lstrip("#").strip() for l in lines if l.lstrip().startswith("#")][:8]
    # 统计"可用于沉淀"的结构单元：小节、引用块、编号列表
    units = sum(1 for l in lines if l.strip().lstrip().startswith(("#", ">", "- [", "1.", "1、")))
    return {"length": len(text), "headlines": headlines, "units": units}


def write_draft(session_dir, rel_path, change_kind, insight, report_path):
    """生成一份符合 wiki 四段结构的写作技巧落库草稿 .draft.md 到 drafts/。

    遵循 AGENTS.md 四段结构（定义 / 证据出处 / 相关概念 / 内化级别），
    但不复制原文，且明确标注 source。返回草稿路径。
    """
    drafts_dir = os.path.join(session_dir, "concepts-drafts")
    os.makedirs(drafts_dir, exist_ok=True)
    slug = os.path.basename(rel_path).replace(".", "-").lower()
    draft_path = os.path.join(drafts_dir, f"{slug}.{change_kind}.draft.md")

    kind_cn = {"added": "新增", "modified": "修订", "deleted": "删除"}.get(change_kind, change_kind)
    insight_meta = ""
    if insight:
        insight_meta = (
            f"- 篇幅：{insight['length']} 字符\n"
            + f"- 结构单元数（章节/列表/引用）：{insight['units']}\n"
            + ("- 主要小节：" + "、".join(insight["headlines"]) if insight["headlines"] else "- 主要小节：无显式标题")
        )
    blueprint = (
        f"# 待命名写作技巧 (DRAFT)\n"
        f"> **一句话定义**：〔待人工提炼，指向一个可复用的写作/工程决策〕\n"
        f"> 来源：`{rel_path}`（{kind_cn}）via checkmd\n"
        f"> 相关：[[experience-retention]] [[knowledge-as-asset]]\n"
        f"> 实证：`{rel_path}`\n\n"
        f"## 定义\n\n〔根据本次 {kind_cn} 的内容，用一句话概括可沉淀的写作技巧。\n"
        f"不复制原文，只提炼约束哪个写作/工程决策。〕\n\n"
        f"## 证据出处\n\n- 变更文件：`{rel_path}`（{kind_cn}）\n"
        f"- 检测时间：{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- 变更报告：`{os.path.relpath(report_path, session_dir)}`\n\n"
        f"## 相关概念\n\n- [[experience-retention]]\n- [[knowledge-as-asset]]\n\n"
        f"## 内化级别\n\n- 〔A 强内化 / B 弱内化〕（由 HITL 判定）\n\n"
        f"## 待确认字段（HITL）\n\n- 概念名：\n- 一句话定义：\n- 内化级别：\n- 来源补证：\n\n"
        f"---\n\n*本草稿由 checkmd 自动生成，未定稿，不参与导航。人工确认后按 wiki 元规约 W1-W4 定稿移入 `wiki/concepts/` 并在 `wiki/log.md` 留痕。*\n"
    )
    body = f"## 自动提取信号\n\n{insight_meta}\n\n---\n\n{blueprint}"
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(body)
    return draft_path


def load_state(session_state_path):
    if os.path.exists(session_state_path):
        try:
            with open(session_state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def save_state(session_state_path, state):
    os.makedirs(os.path.dirname(session_state_path), exist_ok=True)
    tmp = session_state_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, session_state_path)  # 原子替换，防并发损坏


def resolve_target(args, project_root):
    """把 target_dir 解析为绝对路径。支持相对 publish 或绝对路径。"""
    if os.path.isabs(args.target):
        return args.target
    cand = os.path.join(project_root, args.target)
    if os.path.isdir(cand):
        return cand
    # 尝试直接当相对当前目录
    if os.path.isdir(args.target):
        return os.path.abspath(args.target)
    return cand


def run_once(args, project_root, session_dir, session_state_path, report_dir, write_artifacts=True):
    target = resolve_target(args, project_root)
    files = md_files_under(target)
    snap_now = fingerprint(files)

    state = load_state(session_state_path)
    before = state.get("snapshot", {})

    added, modified, deleted = ([], [], [])
    if before:
        added, modified, deleted = diff_snapshot(before, snap_now)

    change_count = len(added) + len(modified) + len(deleted)
    _log(f"检测 {target}：.md 文件 {len(files)} 个，变化 {change_count} 个"
         f"（+{len(added)} 新增 / ~{len(modified)} 修改 / -{len(deleted)} 删除）")

    # 写变更报告（无论变化多少都写一份，便于 Agent 汇总）
    os.makedirs(report_dir, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = os.path.join(report_dir, f"report-{stamp}.md")
    lines = [
        "# checkmd 变更报告",
        "",
        f"- 目标目录：`{target}`",
        f"- 检测时间：{stamp}",
        f"- 监控窗口：每 {args.interval} 分钟 × {args.duration} 天",
        f"- 本次变化：+{len(added)} 新增 / ~{len(modified)} 修改 / -{len(deleted)} 删除",
        "",
    ]
    def dump(kind, lst, label):
        if not lst:
            return
        lines.append(f"## {label}（{len(lst)}）")
        for p in lst:
            rel = os.path.relpath(p, project_root)
            insight = extract_insight(p) if os.path.exists(p) else None
            lines.append(f"- `{rel}`" + (f"｜{insight['length']}字符｜{insight['units']}单元" if insight and insight['length'] else ""))
        lines.append("")

    dump("added", added, "新增")
    dump("modified", modified, "修改")
    dump("deleted", deleted, "删除")

    if change_count == 0 and not added and not modified and not deleted and not before:
        lines.append("（首次快照建立，作为基线，无历史可比。）")
    elif change_count == 0:
        lines.append("（无变化。）")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # 生成落库草稿（仅在非 dry-run 且存在变化时）
    draft_paths = []
    if write_artifacts and change_count > 0:
        candidates = [(p, "added") for p in added] + [(p, "modified") for p in modified] + [(p, "deleted") for p in deleted]
        for p, kind in candidates:
            insight = extract_insight(p) if os.path.exists(p) else {"length": 0, "headlines": [], "units": 0}
            rel = os.path.relpath(p, project_root)
            dp = write_draft(session_dir, rel, kind, insight, report_path)
            draft_paths.append(dp)
        _log(f"已生成 {len(draft_paths)} 份落库草稿到 concepts-drafts/")

    # 更新快照（必须用最新状态）
    state["snapshot"] = snap_now
    state["last_scan"] = dt.datetime.now().isoformat()
    save_state(session_state_path, state)

    return report_path, draft_paths, change_count


def main():
    parser = argparse.ArgumentParser(description="MD 文件变化后台监控器")
    parser.add_argument("--project", default=os.getcwd(), help="项目根目录（绝对路径）")
    parser.add_argument("--target", default="publish", help="待监控的相对或绝对目录，默认 <project>/publish")
    parser.add_argument("--interval", type=int, default=30, help="检查间隔（分钟），默认 30")
    parser.add_argument("--duration", type=int, default=3, help="持续天数，默认 3")
    parser.add_argument("--once", action="store_true", help="只检查一个周期后退出（不循环）")
    parser.add_argument("--name", default="mdwatch", help="会话名（隔离多次任务），默认 mdwatch")
    parser.add_argument("--session-dir", default=None, help="会话状态/产物目录（默认 <project>/.checkmd/<name>）")
    parser.add_argument("--dry-run", action="store_true", help="只检测与写报告，不生成落库草稿")
    parser.add_argument("--check", action="store_true", help="快速自检参数与目录后退出")
    args = parser.parse_args()

    project_root = os.path.abspath(args.project)
    if not os.path.isdir(project_root):
        _log(f"错误：项目目录不存在 {project_root}")
        return EXIT_ERROR

    # 参数校验
    if args.interval < 1:
        _log("错误：--interval 必须 >= 1 分钟")
        return EXIT_ERROR
    if args.duration < 1:
        _log("错误：--duration 必须 >= 1 天")
        return EXIT_ERROR

    target = resolve_target(args, project_root)
    if not os.path.isdir(target):
        _log(f"错误：目标目录不存在 {target}")
        return EXIT_ERROR

    session_dir = args.session_dir or os.path.join(project_root, ".checkmd", args.name)
    session_state_path = os.path.join(session_dir, "state.json")
    report_dir = os.path.join(session_dir, "reports")
    if args.dry_run:
        # dry-run 用一个独立会话，避免污染真实快照
        session_dir = os.path.join(session_dir, ".dryrun")
        session_state_path = os.path.join(session_dir, "state.json")

    if args.check:
        _log(f"自检通过：project={project_root} target={target} "
             f"interval={args.interval}min duration={args.duration}d session={session_dir}")
        return EXIT_OK

    _log(f"启动监控：target={target} interval={args.interval}min duration={args.duration}d")

    # 计算到期时间（持久化到会话，保证跨重启的窗口语义）
    state = load_state(session_state_path)
    if "deadline" not in state:
        deadline = time.time() + args.duration * 86400
        state["deadline"] = deadline
        save_state(session_state_path, state)
        _log(f"窗口建立：到期时刻 {dt.datetime.fromtimestamp(deadline).strftime('%Y-%m-%d %H:%M')}"
             f"（{args.duration} 天后自动停止）")
    else:
        deadline = state["deadline"]
        remain_days = (deadline - time.time()) / 86400
        if remain_days <= 0:
            _log("窗口已到期，自动停止。")
            return EXIT_OK
        _log(f"续跑：剩余 {remain_days:.2f} 天")

    # 主循环
    first = True
    while True:
        report_path, draft_paths, change_count = run_once(
            args, project_root, session_dir, session_state_path, report_dir,
            write_artifacts=not args.dry_run,
        )
        # 打印产物路径（Agent 可解析）
        _log(f"变更报告：{report_path}")
        for dp in draft_paths:
            _log(f"落库草稿：{dp}")

        if args.once:
            _log("--once：单个周期结束，退出。")
            break

        # 判断是否到期
        if time.time() >= deadline:
            _log("窗口到期，监控停止。")
            break

        remain_days = (deadline - time.time()) / 86400
        if first:
            _log(f"进入轮询：每 {args.interval} 分钟一次，剩余 {remain_days:.2f} 天。")
            first = False
        time.sleep(args.interval * 60)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())