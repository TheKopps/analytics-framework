from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from analytics_framework.core.pipeline_step import PipelineStep


def _get_dataframe_from_context(
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


def _validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing_columns = [column for column in columns if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Columns not found: {missing_columns}")


def save_line_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    output_path: str | Path,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotate_x: bool = True,
) -> Path:
    _validate_columns(df, [x_column, y_column])

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 5))
    plt.plot(df[x_column], df[y_column], marker="o")

    plt.title(title or f"{y_column} by {x_column}")
    plt.xlabel(xlabel or x_column)
    plt.ylabel(ylabel or y_column)

    if rotate_x:
        plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


def save_bar_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    output_path: str | Path,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotate_x: bool = True,
) -> Path:
    _validate_columns(df, [x_column, y_column])

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 5))
    plt.bar(df[x_column], df[y_column])

    plt.title(title or f"{y_column} by {x_column}")
    plt.xlabel(xlabel or x_column)
    plt.ylabel(ylabel or y_column)

    if rotate_x:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


def save_histogram(
    df: pd.DataFrame,
    column: str,
    output_path: str | Path,
    bins: int = 30,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str = "Frequency",
) -> Path:
    _validate_columns(df, [column])

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.hist(df[column].dropna(), bins=bins)

    plt.title(title or f"Distribution of {column}")
    plt.xlabel(xlabel or column)
    plt.ylabel(ylabel)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


class LinePlotStep(PipelineStep):
    """
    Pipeline step used to generate a line plot.
    """

    def __init__(
        self,
        input_key: str,
        x_column: str,
        y_column: str,
        output_path: str | Path,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        name: str = "Generate Line Plot",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.x_column = x_column
        self.y_column = y_column
        self.output_path = Path(output_path)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        output_path = save_line_plot(
            df=df,
            x_column=self.x_column,
            y_column=self.y_column,
            output_path=self.output_path,
            title=self.title,
            xlabel=self.xlabel,
            ylabel=self.ylabel,
        )

        context.setdefault("figures", []).append(output_path)

        return context


class BarPlotStep(PipelineStep):
    """
    Pipeline step used to generate a bar plot.
    """

    def __init__(
        self,
        input_key: str,
        x_column: str,
        y_column: str,
        output_path: str | Path,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        name: str = "Generate Bar Plot",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.x_column = x_column
        self.y_column = y_column
        self.output_path = Path(output_path)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        output_path = save_bar_plot(
            df=df,
            x_column=self.x_column,
            y_column=self.y_column,
            output_path=self.output_path,
            title=self.title,
            xlabel=self.xlabel,
            ylabel=self.ylabel,
        )

        context.setdefault("figures", []).append(output_path)

        return context


class HistogramPlotStep(PipelineStep):
    """
    Pipeline step used to generate a histogram.
    """

    def __init__(
        self,
        input_key: str,
        column: str,
        output_path: str | Path,
        bins: int = 30,
        title: str | None = None,
        xlabel: str | None = None,
        name: str = "Generate Histogram",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.column = column
        self.output_path = Path(output_path)
        self.bins = bins
        self.title = title
        self.xlabel = xlabel

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        output_path = save_histogram(
            df=df,
            column=self.column,
            output_path=self.output_path,
            bins=self.bins,
            title=self.title,
            xlabel=self.xlabel,
        )

        context.setdefault("figures", []).append(output_path)

        return context
