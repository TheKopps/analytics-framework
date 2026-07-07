from analytics_framework import Pipeline, PipelineStep, setup_logger


class LoadDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Load Data")

    def execute(self, context):
        context["data"] = [10, 20, 30]
        return context


class ComputeTotalStep(PipelineStep):
    def __init__(self):
        super().__init__("Compute Total")

    def execute(self, context):
        context["total"] = sum(context["data"])
        return context


logger = setup_logger(log_file="examples/logs/pipeline.log")

pipeline = Pipeline(
    project_name="Logger Demo Pipeline",
    logger=logger,
)

pipeline.add_step(LoadDataStep())
pipeline.add_step(ComputeTotalStep())

result = pipeline.run()

print(result)