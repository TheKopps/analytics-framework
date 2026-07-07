class AnalyticsFrameworkError(Exception):
    """
    Base exception for the analytics framework.
    """


class PipelineError(AnalyticsFrameworkError):
    """
    Raised when a pipeline-level error occurs.
    """


class StepExecutionError(PipelineError):
    """
    Raised when a pipeline step fails during execution.
    """

    def __init__(self, step_name: str, original_exception: Exception):
        self.step_name = step_name
        self.original_exception = original_exception

        message = (
            f"Step '{step_name}' failed. "
            f"Original error: {type(original_exception).__name__}: {original_exception}"
        )

        super().__init__(message)