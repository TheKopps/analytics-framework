from pathlib import Path

import pandas as pd

from analytics_framework import Pipeline
from analytics_framework.ingestion import CSVLoaderStep

sample_path = Path("examples/data/sample_sales.csv")
sample_path.parent.mkdir(parents=True, exist_ok=True)

sample_data = pd.DataFrame(
    {
        "order_id": [1, 2, 3],
        "revenue": [120.5, 89.9, 250.0],
        "customer": ["A", "B", "C"],
    }
)

sample_data.to_csv(sample_path, index=False)

pipeline = Pipeline("CSV Ingestion Demo")

pipeline.add_step(
    CSVLoaderStep(
        path=sample_path,
        output_key="sales",
    )
)

result = pipeline.run()

print(result["sales"])
