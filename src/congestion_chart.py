"""Matplotlib dashboards for the console application."""
from __future__ import annotations

import math
import os
import re
from pathlib import Path

# Use a smaller on-screen canvas. PNG exports use 160 DPI.
PREVIEW_DPI = 45

LEVELS = {"여유": 1, "보통": 2, "약간 붐빔": 3, "붐빔": 4}
LEVEL_LABELS = {1: "여유", 2: "보통", 3: "약간 붐빔", 4: "붐빔"}


def _configure_font(plt, font_manager) -> None:
    manager = font_manager.fontManager
    if os.name == "nt":
        # The cached font list can omit fonts installed after Matplotlib first ran.
        font_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        registered_paths = {Path(font.fname) for font in manager.ttflist}
        for name in ("malgun.ttf", "malgunbd.ttf"):
            path = font_dir / name
            if path.is_file() and path not in registered_paths:
                manager.addfont(path)

    installed_fonts = {font.name for font in manager.ttflist}
    for font_name in ("Malgun Gothic", "Apple SD Gothic Neo", "NanumGothic", "Noto Sans CJK KR", "Gulim"):
        if font_name in installed_fonts:
            plt.rcParams["font.family"] = font_name
            break
    plt.rcParams["axes.unicode_minus"] = False


def _save_and_show(plt, fig, output: Path, show: bool) -> None:
    from matplotlib.backend_bases import FigureManagerBase

    try:
        fig.savefig(output, dpi=160, bbox_inches="tight")
        if show:
            manager = fig.canvas.manager
            if os.name == "nt" and type(manager).show is FigureManagerBase.show:
                # Non-interactive backends can save PNGs but cannot open windows.
                try:
                    os.startfile(output.resolve())
                except OSError:
                    print(f"이미지 뷰어를 열 수 없습니다. 저장된 파일을 확인하세요: {output.resolve()}")
            else:
                window = getattr(manager, "window", None)
                if os.name == "nt" and hasattr(window, "wm_geometry"):
                    # Leave room for the editor on the left of the preview.
                    window.wm_geometry("-24+80")
                plt.show()
    finally:
        plt.close(fig)


def is_sample_congestion(congestion: str | None) -> bool:
    return isinstance(congestion, str) and congestion.strip().endswith(" (샘플)")


def _normalize(congestion: str | None) -> tuple[int | None, str]:
    raw = congestion if isinstance(congestion, str) else ""
    label = raw.replace(" (샘플)", "").strip()
    return LEVELS.get(label), label if label in LEVELS else "정보 없음"


def parse_temperature(weather: str | float | None) -> float | None:
    match = re.fullmatch(r"([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*(?:°C)?", str(weather).strip())
    if match:
        value = float(match.group(1))
        if math.isfinite(value):
            return value
    return None


def plot_congestion_comparison(
    first_area: str,
    first_congestion: str | None,
    second_area: str,
    second_congestion: str | None,
    first_weather: str | None = None,
    second_weather: str | None = None,
    output_path: str | Path | None = None,
    show: bool = True,
) -> Path:
    """밝은 카드형 화면에서 두 지역의 혼잡도와 기온을 비교합니다."""
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.patches import FancyBboxPatch, Wedge

    _configure_font(plt, font_manager)
    first_score, first_label = _normalize(first_congestion)
    second_score, second_label = _normalize(second_congestion)
    output = Path(output_path) if output_path else Path(__file__).resolve().parents[1] / "experiments" / "congestion_comparison.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    bg, ink, muted = "#fbf7ed", "#282b35", "#7e8085"
    palette = ["#86a88c", "#e4cb70", "#dc9867", "#be705e"]
    fig = plt.figure(figsize=(16, 9), dpi=PREVIEW_DPI, facecolor=bg)
    first_sample = is_sample_congestion(first_congestion)
    second_sample = is_sample_congestion(second_congestion)
    mixed_sources = first_sample != second_sample
    source_summary = "실시간·시연 혼합" if mixed_sources else ("시연 데이터" if first_sample else "실시간")
    fig.text(0.045, 0.92, "서울 실시간 도시데이터  ·  " + source_summary,
             color="#46516a", fontsize=13, fontweight="bold")
    fig.text(0.045, 0.82, "지역별 혼잡도 비교", color=ink, fontsize=31, fontweight="bold")
    fig.text(0.70, 0.835, "두 지역 혼잡도", color=ink, fontsize=20, fontweight="bold", ha="center")

    def add_card(rect, edge="#ebe7df"):
        ax = fig.add_axes(rect)
        ax.set_axis_off()
        ax.add_patch(FancyBboxPatch((0, 0), 1, 1,
                        boxstyle="round,pad=0.012,rounding_size=0.045",
                        transform=ax.transAxes, facecolor="#ffffff", edgecolor=edge,
                        linewidth=1.2, clip_on=False))
        return ax

    def summary_card(y, label, value, note=""):
        ax = add_card([0.045, y, 0.245, 0.19])
        ax.text(0.08, 0.76, label, transform=ax.transAxes, color=muted, fontsize=13, fontweight="bold")
        ax.text(0.08, 0.31, value, transform=ax.transAxes, color="#26344d", fontsize=27, fontweight="bold")
        if note:
            ax.text(0.62, 0.35, note, transform=ax.transAxes, color="#a38b60", fontsize=12, fontweight="bold")

    summary_card(0.62, "조회 지역", "2개")
    if mixed_sources:
        summary_card(0.395, "데이터 출처가 다릅니다", "평균 산출 생략")
    elif first_score is None or second_score is None:
        summary_card(0.395, "평균 혼잡도", "정보 없음")
    else:
        avg_score = (first_score + second_score) / 2
        avg_level = min(4, max(1, int(math.floor(avg_score + 0.5))))
        summary_card(0.395, "평균 혼잡도", LEVEL_LABELS[avg_level], f"{avg_score:.1f} / 4")
    if not mixed_sources:
        temps = [parse_temperature(weather) for weather in (first_weather, second_weather)]
        temps = [value for value in temps if value is not None]
        summary_card(0.17, "날씨 요약", "기온",
                     f"평균 {sum(temps)/len(temps):.1f}°C" if temps else "정보 없음")

    def draw_region_card(rect, name, score, label, weather):
        ax = add_card(rect)
        ax.text(0.5, 0.90, name, transform=ax.transAxes, color=ink, fontsize=19,
                fontweight="bold", ha="center", va="center")
        center, radius = (0.5, 0.55), 0.25
        for index, color in enumerate(palette):
            theta1 = 180 - (index + 1) * 45
            theta2 = 180 - index * 45
            ax.add_patch(Wedge(center, radius, theta1, theta2, width=0.065,
                               transform=ax.transAxes,
                               facecolor=color if score and index < score else "#e8e8e8", edgecolor="none"))
        if score:
            angle = math.radians(180 - score * 45)
            tip = (center[0] + radius * 0.72 * math.cos(angle), center[1] + radius * 0.72 * math.sin(angle))
            ax.plot([center[0], tip[0]], [center[1], tip[1]], transform=ax.transAxes,
                    color="#556b80", linewidth=2.4, solid_capstyle="round")
            ax.scatter([center[0]], [center[1]], transform=ax.transAxes, s=24, color="#556b80", zorder=4)
        ax.text(0.5, 0.39, f"{score}/4" if score else "--/4", transform=ax.transAxes, ha="center",
                color="#28344a", fontsize=32, fontweight="bold")
        ax.text(0.5, 0.30, label, transform=ax.transAxes, ha="center",
                color=palette[score - 1] if score else muted, fontsize=15, fontweight="bold")
        ax.plot([0.08, 0.92], [0.21, 0.21], transform=ax.transAxes, color="#e7e4df", lw=1)
        temperature = parse_temperature(weather)
        temp = f"{temperature:.1f}°C" if temperature is not None else "정보 없음"
        ax.text(0.09, 0.13, "기온", transform=ax.transAxes, color=muted, fontsize=12, fontweight="bold")
        ax.text(0.09, 0.055, temp, transform=ax.transAxes, color=ink, fontsize=20, fontweight="bold")
        for j in range(3):
            ax.add_patch(FancyBboxPatch((0.48, 0.055 + j * 0.047), 0.42, 0.029,
                         boxstyle="round,pad=0.005,rounding_size=0.02", transform=ax.transAxes,
                         facecolor=(palette[min(j, 2)] if score and j < score else "#dedfe1"), edgecolor="none"))

    draw_region_card([0.33, 0.17, 0.29, 0.59], first_area, first_score, first_label, first_weather)
    draw_region_card([0.65, 0.17, 0.29, 0.59], second_area, second_score, second_label, second_weather)
    for x, sample in ((0.34, first_sample), (0.66, second_sample)):
        fig.text(x, 0.78, "시연 데이터" if sample else "실시간 데이터",
                 color=muted, fontsize=11, fontweight="bold")
    fig.text(0.045, 0.055, "혼잡도는 서울시 API의 4단계 분류를 표시합니다. 실제 백분율이 아닙니다.",
             color=muted, fontsize=10)
    _save_and_show(plt, fig, output, show)
    return output

def plot_area_dashboard(
    area_name: str,
    congestion: str | None,
    weather: str | None,
    output_path: str | Path | None = None,
    show: bool = True,
) -> Path:
    """선택한 한 지역의 혼잡도와 날씨를 밝은 카드형 화면으로 표시합니다."""
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.patches import FancyBboxPatch, Wedge

    _configure_font(plt, font_manager)
    output = Path(output_path) if output_path else Path(__file__).resolve().parents[1] / "experiments" / "area_dashboard.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    score, label = _normalize(congestion)
    value = parse_temperature(weather)
    temperature = f"{value:.1f}°C" if value is not None else "정보 없음"
    bg, ink, muted = "#fbf7ed", "#282b35", "#7e8085"
    palette = ["#86a88c", "#e4cb70", "#dc9867", "#be705e"]
    fig = plt.figure(figsize=(16, 9), dpi=PREVIEW_DPI, facecolor=bg)
    fig.text(0.045, 0.92, "서울 실시간 도시데이터", color="#46516a", fontsize=13, fontweight="bold")
    fig.text(0.045, 0.82, "대시보드 화면", color=ink, fontsize=31, fontweight="bold")
    fig.text(0.95, 0.835, "단일 지역 실시간 현황", color=ink, fontsize=17, fontweight="bold", ha="right")

    def card(rect, edge="#ebe7df"):
        ax = fig.add_axes(rect)
        ax.set_axis_off()
        ax.add_patch(FancyBboxPatch((0, 0), 1, 1,
                        boxstyle="round,pad=0.012,rounding_size=0.045",
                        transform=ax.transAxes, facecolor="#ffffff", edgecolor=edge,
                        linewidth=1.2, clip_on=False))
        return ax

    def summary(rect, title, value, note="", edge="#ebe7df"):
        ax = card(rect, edge)
        ax.text(0.08, 0.76, title, transform=ax.transAxes, color=muted, fontsize=13, fontweight="bold")
        ax.text(0.08, 0.30, value, transform=ax.transAxes, color="#26344d", fontsize=21, fontweight="bold")
        if note:
            ax.text(0.08, 0.10, note, transform=ax.transAxes, color=muted, fontsize=9)

    summary([0.045, 0.59, 0.245, 0.16], "조회 지역", "1개", area_name)
    summary([0.045, 0.38, 0.245, 0.16], "현재 혼잡도", label if score else "정보 없음",
            f"{score}/4단계" if score else "API 응답에 값이 없습니다")
    sample_mode = is_sample_congestion(congestion)
    summary([0.045, 0.17, 0.245, 0.16], "시스템 안내",
            "시연 데이터" if sample_mode else "실시간 API",
            "혼잡도는 API 4단계로 표시합니다.", edge="#e3c78d")

    ax = card([0.34, 0.12, 0.61, 0.63])
    ax.text(0.055, 0.91, area_name, transform=ax.transAxes, color=ink, fontsize=24, fontweight="bold")
    ax.text(0.06, 0.73, f"{score}/4" if score else "--/4", transform=ax.transAxes,
            color=palette[score - 1] if score else muted, fontsize=36, fontweight="bold")
    ax.text(0.065, 0.63, f"혼잡 단계: {label}" if score else "혼잡도 정보 없음",
            transform=ax.transAxes, color=ink, fontsize=14)
    center, radius = (0.73, 0.70), 0.21
    for i, color in enumerate(palette):
        theta1, theta2 = 180 - (i + 1) * 45, 180 - i * 45
        ax.add_patch(Wedge(center, radius, theta1, theta2, width=0.06,
                           transform=ax.transAxes,
                           facecolor=color if score and i < score else "#e8e8e8", edgecolor="none"))
    if score:
        angle = math.radians(180 - score * 45)
        tip = (center[0] + radius * 0.70 * math.cos(angle), center[1] + radius * 0.70 * math.sin(angle))
        ax.plot([center[0], tip[0]], [center[1], tip[1]], transform=ax.transAxes,
                color="#556b80", linewidth=2.4, solid_capstyle="round")
        ax.scatter([center[0]], [center[1]], transform=ax.transAxes, s=26, color="#556b80", zorder=4)
    ax.add_patch(FancyBboxPatch((0.055, 0.38), 0.89, 0.20,
                   boxstyle="round,pad=0.01,rounding_size=0.025", transform=ax.transAxes,
                   facecolor="#fbfaf7", edgecolor="#e7e4df", linewidth=1))
    ax.text(0.09, 0.525, "혼잡도 4단계 게이지", transform=ax.transAxes, color=ink,
            fontsize=13, fontweight="bold")
    for i, color in enumerate(palette):
        ax.add_patch(FancyBboxPatch((0.25 + i*0.17, 0.455), 0.15, 0.035,
                       boxstyle="round,pad=0.005,rounding_size=0.02", transform=ax.transAxes,
                       facecolor=color if score and i < score else "#e8e8e8", edgecolor="none"))
    ax.text(0.09, 0.395, "여유 · 보통 · 약간 붐빔 · 붐빔", transform=ax.transAxes,
            color=muted, fontsize=9)
    ax.plot([0.055, 0.945], [0.33, 0.33], transform=ax.transAxes, color="#e7e4df", lw=1)
    ax.text(0.07, 0.235, "기온", transform=ax.transAxes, color=muted, fontsize=13, fontweight="bold")
    ax.text(0.07, 0.12, temperature, transform=ax.transAxes, color=ink, fontsize=23, fontweight="bold")
    for i in range(3):
        ax.add_patch(FancyBboxPatch((0.48, 0.22 - i*0.07), 0.42, 0.043,
                       boxstyle="round,pad=0.004,rounding_size=0.02", transform=ax.transAxes,
                       facecolor=(palette[min(i, 2)] if score and i < score else "#dedfe1"), edgecolor="none"))
    freshness = "샘플 데이터입니다." if sample_mode else "API 갱신 시각에 따라 값이 달라질 수 있습니다."
    ax.text(0.48, 0.055, freshness, transform=ax.transAxes, color=muted, fontsize=9)
    fig.text(0.045, 0.055, "혼잡도는 서울시 API의 4단계 분류를 표시합니다. 실제 백분율이 아닙니다.",
             color=muted, fontsize=10)
    _save_and_show(plt, fig, output, show)
    return output

def plot_full_dashboard(rows, output_path: str | Path | None = None, show: bool = True) -> Path:
    """모든 지역의 혼잡도와 기온을 나란한 그래프로 표시합니다."""
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    _configure_font(plt, font_manager)
    output = Path(output_path) if output_path else Path(__file__).resolve().parents[1] / "experiments" / "full_dashboard.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    bg, panel, ink, muted = "#fbf7ed", "#eef0f1", "#283044", "#747982"
    palette = {1: "#8eaa8e", 2: "#d8c477", 3: "#d9a76d", 4: "#c78066"}
    names, scores, temps, temp_names = [], [], [], []
    sources = set()
    for place, data in rows:
        name = getattr(place, "area_name", str(place))
        congestion = getattr(data, "congestion", None)
        sample = is_sample_congestion(congestion)
        sources.add(sample)
        if sample:
            name += "\n(시연)"
        score, _ = _normalize(congestion)
        if score is not None:
            names.append(name)
            scores.append(score * 25)
        temperature = parse_temperature(getattr(data, "weather", None))
        if temperature is not None:
            temp_names.append(name)
            temps.append(temperature)
    source_label = "실시간 분석"
    if len(sources) == 2:
        source_label = "실시간·시연 혼합"
    elif sources == {True}:
        source_label = "시연 데이터"
    fig = plt.figure(figsize=(16, 9), dpi=PREVIEW_DPI, facecolor=bg)
    fig.text(0.045, 0.94, "서울 실시간 도시데이터", color="#596274", fontsize=13, fontweight="bold")
    fig.text(0.045, 0.855, "서울 실시간 도시데이터 대시보드", color=ink, fontsize=27, fontweight="bold")
    fig.text(0.95, 0.87, source_label,
             color="#907748", fontsize=11, fontweight="bold", ha="right",
             bbox={"boxstyle": "round,pad=0.45", "facecolor":"#eee5d3", "edgecolor":"none"})
    congestion_ax = fig.add_axes([0.085, 0.24, 0.38, 0.51])
    temperature_ax = fig.add_axes([0.575, 0.24, 0.38, 0.51])
    for ax in (congestion_ax, temperature_ax):
        ax.set_facecolor(panel)
        for spine in ax.spines.values():
            spine.set_color("#e0e2e3")
        ax.tick_params(colors=muted, labelsize=9)
        ax.grid(axis="y", color="#c9cdd0", alpha=0.6, linewidth=0.7)
        ax.set_axisbelow(True)
    if names:
        bar_colors = [palette[min(4, max(1, round(value / 25)))] for value in scores]
        bars = congestion_ax.bar(names, scores, color=bar_colors, width=0.68)
        congestion_ax.set_ylim(0, 112)
        congestion_ax.set_yticks((0, 20, 40, 60, 80, 100))
        congestion_ax.set_ylabel("혼잡 단계 지수 (0–100)", color=muted, fontsize=10)
        congestion_ax.tick_params(axis="x", labelrotation=32, colors=ink)
        for bar, value in zip(bars, scores):
            congestion_ax.text(bar.get_x() + bar.get_width()/2, value + 2, f"{value}점",
                               ha="center", color=ink, fontsize=8, fontweight="bold")
    else:
        congestion_ax.text(0.5, 0.5, "혼잡도 정보가 없습니다", ha="center", color=ink,
                          transform=congestion_ax.transAxes)
    congestion_ax.set_title("지역별 혼잡 단계 지수", loc="left", color=ink, fontsize=14,
                            fontweight="bold", pad=12)
    if temp_names:
        bars = temperature_ax.bar(temp_names, temps, color="#9bb8ca", width=0.68)
        bottom, top = min(0, min(temps)), max(0, max(temps))
        padding = max(2, (top - bottom) * 0.15)
        temperature_ax.set_ylim(bottom - padding if bottom < 0 else 0, top + padding)
        temperature_ax.axhline(0, color=muted, linewidth=0.8)
        temperature_ax.set_ylabel("기온 (°C)", color=muted, fontsize=10)
        temperature_ax.tick_params(axis="x", labelrotation=32, colors=ink)
        for bar, value in zip(bars, temps):
            temperature_ax.annotate(
                f"{value:.1f}°C",
                (bar.get_x() + bar.get_width() / 2, value),
                xytext=(0, 3 if value >= 0 else -3), textcoords="offset points",
                ha="center", va="bottom" if value >= 0 else "top",
                color=ink, fontsize=8, fontweight="bold",
            )
    else:
        temperature_ax.text(0.5, 0.5, "기온 정보가 없습니다", ha="center", color=ink,
                            transform=temperature_ax.transAxes)
    temperature_ax.set_title("지역별 기온 비교", loc="left", color=ink, fontsize=14,
                             fontweight="bold", pad=12)
    fig.text(0.045, 0.085, "혼잡 지수는 API의 4단계 혼잡도를 바탕으로 환산한 값이며, 실제 백분율이 아닙니다.",
             color=muted, fontsize=9)
    _save_and_show(plt, fig, output, show)
    return output


