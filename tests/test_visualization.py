import pandas as pd
import pytest

from analytics_framework import Pipeline, StepExecutionError
from analytics_framework.visualization import (
    BarPlotStep,
    HistogramPlotStep,
    LinePlotStep,
    save_bar_plot,
    save_histogram,
    save_line_plot,
)


def test_save_line_plot_creates_file(tmp_path):
    df = pd.DataFrame(
        {
            "month": ["2024-01", "2024-02"],
            "revenue": [100, 200],
        }
    )

    output_path = tmp_path / "line.png"

    result = save_line_plot(
        df=df,
        x_column="month",
        y_column="revenue",
        output_path=output_path,
    )

    assert result.exists()
    assert result.suffix == ".png"


def test_save_bar_plot_creates_file(tmp_path):
    df = pd.DataFrame(
        {
            "category": ["A", "B"],
            "revenue": [100, 200],
        }
    )

    output_path = tmp_path / "bar.png"

    result = save_bar_plot(
        df=df,
        x_column="category",
        y_column="revenue",
        output_path=output_path,
    )

    assert result.exists()
    assert result.suffix == ".png"


def test_save_histogram_creates_file(tmp_path):
    df = pd.DataFrame(
        {
            "revenue": [100, 120, 150, 200],
        }
    )

    output_path = tmp_path / "histogram.png"

    result = save_histogram(
        df=df,
        column="revenue",
        output_path=output_path,
    )

    assert result.exists()
    assert result.suffix == ".png"


def test_line_plot_step_updates_context(tmp_path):
    df = pd.DataFrame(
        {
            "month": ["2024-01", "2024-02"],
            "revenue": [100, 200],
        }
    )

    pipeline = Pipeline("Line Plot Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        LinePlotStep(
            input_key="sales",
            x_column="month",
            y_column="revenue",
            output_path=tmp_path / "line.png",
        )
    )

    result = pipeline.run()

    assert "figures" in result
    assert result["figures"][0].exists()


def test_bar_plot_step_updates_context(tmp_path):
    df = pd.DataFrame(
        {
            "category": ["A", "B"],
            "revenue": [100, 200],
        }
    )

    pipeline = Pipeline("Bar Plot Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        BarPlotStep(
            input_key="sales",
            x_column="category",
            y_column="revenue",
            output_path=tmp_path / "bar.png",
        )
    )

    result = pipeline.run()

    assert "figures" in result
    assert result["figures"][0].exists()


def test_histogram_plot_step_updates_context(tmp_path):
    df = pd.DataFrame(
        {
            "revenue": [100, 120, 150, 200],
        }
    )

    pipeline = Pipeline("Histogram Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        HistogramPlotStep(
            input_key="sales",
            column="revenue",
            output_path=tmp_path / "histogram.png",
        )
    )

    result = pipeline.run()

    assert "figures" in result
    assert result["figures"][0].exists()


def test_plot_step_raises_error_for_missing_column(tmp_path):
    df = pd.DataFrame(
        {
            "month": ["2024-01", "2024-02"],
        }
    )

    pipeline = Pipeline("Failing Plot Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        LinePlotStep(
            input_key="sales",
            x_column="month",
            y_column="revenue",
            output_path=tmp_path / "line.png",
        )
    )

    with pytest.raises(StepExecutionError):
        pipeline.run()
