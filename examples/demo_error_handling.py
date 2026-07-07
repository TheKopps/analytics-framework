from analytics_framework import Pipeline, PipelineStep, StepExecutionError


class LoadDataStep(PipelineStep):
    def __init__(self):
        super().__init__("Load Data")

    def execute(self, context):
        context["data"] = [1, 2, 3]
        return context


class FailingStep(PipelineStep):
    def __init__(self):
        super().__init__("Failing Step")

    def execute(self, context):
        raise ValueError("This is a simulated pipeline failure.")


pipeline = Pipeline("Error Handling Demo Pipeline")

pipeline.add_step(LoadDataStep())
pipeline.add_step(FailingStep())

try:
    pipeline.run()

except StepExecutionError as error:
    print("Custom error caught successfully.")
    print(error)
