import pandas as pd

from analytics_framework import Pipeline
from analytics_framework.visualization import (
    BarPlotStep,
    HistogramPlotStep,
    LinePlotStep,
)

sales = pd.DataFrame(
    {
        "month": ["2024-01", "2024-02", "2024-03"],
        "revenue": [1000, 1500, 1300],
        "orders": [10, 15, 13],
    }
)

pipeline = Pipeline("Visualization Demo")
pipeline.context["sales"] = sales

pipeline.add_step(
    LinePlotStep(
        input_key="sales",
        x_column="month",
        y_column="revenue",
        output_path="examples/figures/revenue_over_time.png",
        title="Revenue Over Time",
    )
)

pipeline.add_step(
    BarPlotStep(
        input_key="sales",
        x_column="month",
        y_column="orders",
        output_path="examples/figures/orders_by_month.png",
        title="Orders by Month",
    )
)

pipeline.add_step(
    HistogramPlotStep(
        input_key="sales",
        column="revenue",
        output_path="examples/figures/revenue_distribution.png",
        title="Revenue Distribution",
    )
)

result = pipeline.run()

print(result["figures"])
