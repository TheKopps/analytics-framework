import pandas as pd
import pytest

from analytics_framework import Pipeline, StepExecutionError
from analytics_framework.reporting import (
    MarkdownReportStep,
    dataframe_to_markdown_table,
    render_context_value,
    render_markdown_report,
    write_markdown_report,
)


def test_dataframe_to_markdown_table_renders_table():
    df = pd.DataFrame(
        {
            "metric": ["revenue"],
            "value": [100],
        }
    )

    result = dataframe_to_markdown_table(df)

    assert "| metric | value |" in result
    assert "| revenue | 100 |" in result


def test_render_context_value_with_dataframe():
    df = pd.DataFrame(
        {
            "metric": ["orders"],
            "value": [10],
        }
    )

    result = render_context_value(df)

    assert "| metric | value |" in result


def test_render_context_value_with_list():
    result = render_context_value(["First insight", "Second insight"])

    assert "- First insight" in result
    assert "- Second insight" in result


def test_render_markdown_report_contains_sections():
    result = render_markdown_report(
        title="Demo Report",
        sections=[
            {
                "title": "Summary",
                "content": "This is a summary.",
            }
        ],
    )

    assert "# Demo Report" in result
    assert "## Summary" in result
    assert "This is a summary." in result


def test_write_markdown_report_creates_file(tmp_path):
    output_path = tmp_path / "report.md"

    result = write_markdown_report(
        content="# Test Report",
        output_path=output_path,
    )

    assert result.exists()
    assert result.read_text(encoding="utf-8") == "# Test Report"


def test_markdown_report_step_creates_report(tmp_path):
    metrics = pd.DataFrame(
        {
            "metric": ["total_revenue"],
            "value": [1000],
        }
    )

    output_path = tmp_path / "reports" / "report.md"

    pipeline = Pipeline("Markdown Report Test")
    pipeline.context["metrics"] = metrics

    pipeline.add_step(
        MarkdownReportStep(
            title="Test Report",
            output_path=output_path,
            context_keys=["metrics"],
        )
    )

    result = pipeline.run()

    assert "markdown_report_path" in result
    assert result["markdown_report_path"].exists()

    content = result["markdown_report_path"].read_text(encoding="utf-8")

    assert "# Test Report" in content
    assert "Total Revenue" in content or "total_revenue" in content


def test_markdown_report_step_raises_error_for_missing_context_key(tmp_path):
    pipeline = Pipeline("Failing Markdown Report Test")

    pipeline.add_step(
        MarkdownReportStep(
            title="Failing Report",
            output_path=tmp_path / "report.md",
            context_keys=["missing_key"],
        )
    )

    with pytest.raises(StepExecutionError):
        pipeline.run()
