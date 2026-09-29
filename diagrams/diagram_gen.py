#!/usr/bin/env python3
"""diagram_gen.py — 《MultiAgent Fabrication》系列 drawio 单一数据源生成器。

用法:
    python diagrams/diagram_gen.py                     # 生成全部图（default: 全部）
    python diagrams/diagram_gen.py <fig-id>            # 只生成某张图
    python diagrams/arch_qa.py <fig-id>                # 对某图做几何 QA
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_src import FIGURES, COLORS  # noqa: E402

_OUT = Path(__file__).resolve().parent / "out"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;").replace("\n", "&#10;")
    )


# ─────────────────────────────── draw.io 输出 ───────────────────────────────
def build_drawio(nodes, edges, page_w=1300, page_h=900) -> str:
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    for n in nodes:
        fill, stroke = COLORS[n["color"]]
        style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        if n.get("dash") or n["color"] == "zone":
            style += "dashed=1;"
        if n["color"] == "zone":
            style += "verticalAlign=top;fontStyle=1;fontSize=13;"
        text = n["text"]
        if n.get("sub"):
            text += f'\n\n<font style="font-size:10px;color:#5b6475;">{esc(n["sub"])}</font>'
        cells.append(
            f'<mxCell id="{n["id"]}" value="{esc(text)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" as="geometry"/>'
            f"</mxCell>"
        )
    for i, (src, dst, dash, label) in enumerate(edges):
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;"
        if dash:
            style += "dashed=1;strokeColor=#94a3b8;"
        if label:
            style += "labelBackgroundColor=#f8fafc;fontSize=11;"
        cells.append(
            f'<mxCell id="e{i}" value="{esc(label)}" style="{style}" edge="1" parent="1" '
            f'source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
    return (
        '<mxfile host="app.diagrams.net" agent="MultiAgentFabrication" version="24.0.0">\n'
        '<diagram id="maf" name="Page-1">\n'
        f'<mxGraphModel dx="1300" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" '
        f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" '
        f'pageHeight="{page_h}" math="0" shadow="0">\n'
        f"<root>\n" + "\n".join(cells) + '\n</root>\n</mxGraphModel>\n</diagram>\n</mxfile>'
    )


# ─────────────────────────────── 边/线上标签避让 ───────────────────────────────
def _label_extent_px(nlen: int) -> tuple:
    """估算 11px 边标签的绘制宽/高（每中文字约 7.2px，另加左右内边距各 6px）。"""
    return nlen * 7.2 + 12.0, 18.0


def _ortho_route(s, d):
    """两点间正交折线（S → 中缝垂直走廊 → D），返回 (points_csv, 中点)。

    沿用图库"中缝走廊"约定：先水平到 x 中点，再垂直过走廊到目标 y，再水平到目标。
    连续重复的点被去重，纯竖直/纯水平边因此只保留单段，避免输出叠加重合点。
    """
    sx, sy = s
    dx, dy = d
    midx = (sx + dx) / 2.0
    raw = [(sx, sy), (midx, sy), (midx, dy), (dx, dy)]
    pts_out = [raw[0]]
    for p in raw[1:]:
        if abs(p[0] - pts_out[-1][0]) > 1e-6 or abs(p[1] - pts_out[-1][1]) > 1e-6:
            pts_out.append(p)
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts_out)
    return pts, (midx, (sy + dy) / 2.0)


def _gap_label_anchor(s, d, sb, db, lw, lh, nodes):
    """把边标签放在两端节点之间的空走廊中央（避开流程框），返回文本框中点坐标。

    sb/db 为 src/dst 节点矩形(x,y,w,h)；nodes 为全部节点 dict 列表。
    起止节点之外的所有非 zone 节点视为障碍矩形（带 4px 外扩余量）。
    竖直叠放取共享中心 x、竖直间隙中点 y；水平并排取共享中心 y、水平间隙中点 x；
    斜角连接退回几何中点。若标签矩形与障碍相交，沿走廊主轴以小步长(2px)
    朝间隙外侧/上下扩展搜索；走廊内找不到则平面内沿另一主轴/对角试探取
    "离理想锚点最近"可行位置；仍无则退回几何中点（保底不崩）。
    """
    a, b = sb, db
    EXP = 4.0
    STEP = 2.0
    # 共享中心（两端节点矩形的几何中点）
    cx = ((a["x"] + a["w"] / 2.0) + (b["x"] + b["w"] / 2.0)) / 2.0
    cy = ((a["y"] + a["h"] / 2.0) + (b["y"] + b["h"] / 2.0)) / 2.0
    # 竖直间隙（上节点底边 ~ 下节点顶边）
    gap_top = min(a["y"] + a["h"], b["y"] + b["h"])
    gap_bot = max(a["y"], b["y"])
    # 水平间隙
    gap_l = min(a["x"] + a["w"], b["x"] + b["w"])
    gap_r = max(a["x"], b["x"])
    # 上/下、左/右判定
    a_is_up = a["y"] + a["h"] <= b["y"]
    a_is_down = b["y"] + b["h"] <= a["y"]
    a_is_left = a["x"] + a["w"] <= b["x"]
    a_is_right = b["x"] + b["w"] <= a["x"]

    # 障碍矩形：起止节点之外其余非 zone 节点（带 4px 外扩余量）
    obs = []
    for n in nodes:
        if n.get("color") == "zone":
            continue
        obs.append((n["x"] - EXP, n["y"] - EXP, n["w"] + 2.0 * EXP, n["h"] + 2.0 * EXP))

    def _valid(lx, ly):
        # 渲染后的标签矩形（与 build_html 输出一致）再外扩 4px 作安全余量
        rx = lx - lw / 2.0 - EXP
        ry = ly - lh + 3.0 - EXP
        rw = lw + 2.0 * EXP
        rh = lh + 2.0 * EXP
        for (ox, oy, ow, oh) in obs:
            if not (rx + rw <= ox or ox + ow <= rx or ry + rh <= oy or oy + oh <= ry):
                return False
        return True

    if a_is_up or a_is_down:
        # 上下叠放：理想锚点取共享中心 x、竖直间隙中点 y
        if gap_bot - gap_top >= 8.0:
            ideal = (cx, (gap_top + gap_bot) / 2.0)
        elif a_is_up:
            ideal = (cx, gap_top - 4.0)
        else:
            ideal = (cx, gap_bot + 4.0)
        orient = "v"
    elif a_is_left or a_is_right:
        # 左右并排：理想锚点取共享中心 y、水平间隙中点 x
        if gap_r - gap_l >= 8.0:
            ideal = ((gap_l + gap_r) / 2.0, cy)
        elif a_is_left:
            ideal = (gap_l - 4.0, cy)
        else:
            ideal = (gap_r + 4.0, cy)
        orient = "h"
    else:
        # 斜角连接：退回几何中点（保底）
        return cx, cy

    if _valid(ideal[0], ideal[1]):
        return ideal

    # 走廊主轴逐步外扩搜索（每步 2px，正负两方向都尝试）
    x0 = min(n["x"] for n in nodes)
    y0 = min(n["y"] for n in nodes)
    x1 = max(n["x"] + n["w"] for n in nodes)
    y1 = max(n["y"] + n["h"] for n in nodes)
    span = max(x1 - x0, y1 - y0)
    kmax = int(span / STEP) + 2
    for k in range(1, kmax + 1):
        m = k * STEP
        for sgn in (1.0, -1.0):
            if orient == "v":
                cand = (cx, ideal[1] + sgn * m)
            else:
                cand = (ideal[0] + sgn * m, cy)
            if _valid(cand[0], cand[1]):
                return cand

    # 平面内试探：先沿另一主轴、再对角，取离理想锚点最近的可行位置
    best = None
    best_d = None
    for k in range(1, kmax + 1):
        m = k * STEP
        # 另一主轴
        if orient == "v":
            cross = [(ideal[0] + m, ideal[1]), (ideal[0] - m, ideal[1])]
        else:
            cross = [(ideal[0], ideal[1] + m), (ideal[0], ideal[1] - m)]
        for cand in cross:
            if _valid(cand[0], cand[1]):
                if best_d is None or m < best_d:
                    best_d = m
                    best = cand
        # 两主轴对角
        for sx in (1.0, -1.0):
            for sy in (1.0, -1.0):
                cand = (ideal[0] + sx * m, ideal[1] + sy * m)
                if _valid(cand[0], cand[1]):
                    dm = 2.0 * m
                    if best_d is None or dm < best_d:
                        best_d = dm
                        best = cand
    if best is not None:
        return best
    # 仍无可行位置：退回几何中点（保底不崩）
    return cx, cy


# ─────────────────────────────── HTML/SVG 输出 ──────────────────────────────
CSS_HEAD = """
  :root { color-scheme: light dark; --bg:#f8fafc; --fg:#172033; --muted:#5b6475; --line:#64748b;
    --neutral:#e2e8f0; --input:#bfdbfe; --process:#c7d2fe; --storage:#99f6e4;
    --external:#fde68a; --risk:#fecaca; --wiki:#ddd6fe; }
  @media (prefers-color-scheme: dark) { :root { --bg:#0f172a; --fg:#e5e7eb; --muted:#a3adbd;
    --line:#94a3b8; --neutral:#334155; --input:#1d4ed8; --process:#4338ca; --storage:#0f766e;
    --external:#92400e; --risk:#991b1b; --wiki:#5b4b9e; } }
  @media print {
    :root { color-scheme: light; --bg:#ffffff; --fg:#111827; --muted:#4b5563; --line:#6b7280;
      --neutral:#e5e7eb; --input:#bfdbfe; --process:#c7d2fe; --storage:#a7f3d0;
      --external:#fde68a; --risk:#fecaca; --wiki:#ddd6fe; }
    body { margin:0; }
    .stage { border:0.025in solid #6b7280; break-inside:avoid; }
    .node, .zone { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  }
"""


def build_html(fig) -> str:
    nodes, edges, w, h = fig["NODES"], fig["EDGES"], fig["W"], fig["H"]
    boxes = []
    for n in nodes:
        if n["color"] == "zone":
            tint = " tinted" if n.get("bg") else ""
            hl = " hl" if n.get("hl") else ""
            boxes.append(
                f'<div class="zone{tint}{hl}" style="left:{n["x"]}px;top:{n["y"]}px;width:{n["w"]}px;'
                f'height:{n["h"]}px">'
                f'<span class="zone-label">{esc(n["text"])}</span>'
                + (f'<span class="zone-note">{esc(n["sub"])}</span>' if n.get("sub") else "")
                + "</div>")
        else:
            color = n["color"]
            boxes.append(
                f'<div class="node {color}" style="left:{n["x"]}px;top:{n["y"]}px;width:{n["w"]}px;'
                f'height:{n["h"]}px"><b>{esc(n["text"])}</b>'
                + (f'<small>{esc(n["sub"])}</small>' if n.get("sub") else "")
                + "</div>")
    boxes_html = "\n    ".join(boxes)

    # SVG 连接线：正交折线走廊式绕行；边标签放在两端节点空走廊中央并加淡底色浮层，
    # 避免文字被流程框覆盖（fig-09-key 等旧版问题）。
    svg_lines = []
    nmap = {n["id"]: n for n in nodes}
    pos = {n["id"]: (n["x"] + n["w"] / 2.0, n["y"] + n["h"] / 2.0) for n in nodes}
    for i, (src, dst, dash, label) in enumerate(edges):
        s, d = pos[src], pos[dst]
        pts, _mid = _ortho_route(s, d)
        dash_attr = 'stroke-dasharray="6,4"' if dash else ""
        svg_lines.append(
            f'<polyline points="{pts}" fill="none" stroke="var(--line)" stroke-width="1.6" {dash_attr}/>'
            f'<circle cx="{s[0]:.1f}" cy="{s[1]:.1f}" r="2.6" fill="var(--line)"/>'
            f'<circle cx="{d[0]:.1f}" cy="{d[1]:.1f}" r="3.0" fill="var(--line)"/>')
        if label:
            lw, lh = _label_extent_px(len(label))
            lx, ly = _gap_label_anchor(s, d, nmap[src], nmap[dst], lw, lh, nodes)
            svg_lines.append(
                f'<rect x="{lx - lw / 2.0:.1f}" y="{ly - lh + 3}" width="{lw:.1f}" height="{lh:.1f}" rx="4" '
                f'fill="var(--bg)"/>'
                f'<text x="{lx:.1f}" y="{ly}" font-size="11" fill="var(--muted)" text-anchor="middle" ' 
                f'dominant-baseline="middle">{esc(label)}</text>')
    svg_html = "\n    ".join(svg_lines)

    return f"""<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(fig["title"])}</title>
<style>
{CSS_HEAD}
  body {{ background:var(--bg); color:var(--fg); margin:16px; line-height:1.525; font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif; }}
  h1 {{ font-size:17px; margin:0 0 4px; font-weight:600; letter-spacing:.025em; }}
  .sub {{ font-size:12px; color:var(--muted); margin-bottom:12px; line-height:1.55; }}
  .stage {{ position:relative; width:{w}px; height:{h}px; border:1px solid var(--line); border-radius:8px; margin-top:8px; overflow:hidden; }}
  svg {{ position:absolute; inset:0; width:100%; height:100%; pointer-events:none; }}
  .node {{ position:absolute; border-radius:8px; border:1.4px solid; padding:6px 10px; box-sizing:border-box;
    font-size:12.5px; display:flex; flex-direction:column; justify-content:center; z-index:2; color:var(--fg); }}
  .node b {{ font-weight:600; }}
  .node small {{ font-size:10px; color:var(--fg); opacity:.72; margin-top:2px; line-height:1.3; }}
  .node.neutral   {{ background:var(--neutral); border-color:var(--line); }}
  .node.input     {{ background:var(--input);   border-color:var(--line); }}
  .node.process   {{ background:var(--process); border-color:var(--line); }}
  .node.storage   {{ background:var(--storage); border-color:var(--line); }}
  .node.external  {{ background:var(--external);border-color:var(--line); }}
  .node.risk      {{ background:var(--risk);    border-color:var(--line); }}
  .zone {{ position:absolute; border:1.4px dashed var(--line); border-radius:10px; z-index:1; }}
  .zone.tinted {{ background:color-mix(in srgb, var(--line) 7%, transparent); }}
  .zone.hl {{ border-style:solid; border-width:2px; border-color:var(--process); background:color-mix(in srgb, var(--process) 8%, transparent); }}
  .zone-label {{ position:absolute; top:-4px; left:10px; font-size:12px; color:var(--muted);
    background:var(--bg); padding:0 6px; font-weight:600; white-space:nowrap; }}
  .zone-note {{ position:absolute; left:14px; right:14px; bottom:8px; font-size:11px;
    color:var(--muted); line-height:1.4; opacity:.94; }}
</style>
</head>
<body>
<h1>{esc(fig["title"])}</h1>
<div class="sub">{esc(fig.get("sub", ""))}</div>
<div class="stage">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">
  {svg_html}
  </svg>
  {boxes_html}
</div>
</body>
</html>
"""


def _fig_pagesize(fig):
    """返回 drawio 页面宽/高（在内容 W/H 基础上加一圈留白）。"""
    return fig["W"] + 80, fig["H"] + 120


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("filters", nargs="*", help="fig-id；缺省或 --all = 全部")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default=None, help="输出目录（默认 diagrams/out）")
    args = ap.parse_args()

    outdir = Path(args.out) if args.out else _OUT
    outdir.mkdir(parents=True, exist_ok=True)

    if args.all or not args.filters:
        ids = list(FIGURES.keys())
    else:
        ids = args.filters

    for fid in ids:
        fig = FIGURES.get(fid)
        if fig is None:
            print(f"未找到图: {fid}")
            continue
        pw, ph = _fig_pagesize(fig)
        (outdir / f"{fid}.drawio").write_text(
            build_drawio(fig["NODES"], fig["EDGES"], pw, ph), encoding="utf-8"
        )
        (outdir / f"{fid}.html").write_text(build_html(fig), encoding="utf-8")
        print(f"已生成 {fid}.drawio / {fid}.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())