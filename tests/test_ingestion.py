import pandas as pd
import pytest

from analytics_framework import Pipeline
from analytics_framework.ingestion import (
    CSVLoaderStep,
    MultipleCSVLoaderStep,
    load_csv,
    load_multiple_csv,
)


def test_load_csv_returns_dataframe(tmp_path):
    csv_path = tmp_path / "sample.csv"

    expected_df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    expected_df.to_csv(csv_path, index=False)

    result = load_csv(csv_path)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)
    assert result["value"].sum() == 30


def test_load_csv_raises_file_not_found_error(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(missing_path)


def test_load_multiple_csv_returns_dictionary(tmp_path):
    first_path = tmp_path / "first.csv"
    second_path = tmp_path / "second.csv"

    pd.DataFrame({"id": [1]}).to_csv(first_path, index=False)
    pd.DataFrame({"id": [2]}).to_csv(second_path, index=False)

    result = load_multiple_csv(
        {
            "first": first_path,
            "second": second_path,
        }
    )

    assert set(result.keys()) == {"first", "second"}
    assert result["first"].iloc[0]["id"] == 1
    assert result["second"].iloc[0]["id"] == 2


def test_csv_loader_step_updates_pipeline_context(tmp_path):
    csv_path = tmp_path / "sales.csv"

    pd.DataFrame(
        {
            "order_id": [1, 2],
            "revenue": [100, 200],
        }
    ).to_csv(csv_path, index=False)

    pipeline = Pipeline("CSV Loader Test")

    pipeline.add_step(
        CSVLoaderStep(
            path=csv_path,
            output_key="sales",
        )
    )

    result = pipeline.run()

    assert "sales" in result
    assert result["sales"]["revenue"].sum() == 300


def test_multiple_csv_loader_step_updates_pipeline_context(tmp_path):
    customers_path = tmp_path / "customers.csv"
    orders_path = tmp_path / "orders.csv"

    pd.DataFrame({"customer_id": [1, 2]}).to_csv(customers_path, index=False)
    pd.DataFrame({"order_id": [10, 20]}).to_csv(orders_path, index=False)

    pipeline = Pipeline("Multiple CSV Loader Test")

    pipeline.add_step(
        MultipleCSVLoaderStep(
            files={
                "customers": customers_path,
                "orders": orders_path,
            },
            output_key="datasets",
        )
    )

    result = pipeline.run()

    assert "datasets" in result
    assert set(result["datasets"].keys()) == {"customers", "orders"}
    assert result["datasets"]["customers"].shape == (2, 1)
    assert result["datasets"]["orders"].shape == (2, 1)
