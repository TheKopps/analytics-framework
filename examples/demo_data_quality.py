import pandas as pd

from analytics_framework import Pipeline
from analytics_framework.quality import DataQualityValidatorStep

sales = pd.DataFrame(
    {
        "order_id": [1, 2, 3, 3],
        "revenue": [120.5, 89.9, -50.0, 250.0],
        "status": ["delivered", "delivered", "cancelled", "unknown"],
    }
)

pipeline = Pipeline("Data Quality Demo")

pipeline.context["sales"] = sales

pipeline.add_step(
    DataQualityValidatorStep(
        input_key="sales",
        required_columns=["order_id", "revenue", "status"],
        non_negative_columns=["revenue"],
        allowed_values={
            "status": ["delivered", "cancelled"],
        },
        duplicate_subset=["order_id"],
        fail_on_error=False,
    )
)

result = pipeline.run()

print(result["data_quality_report"])
