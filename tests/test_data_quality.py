import pandas as pd
import pytest

from analytics_framework import Pipeline, StepExecutionError
from analytics_framework.quality import DataQualityValidator, DataQualityValidatorStep


def test_required_columns_check_passes():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    validator = DataQualityValidator()
    validator.check_required_columns(df, ["id", "value"])

    report = validator.to_dataframe()

    assert report.iloc[0]["status"] == "PASS"


def test_required_columns_check_fails():
    df = pd.DataFrame(
        {
            "id": [1, 2],
        }
    )

    validator = DataQualityValidator()
    validator.check_required_columns(df, ["id", "value"])

    report = validator.to_dataframe()

    assert report.iloc[0]["status"] == "FAIL"
    assert report.iloc[0]["value"] == ["value"]


def test_duplicate_check_fails_when_duplicates_exist():
    df = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "value": [10, 10, 20],
        }
    )

    validator = DataQualityValidator()
    validator.check_duplicates(df, subset=["id"])

    report = validator.to_dataframe()

    assert report.iloc[0]["status"] == "FAIL"
    assert report.iloc[0]["value"] == 1


def test_non_negative_check_fails_with_negative_values():
    df = pd.DataFrame(
        {
            "revenue": [100, -20, 50],
        }
    )

    validator = DataQualityValidator()
    validator.check_non_negative_values(df, ["revenue"])

    report = validator.to_dataframe()

    assert report.iloc[0]["status"] == "FAIL"
    assert report.iloc[0]["value"] == {"revenue": 1}


def test_data_quality_step_updates_context():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "revenue": [100, 200],
            "status": ["delivered", "cancelled"],
        }
    )

    pipeline = Pipeline("Data Quality Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        DataQualityValidatorStep(
            input_key="sales",
            required_columns=["id", "revenue", "status"],
            non_negative_columns=["revenue"],
            allowed_values={
                "status": ["delivered", "cancelled"],
            },
            fail_on_error=True,
        )
    )

    result = pipeline.run()

    assert "data_quality_report" in result
    assert set(result["data_quality_report"]["status"]) == {"PASS"}


def test_data_quality_step_raises_error_when_validation_fails():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "revenue": [100, -200],
        }
    )

    pipeline = Pipeline("Failing Data Quality Test")
    pipeline.context["sales"] = df

    pipeline.add_step(
        DataQualityValidatorStep(
            input_key="sales",
            required_columns=["id", "revenue"],
            non_negative_columns=["revenue"],
            fail_on_error=True,
        )
    )

    with pytest.raises(StepExecutionError):
        pipeline.run()
