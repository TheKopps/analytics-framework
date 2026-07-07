from analytics_framework import Pipeline, PipelineStep


class LoadDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Load Data")

    def execute(self, context):
        context["data"] = [1, 2, 3, 4, 5]
        return context


class SumDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Sum Data")

    def execute(self, context):
        context["total"] = sum(context["data"])
        return context


pipeline = Pipeline("Demo Analytics Pipeline")

pipeline.add_step(LoadDataStep())
pipeline.add_step(SumDataStep())

result = pipeline.run()

print(result)
