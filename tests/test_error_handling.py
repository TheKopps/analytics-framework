import pytest

from analytics_framework import Pipeline, PipelineStep, StepExecutionError


class FailingStep(PipelineStep):
    def __init__(self):
        super().__init__("Failing Step")

    def execute(self, context):
        raise ValueError("Simulated failure")


class SafeStep(PipelineStep):
    def __init__(self):
        super().__init__("Safe Step")

    def execute(self, context):
        context["safe_step_executed"] = True
        return context


def test_pipeline_raises_step_execution_error():
    pipeline = Pipeline("Error Test Pipeline")

    pipeline.add_step(FailingStep())

    with pytest.raises(StepExecutionError) as error:
        pipeline.run()

    assert "Failing Step" in str(error.value)
    assert "Simulated failure" in str(error.value)


def test_pipeline_can_continue_when_stop_on_error_is_false():
    pipeline = Pipeline(
        "Continue On Error Pipeline",
        stop_on_error=False,
    )

    pipeline.add_step(FailingStep())
    pipeline.add_step(SafeStep())

    result = pipeline.run()

    assert result["safe_step_executed"] is True