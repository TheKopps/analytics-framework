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

    value = context[input_key]

    if not isinstance(value, pd.DataFrame):
        raise TypeError(
            f"Expected pandas DataFrame for key '{input_key}', "
            f"got {type(value).__name__}."
        )

    return value.copy()


def export_dataframe_to_csv(
    df: pd.DataFrame,
    output_path: str | Path,
    index: bool = False,
    **to_csv_kwargs: Any,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=index, **to_csv_kwargs)

    return output_path


def export_dataframe_to_excel(
    df: pd.DataFrame,
    output_path: str | Path,
    sheet_name: str = "Sheet1",
    index: bool = False,
    **to_excel_kwargs: Any,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(
        output_path,
        sheet_name=sheet_name,
        index=index,
        **to_excel_kwargs,
    )

    return output_path


def export_multiple_dataframes_to_excel(
    dataframes: dict[str, pd.DataFrame],
    output_path: str | Path,
    index: bool = False,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in dataframes.items():
            if not isinstance(df, pd.DataFrame):
                raise TypeError(
                    f"Expected pandas DataFrame for sheet '{sheet_name}', "
                    f"got {type(df).__name__}."
                )

            safe_sheet_name = sheet_name[:31]

            df.to_excel(
                writer,
                sheet_name=safe_sheet_name,
                index=index,
            )

    return output_path


class CSVExportStep(PipelineStep):
    """
    Pipeline step used to export a DataFrame to CSV.
    """

    def __init__(
        self,
        input_key: str,
        output_path: str | Path,
        output_key: str = "csv_export_path",
        index: bool = False,
        name: str = "Export DataFrame to CSV",
        **to_csv_kwargs: Any,
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_path = Path(output_path)
        self.output_key = output_key
        self.index = index
        self.to_csv_kwargs = to_csv_kwargs

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        output_path = export_dataframe_to_csv(
            df=df,
            output_path=self.output_path,
            index=self.index,
            **self.to_csv_kwargs,
        )

        context[self.output_key] = output_path

        return context


class ExcelExportStep(PipelineStep):
    """
    Pipeline step used to export a DataFrame to Excel.
    """

    def __init__(
        self,
        input_key: str,
        output_path: str | Path,
        sheet_name: str = "Sheet1",
        output_key: str = "excel_export_path",
        index: bool = False,
        name: str = "Export DataFrame to Excel",
        **to_excel_kwargs: Any,
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_path = Path(output_path)
        self.sheet_name = sheet_name
        self.output_key = output_key
        self.index = index
        self.to_excel_kwargs = to_excel_kwargs

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        df = _get_dataframe_from_context(context, self.input_key)

        output_path = export_dataframe_to_excel(
            df=df,
            output_path=self.output_path,
            sheet_name=self.sheet_name,
            index=self.index,
            **self.to_excel_kwargs,
        )

        context[self.output_key] = output_path

        return context


class MultiSheetExcelExportStep(PipelineStep):
    """
    Pipeline step used to export multiple DataFrames to one Excel workbook.
    """

    def __init__(
        self,
        input_keys: dict[str, str],
        output_path: str | Path,
        output_key: str = "multi_sheet_excel_export_path",
        index: bool = False,
        name: str = "Export Multiple DataFrames to Excel",
    ):
        super().__init__(name)
        self.input_keys = input_keys
        self.output_path = Path(output_path)
        self.output_key = output_key
        self.index = index

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        dataframes = {}

        for sheet_name, context_key in self.input_keys.items():
            dataframes[sheet_name] = _get_dataframe_from_context(
                context,
                context_key,
            )

        output_path = export_multiple_dataframes_to_excel(
            dataframes=dataframes,
            output_path=self.output_path,
            index=self.index,
        )

        context[self.output_key] = output_path

        return context
