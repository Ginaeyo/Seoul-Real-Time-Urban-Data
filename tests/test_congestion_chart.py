import os
import sys

os.environ.setdefault("MPLBACKEND", "Agg")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from congestion_chart import plot_area_dashboard


def test_single_area_dashboard_renders_sample_and_missing_weather(tmp_path):
    output = tmp_path / "area_dashboard.png"

    result = plot_area_dashboard(
        "강남역",
        "약간 붐빔 (샘플)",
        None,
        output_path=output,
        show=False, data_source="sample",
    )

    assert result == output
    assert output.exists()
    assert output.stat().st_size > 10_000



def test_two_area_dashboard_renders_weather_and_sample_marker(tmp_path):
    from congestion_chart import plot_congestion_comparison

    output = tmp_path / "comparison.png"
    result = plot_congestion_comparison(
        "강남역", "약간 붐빔 (샘플)",
        "홍대입구역(2호선)", "여유 (샘플)",
        "18.5°C", "16.3°C",
        output_path=output, show=False, first_data_source="sample", second_data_source="sample", average_temperature=17.4,
    )

    assert result == output
    assert output.exists()
    assert output.stat().st_size > 10_000


def test_comparison_preserves_weather_when_congestion_is_missing(monkeypatch, tmp_path):
    from matplotlib.figure import Figure
    from congestion_chart import plot_congestion_comparison

    rendered_text = []
    savefig = Figure.savefig

    def capture_labels(figure, *args, **kwargs):
        rendered_text.extend((text.get_text(), text.get_color()) for ax in figure.axes for text in ax.texts)
        return savefig(figure, *args, **kwargs)

    monkeypatch.setattr(Figure, "savefig", capture_labels)
    path = plot_congestion_comparison(
        "강남역", None, "서울역", "여유", 0, "-3°C",
        output_path=tmp_path / "incomplete.png", show=False, second_traffic="원활", first_data_source="api", second_data_source="api", average_temperature=-1.5,
    )

    assert path.exists()
    labels = dict(rendered_text)
    assert "정보 없음" in labels
    assert "0.0°C" in labels
    assert "-3.0°C" in labels
    assert "도로 교통상황" in labels
    assert "원활" in labels
    assert labels["여유"] == "#397455"
    assert all("/4" not in label for label in labels)


def test_numeric_zero_and_scientific_temperature():
    from congestion_chart import _population_label, parse_temperature
    assert _population_label(0) == '약 0명'
    assert parse_temperature(0.0) == 0.0
    assert parse_temperature(1e-7) == 1e-7
    assert parse_temperature(float('nan')) is None


def test_chart_uses_explicit_sources_and_supplied_average(monkeypatch, tmp_path):
    from matplotlib.figure import Figure
    from congestion_chart import plot_congestion_comparison
    seen = []
    def capture(fig, *args, **kwargs):
        seen.extend(t.get_text() for t in fig.texts)
        seen.extend(t.get_text() for ax in fig.axes for t in ax.texts)
    monkeypatch.setattr(Figure, 'savefig', capture)
    plot_congestion_comparison('A', '여유 (샘플)', 'B', '붐빔', 10, 20,
        first_data_source='api', second_data_source='api', average_temperature=12.5,
        output_path=tmp_path / 'chart.png', show=False)
    assert '실시간 API' in seen
    assert '12.5°C' in seen
    seen.clear()
    plot_congestion_comparison('A', '여유', 'B', '붐빔', 10, 20,
        first_data_source='api', second_data_source='sample', average_temperature=None,
        output_path=tmp_path / 'mixed.png', show=False)
    assert '실시간·시연 혼합' in seen
    assert '15.0°C' not in seen
