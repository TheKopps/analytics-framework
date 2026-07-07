import pandas as pd

from analytics_framework import Pipeline
from analytics_framework.reporting import MarkdownReportStep

metrics = pd.DataFrame(
    {
        "metric": ["total_revenue", "total_orders", "average_order_value"],
        "value": [12500, 145, 86.2],
    }
)

recommendations = [
    "Increase marketing campaigns during low-performing periods.",
    "Monitor categories with high revenue concentration.",
    "Investigate operational delays before scaling the business.",
]

pipeline = Pipeline("Reporting Demo")

pipeline.context["metrics"] = metrics
pipeline.context["recommendations"] = recommendations

pipeline.add_step(
    MarkdownReportStep(
        title="Executive Analytics Report",
        output_path="examples/reports/executive_report.md",
        context_keys=["metrics", "recommendations"],
    )
)

result = pipeline.run()

print(result["markdown_report_path"])
