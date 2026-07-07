import pandas as pd
import pytest

from analytics_framework import Pipeline, StepExecutionError
from analytics_framework.export import (
    CSVExportStep,
    ExcelExportStep,
    MultiSheetExcelExportStep,
    export_dataframe_to_csv,
    export_dataframe_to_excel,
    export_multiple_dataframes_to_excel,
)


def test_export_dataframe_to_csv_creates_file(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    output_path = tmp_path / "exports" / "data.csv"

    result = export_dataframe_to_csv(df, output_path)

    assert result.exists()

    exported_df = pd.read_csv(result)

    assert exported_df.shape == (2, 2)
    assert exported_df["value"].sum() == 30


def test_export_dataframe_to_excel_creates_file(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    output_path = tmp_path / "exports" / "data.xlsx"

    result = export_dataframe_to_excel(
        df=df,
        output_path=output_path,
        sheet_name="Data",
    )

    assert result.exists()

    exported_df = pd.read_excel(result, sheet_name="Data")

    assert exported_df.shape == (2, 2)
    assert exported_df["value"].sum() == 30


def test_export_multiple_dataframes_to_excel_creates_workbook(tmp_path):
    first_df = pd.DataFrame({"id": [1], "value": [10]})
    second_df = pd.DataFrame({"id": [2], "value": [20]})

    output_path = tmp_path / "exports" / "workbook.xlsx"

    result = export_multiple_dataframes_to_excel(
        dataframes={
            "First": first_df,
            "Second": second_df,
        },
        output_path=output_path,
    )

    assert result.exists()

    first_exported = pd.read_excel(result, sheet_name="First")
    second_exported = pd.read_excel(result, sheet_name="Second")

    assert first_exported["value"].iloc[0] == 10
    assert second_exported["value"].iloc[0] == 20


def test_csv_export_step_updates_context(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    output_path = tmp_path / "data.csv"

    pipeline = Pipeline("CSV Export Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        CSVExportStep(
            input_key="data",
            output_path=output_path,
        )
    )

    result = pipeline.run()

    assert result["csv_export_path"].exists()


def test_excel_export_step_updates_context(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    output_path = tmp_path / "data.xlsx"

    pipeline = Pipeline("Excel Export Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        ExcelExportStep(
            input_key="data",
            output_path=output_path,
            sheet_name="Data",
        )
    )

    result = pipeline.run()

    assert result["excel_export_path"].exists()


def test_multi_sheet_excel_export_step_updates_context(tmp_path):
    first_df = pd.DataFrame({"id": [1], "value": [10]})
    second_df = pd.DataFrame({"id": [2], "value": [20]})

    output_path = tmp_path / "workbook.xlsx"

    pipeline = Pipeline("Multi Sheet Excel Export Test")
    pipeline.context["first"] = first_df
    pipeline.context["second"] = second_df

    pipeline.add_step(
        MultiSheetExcelExportStep(
            input_keys={
                "First": "first",
                "Second": "second",
            },
            output_path=output_path,
        )
    )

    result = pipeline.run()

    assert result["multi_sheet_excel_export_path"].exists()


def test_export_step_raises_error_for_missing_context_key(tmp_path):
    pipeline = Pipeline("Failing Export Test")

    pipeline.add_step(
        CSVExportStep(
            input_key="missing_key",
            output_path=tmp_path / "data.csv",
        )
    )

    with pytest.raises(StepExecutionError):
        pipeline.run()
