from analytics_framework import Pipeline, PipelineStep


class LoadDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Load Data")

    def execute(self, context):
        context["data"] = [1, 2, 3]
        return context


class SumDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Sum Data")

    def execute(self, context):
        context["total"] = sum(context["data"])
        return context


def test_pipeline_runs_steps_and_updates_context():
    pipeline = Pipeline("Test Pipeline")

    pipeline.add_step(LoadDataStep())
    pipeline.add_step(SumDataStep())

    result = pipeline.run()

    assert result["data"] == [1, 2, 3]
    assert result["total"] == 6
    assert len(pipeline.steps) == 2
