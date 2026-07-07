from typing import Any

from analytics_framework.core.pipeline_step import PipelineStep


class Pipeline:
    """
    Modular pipeline engine for analytics projects.
    """

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.steps: list[PipelineStep] = []
        self.context: dict[str, Any] = {}

    def add_step(self, step: PipelineStep) -> "Pipeline":
        self.steps.append(step)
        return self

    def run(self) -> dict[str, Any]:
        print("=" * 60)
        print(f"Running pipeline: {self.project_name}")
        print("=" * 60)

        for index, step in enumerate(self.steps, start=1):
            print(f"[{index}/{len(self.steps)}] Running step: {step.name}")
            self.context = step.execute(self.context)
            print(f"[OK] Step completed: {step.name}")

        print("=" * 60)
        print("Pipeline completed successfully.")
        print("=" * 60)

        return self.context