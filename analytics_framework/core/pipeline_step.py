from abc import ABC, abstractmethod
from typing import Any


class PipelineStep(ABC):
    """
    Base class for all pipeline steps.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the step and update the pipeline context.
        """
        pass