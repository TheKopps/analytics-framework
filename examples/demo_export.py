import pandas as pd

from analytics_framework import Pipeline
from analytics_framework.export import (
    CSVExportStep,
    ExcelExportStep,
    MultiSheetExcelExportStep,
)

metrics = pd.DataFrame(
    {
        "metric": ["total_revenue", "total_orders", "average_order_value"],
        "value": [12500, 145, 86.2],
    }
)

category_metrics = pd.DataFrame(
    {
        "category": ["A", "B", "C"],
        "revenue": [5000, 4500, 3000],
    }
)

pipeline = Pipeline("Export Demo")

pipeline.context["metrics"] = metrics
pipeline.context["category_metrics"] = category_metrics

pipeline.add_step(
    CSVExportStep(
        input_key="metrics",
        output_path="examples/exports/metrics.csv",
    )
)

pipeline.add_step(
    ExcelExportStep(
        input_key="metrics",
        output_path="examples/exports/metrics.xlsx",
        sheet_name="KPIs",
    )
)

pipeline.add_step(
    MultiSheetExcelExportStep(
        input_keys={
            "KPIs": "metrics",
            "Categories": "category_metrics",
        },
        output_path="examples/exports/executive_dashboard.xlsx",
    )
)

result = pipeline.run()

print(result["csv_export_path"])
print(result["excel_export_path"])
print(result["multi_sheet_excel_export_path"])
