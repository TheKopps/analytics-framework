import pandas as pd
import pytest

from analytics_framework import Pipeline, StepExecutionError
from analytics_framework.analytics import (
    BasicMetricsStep,
    GroupByMetricsStep,
    TimeSeriesMetricsStep,
    compute_basic_metrics,
    compute_groupby_metrics,
    compute_time_series_metrics,
)


def test_compute_basic_metrics_returns_expected_values():
    df = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "revenue": [100, 200, 300],
        }
    )

    result = compute_basic_metrics(
        df,
        {
            "total_revenue": {
                "column": "revenue",
                "operation": "sum",
            },
            "total_orders": {
                "column": "order_id",
                "operation": "nunique",
            },
        },
    )

    assert result.loc[result["metric"] == "total_revenue", "value"].iloc[0] == 600
    assert result.loc[result["metric"] == "total_orders", "value"].iloc[0] == 3


def test_compute_basic_metrics_raises_error_for_missing_column():
    df = pd.DataFrame(
        {
            "revenue": [100, 200],
        }
    )

    with pytest.raises(KeyError):
        compute_basic_metrics(
            df,
            {
                "total_orders": {
                    "column": "order_id",
                    "operation": "nunique",
                },
            },
        )


def test_compute_groupby_metrics_returns_expected_values():
    df = pd.DataFrame(
        {
            "category": ["A", "A", "B"],
            "revenue": [100, 200, 300],
            "order_id": [1, 2, 3],
        }
    )

    result = compute_groupby_metrics(
        df,
        groupby_columns=["category"],
        aggregations={
            "revenue": "sum",
            "order_id": "nunique",
        },
    )

    category_a_revenue = result.loc[result["category"] == "A", "revenue"].iloc[0]

    assert category_a_revenue == 300


def test_compute_time_series_metrics_returns_monthly_values():
    df = pd.DataFrame(
        {
            "order_date": [
                "2024-01-01",
                "2024-01-15",
                "2024-02-01",
            ],
            "revenue": [100, 200, 300],
        }
    )

    result = compute_time_series_metrics(
        df,
        date_column="order_date",
        value_column="revenue",
        frequency="M",
        operation="sum",
    )

    assert result.shape[0] == 2
    assert result["sum_revenue"].sum() == 600


def test_basic_metrics_step_updates_context():
    df = pd.DataFrame(
        {
            "order_id": [1, 2],
            "revenue": [100, 200],
        }
    )

    pipeline = Pipeline("Basic Metrics Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        BasicMetricsStep(
            input_key="sales",
            metrics={
                "total_revenue": {
                    "column": "revenue",
                    "operation": "sum",
                },
            },
        )
    )

    result = pipeline.run()

    assert "basic_metrics" in result
    assert result["basic_metrics"]["value"].iloc[0] == 300


def test_groupby_metrics_step_updates_context():
    df = pd.DataFrame(
        {
            "category": ["A", "A", "B"],
            "revenue": [100, 200, 300],
        }
    )

    pipeline = Pipeline("GroupBy Metrics Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        GroupByMetricsStep(
            input_key="sales",
            groupby_columns=["category"],
            aggregations={
                "revenue": "sum",
            },
        )
    )

    result = pipeline.run()

    assert "groupby_metrics" in result
    assert result["groupby_metrics"]["revenue"].sum() == 600


def test_time_series_metrics_step_updates_context():
    df = pd.DataFrame(
        {
            "order_date": [
                "2024-01-01",
                "2024-01-15",
            ],
            "revenue": [100, 200],
        }
    )

    pipeline = Pipeline("Time Series Metrics Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        TimeSeriesMetricsStep(
            input_key="sales",
            date_column="order_date",
            value_column="revenue",
            frequency="M",
            operation="sum",
        )
    )

    result = pipeline.run()

    assert "time_series_metrics" in result
    assert result["time_series_metrics"]["sum_revenue"].iloc[0] == 300


def test_metrics_step_raises_step_execution_error_for_missing_column():
    df = pd.DataFrame(
        {
            "revenue": [100, 200],
        }
    )

    pipeline = Pipeline("Failing Metrics Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        BasicMetricsStep(
            input_key="sales",
            metrics={
                "total_orders": {
                    "column": "order_id",
                    "operation": "nunique",
                },
            },
        )
    )

    with pytest.raises(StepExecutionError):
        pipeline.run()
