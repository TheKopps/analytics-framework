from dataclasses import dataclass
from typing import Any

import pandas as pd

from analytics_framework.core.pipeline_step import PipelineStep


@dataclass
class DataQualityResult:
    check_name: str
    status: str
    details: str
    value: Any | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_name": self.check_name,
            "status": self.status,
            "details": self.details,
            "value": self.value,
        }


class DataQualityValidator:
    """
    Generic data quality validator for pandas DataFrames.
    """

    def __init__(self):
        self.results: list[DataQualityResult] = []

    def add_result(
        self,
        check_name: str,
        status: str,
        details: str,
        value: Any | None = None,
    ) -> None:
        self.results.append(
            DataQualityResult(
                check_name=check_name,
                status=status,
                details=details,
                value=value,
            )
        )

    def check_required_columns(
        self,
        df: pd.DataFrame,
        required_columns: list[str],
    ) -> "DataQualityValidator":
        missing_columns = [
            column for column in required_columns if column not in df.columns
        ]

        if missing_columns:
            self.add_result(
                check_name="required_columns",
                status="FAIL",
                details="Missing required columns.",
                value=missing_columns,
            )
        else:
            self.add_result(
                check_name="required_columns",
                status="PASS",
                details="All required columns are present.",
                value=required_columns,
            )

        return self

    def check_duplicates(
        self,
        df: pd.DataFrame,
        subset: list[str] | None = None,
        max_duplicates: int = 0,
    ) -> "DataQualityValidator":
        duplicate_count = df.duplicated(subset=subset).sum()

        status = "PASS" if duplicate_count <= max_duplicates else "FAIL"

        self.add_result(
            check_name="duplicates",
            status=status,
            details="Duplicate row check completed.",
            value=int(duplicate_count),
        )

        return self

    def check_missing_values(
        self,
        df: pd.DataFrame,
        columns: list[str] | None = None,
        max_missing_ratio: float = 0.0,
    ) -> "DataQualityValidator":
        columns_to_check = columns or df.columns.tolist()

        missing_summary = {}

        for column in columns_to_check:
            if column not in df.columns:
                continue

            missing_ratio = df[column].isna().mean()
            missing_summary[column] = round(float(missing_ratio), 4)

        failing_columns = [
            column
            for column, missing_ratio in missing_summary.items()
            if missing_ratio > max_missing_ratio
        ]

        status = "PASS" if not failing_columns else "WARNING"

        self.add_result(
            check_name="missing_values",
            status=status,
            details="Missing values check completed.",
            value=missing_summary,
        )

        return self

    def check_non_negative_values(
        self,
        df: pd.DataFrame,
        columns: list[str],
    ) -> "DataQualityValidator":
        negative_summary = {}

        for column in columns:
            if column not in df.columns:
                continue

            negative_summary[column] = int((df[column] < 0).sum())

        failing_columns = [
            column for column, count in negative_summary.items() if count > 0
        ]

        status = "PASS" if not failing_columns else "FAIL"

        self.add_result(
            check_name="non_negative_values",
            status=status,
            details="Non-negative values check completed.",
            value=negative_summary,
        )

        return self

    def check_allowed_values(
        self,
        df: pd.DataFrame,
        column: str,
        allowed_values: list[Any],
    ) -> "DataQualityValidator":
        if column not in df.columns:
            self.add_result(
                check_name=f"allowed_values_{column}",
                status="FAIL",
                details=f"Column '{column}' does not exist.",
                value=None,
            )
            return self

        invalid_values = sorted(set(df[column].dropna().unique()) - set(allowed_values))

        status = "PASS" if not invalid_values else "FAIL"

        self.add_result(
            check_name=f"allowed_values_{column}",
            status=status,
            details="Allowed values check completed.",
            value=invalid_values,
        )

        return self

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([result.to_dict() for result in self.results])


class DataQualityValidatorStep(PipelineStep):
    """
    Pipeline step for generic DataFrame quality validation.
    """

    def __init__(
        self,
        input_key: str,
        output_key: str = "data_quality_report",
        required_columns: list[str] | None = None,
        non_negative_columns: list[str] | None = None,
        missing_value_columns: list[str] | None = None,
        max_missing_ratio: float = 0.0,
        allowed_values: dict[str, list[Any]] | None = None,
        check_duplicates: bool = True,
        duplicate_subset: list[str] | None = None,
        fail_on_error: bool = True,
        name: str = "Validate Data Quality",
    ):
        super().__init__(name)
        self.input_key = input_key
        self.output_key = output_key
        self.required_columns = required_columns or []
        self.non_negative_columns = non_negative_columns or []
        self.missing_value_columns = missing_value_columns
        self.max_missing_ratio = max_missing_ratio
        self.allowed_values = allowed_values or {}
        self.check_duplicates_enabled = check_duplicates
        self.duplicate_subset = duplicate_subset
        self.fail_on_error = fail_on_error

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        if self.input_key not in context:
            raise KeyError(f"Input key not found in context: {self.input_key}")

        df = context[self.input_key]

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Expected pandas DataFrame for key '{self.input_key}', "
                f"got {type(df).__name__}."
            )

        validator = DataQualityValidator()

        if self.required_columns:
            validator.check_required_columns(df, self.required_columns)

        if self.check_duplicates_enabled:
            validator.check_duplicates(df, subset=self.duplicate_subset)

        validator.check_missing_values(
            df,
            columns=self.missing_value_columns,
            max_missing_ratio=self.max_missing_ratio,
        )

        if self.non_negative_columns:
            validator.check_non_negative_values(
                df,
                self.non_negative_columns,
            )

        for column, values in self.allowed_values.items():
            validator.check_allowed_values(df, column, values)

        report = validator.to_dataframe()
        context[self.output_key] = report

        has_failures = (report["status"] == "FAIL").any()

        if has_failures and self.fail_on_error:
            failed_checks = report.loc[
                report["status"] == "FAIL",
                "check_name",
            ].tolist()

            raise ValueError(
                f"Data quality validation failed for checks: {failed_checks}"
            )

        return context
