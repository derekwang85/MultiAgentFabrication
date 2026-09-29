#!/usr/bin/env python3
"""evaluate-en.py — English evaluation tool for the AI Harness series' English editions.

Data source: writing-harness/evaluation-scoreboard-en.json
Rule (see writing-harness/EVALUATION-EN.md):
  Every new English essay must score strictly above the running average of all
  previously recorded English essays (ratchet rule). Recording recomputes the
  rolling average as the next essay's baseline.

English-native breakthrough dimensions (differentiated from CN):
  native-voice, reproducible-evidence, english-allusions, scannability, memorable-phrasing

Usage:
  python evaluate-en.py --list                  # print scoreboard + baseline
  python evaluate-en.py --next [--exclude key]  # print target for next essay
  python evaluate-en.py --recalib               # replay running averages, audit ratchet
  python evaluate-en.py --record articles/00-prologue.en.md --score 8.7 [--breakthrough ...] [--note ...]
  python evaluate-en.py --update articles/xx.en.md [--score ...] [--breakthrough ...] [--note ...]
  python evaluate-en.py --check                 # validate data source
"""

import argparse
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SCOREBOARD = os.path.join(HERE, "evaluation-scoreboard-en.json")

VALID_DIMS = [
    "native-voice",          # sounds like a native engineer, not a translated document
    "reproducible-evidence",  # numbers/files/commands point to verifiable places
    "english-allusions",      # quotes/cases an English reader already knows (or localized well)
    "scannability",           # sentence-case functional subheads, first-screen payoff
    "memorable-phrasing",     # a line readers can quote (English rhythm, not CN parallel structure)
]


def now_str():
    return date.today().isoformat()


def load():
    with open(SCOREBOARD, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(SCOREBOARD, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[written] {SCOREBOARD}")


def average(articles):
    if not articles:
        return 0.0
    return round(sum(a["score"] for a in articles) / len(articles), 2)


def exclude_key(articles, exclude):
    if not exclude:
        return articles
    arts = [a for a in articles if not (
        a["key"] == exclude
        or a["file"] == exclude
        or os.path.basename(a["file"]) == exclude
    )]
    if len(arts) == len(articles):
        print(f"[warn] --exclude '{exclude}' matched nothing; using all.")
    return arts


def find(articles, key):
    for a in articles:
        if a["key"] == key or a["file"] == key or os.path.basename(a["file"]) == key:
            return a
    return None


def rule_check(new_score, avg):
    # 主导规则（与中文版一致，经裁定 2026-09-23）：每篇锁定 9.5-9.9 目标带，
    # 向带内上沿递进；相对前序均分采用“不低于”（>=）而非“严格大于”（>）。
    ok = new_score >= avg
    print(f"  => score {new_score} vs baseline {avg} -> {'PASS' if ok else 'FAIL'} (须不低于，>=)")
    return ok


def cmd_list(data):
    arts = data["articles"]
    print("=== AI Harness EN scoreboard ===")
    print(f"{'key':<30}{'score':<8}{'status':<12}{'date'}")
    print("-" * 70)
    for a in arts:
        print(f"{a['key']:<30}{str(a['score']):<8}{a['status']:<12}{a['date']}")
    avg = average(arts)
    print("-" * 70)
    print(f"Running average (baseline): {avg}")
    print(f"Next essay target: 锁定 9.5-9.9 目标带，向 9.9 收敛；不低于前均 {avg}")


def cmd_next(data, args):
    arts = exclude_key(data["articles"], getattr(args, "exclude", "") or "")
    avg = average(arts)
    print(f"Baseline scope: {'excluding --exclude' if args.exclude else 'all recorded'} essays")
    print(f"Running average (baseline): {avg:.2f}")
    print(f"Next essay target: strictly > {avg:.2f} (aim for {avg + 0.2:.2f}+ for margin)")
    print("Breakthrough dimensions (record at least 1): " + " / ".join(VALID_DIMS))


def cmd_recalib(data):
    arts = data["articles"]
    print("--- Recalibration: running-average replay ---")
    print(f"{'key':<30}{'score':<8}{'running-avg':<12}{'verdict'}")
    print("-" * 66)
    cum = 0.0
    for i, a in enumerate(arts):
        base_prev = 0.0 if i == 0 else round(cum / i, 2)
        ok = a["score"] >= base_prev
        print(f"{a['key']:<30}{str(a['score']):<8}{str(base_prev):<12}{'PASS' if ok else 'FAIL'} (>={base_prev})")
        cum += a["score"]
    print("-" * 66)
    print(f"Final running average: {round(cum / len(arts), 2)}")
    print("Note: first essay has no predecessor; baseline = 0.0. Order by scoreboard order.")


def cmd_record(data, args):
    arts = data["articles"]
    target_key = os.path.splitext(os.path.basename(args.target))[0]
    if find(arts, target_key):
        print(f"[error] {args.target} already exists. Use --record for new, --update for edits.")
        sys.exit(1)
    if args.score < 0 or args.score > data["system"]["scale_max"]:
        print(f"[error] score must be 0 ~ {data['system']['scale_max']}.")
        sys.exit(1)
    print("--- pre-record check ---")
    avg = average(arts)
    rule_check(args.score, avg)
    arts.append({
        "key": target_key,
        "title": args.title or target_key,
        "file": args.target,
        "score": args.score,
        "status": "draft-review",
        "date": args.date or now_str(),
        "breakthrough": args.breakthrough or "",
        "note": args.note or "",
    })
    arts.sort(key=lambda a: a["key"])
    data["updated"] = now_str()
    save(data)
    print(f"--- recorded {args.target}, score {args.score} ---")
    print(f"New running average (incl. this essay): {average(arts)}")


def cmd_update(data, args):
    arts = data["articles"]
    target_key = os.path.splitext(os.path.basename(args.target))[0]
    a = find(arts, target_key)
    if not a:
        print(f"[error] not found: {args.target}. Use full path or essay key.")
        sys.exit(1)
    prev = a["score"]
    changed = False
    if args.score is not None:
        if args.score < 0 or args.score > data["system"]["scale_max"]:
            print(f"[error] score must be 0 ~ {data['system']['scale_max']}.")
            sys.exit(1)
        a.setdefault("score_history", []).append([str(prev), a["date"], a.get("note", "")])
        a["score"] = args.score
        a["date"] = now_str()
        changed = True
    if args.breakthrough:
        a["breakthrough"] = args.breakthrough
        changed = True
    if args.note:
        a["note"] = args.note
        changed = True
    if changed:
        a["status"] = "draft-review" if args.status is None else args.status
        print(f"--- updated {args.target}: {prev} -> {a['score']} ---")
        avg = average(arts)
        print(f"New running average (all EN essays): {avg}")
        if args.score is not None:
            rule_check(a["score"], avg)
        data["updated"] = now_str()
        save(data)
    else:
        print("[info] no fields changed; skipped.")


def cmd_check(data):
    arts = data["articles"]
    errs = []
    print(f"--- validate ({SCOREBOARD}) ---")
    print(f"scale: 0 ~ {data['system']['scale_max']}; essays: {len(arts)}; avg: {average(arts)}")
    for a in arts:
        if not (0 <= a["score"] <= data["system"]["scale_max"]):
            errs.append(f"  [{a['key']}] score {a['score']} out of range")
        if not a.get("breakthrough"):
            errs.append(f"  [{a['key']}] missing breakthrough dimension")
        if not a.get("file", "").endswith(".en.md"):
            errs.append(f"  [{a['key']}] file should be *.en.md: {a.get('file')}")
    if errs:
        for e in errs:
            print(e)
        sys.exit(1)
    print("OK.")


def main():
    parser = argparse.ArgumentParser(description="AI Harness EN essays evaluation tool")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--exclude", dest="exclude", help="exclude essay from baseline calculation")
    parser.add_argument("--recalib", action="store_true")
    parser.add_argument("--record", dest="target", help="record a new essay file")
    parser.add_argument("--update", dest="update_target", help="update an existing essay file")
    parser.add_argument("--score", type=float)
    parser.add_argument("--breakthrough", help="breakthrough dimension descriptor")
    parser.add_argument("--note", help="scoring note")
    parser.add_argument("--title", help="title (on record)")
    parser.add_argument("--date", help="date YYYY-MM-DD")
    parser.add_argument("--status", help="status")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(SCOREBOARD):
        print(f"[error] scoreboard not found: {SCOREBOARD}")
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
    elif args.target:
        cmd_record(data, args)
    elif args.update_target:
        args.target = args.update_target
        cmd_update(data, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()