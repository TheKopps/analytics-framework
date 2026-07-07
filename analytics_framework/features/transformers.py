from pathlib import Path
from typing import Any

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


class DropDuplicatesStep(PipelineStep):
    """
    Pipeline step used to remove duplicate rows from a DataFrame.
    """

    def __init__(
        self,
        input_key: str,
        output_key: str | None = None,
        subset: list[str] | None = None,
        name: str = "Drop Duplicates",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key or input_key
        self.subset = subset

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        context[self.output_key] = df.drop_duplicates(subset=self.subset)

        return context


class FillMissingValuesStep(PipelineStep):
    """
    Pipeline step used to fill missing values in selected columns.
    """

    def __init__(
        self,
        input_key: str,
        fill_values: dict[str, Any],
        output_key: str | None = None,
        name: str = "Fill Missing Values",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key or input_key
        self.fill_values = fill_values

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        missing_columns = [
            column for column in self.fill_values if column not in df.columns
        ]

        if missing_columns:
            raise KeyError(f"Columns not found: {missing_columns}")

        context[self.output_key] = df.fillna(self.fill_values)

        return context


class ConvertDateColumnsStep(PipelineStep):
    """
    Pipeline step used to convert selected columns to datetime.
    """

    def __init__(
        self,
        input_key: str,
        columns: list[str],
        output_key: str | None = None,
        errors: str = "coerce",
        name: str = "Convert Date Columns",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key or input_key
        self.columns = columns
        self.errors = errors

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        missing_columns = [
            column for column in self.columns if column not in df.columns
        ]

        if missing_columns:
            raise KeyError(f"Columns not found: {missing_columns}")

        for column in self.columns:
            df[column] = pd.to_datetime(df[column], errors=self.errors)

        context[self.output_key] = df

        return context


class RenameColumnsStep(PipelineStep):
    """
    Pipeline step used to rename DataFrame columns.
    """

    def __init__(
        self,
        input_key: str,
        columns_mapping: dict[str, str],
        output_key: str | None = None,
        name: str = "Rename Columns",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key or input_key
        self.columns_mapping = columns_mapping

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        context[self.output_key] = df.rename(columns=self.columns_mapping)

        return context


class SelectColumnsStep(PipelineStep):
    """
    Pipeline step used to keep only selected columns.
    """

    def __init__(
        self,
        input_key: str,
        columns: list[str],
        output_key: str | None = None,
        name: str = "Select Columns",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key or input_key
        self.columns = columns

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        missing_columns = [
            column for column in self.columns if column not in df.columns
        ]

        if missing_columns:
            raise KeyError(f"Columns not found: {missing_columns}")

        context[self.output_key] = df[self.columns].copy()

        return context


class ExportDataFrameStep(PipelineStep):
    """
    Pipeline step used to export a DataFrame to CSV.
    """

    def __init__(
        self,
        input_key: str,
        path: str | Path,
        name: str = "Export DataFrame",
        **to_csv_kwargs: Any,
    ):
        super().__init__(name)
        self.input_key = input_key
        self.path = Path(path)
        self.to_csv_kwargs = to_csv_kwargs

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        self.path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.path, index=False, **self.to_csv_kwargs)

        return context
