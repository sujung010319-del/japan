"""
갈등 발생 시점(t=0)을 100으로 지수화한 방일 외국인 방문객 추이 차트.

원자료: 일본 입국 외국인 통계(월별, Bloomberg JFVA* Index), 2008.12 ~ 2026.06
출력:  conflict_index_log.png   - 5개 사건 전체 (로그축)
       conflict_index_clean.png - 코로나 이전 구간만 (선형축)
       conflict_index_data.xlsx - 지수화 원표
"""

import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
SRC = BASE / "data" / "japan_visitors.xlsm"
HORIZON = 24  # t+0 ~ t+24

# 일본 인바운드가 코로나로 붕괴한 첫 달. 이후 구간은 갈등 효과와 분리 불가.
COVID_START = (2020, 2)

COLUMNS = [
    "전체", "아시아", "한국", "중국", "대만", "홍콩", "태국",
    "유럽", "북미", "남아메리카", "오세아니아", "아프리카", "기타",
]

# (라벨, 발생 년, 월, 지수화할 계열)
# 계열은 각 갈등의 '보복/보이콧 주체 또는 직접 영향권' 국가를 방일객 기준으로 매핑.
EVENTS = [
    ("2010.09 중일 센카쿠 갈등",     2010,  9, "중국"),
    ("2016.07 한중 사드 갈등",       2016,  7, "중국"),
    ("2018.03 미중 무역전쟁",        2018,  3, "중국"),
    ("2019.07 한일 분쟁",            2019,  7, "한국"),
    ("2020.05 호주-중국 무역 분쟁",  2020,  5, "오세아니아"),
]

# dataviz 카테고리 팔레트 슬롯 1-5 (light). validate_palette.js 통과.
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"


def month_key(year, month):
    """년/월을 단조 증가하는 정수 인덱스로."""
    return year * 12 + (month - 1)


def key_to_ym(key):
    return divmod(key, 12)[0], divmod(key, 12)[1] + 1


def load_series():
    """워크북에서 계열별 {월인덱스: 값} 딕셔너리를 읽는다."""
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["Sheet1"]
    series = {name: {} for name in COLUMNS}
    for row in ws.iter_rows(min_row=4, values_only=True):
        date = row[2]
        if not isinstance(date, datetime.datetime):
            continue
        key = month_key(date.year, date.month)
        for name, value in zip(COLUMNS, row[3:3 + len(COLUMNS)]):
            if value is not None:
                series[name][key] = value
    wb.close()
    return series


def build_tracks(series):
    """각 사건에 대해 t=0을 100으로 한 지수 계열을 만든다."""
    covid_key = month_key(*COVID_START)
    tracks = []
    for label, year, month, column in EVENTS:
        t0 = month_key(year, month)
        raw = series[column]
        base = raw[t0]
        points = []
        for t in range(HORIZON + 1):
            key = t0 + t
            if key not in raw:
                continue
            points.append({
                "t": t,
                "level": raw[key],
                "index": 100.0 * raw[key] / base,
                "covid": key >= covid_key,
            })
        tracks.append({
            "label": label,
            "column": column,
            "base": base,
            "base_ym": (year, month),
            "points": points,
        })
    return tracks


def split_runs(points):
    """코로나 이전/이후를 각각 실선/점선으로 그리기 위해 두 구간으로 자른다.
    경계에서 선이 끊기지 않도록 첫 코로나 점 직전 점을 양쪽에 모두 포함시킨다."""
    pre = [p for p in points if not p["covid"]]
    post = [p for p in points if p["covid"]]
    if pre and post:
        post = [pre[-1]] + post
    return pre, post


def setup_font():
    path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    if Path(path).exists():
        font_manager.fontManager.addfont(path)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
    plt.rcParams["axes.unicode_minus"] = False


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(True, which="major", axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.grid(True, which="major", axis="x", color=GRID, linewidth=0.8, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(1.0)
    ax.tick_params(colors=MUTED, labelsize=10, length=0)


def draw_series(ax, track, color, points):
    """실선(코로나 이전) + 점선(코로나 이후)으로 한 계열을 그린다."""
    pre, post = split_runs(points)
    if pre:
        ax.plot([p["t"] for p in pre], [p["index"] for p in pre],
                color=color, linewidth=2.0, solid_capstyle="round", zorder=3)
        ax.plot([p["t"] for p in pre], [p["index"] for p in pre],
                color=color, linestyle="none", marker="o", markersize=3.2,
                markeredgecolor=SURFACE, markeredgewidth=0.8, zorder=4)
    if len(post) > 1:
        ax.plot([p["t"] for p in post], [p["index"] for p in post],
                color=color, linewidth=2.0, linestyle=(0, (2, 2)),
                solid_capstyle="round", zorder=3)


def label_end(ax, track, color, points, log=False):
    """선 끝에 직접 라벨. (팔레트 대비 WARN에 대한 relief 규칙)"""
    last = points[-1]
    value = last["index"]
    text = f"{value:,.0f}" if value >= 10 else f"{value:,.2g}"
    ax.annotate(
        text,
        xy=(last["t"], last["index"]),
        xytext=(6, 0), textcoords="offset points",
        color=color, fontsize=9.5, fontweight="bold",
        va="center", ha="left", zorder=5,
    )


def chart_log(tracks, out):
    fig, ax = plt.subplots(figsize=(12.5, 7.2), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    style_axes(ax)
    ax.set_yscale("log")

    ax.axhline(100, color=AXIS, linewidth=1.2, zorder=1)

    for track, color in zip(tracks, PALETTE):
        draw_series(ax, track, color, track["points"])
        label_end(ax, track, color, track["points"], log=True)

    ax.set_xlim(-0.6, HORIZON + 2.4)
    ax.set_xticks(range(0, HORIZON + 1, 2))
    ax.set_xticklabels([f"t+{t}" if t else "t=0" for t in range(0, HORIZON + 1, 2)])
    ax.set_yticks([0.01, 0.1, 1, 10, 100, 1000, 10000])
    ax.set_yticklabels(["0.01", "0.1", "1", "10", "100", "1,000", "10,000"])
    ax.set_ylim(0.0015, 120000)
    ax.set_xlabel("갈등 발생 이후 경과 개월", color=INK_SECONDARY, fontsize=10.5, labelpad=10)
    ax.set_ylabel("지수 (t=0 → 100, 로그 스케일)", color=INK_SECONDARY, fontsize=10.5, labelpad=10)

    handles = [
        plt.Line2D([], [], color=color, linewidth=2.4,
                   label=f"{t['label']}  ·  {t['column']} 방일객")
        for t, color in zip(tracks, PALETTE)
    ]
    handles.append(plt.Line2D([], [], color=MUTED, linewidth=2.0,
                              linestyle=(0, (2, 2)), label="점선 = 2020.02 이후 (코로나 구간)"))
    leg = ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, -0.13),
                    ncol=2, frameon=False, fontsize=10,
                    labelspacing=0.7, columnspacing=2.5, handlelength=2.2)
    for text in leg.get_texts():
        text.set_color(INK_SECONDARY)

    fig.suptitle("갈등 발생 시점 기준 방일 방문객 지수 추이 (t=0 = 100)",
                 x=0.055, ha="left", y=0.975, fontsize=16, fontweight="bold", color=INK)
    fig.text(0.055, 0.928,
             "각 갈등의 발생 년월을 t=0으로 정렬, 해당 월 방문객 수를 100으로 지수화 · 로그 스케일",
             ha="left", fontsize=10.5, color=INK_SECONDARY)
    fig.text(0.055, 0.025,
             "자료: 일본 입국 외국인 통계(월별). 점선 구간은 코로나로 인바운드가 붕괴한 2020.02 이후로, "
             "갈등 효과와 분리할 수 없음.\n"
             "'2020.05 호주-중국'은 t=0 오세아니아 방일객이 6명(코로나 저점)이라 지수 자체가 무의미 — 비교 대상에서 제외하고 읽을 것.",
             ha="left", fontsize=9, color=MUTED, linespacing=1.6)

    fig.subplots_adjust(left=0.075, right=0.955, top=0.885, bottom=0.30)
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)


def chart_clean(tracks, out):
    """코로나에 오염되지 않은 구간만 선형축으로."""
    fig, ax = plt.subplots(figsize=(12.5, 7.2), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    style_axes(ax)

    ax.axhline(100, color=AXIS, linewidth=1.2, zorder=1)

    shown = []
    for track, color in zip(tracks, PALETTE):
        pre = [p for p in track["points"] if not p["covid"]]
        if len(pre) < 2:
            continue
        shown.append((track, color, pre))
        ax.plot([p["t"] for p in pre], [p["index"] for p in pre],
                color=color, linewidth=2.0, solid_capstyle="round", zorder=3)
        ax.plot([p["t"] for p in pre], [p["index"] for p in pre],
                color=color, linestyle="none", marker="o", markersize=3.6,
                markeredgecolor=SURFACE, markeredgewidth=0.9, zorder=4)
        ax.annotate(f"{pre[-1]['index']:,.0f}",
                    xy=(pre[-1]["t"], pre[-1]["index"]), xytext=(6, 0),
                    textcoords="offset points", color=color, fontsize=9.5,
                    fontweight="bold", va="center", ha="left", zorder=5)

    ax.set_xlim(-0.6, HORIZON + 2.0)
    ax.set_xticks(range(0, HORIZON + 1, 2))
    ax.set_xticklabels([f"t+{t}" if t else "t=0" for t in range(0, HORIZON + 1, 2)])
    ax.set_ylim(0, 200)
    ax.set_yticks(range(0, 201, 25))
    ax.set_xlabel("갈등 발생 이후 경과 개월", color=INK_SECONDARY, fontsize=10.5, labelpad=10)
    ax.set_ylabel("지수 (t=0 → 100)", color=INK_SECONDARY, fontsize=10.5, labelpad=10)

    handles = [
        plt.Line2D([], [], color=color, linewidth=2.4,
                   label=f"{t['label']}  ·  {t['column']} 방일객  (t+0~t+{pre[-1]['t']})")
        for t, color, pre in shown
    ]
    leg = ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, -0.13),
                    ncol=2, frameon=False, fontsize=10,
                    labelspacing=0.7, columnspacing=2.5, handlelength=2.2)
    for text in leg.get_texts():
        text.set_color(INK_SECONDARY)

    fig.suptitle("갈등 발생 시점 기준 방일 방문객 지수 — 코로나 이전 구간만",
                 x=0.055, ha="left", y=0.975, fontsize=16, fontweight="bold", color=INK)
    fig.text(0.055, 0.928,
             "위 차트와 동일하나 2020.02 이후를 잘라내고 선형축으로 표시 — 실제로 해석 가능한 구간",
             ha="left", fontsize=10.5, color=INK_SECONDARY)
    fig.text(0.055, 0.025,
             "자료: 일본 입국 외국인 통계(월별). '2019.07 한일 분쟁'은 t+7(2020.02)에서, "
             "'2018.03 미중 무역전쟁'은 t+22(2020.01)에서 끊김.\n"
             "'2020.05 호주-중국'은 전 구간이 코로나 이후라 이 차트에 표시되지 않음. "
             "월별 관광 데이터는 계절성이 크므로 전년동월 대비와 함께 볼 것.",
             ha="left", fontsize=9, color=MUTED, linespacing=1.6)

    fig.subplots_adjust(left=0.075, right=0.955, top=0.885, bottom=0.28)
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)


def write_workbook(tracks, out):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "지수화"

    head = Font(name="Arial", bold=True, size=10)
    body = Font(name="Arial", size=10)
    note = Font(name="Arial", size=9, italic=True, color="898781")
    fill = PatternFill("solid", fgColor="F0EFEC")

    ws["A1"] = "갈등 발생 시점(t=0)을 100으로 지수화한 방일 방문객 추이"
    ws["A1"].font = Font(name="Arial", bold=True, size=12)
    ws["A2"] = "자료: 일본 입국 외국인 통계(월별). 회색 음영 = 2020.02 이후 코로나 구간(해석 불가)."
    ws["A2"].font = note

    ws["A4"] = "t"
    ws["A4"].font = head
    for col, track in enumerate(tracks, start=2):
        cell = ws.cell(row=4, column=col, value=track["label"])
        cell.font = head
        cell.alignment = Alignment(wrap_text=True, vertical="bottom", horizontal="center")
        sub = ws.cell(row=5, column=col,
                      value=f"{track['column']} · t=0 실측 {track['base']:,}명")
        sub.font = note
        sub.alignment = Alignment(wrap_text=True, horizontal="center")
        ws.column_dimensions[get_column_letter(col)].width = 22
    ws.row_dimensions[4].height = 32
    ws.row_dimensions[5].height = 26
    ws.column_dimensions["A"].width = 8

    lookup = [{p["t"]: p for p in t["points"]} for t in tracks]
    for t in range(HORIZON + 1):
        row = 6 + t
        label = ws.cell(row=row, column=1, value=f"t+{t}" if t else "t=0")
        label.font = head if t == 0 else body
        for col, points in enumerate(lookup, start=2):
            point = points.get(t)
            if point is None:
                continue
            cell = ws.cell(row=row, column=col, value=round(point["index"], 1))
            cell.font = body
            cell.number_format = "#,##0.0"
            if point["covid"]:
                cell.fill = fill

    tail = 6 + HORIZON + 2
    ws.cell(row=tail, column=1,
            value="지수 = 100 × (해당 월 방문객 수) ÷ (t=0 월 방문객 수). 실측치 기준, 계절조정 없음.").font = note
    ws.cell(row=tail + 1, column=1,
            value="계열 매핑은 각 갈등의 보복/보이콧 주체 또는 직접 영향권 국가를 방일객 기준으로 잡은 것 "
                  "(센카쿠·사드·미중→중국, 한일→한국, 호주-중국→오세아니아).").font = note
    ws.cell(row=tail + 2, column=1,
            value="'2020.05 호주-중국'은 t=0 기준값이 6명이라 지수가 수만까지 튐 — 다른 사건과 비교 불가.").font = note

    ws.freeze_panes = "B6"
    wb.save(out)


def main():
    setup_font()
    series = load_series()
    tracks = build_tracks(series)
    out_dir = BASE / "output"
    out_dir.mkdir(exist_ok=True)
    chart_log(tracks, out_dir / "conflict_index_log.png")
    chart_clean(tracks, out_dir / "conflict_index_clean.png")
    write_workbook(tracks, out_dir / "conflict_index_data.xlsx")
    for track in tracks:
        pre = [p for p in track["points"] if not p["covid"]]
        low = f"{min(p['index'] for p in pre):7.1f}" if pre else "      -"
        print(f"{track['label']:28s} {track['column']:6s} base={track['base']:>9,} "
              f"clean={max(len(pre) - 1, 0):>2d}개월 min={low}")


if __name__ == "__main__":
    main()
