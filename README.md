# Analytics Framework

Reusable Python analytics framework for building end-to-end Data Analytics, Business Intelligence and Data Science projects.

This framework provides reusable pipeline components for data ingestion, data quality validation, transformations, metrics computation, visualization, reporting and exports.

It is designed to be used across multiple portfolio and business analytics projects.

---

## Overview

`analytics-framework` is a modular Python package created to standardize the structure of analytics projects.

Instead of rewriting the same logic in every project, this framework provides reusable building blocks such as:

- pipeline orchestration
- pipeline steps
- shared execution context
- configuration management
- logging
- error handling
- data ingestion
- data quality validation
- dataframe transformations
- metrics computation
- visualization
- Markdown reporting
- CSV and Excel exports

The goal is to make analytics projects cleaner, more reusable and closer to professional software engineering practices.

---

## Key Features

### Core

- Modular `Pipeline` engine
- Abstract `PipelineStep` class
- Shared context between pipeline steps
- YAML configuration support
- Centralized logging
- Custom exceptions
- Step-level error handling
- Optional stop-on-error behavior

### Data Processing

- CSV loading utilities
- Multiple CSV ingestion step
- Data quality validation checks
- Duplicate detection
- Required column checks
- Missing value checks
- Non-negative value checks
- Allowed values checks
- Reusable dataframe transformation steps

### Analytics

- Basic metrics computation
- Group-by metrics computation
- Time-series metrics computation
- Reusable analytics steps

### Visualization

- Line plot generation
- Bar plot generation
- Histogram generation
- Automated figure export

### Reporting and Export

- Markdown report generation
- DataFrame to Markdown table conversion
- CSV export
- Excel export
- Multi-sheet Excel export

### Development

- Unit tests with `pytest`
- Code quality with `ruff`
- GitHub Actions CI
- Editable package installation
- Professional Git workflow

---

## Project Structure

```text
analytics-framework/
│
├── analytics_framework/
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logger.py
│   │   ├── pipeline.py
│   │   └── pipeline_step.py
│   │
│   ├── ingestion/
│   │   └── csv_loader.py
│   │
│   ├── quality/
│   │   └── validators.py
│   │
│   ├── features/
│   │   └── transformers.py
│   │
│   ├── analytics/
│   │   └── metrics.py
│   │
│   ├── visualization/
│   │   └── plots.py
│   │
│   ├── reporting/
│   │   └── markdown.py
│   │
│   ├── export/
│   │   └── dataframe_export.py
│   │
│   ├── ml/
│   │
│   ├── utils/
│   │
│   └── __init__.py
│
├── examples/
│   ├── config_example.yaml
│   ├── demo_config.py
│   ├── demo_data_quality.py
│   ├── demo_error_handling.py
│   ├── demo_export.py
│   ├── demo_ingestion.py
│   ├── demo_logger.py
│   ├── demo_metrics.py
│   ├── demo_pipeline.py
│   ├── demo_reporting.py
│   ├── demo_transformations.py
│   └── demo_visualization.py
│
├── tests/
│   ├── test_config.py
│   ├── test_data_quality.py
│   ├── test_error_handling.py
│   ├── test_export.py
│   ├── test_ingestion.py
│   ├── test_metrics.py
│   ├── test_pipeline.py
│   ├── test_reporting.py
│   ├── test_transformers.py
│   └── test_visualization.py
│
├── docs/
│   ├── architecture.md
│   └── code_quality.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/TheKopps/analytics-framework.git
cd analytics-framework
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

For development, install optional development dependencies:

```bash
python -m pip install -e ".[dev]"
```

---

## Quick Start

```python
from analytics_framework import Pipeline, PipelineStep


class LoadDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Load Data")

    def execute(self, context):
        context["data"] = [1, 2, 3, 4, 5]
        return context


class SumDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Sum Data")

    def execute(self, context):
        context["total"] = sum(context["data"])
        return context


pipeline = Pipeline("Demo Analytics Pipeline")

pipeline.add_step(LoadDataStep())
pipeline.add_step(SumDataStep())

result = pipeline.run()

print(result)
```

Expected output:

```text
{
    "data": [1, 2, 3, 4, 5],
    "total": 15
}
```

---

## Pipeline Concept

The framework is based on three core concepts:

### 1. Pipeline

The `Pipeline` controls the execution of all steps.

It stores a shared `context` dictionary and passes it from one step to the next.

```python
pipeline = Pipeline("My Analytics Pipeline")
```

### 2. PipelineStep

Each operation is represented by a `PipelineStep`.

Every step must implement an `execute()` method.

```python
class MyStep(PipelineStep):
    def __init__(self):
        super().__init__("My Step")

    def execute(self, context):
        context["result"] = "done"
        return context
```

### 3. Context

The context is a shared dictionary used to pass data between steps.

```python
context = {
    "raw_data": raw_data,
    "clean_data": clean_data,
    "metrics": metrics,
}
```

---

## Configuration

The framework includes a YAML configuration engine.

Example `config_example.yaml`:

```yaml
project:
  name: Supply Chain Analytics
  version: 0.1.0

paths:
  raw_data: data/raw
  processed_data: data/processed
  reports: reports

pipeline:
  enable_logging: true
  stop_on_error: true
```

Usage:

```python
from analytics_framework import Config

config = Config.from_yaml("examples/config_example.yaml")

project_name = config.get("project.name")
reports_path = config.resolve_path("paths.reports")
```

---

## Logging

The framework provides a reusable logger.

```python
from analytics_framework import setup_logger

logger = setup_logger(
    name="my_pipeline",
    log_file="reports/pipeline.log",
)
```

The logger can be injected into a pipeline:

```python
from analytics_framework import Pipeline

pipeline = Pipeline(
    project_name="My Pipeline",
    logger=logger,
)
```

---

## Error Handling

The framework includes custom exceptions:

- `AnalyticsFrameworkError`
- `PipelineError`
- `StepExecutionError`

Example:

```python
from analytics_framework import Pipeline, StepExecutionError

try:
    pipeline.run()
except StepExecutionError as error:
    print(error)
```

If a step fails, the framework raises a clear error message showing which step failed and what the original exception was.

---

## Ingestion

The ingestion module provides reusable CSV loading utilities.

```python
from analytics_framework.ingestion import MultipleCSVLoaderStep

files = {
    "customers": "data/raw/customers.csv",
    "orders": "data/raw/orders.csv",
}

pipeline.add_step(
    MultipleCSVLoaderStep(
        files=files,
        output_key="datasets",
    )
)
```

The loaded datasets are stored in the pipeline context:

```python
context["datasets"]
```

---

## Data Quality

The quality module provides reusable validation checks.

```python
from analytics_framework.quality import DataQualityValidatorStep

pipeline.add_step(
    DataQualityValidatorStep(
        input_key="sales",
        output_key="quality_report",
        required_columns=["order_id", "customer_id", "price"],
        non_negative_columns=["price"],
        fail_on_error=True,
    )
)
```

The validation report is stored as a DataFrame in the context:

```python
context["quality_report"]
```

---

## Transformations

The features module provides reusable DataFrame transformation steps.

Available steps include:

- `DropDuplicatesStep`
- `FillMissingValuesStep`
- `ConvertDateColumnsStep`
- `RenameColumnsStep`
- `SelectColumnsStep`
- `ExportDataFrameStep`

Example:

```python
from analytics_framework.features import ConvertDateColumnsStep, DropDuplicatesStep

pipeline.add_step(
    DropDuplicatesStep(
        input_key="raw_data",
        output_key="clean_data",
    )
)

pipeline.add_step(
    ConvertDateColumnsStep(
        input_key="clean_data",
        output_key="clean_data",
        columns=["order_date"],
    )
)
```

---

## Metrics

The analytics module provides reusable metrics computation steps.

### Basic Metrics

```python
from analytics_framework.analytics import BasicMetricsStep

pipeline.add_step(
    BasicMetricsStep(
        input_key="sales",
        output_key="executive_metrics",
        metrics={
            "total_revenue": {
                "column": "revenue",
                "operation": "sum",
            },
            "average_order_value": {
                "column": "revenue",
                "operation": "mean",
            },
        },
    )
)
```

### Group-By Metrics

```python
from analytics_framework.analytics import GroupByMetricsStep

pipeline.add_step(
    GroupByMetricsStep(
        input_key="sales",
        output_key="category_metrics",
        groupby_columns=["category"],
        aggregations={
            "revenue": "sum",
            "order_id": "nunique",
        },
    )
)
```

### Time-Series Metrics

```python
from analytics_framework.analytics import TimeSeriesMetricsStep

pipeline.add_step(
    TimeSeriesMetricsStep(
        input_key="sales",
        output_key="monthly_revenue",
        date_column="order_date",
        value_column="revenue",
        frequency="M",
        operation="sum",
    )
)
```

---

## Visualization

The visualization module provides reusable plotting steps.

```python
from analytics_framework.visualization import LinePlotStep, BarPlotStep

pipeline.add_step(
    LinePlotStep(
        input_key="monthly_revenue",
        x_column="month",
        y_column="revenue",
        output_path="reports/figures/monthly_revenue.png",
        title="Monthly Revenue Evolution",
        xlabel="Month",
        ylabel="Revenue",
    )
)

pipeline.add_step(
    BarPlotStep(
        input_key="category_metrics",
        x_column="category",
        y_column="revenue",
        output_path="reports/figures/revenue_by_category.png",
        title="Revenue by Category",
        xlabel="Category",
        ylabel="Revenue",
    )
)
```

---

## Reporting

The reporting module can generate Markdown reports from pipeline context values.

```python
from analytics_framework.reporting import MarkdownReportStep

pipeline.add_step(
    MarkdownReportStep(
        title="Executive Analytics Report",
        output_path="reports/executive_report.md",
        context_keys=[
            "executive_metrics",
            "category_metrics",
            "quality_report",
        ],
    )
)
```

The report is written to disk and the path is stored in the context:

```python
context["markdown_report_path"]
```

---

## Export

The export module provides CSV and Excel export steps.

### CSV Export

```python
from analytics_framework.export import CSVExportStep

pipeline.add_step(
    CSVExportStep(
        input_key="sales",
        output_path="data/processed/sales.csv",
    )
)
```

### Excel Export

```python
from analytics_framework.export import ExcelExportStep

pipeline.add_step(
    ExcelExportStep(
        input_key="metrics",
        output_path="reports/metrics.xlsx",
        sheet_name="KPIs",
    )
)
```

### Multi-Sheet Excel Export

```python
from analytics_framework.export import MultiSheetExcelExportStep

pipeline.add_step(
    MultiSheetExcelExportStep(
        input_keys={
            "KPIs": "executive_metrics",
            "Categories": "category_metrics",
            "Quality": "quality_report",
        },
        output_path="reports/executive_dashboard.xlsx",
    )
)
```

---

## Example Use Case

This framework is currently used in the following project:

- [supply-chain-analytics](https://github.com/TheKopps/supply-chain-analytics)

In that project, the framework is used to:

- load raw Olist CSV files
- create a consolidated sales table
- validate data quality
- clean and transform the data
- compute business KPIs
- generate charts
- create a Markdown executive report
- export Excel dashboards

---

## Development

Run unit tests:

```bash
python -m pytest -q
```

Run Ruff linting:

```bash
ruff check .
```

Auto-fix linting issues:

```bash
ruff check . --fix
```

Format code:

```bash
ruff format .
```

Check formatting:

```bash
ruff format --check .
```

Recommended full local check:

```bash
ruff check . --fix
ruff format .
ruff check .
ruff format --check .
python -m pytest -q
```

---

## Continuous Integration

The repository uses GitHub Actions to automatically run:

- Ruff linting
- Ruff formatting check
- Pytest unit tests

CI is triggered on:

- pull requests to `develop`
- pull requests to `main`
- pushes to `develop`
- pushes to `main`

---

## Git Workflow

The project follows a simple professional Git workflow:

```text
main
  stable releases

develop
  integration branch

feature/*
  new features
```

Example:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/new-module
```

After development:

```bash
git add .
git commit -m "feat(module): add new module"
git push -u origin feature/new-module
```

Then create a pull request into `develop`.

---

## Current Version

Current release:

```text
v0.1.0
```

This first version includes the complete foundation of the analytics framework:

```text
Pipeline
Config
Logger
Error Handling
Tests
CI
Ingestion
Quality
Transformations
Metrics
Visualization
Reporting
Export
```

---

## Roadmap

Planned improvements:

- Add SQL connectors
- Add database export utilities
- Add Power BI preparation helpers
- Add Streamlit dashboard helpers
- Add automated insight generation
- Add ML preprocessing steps
- Add model training pipeline steps
- Add model evaluation utilities
- Add Docker support
- Add package publishing workflow
- Add more advanced documentation

---

## Portfolio Vision

This framework is designed to support multiple end-to-end analytics projects, including:

- Supply Chain Analytics
- Formula 1 Race Analytics
- Predictive Maintenance
- Job Market Intelligence
- Business Intelligence dashboards
- Machine Learning projects

The objective is to demonstrate both data skills and software engineering skills:

- Python package design
- modular architecture
- reusable pipeline components
- testing
- CI/CD
- documentation
- Git workflow
- analytics automation

---

## Author

Adrien Monteiro