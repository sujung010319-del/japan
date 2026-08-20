"""
한국 반도체 장비 시장(SEMI 지역별 빌링스) 추이와 2026년 전망 차트.

원자료: SEMI 연간/분기 빌링스 보도자료, 뉴스N연합(2026) 팹 장비 투자 전망
출력:  kr_semi_equipment_trend.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = Path(__file__).resolve().parent
OUT = BASE / "output" / "kr_semi_equipment_trend.png"

# (연도, 억달러, 증감 라벨, 확정 실적 여부)
# 2021년은 2022년 -14%에서 역산한 추정치라 제외. 확정 빌링스만 실선으로 둔다.
BILLINGS = [
    (2022, 215, "-14%", True),
    (2023, 199, "-7%", True),
    (2024, 205, "+3%", True),
    (2025, 258, "+26%", True),
]

# 2026년은 '팹 장비 투자' 기준 전망치. 빌링스와 기준이 달라 별도 표기.
FORECAST_2026 = (2026, 297, "+27.2%")

# 2026년 1분기 실적을 4배 한 값. 전망치가 보수적임을 보여주는 참조선.
Q1_2026 = 89.3
ANNUALIZED = Q1_2026 * 4

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"


def setup_font():
    path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    if Path(path).exists():
        font_manager.fontManager.addfont(path)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
    plt.rcParams["axes.unicode_minus"] = False


def draw():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    years = [y for y, _, _, _ in BILLINGS] + [FORECAST_2026[0]]
    values = [v for _, v, _, _ in BILLINGS] + [FORECAST_2026[1]]
    deltas = [d for _, _, d, _ in BILLINGS] + [FORECAST_2026[2]]

    # 확정 실적은 채운 막대, 전망치는 테두리만 — 눈으로 바로 구분되게.
    for x, value, delta in zip(years, values, deltas):
        actual = x != FORECAST_2026[0]
        ax.bar(
            x, value, width=0.58,
            color=PALETTE[0] if actual else SURFACE,
            edgecolor=PALETTE[0], linewidth=0 if actual else 2.0,
            linestyle="solid" if actual else (0, (4, 2)),
            zorder=3,
        )
        ax.annotate(
            f"{value}억달러",
            (x, value), xytext=(0, 10), textcoords="offset points",
            ha="center", va="bottom", fontsize=11, fontweight="bold",
            color=INK if actual else PALETTE[0], zorder=5,
        )
        ax.annotate(
            delta,
            (x, value), xytext=(0, 26), textcoords="offset points",
            ha="center", va="bottom", fontsize=9.5,
            color=MUTED, zorder=5,
        )

    # 1분기 실적 연율 환산선. 전망치(297)보다 위에 있다는 게 이 차트의 핵심.
    ax.axhline(ANNUALIZED, color=PALETTE[1], linewidth=1.4,
               linestyle=(0, (5, 3)), zorder=2)
    ax.annotate(
        f"2026년 1분기 실적 연율 환산 {ANNUALIZED:.0f}억달러",
        (2021.55, ANNUALIZED), xytext=(0, 6), textcoords="offset points",
        ha="left", va="bottom", fontsize=9.5, fontweight="bold", color=PALETTE[1],
    )

    ax.set_xticks(years)
    ax.set_xticklabels(
        [f"{y}" if y != 2026 else "2026 (전망)" for y in years],
        fontsize=11, color=INK_SECONDARY,
    )
    ax.set_ylim(0, 400)
    ax.set_yticks(range(0, 401, 100))
    ax.set_ylabel("한국 반도체 장비 매출 (억달러)", color=INK_SECONDARY,
                  fontsize=10.5, labelpad=10)
    ax.tick_params(axis="y", colors=INK_SECONDARY, labelsize=10)
    ax.tick_params(axis="x", length=0)

    ax.grid(axis="y", color=GRID, linewidth=0.9, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)

    fig.suptitle("한국 반도체 장비 매출 추이와 2026년 전망",
                 x=0.055, ha="left", y=0.975, fontsize=16,
                 fontweight="bold", color=INK)
    fig.text(0.055, 0.912,
             "메모리 재고조정으로 2년 연속 감소한 뒤, HBM·첨단 D램 투자가 시장을 다시 밀어 올렸다.",
             ha="left", fontsize=10.5, color=INK_SECONDARY)

    fig.text(
        0.055, 0.045,
        "2022~2025년은 SEMI 지역별 빌링스 확정 실적. 2026년 297억달러는 '팹 장비 투자' 기준 전망치로,\n"
        "빌링스보다 좁은 기준이라 같은 잣대가 아니다. 2026년 1분기 빌링스 89.3억달러를 단순 연율 환산하면\n"
        "357억달러로 전망치를 웃돈다 — 실제 2026년 빌링스는 297억달러보다 높게 나올 가능성이 크다.\n"
        "자료: SEMI 보도자료(2023.04·2024.04·2026.04·2026.06), 뉴스N연합(2026)",
        ha="left", fontsize=9, color=MUTED, linespacing=1.6,
    )

    fig.subplots_adjust(left=0.09, right=0.97, top=0.855, bottom=0.235)
    fig.savefig(OUT, dpi=200, facecolor=SURFACE)
    plt.close(fig)


if __name__ == "__main__":
    setup_font()
    draw()
    print(f"saved: {OUT}")
