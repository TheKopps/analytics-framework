import pandas as pd

from analytics_framework import Pipeline
from analytics_framework.features import (
    ConvertDateColumnsStep,
    DropDuplicatesStep,
    FillMissingValuesStep,
    RenameColumnsStep,
    SelectColumnsStep,
)

sales = pd.DataFrame(
    {
        "order_id": [1, 2, 2, 3],
        "order_date": ["2024-01-01", "2024-01-02", "2024-01-02", None],
        "revenue": [100.0, None, None, 250.0],
        "customer": ["A", "B", "B", "C"],
    }
)

pipeline = Pipeline("Transformation Demo")
pipeline.context["sales"] = sales

pipeline.add_step(
    DropDuplicatesStep(
        input_key="sales",
        subset=["order_id"],
    )
)

pipeline.add_step(
    FillMissingValuesStep(
        input_key="sales",
        fill_values={
            "revenue": 0,
        },
    )
)

pipeline.add_step(
    ConvertDateColumnsStep(
        input_key="sales",
        columns=["order_date"],
    )
)

pipeline.add_step(
    RenameColumnsStep(
        input_key="sales",
        columns_mapping={
            "order_date": "purchase_date",
        },
    )
)

pipeline.add_step(
    SelectColumnsStep(
        input_key="sales",
        columns=["order_id", "purchase_date", "revenue"],
    )
)

result = pipeline.run()

print(result["sales"])
