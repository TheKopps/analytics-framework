import time
from logging import Logger
from typing import Any

from analytics_framework.core.logger import setup_logger
from analytics_framework.core.pipeline_step import PipelineStep


class Pipeline:
    """
    Modular pipeline engine for analytics projects.
    """

    def __init__(
        self,
        project_name: str,
        logger: Logger | None = None,
    ):
        self.project_name = project_name
        self.steps: list[PipelineStep] = []
        self.context: dict[str, Any] = {}
        self.logger = logger or setup_logger()

    def add_step(self, step: PipelineStep) -> "Pipeline":
        self.steps.append(step)
        return self

    def run(self) -> dict[str, Any]:
        pipeline_start = time.perf_counter()

        self.logger.info("=" * 60)
        self.logger.info(f"Running pipeline: {self.project_name}")
        self.logger.info("=" * 60)

        for index, step in enumerate(self.steps, start=1):
            step_start = time.perf_counter()

            self.logger.info(
                f"[{index}/{len(self.steps)}] Running step: {step.name}"
            )

            self.context = step.execute(self.context)

            step_duration = round(time.perf_counter() - step_start, 2)

            self.logger.info(
                f"[OK] Step completed: {step.name} in {step_duration}s"
            )

        pipeline_duration = round(time.perf_counter() - pipeline_start, 2)

        self.logger.info("=" * 60)
        self.logger.info(
            f"Pipeline completed successfully in {pipeline_duration}s."
        )
        self.logger.info("=" * 60)

        return self.context