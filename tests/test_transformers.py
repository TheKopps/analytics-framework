import pandas as pd
import pytest

from analytics_framework import Pipeline, StepExecutionError
from analytics_framework.features import (
    ConvertDateColumnsStep,
    DropDuplicatesStep,
    ExportDataFrameStep,
    FillMissingValuesStep,
    RenameColumnsStep,
    SelectColumnsStep,
)


def test_drop_duplicates_step_removes_duplicates():
    df = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "value": [10, 10, 20],
        }
    )

    pipeline = Pipeline("Drop Duplicates Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        DropDuplicatesStep(
            input_key="data",
            subset=["id"],
        )
    )

    result = pipeline.run()

    assert result["data"].shape == (2, 2)


def test_fill_missing_values_step_fills_nulls():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, None],
        }
    )

    pipeline = Pipeline("Fill Missing Values Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        FillMissingValuesStep(
            input_key="data",
            fill_values={
                "value": 0,
            },
        )
    )

    result = pipeline.run()

    assert result["data"]["value"].isna().sum() == 0
    assert result["data"]["value"].iloc[1] == 0


def test_convert_date_columns_step_converts_to_datetime():
    df = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
        }
    )

    pipeline = Pipeline("Convert Dates Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        ConvertDateColumnsStep(
            input_key="data",
            columns=["date"],
        )
    )

    result = pipeline.run()

    assert pd.api.types.is_datetime64_any_dtype(result["data"]["date"])


def test_rename_columns_step_renames_columns():
    df = pd.DataFrame(
        {
            "old_name": [1, 2],
        }
    )

    pipeline = Pipeline("Rename Columns Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        RenameColumnsStep(
            input_key="data",
            columns_mapping={
                "old_name": "new_name",
            },
        )
    )

    result = pipeline.run()

    assert "new_name" in result["data"].columns
    assert "old_name" not in result["data"].columns


def test_select_columns_step_keeps_selected_columns():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
            "extra": ["A", "B"],
        }
    )

    pipeline = Pipeline("Select Columns Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        SelectColumnsStep(
            input_key="data",
            columns=["id", "value"],
        )
    )

    result = pipeline.run()

    assert result["data"].columns.tolist() == ["id", "value"]


def test_missing_column_raises_step_execution_error():
    df = pd.DataFrame(
        {
            "id": [1, 2],
        }
    )

    pipeline = Pipeline("Missing Column Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        SelectColumnsStep(
            input_key="data",
            columns=["id", "missing_column"],
        )
    )

    with pytest.raises(StepExecutionError):
        pipeline.run()


def test_export_dataframe_step_creates_csv(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    output_path = tmp_path / "processed" / "data.csv"

    pipeline = Pipeline("Export DataFrame Test")
    pipeline.context["data"] = df

    pipeline.add_step(
        ExportDataFrameStep(
            input_key="data",
            path=output_path,
        )
    )

    pipeline.run()

    assert output_path.exists()

    exported_df = pd.read_csv(output_path)

    assert exported_df.shape == (2, 2)
