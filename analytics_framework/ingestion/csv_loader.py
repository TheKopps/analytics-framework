from pathlib import Path
from typing import Any

import pandas as pd

from analytics_framework.core.pipeline_step import PipelineStep


def load_csv(path: str | Path, **read_csv_kwargs: Any) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    return pd.read_csv(path, **read_csv_kwargs)


def load_multiple_csv(
    files: dict[str, str | Path],
    **read_csv_kwargs: Any,
) -> dict[str, pd.DataFrame]:
    """
    Load multiple CSV files into a dictionary of DataFrames.
    """
    return {name: load_csv(path, **read_csv_kwargs) for name, path in files.items()}


class CSVLoaderStep(PipelineStep):
    """
    Pipeline step used to load a single CSV file.
    """

    def __init__(
        self,
        path: str | Path,
        output_key: str = "data",
        name: str | None = None,
        **read_csv_kwargs: Any,
    ):
        super().__init__(name or f"Load CSV: {Path(path).name}")
        self.path = Path(path)
        self.output_key = output_key
        self.read_csv_kwargs = read_csv_kwargs

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        context[self.output_key] = load_csv(
            self.path,
            **self.read_csv_kwargs,
        )
        return context


class MultipleCSVLoaderStep(PipelineStep):
    """
    Pipeline step used to load multiple CSV files.
    """

    def __init__(
        self,
        files: dict[str, str | Path],
        output_key: str = "datasets",
        name: str = "Load Multiple CSV Files",
        **read_csv_kwargs: Any,
    ):
        super().__init__(name)
        self.files = files
        self.output_key = output_key
        self.read_csv_kwargs = read_csv_kwargs

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        context[self.output_key] = load_multiple_csv(
            self.files,
            **self.read_csv_kwargs,
        )
        return context
