"""혼잡도·교통혼잡도 카드형 그래프. 실제/샘플 데이터를 구분합니다."""
from __future__ import annotations
import math
import os
import re
from pathlib import Path

PREVIEW_DPI = 70
LEVELS = {"여유":1,"보통":2,"약간 붐빔":3,"붐빔":4}
TRAFFIC_LEVELS = {"원활":1,"서행":2,"정체":3}
CROWD_COLORS = ["#397455", "#8a6800", "#a74e1c", "#ac393c"]
TRAFFIC_COLORS = ["#397455", "#8a6800", "#ac393c"]
BG, INK, MUTED, LINE = "#f7f8fb", "#172136", "#646f81", "#d9dde6"
PANEL = "#eef0f6"
ARC_COLORS = ("#48cd90", "#f5c635", "#f18549", "#e6544e")


def _configure_font(plt, font_manager):
    manager = font_manager.fontManager
    if os.name == "nt":
        font_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        for name in ("NotoSansKR-Regular.ttf", "NotoSansKR-Bold.ttf", "malgun.ttf", "malgunbd.ttf"):
            p = font_dir / name
            if p.is_file():
                manager.addfont(str(p))
    installed = {f.name for f in manager.ttflist}
    for name in ("Noto Sans KR", "Noto Sans CJK KR", "Malgun Gothic",
                 "Apple SD Gothic Neo", "NanumGothic", "DejaVu Sans"):
        if name in installed:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def _save_and_show(plt, fig, output, show):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(output, dpi=160, facecolor=BG)
        if show:
            from matplotlib.backend_bases import FigureManagerBase
            manager = fig.canvas.manager
            if os.name == "nt" and type(manager).show is FigureManagerBase.show:
                os.startfile(str(output.resolve()))
            else:
                plt.show()
    finally:
        plt.close(fig)


def is_sample_congestion(congestion):
    return isinstance(congestion, str) and congestion.strip().endswith(" (샘플)")


def _normalize(congestion):
    clean = str(congestion or "").replace(" (샘플)", "").strip()
    return LEVELS.get(clean), clean if clean in LEVELS else "정보 없음"


def parse_temperature(weather):
    match = re.fullmatch(r"([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*(?:°C)?", str(weather).strip())
    if match:
        n = float(match.group(1))
        return n if math.isfinite(n) else None
    return None



def _card(fig, rect, fill="white", shadow=False):
    from matplotlib.patches import FancyBboxPatch

    ax = fig.add_axes(rect)
    ax.set_axis_off()
    if shadow:
        for offset, alpha in ((.024, .025), (.014, .035), (.007, .05)):
            ax.add_patch(FancyBboxPatch(
                (.004, -offset), .997, 1, boxstyle="round,pad=0,rounding_size=.027",
                transform=ax.transAxes, facecolor=INK, edgecolor="none",
                alpha=alpha, clip_on=False,
            ))
    ax.add_patch(FancyBboxPatch(
        (0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=.027",
        transform=ax.transAxes, facecolor=fill, edgecolor=LINE, linewidth=1,
        clip_on=False,
    ))
    return ax


def _text(ax, x, y, value, size=14, color=INK, weight="normal", ha="left"):
    ax.text(x, y, value, fontsize=size, color=color, weight=weight,
            ha=ha, va="center", transform=ax.transAxes)


def _metric(fig, rect, title, value, color=INK, size=37):
    ax = _card(fig, rect, shadow=True)
    _text(ax, .09, .76, title, 19)
    _text(ax, .09, .38, value, size, color, "bold")
    return ax


def _traffic_value(traffic):
    label = str(traffic or "").strip()
    level = TRAFFIC_LEVELS.get(label)
    return (label, TRAFFIC_COLORS[level - 1]) if level else ("정보 없음", MUTED)


def _traffic_comparison(fig, rect, areas):
    ax = _card(fig, rect, shadow=True)
    _text(ax, .09, .79, "도로 교통상황", 19)
    for y, (name, traffic) in zip((.49, .23), areas):
        label, color = _traffic_value(traffic)
        _text(ax, .09, y, name, 13)
        _text(ax, .91, y, label, 24, color, "bold", "right")


def _header(plt, subtitle, samples):
    fig = plt.figure(figsize=(16, 9), dpi=PREVIEW_DPI, facecolor=BG)
    from matplotlib.patheffects import withStroke

    title = fig.text(.048, .884, "서울 실시간 도시데이터", fontsize=49, weight="bold", color=INK)
    title.set_path_effects([withStroke(linewidth=.85, foreground=INK)])
    fig.text(.049, .826, subtitle, fontsize=25, color=MUTED)
    source = "시연 데이터" if all(samples) else "실시간·시연 혼합" if any(samples) else "실시간 API"
    fig.text(.947, .850, source, fontsize=13, color=MUTED, ha="right")
    return fig


def _gauge(fig, rect, level):
    from matplotlib.patches import Wedge

    ax = fig.add_axes(rect, frameon=False)
    ax.set(xlim=(-1.05, 1.05), ylim=(-.07, 1.05), aspect="equal")
    ax.set_axis_off()
    ax.add_patch(Wedge((0, 0), 1, 0, 180, width=.22, facecolor="#dfe3eb"))
    if level:
        stop = 180 - 45 * level
        ax.add_patch(Wedge((0, 0), 1, stop, 180, width=.22,
                           facecolor=ARC_COLORS[level - 1]))
        needle = math.radians(stop + 22.5)
        ax.plot([0, .68 * math.cos(needle)], [0, .68 * math.sin(needle)],
                color="#62718a", lw=3, solid_capstyle="round")
        ax.scatter([0], [0], s=31, color="#62718a", zorder=3)


def _scale(ax, level, y, width):
    from matplotlib.patches import FancyBboxPatch

    step = width / len(ARC_COLORS)
    left = (1 - width) / 2
    for index, color in enumerate(ARC_COLORS, 1):
        ax.add_patch(FancyBboxPatch(
            (left + (index - 1) * step, y), step - .01, .028,
            boxstyle="round,pad=0,rounding_size=.01", transform=ax.transAxes,
            facecolor=color, edgecolor="none", alpha=1 if index == level else .62,
        ))


def _temperature_label(weather):
    temperature = parse_temperature(weather)
    return f"{temperature:.1f}°C" if temperature is not None else "정보 없음"


def _population_label(population):
    raw = str(population or "").split(" ", 1)[0].replace(",", "")
    return f"약 {int(raw):,}명" if raw.isdecimal() else "정보 없음"


def _environment_card(fig, readings, names=None):
    ax = _card(fig, [.064, .309, .29, .208], shadow=True)
    ax.plot([.56, .56], [.15, .86], color=LINE, linewidth=1, transform=ax.transAxes)
    _text(ax, .09, .78, "강수확률", 17)
    _text(ax, .63, .78, "미세먼지", 17)
    dust_colors = {
        "좋음": CROWD_COLORS[0], "보통": CROWD_COLORS[1],
        "나쁨": CROWD_COLORS[2], "매우나쁨": CROWD_COLORS[3],
    }
    for index, (rain_chance, dust_status) in enumerate(readings):
        rain = f"{rain_chance:g}%" if rain_chance is not None else "정보 없음"
        dust = dust_status or "정보 없음"
        color = dust_colors.get(dust.replace(" ", ""), MUTED)
        if names:
            y = (.47, .22)[index]
            name = names[index]
            compact_name = name.split("(", 1)[0]
            if len(compact_name) > 8:
                compact_name = compact_name[:7] + "…"
            _text(ax, .08, y, compact_name, 10)
            _text(ax, .53, y, rain, 18, INK, "bold", "right")
            _text(ax, .63, y, dust, 19, color, "bold")
        else:
            _text(ax, .09, .34, rain, 31 if rain_chance is not None else 19, INK, "bold")
            _text(ax, .63, .34, dust, 31 if len(dust) <= 2 else 19, color, "bold")


def _temperature_card(fig, title, weather):
    ax = _card(fig, [.523, .159, .334, .091])
    _text(ax, .08, .5, title, 22, MUTED)
    _text(ax, .92, .5, _temperature_label(weather), 25, INK, "bold", "right")


def _classification_note(fig):
    ax = _card(fig, [.44, .085, .499, .057], fill=PANEL)
    _text(ax, .5, .5, "인구혼잡도는 서울시 API의 4단계 분류입니다.", 13, MUTED, ha="center")


def plot_area_dashboard(area_name, congestion, weather, output_path=None,
                        show=True, traffic=None, population=None,
                        rain_chance=None, dust_status=None):
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    _configure_font(plt, font_manager)
    output = Path(output_path) if output_path else Path(__file__).resolve().parents[1] / "experiments" / "area_dashboard.png"
    fig = _header(plt, "대시보드 화면 · 단일 지역 현황", [is_sample_congestion(congestion)])
    level, label = _normalize(congestion)
    status_color = CROWD_COLORS[level - 1] if level else MUTED
    traffic_label, traffic_color = _traffic_value(traffic)
    _metric(fig, [.064, .555, .29, .208], "도로 교통상황", traffic_label, traffic_color)
    _environment_card(fig, [(rain_chance, dust_status)])
    _metric(fig, [.064, .063, .29, .208], "추정 인구", _population_label(population))

    frame = _card(fig, [.413, .063, .54, .70], shadow=True)
    _text(frame, .5, .924, area_name, 24, weight="bold", ha="center")
    panel = _card(fig, [.435, .273, .496, .414], fill=PANEL)
    _gauge(fig, [.582, .477, .205, .187], level)
    _text(panel, .5, .38, label, 43, status_color, "bold", "center")
    _text(panel, .5, .22, "인구혼잡도", 17, MUTED, ha="center")
    _scale(panel, level, .08, .62)
    _temperature_card(fig, "기온", weather)
    _classification_note(fig)
    _save_and_show(plt, fig, output, show)
    return output


def _comparison_region(fig, left, name, congestion, weather):
    panel = _card(fig, [left, .273, .239, .414], fill=PANEL)
    level, label = _normalize(congestion)
    _text(panel, .5, .884, name, 23 if len(name) <= 11 else 19, weight="bold", ha="center")
    _gauge(fig, [left + .022, .438, .195, .160], level)
    color = CROWD_COLORS[level - 1] if level else MUTED
    _text(panel, .5, .334, label, 33, color, "bold", "center")
    _scale(panel, level, .19, .84)
    _text(panel, .10, .082, "기온", 14, MUTED)
    _text(panel, .90, .082, _temperature_label(weather), 19, weight="bold", ha="right")


def plot_congestion_comparison(first_area, first_congestion, second_area, second_congestion,
                               first_weather=None, second_weather=None, output_path=None,
                               show=True, first_traffic=None, second_traffic=None,
                               first_population=None, second_population=None,
                               first_environment=(None, None), second_environment=(None, None)):
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    _configure_font(plt, font_manager)
    output = Path(output_path) if output_path else Path(__file__).resolve().parents[1] / "experiments" / "congestion_comparison.png"
    samples = [is_sample_congestion(first_congestion), is_sample_congestion(second_congestion)]
    comparable = samples[0] == samples[1]
    fig = _header(plt, "대시보드 화면 · 두 지역 혼잡도 비교", samples)

    _traffic_comparison(fig, [.064, .555, .29, .208],
                        [(first_area, first_traffic), (second_area, second_traffic)])
    _environment_card(fig, [first_environment, second_environment], [first_area, second_area])
    population = _card(fig, [.064, .063, .29, .208], shadow=True)
    _text(population, .09, .79, "추정 인구", 19)
    for y, (name, value) in zip((.49, .23), [(first_area, first_population), (second_area, second_population)]):
        _text(population, .09, y, name, 13)
        _text(population, .91, y, _population_label(value), 15, INK, "bold", "right")

    frame = _card(fig, [.413, .063, .54, .70], shadow=True)
    _text(frame, .5, .924, f"{first_area} vs {second_area}", 21, weight="bold", ha="center")
    _comparison_region(fig, .435, first_area, first_congestion, first_weather)
    _comparison_region(fig, .692, second_area, second_congestion, second_weather)
    temps = [parse_temperature(first_weather), parse_temperature(second_weather)]
    average = sum(temps) / 2 if comparable and None not in temps else None
    _temperature_card(fig, "평균 기온", average)
    _classification_note(fig)
    _save_and_show(plt, fig, output, show)
    return output
