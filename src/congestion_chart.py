"""혼잡도·교통혼잡도 카드형 그래프. 실제/샘플 데이터를 구분합니다."""
from __future__ import annotations
import math
import os
import re
from pathlib import Path

PREVIEW_DPI = 70
LEVELS = {"여유":1,"보통":2,"약간 붐빔":3,"붐빔":4}
TRAFFIC_LEVELS = {"원활":1,"서행":2,"정체":3}
CROWD_COLORS = ["#85a98d", "#e6cf72", "#df9666", "#bd7460"]
TRAFFIC_COLORS = ["#76a894", "#e4c76b", "#d78363"]
BG, INK, MUTED, LINE = "#faf7ef", "#283447", "#7d8590", "#e9e4dc"


def _configure_font(plt, font_manager):
    manager = font_manager.fontManager
    if os.name == "nt":
        font_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        for name in ("malgun.ttf", "malgunbd.ttf"):
            p = font_dir / name
            if p.is_file():
                manager.addfont(str(p))
    installed = {f.name for f in manager.ttflist}
    for name in ("Malgun Gothic", "Apple SD Gothic Neo", "NanumGothic", "Noto Sans CJK KR", "DejaVu Sans"):
        if name in installed:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def _save_and_show(plt, fig, output, show):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(output, dpi=160, bbox_inches="tight", facecolor=BG)
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


def _card(fig, rect):
    from matplotlib.patches import FancyBboxPatch
    ax=fig.add_axes(rect)
    ax.axis("off")
    ax.set_xlim(0,1);ax.set_ylim(0,1)
    ax.add_patch(FancyBboxPatch((0.005,0.005),0.99,0.99,
        boxstyle="round,pad=0.0,rounding_size=0.04",facecolor="white",edgecolor=LINE,lw=1.15))
    return ax


def _text(ax,x,y,s,size=13,color=INK,weight="normal",ha="left"):
    ax.text(x,y,str(s),ha=ha,va="center",fontsize=size,color=color,fontweight=weight,
            transform=ax.transAxes,clip_on=False)


def _gauge(ax,level,number,center,radius,palette):
    from matplotlib.patches import Wedge
    for i,color in enumerate(palette):
        a1=180-(i+1)*180/number
        a2=180-i*180/number
        ax.add_patch(Wedge(center,radius,a1,a2,width=radius*.23,transform=ax.transAxes,
                           facecolor=color if level is not None else "#dedede",edgecolor="none"))
    if level is not None:
        angle=math.radians(180-(level-.5)*180/number)
        x=center[0]+radius*.71*math.cos(angle)
        y=center[1]+radius*.71*math.sin(angle)
        ax.plot([center[0],x],[center[1],y],transform=ax.transAxes,color="#586e82",lw=2.2)
        ax.scatter([center[0]],[center[1]],transform=ax.transAxes,s=27,color="#586e82",zorder=4)


def _traffic_label(traffic):
    return str(traffic).strip() if str(traffic).strip() in TRAFFIC_LEVELS else "정보 없음"


def _traffic_card(ax,title,traffic,subtext=None):
    label=_traffic_label(traffic)
    level=TRAFFIC_LEVELS.get(label)
    _text(ax,.07,.92,title,18,INK,"bold")
    _gauge(ax,level,3,(.5,.61),.31,TRAFFIC_COLORS)
    _text(ax,.5,.35,label,27,TRAFFIC_COLORS[level-1] if level else MUTED,"bold","center")
    _text(ax,.5,.24,f"{level}/3 단계" if level else "도로소통 정보 미제공",13,MUTED,ha="center")
    if subtext:
        _text(ax,.5,.12,subtext,11,MUTED,ha="center")


def _crowd_detail(ax,area,congestion,weather):
    level,label=_normalize(congestion)
    _text(ax,.06,.91,area,21,INK,"bold")
    _text(ax,.06,.72,label,27,CROWD_COLORS[level-1] if level else MUTED,"bold")
    _text(ax,.065,.61,f"{level}/4 단계" if level else "정보 없음",14,MUTED)
    _gauge(ax,level,4,(.77,.68),.20,CROWD_COLORS)
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((.05,.36),.90,.16,boxstyle="round,pad=0,rounding_size=.025",
                 edgecolor=LINE,facecolor="#faf9f6",lw=.8,transform=ax.transAxes))
    _text(ax,.085,.47,"혼잡도 4단계 게이지",12,INK,"bold")
    for i,col in enumerate(CROWD_COLORS):
        ax.add_patch(FancyBboxPatch((.12+i*.20,.405),.17,.025,
                        boxstyle="round,pad=0.002,rounding_size=.012",facecolor=col if level and i<level else "#e3e3e3",edgecolor="none",transform=ax.transAxes))
    ax.plot([.06,.94],[.30,.30],transform=ax.transAxes,color=LINE,lw=1)
    _text(ax,.07,.21,"기온",13,MUTED)
    temp=parse_temperature(weather)
    _text(ax,.07,.12,f"{temp:.1f}°C" if temp is not None else "정보 없음",22,INK,"bold")
    _text(ax,.54,.13,"시연 데이터" if is_sample_congestion(congestion) else "API 조회 데이터",11,MUTED)


def plot_area_dashboard(area_name,congestion,weather,output_path=None,show=True,traffic=None):
    """좌측 교통상황, 우측 인구혼잡도·기온. 기존 위치 인수 호환."""
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    _configure_font(plt,font_manager)
    output=Path(output_path) if output_path else Path(__file__).resolve().parents[1]/"experiments"/"area_dashboard.png"
    fig=plt.figure(figsize=(16,9),dpi=PREVIEW_DPI,facecolor=BG)
    fig.text(.045,.92,"서울 도시데이터",fontsize=13,color="#46516a",weight="bold")
    fig.text(.045,.82,"대시보드 화면",fontsize=31,color=INK,weight="bold")
    fig.text(.95,.835,"단일 지역 시연 데이터" if is_sample_congestion(congestion) else "단일 지역 API 데이터",fontsize=16,color=INK,ha="right")
    left=_card(fig,[.045,.13,.29,.61])
    _traffic_card(left,"교통상황",traffic,"도로소통: 원활 · 서행 · 정체")
    right=_card(fig,[.365,.13,.59,.61])
    _crowd_detail(right,area_name,congestion,weather)
    fig.text(.045,.058,"※ 인구혼잡도 4단계 · 도로 교통혼잡도 3단계 (퍼센트가 아닌 분류 등급)",color=MUTED,fontsize=11)
    if is_sample_congestion(congestion):fig.text(.95,.058,"시연용 가상 데이터 · 실제 혼잡도가 아닙니다",ha="right",color="#b27649",fontsize=11)
    _save_and_show(plt,fig,output,show)
    return output


def _comparison_region(ax,name,congestion,weather):
    level,label=_normalize(congestion)
    _text(ax,.5,.91,name,17,INK,"bold","center")
    _gauge(ax,level,4,(.5,.62),.20,CROWD_COLORS)
    _text(ax,.5,.42,label,22,CROWD_COLORS[level-1] if level else MUTED,"bold","center")
    _text(ax,.5,.32,f"{level}/4 단계" if level else "정보 없음",12,MUTED,ha="center")
    ax.plot([.08,.92],[.24,.24],transform=ax.transAxes,color=LINE,lw=1)
    _text(ax,.09,.17,"기온",12,MUTED)
    temp=parse_temperature(weather)
    _text(ax,.09,.08,f"{temp:.1f}°C" if temp is not None else "정보 없음",19,INK,"bold")


def plot_congestion_comparison(first_area,first_congestion,second_area,second_congestion,
        first_weather=None,second_weather=None,output_path=None,show=True,
        first_traffic=None,second_traffic=None):
    """좌측 교통 비교, 우측 두 지역 인구혼잡도 비교. 기존 위치 인수 호환."""
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    _configure_font(plt,font_manager)
    output=Path(output_path) if output_path else Path(__file__).resolve().parents[1]/"experiments"/"congestion_comparison.png"
    fig=plt.figure(figsize=(16,9),dpi=PREVIEW_DPI,facecolor=BG)
    fig.text(.045,.92,"서울 도시데이터 · 지역 비교",fontsize=13,color="#46516a",weight="bold")
    fig.text(.045,.82,"지역별 혼잡도 비교",fontsize=30,color=INK,weight="bold")
    fig.text(.72,.835,"두 지역 인구혼잡도",fontsize=16,color=INK,weight="bold",ha="center")
    a=_card(fig,[.045,.13,.29,.61])
    _text(a,.07,.92,"교통상황 비교",18,INK,"bold")
    for y,name,value in [(.73,first_area,first_traffic),(.42,second_area,second_traffic)]:
        label=_traffic_label(value); level=TRAFFIC_LEVELS.get(label)
        _text(a,.07,y,name,14,INK,"bold")
        _text(a,.07,y-.13,label,22,TRAFFIC_COLORS[level-1] if level else MUTED,"bold")
        for i,col in enumerate(TRAFFIC_COLORS):
            from matplotlib.patches import FancyBboxPatch
            pass
        _gauge(a,level,3,(.72,y-.14),.15,TRAFFIC_COLORS)
    t1,t2=TRAFFIC_LEVELS.get(_traffic_label(first_traffic)),TRAFFIC_LEVELS.get(_traffic_label(second_traffic))
    if is_sample_congestion(first_congestion) != is_sample_congestion(second_congestion):
        compare="실시간·시연 데이터는 교통상황을 비교하지 않습니다"
    elif t1 and t2:
        compare=(f"{first_area} 도로가 더 정체" if t1>t2 else f"{second_area} 도로가 더 정체" if t2>t1 else "두 지역 도로소통 상태 동일")
    else: compare="교통 정보가 없어 비교할 수 없습니다"
    _text(a,.07,.14,compare,11,MUTED)
    first=_card(fig,[.365,.13,.28,.61]);second=_card(fig,[.67,.13,.285,.61])
    _comparison_region(first,first_area,first_congestion,first_weather)
    _comparison_region(second,second_area,second_congestion,second_weather)
    sample1=is_sample_congestion(first_congestion);sample2=is_sample_congestion(second_congestion)
    fig.text(.045,.057,"※ 교통혼잡도는 도로소통 등급이며 보행 인구혼잡도와 다른 지표입니다.",color=MUTED,fontsize=10)
    if sample1 or sample2:fig.text(.95,.057,"시연 데이터 포함 · 실제 측정값 아님" if sample1==sample2 else "실시간·시연 혼합: 비교 주의",color="#b27649",fontsize=10,ha="right")
    _save_and_show(plt,fig,output,show)
    return output
