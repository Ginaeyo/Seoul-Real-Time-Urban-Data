"""Plot congestion values from Seoul's real-time population API."""
from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

import requests

LEVELS = {"여유": 1, "보통": 2, "약간 붐빔": 3, "붐빔": 4}
BASE_URL = "http://openapi.seoul.go.kr:8088"


def parse_response(payload: bytes, requested_area: str) -> tuple[str, int]:
    """Return API area name and ordinal congestion from Seoul XML."""
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as error:
        raise ValueError("The API response was not valid XML.") from error

    result_code = root.findtext(".//RESULT.CODE") or root.findtext(".//CODE")
    if result_code and result_code != "INFO-000":
        message = root.findtext(".//RESULT.MESSAGE") or "The API rejected the request."
        raise ValueError(f"{requested_area}: Seoul API error {result_code}: {message}")

    area_name = root.findtext(".//AREA_NM") or requested_area
    congestion = next(
        (node.text.strip() for node in root.findall(".//AREA_CONGEST_LVL") if node.text and node.text.strip()),
        None,
    )
    if congestion not in LEVELS:
        raise ValueError(f"No supported congestion value was returned for {area_name}.")
    return area_name, LEVELS[congestion]


def fetch_area(area_name: str, api_key: str) -> tuple[str, int]:
    url = f"{BASE_URL}/{quote(api_key, safe='')}/xml/citydata_ppltn/1/5/{quote(area_name, safe='')}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        # Do not include the request exception: it can contain the key-bearing URL.
        raise RuntimeError(f"{area_name}: request failed. Check your key, connection, and exact supported-area name.") from error
    return parse_response(response.content, area_name)


def plot(names: list[str], scores: list[int], output: Path, sample_key: bool) -> None:
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(8, 4.8))
    colors = {1: "#22a06b", 2: "#ed9f24", 3: "#e66b34", 4: "#d74747"}
    bars = ax.bar(names, scores, color=[colors[score] for score in scores])
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4], ["여유", "보통", "약간 붐빔", "붐빔"])
    ax.set_ylabel("실시간 혼잡도")
    title = "서울 실시간 지역별 혼잡도 비교"
    if sample_key:
        title += " (샘플 키)"
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.22)
    labels = {1: "여유", 2: "보통", 3: "약간 붐빔", 4: "붐빔"}
    ax.bar_label(bars, labels=[labels[score] for score in scores], padding=4)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("areas", nargs="+", help="at least two supported Seoul area names")
    parser.add_argument("-o", "--output", type=Path, default=Path("experiments/congestion_comparison.png"))
    args = parser.parse_args()
    if len(args.areas) < 2:
        parser.error("provide at least two area names")

    api_key = os.getenv("SEOUL_API_KEY")
    if not api_key:
        parser.error("SEOUL_API_KEY is not set in this PowerShell window")

    names, scores = [], []
    try:
        for area in args.areas:
            name, score = fetch_area(area, api_key)
            names.append(name)
            scores.append(score)
        plot(names, scores, args.output, sample_key=api_key.lower() == "sample")
    except (RuntimeError, ValueError) as error:
        parser.exit(1, f"Could not create live chart: {error}\n")
    print(f"Chart saved to {args.output}")


if __name__ == "__main__":
    main()

