import pandas as pd

from analytics_framework import Pipeline
from analytics_framework.analytics import (
    BasicMetricsStep,
    GroupByMetricsStep,
    TimeSeriesMetricsStep,
)

sales = pd.DataFrame(
    {
        "order_id": [1, 2, 3, 4],
        "category": ["A", "A", "B", "B"],
        "revenue": [100.0, 150.0, 200.0, 300.0],
        "order_date": [
            "2024-01-01",
            "2024-01-15",
            "2024-02-01",
            "2024-02-20",
        ],
    }
)

pipeline = Pipeline("Metrics Demo")
pipeline.context["sales"] = sales

pipeline.add_step(
    BasicMetricsStep(
        input_key="sales",
        metrics={
            "total_revenue": {
                "column": "revenue",
                "operation": "sum",
            },
            "average_order_value": {
                "column": "revenue",
                "operation": "mean",
            },
            "total_orders": {
                "column": "order_id",
                "operation": "nunique",
            },
        },
    )
)

pipeline.add_step(
    GroupByMetricsStep(
        input_key="sales",
        groupby_columns=["category"],
        aggregations={
            "revenue": "sum",
            "order_id": "nunique",
        },
        output_key="category_metrics",
    )
)

pipeline.add_step(
    TimeSeriesMetricsStep(
        input_key="sales",
        date_column="order_date",
        value_column="revenue",
        frequency="M",
        operation="sum",
        output_key="monthly_revenue",
    )
)

result = pipeline.run()

print(result["basic_metrics"])
print(result["category_metrics"])
print(result["monthly_revenue"])
