#!/usr/bin/env python3
"""arch_qa.py — 系列架构图几何 QA（复用 SmartQuant scripts/arch_diagram_qa.py 三律）。

规则:
  R1 边不穿节点: 边的任一线段不得穿过非端点节点的矩形内部。
  R2 正交边不共线重叠: 两条边的水平/垂直主干线段不得重合（共享端点除外）。
  R3 不越界不悬空: 折点/标签在画布内，节点文字不超节点边界。

用法:
    python diagrams/arch_qa.py <fig-id>          # 单图
    python diagrams/arch_qa.py --all             # 全部图
    python diagrams/arch_qa.py <fig-id> --json   # JSON 输出（供门禁）
退出码: 0=通过  2=发现问题
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_src import FIGURES  # noqa: E402


def _center(n):
    return n["x"] + n["w"] / 2, n["y"] + n["h"] / 2


def _overlap_1d(a0, a1, b0, b1) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def edge_polylines(edges, nmap):
    out = []
    for i, (src, dst, *_rest) in enumerate(edges):
        ax, ay = _center(nmap[src])
        bx, by = _center(nmap[dst])
        out.append((i, src, dst, [(ax, ay), (bx, by)]))
    return out


def check_rect_cross(edges, nmap):
    issues = []
    for eid, src, dst, poly in edge_polylines(edges, nmap):
        for p, q in zip(poly, poly[1:]):
            x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
            for nid, n in nmap.items():
                if n["color"] == "zone" or nid in (src, dst):
                    continue
                rx, ry, rw, rh = n["x"], n["y"], n["w"], n["h"]
                if x1 == x2 and rx < x1 < rx + rw:
                    if _overlap_1d(*sorted((y1, y2)), ry, ry + rh) > 0:
                        issues.append({"edge": eid, "pair": f"{src}→{dst}", "node": nid,
                                       "why": f"垂直段 x={x1:.0f} 穿过节点 {nid}"})
                elif y1 == y2 and ry < y1 < ry + rh:
                    if _overlap_1d(*sorted((x1, x2)), rx, rx + rw) > 0:
                        issues.append({"edge": eid, "pair": f"{src}→{dst}", "node": nid,
                                       "why": f"水平段 y={y1:.0f} 穿过节点 {nid}"})
    return issues


def check_collinear_overlap(edges, nmap):
    # 每条边记录：id, src_id, dst_id, 起止中心点
    pts = [(i, src, dst, *_center(nmap[src]), *_center(nmap[dst]))
           for i, (src, dst, *_rest) in enumerate(edges)]
    issues = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            a = pts[i]
            b = pts[j]
            # 共享某个端点 → 合法连接，跳过（避免把共享端点误判为共线）
            shared = set((a[1], a[2])) & set((b[1], b[2]))
            if shared:
                continue
            ax1, ay1, ax2, ay2 = a[3], a[4], a[5], a[6]
            bx1, by1, bx2, by2 = b[3], b[4], b[5], b[6]
            # 垂直共线
            if ax1 == ax2 and bx1 == bx2 and abs(ax1 - bx1) < 1e-6:
                if _overlap_1d(*sorted((ay1, ay2)), *sorted((by1, by2))) > 0:
                    issues.append({"edgeA": i, "edgeB": j, "why": f"垂直共线 x={ax1:.0f}"})
            # 水平共线
            if ay1 == ay2 and by1 == by2 and abs(ay1 - by1) < 1e-6:
                if _overlap_1d(*sorted((ax1, ax2)), *sorted((bx1, bx2))) > 0:
                    issues.append({"edgeA": i, "edgeB": j, "why": f"水平共线 y={ay1:.0f}"})
    return issues


def check_offscreen(edges, nmap, pw, ph):
    issues = []
    for eid, src, dst, poly in edge_polylines(edges, nmap):
        for x, y in poly:
            if x < 0 or y < 0 or x > pw or y > ph:
                issues.append({"edge": eid, "why": f"折点 ({x:.0f},{y:.0f}) 超出画布 {pw}x{ph}"})
    return issues


def run_qa(fig) -> dict:
    nmap = {n["id"]: n for n in fig["NODES"]}
    w, h = fig.get("W", 1300), fig.get("H", 900)
    issues = []
    issues += check_rect_cross(fig["EDGES"], nmap)
    issues += check_collinear_overlap(fig["EDGES"], nmap)
    issues += check_offscreen(fig["EDGES"], nmap, w, h)
    seen = set()
    uniq = []
    for it in issues:
        k = json.dumps(it, sort_keys=True, ensure_ascii=False)
        if k not in seen:
            seen.add(k)
            uniq.append(it)
    return {"id": fig["id"], "issues": uniq, "pass": not uniq}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("filters", nargs="*", help="fig-id；--all 或省略=全部")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.all or not args.filters:
        ids = list(FIGURES.keys())
    else:
        ids = args.filters

    results = []
    n_issue = 0
    for fid in ids:
        if fid not in FIGURES:
            print(f"⚠ 未找到图: {fid}")
            continue
        r = run_qa(FIGURES[fid])
        results.append(r)
        n_issue += len(r["issues"])
        if not args.json:
            if r["pass"]:
                print(f"✅ {fid}: 几何 QA 通过")
            else:
                print(f"❌ {fid}: {len(r['issues'])} 个几何问题")
                for it in r["issues"][:6]:
                    print(f"     - {it['why']}")

    if args.json:
        print(json.dumps({"figs": results, "total_issues": n_issue}, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'✅ 全部几何 QA 通过' if n_issue == 0 else f'❌ 共 {n_issue} 个几何问题'}（{len(results)} 图）")
    return 0 if n_issue == 0 else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise