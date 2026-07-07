from typing import Any

import pandas as pd

from analytics_framework.core.pipeline_step import PipelineStep

SUPPORTED_OPERATIONS = {
    "sum",
    "mean",
    "median",
    "min",
    "max",
    "count",
    "nunique",
}


def _validate_dataframe(
    context: dict[str, Any],
    input_key: str,
) -> pd.DataFrame:
    if input_key not in context:
        raise KeyError(f"Input key not found in context: {input_key}")

    df = context[input_key]

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"Expected pandas DataFrame for key '{input_key}', got {type(df).__name__}."
        )

    return df.copy()


def _apply_operation(
    series: pd.Series,
    operation: str,
) -> Any:
    if operation not in SUPPORTED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation '{operation}'. "
            f"Supported operations are: {sorted(SUPPORTED_OPERATIONS)}"
        )

    if operation == "sum":
        return series.sum()

    if operation == "mean":
        return series.mean()

    if operation == "median":
        return series.median()

    if operation == "min":
        return series.min()

    if operation == "max":
        return series.max()

    if operation == "count":
        return series.count()

    if operation == "nunique":
        return series.nunique()

    raise ValueError(f"Unsupported operation: {operation}")


def compute_basic_metrics(
    df: pd.DataFrame,
    metrics: dict[str, dict[str, str]],
) -> pd.DataFrame:
    """
    Compute simple metrics from a DataFrame.

    Example:
    {
        "total_revenue": {"column": "revenue", "operation": "sum"},
        "average_revenue": {"column": "revenue", "operation": "mean"},
    }
    """
    results = []

    for metric_name, metric_config in metrics.items():
        column = metric_config["column"]
        operation = metric_config["operation"]

        if column not in df.columns:
            raise KeyError(f"Column not found: {column}")

        value = _apply_operation(df[column], operation)

        results.append(
            {
                "metric": metric_name,
                "column": column,
                "operation": operation,
                "value": value,
            }
        )

    return pd.DataFrame(results)


def compute_groupby_metrics(
    df: pd.DataFrame,
    groupby_columns: list[str],
    aggregations: dict[str, str],
) -> pd.DataFrame:
    """
    Compute grouped metrics.

    Example:
    groupby_columns = ["category"]
    aggregations = {"revenue": "sum", "order_id": "nunique"}
    """
    missing_groupby_columns = [
        column for column in groupby_columns if column not in df.columns
    ]

    if missing_groupby_columns:
        raise KeyError(f"Columns not found: {missing_groupby_columns}")

    missing_aggregation_columns = [
        column for column in aggregations if column not in df.columns
    ]

    if missing_aggregation_columns:
        raise KeyError(f"Columns not found: {missing_aggregation_columns}")

    for operation in aggregations.values():
        if operation not in SUPPORTED_OPERATIONS:
            raise ValueError(
                f"Unsupported operation '{operation}'. "
                f"Supported operations are: {sorted(SUPPORTED_OPERATIONS)}"
            )

    return df.groupby(groupby_columns).agg(aggregations).reset_index()


def compute_time_series_metrics(
    df: pd.DataFrame,
    date_column: str,
    value_column: str,
    frequency: str = "M",
    operation: str = "sum",
) -> pd.DataFrame:
    """
    Compute a time series metric.

    Example:
    monthly revenue = sum revenue grouped by month.
    """
    if date_column not in df.columns:
        raise KeyError(f"Column not found: {date_column}")

    if value_column not in df.columns:
        raise KeyError(f"Column not found: {value_column}")

    if operation not in SUPPORTED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation '{operation}'. "
            f"Supported operations are: {sorted(SUPPORTED_OPERATIONS)}"
        )

    working_df = df.copy()
    working_df[date_column] = pd.to_datetime(
        working_df[date_column],
        errors="coerce",
    )

    working_df = working_df.dropna(subset=[date_column])

    result = (
        working_df.groupby(pd.Grouper(key=date_column, freq=frequency))[value_column]
        .agg(operation)
        .reset_index()
        .rename(columns={value_column: f"{operation}_{value_column}"})
    )

    return result


class BasicMetricsStep(PipelineStep):
    """
    Pipeline step used to compute basic metrics.
    """

    def __init__(
        self,
        input_key: str,
        metrics: dict[str, dict[str, str]],
        output_key: str = "basic_metrics",
        name: str = "Compute Basic Metrics",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key
        self.metrics = metrics

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _validate_dataframe(context, self.input_key)

        context[self.output_key] = compute_basic_metrics(
            df,
            self.metrics,
        )

        return context


class GroupByMetricsStep(PipelineStep):
    """
    Pipeline step used to compute grouped metrics.
    """

    def __init__(
        self,
        input_key: str,
        groupby_columns: list[str],
        aggregations: dict[str, str],
        output_key: str = "groupby_metrics",
        name: str = "Compute GroupBy Metrics",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key
        self.groupby_columns = groupby_columns
        self.aggregations = aggregations

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _validate_dataframe(context, self.input_key)

        context[self.output_key] = compute_groupby_metrics(
            df,
            self.groupby_columns,
            self.aggregations,
        )

        return context


class TimeSeriesMetricsStep(PipelineStep):
    """
    Pipeline step used to compute time series metrics.
    """

    def __init__(
        self,
        input_key: str,
        date_column: str,
        value_column: str,
        frequency: str = "M",
        operation: str = "sum",
        output_key: str = "time_series_metrics",
        name: str = "Compute Time Series Metrics",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key
        self.date_column = date_column
        self.value_column = value_column
        self.frequency = frequency
        self.operation = operation

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _validate_dataframe(context, self.input_key)

        context[self.output_key] = compute_time_series_metrics(
            df=df,
            date_column=self.date_column,
            value_column=self.value_column,
            frequency=self.frequency,
            operation=self.operation,
        )

        return context
