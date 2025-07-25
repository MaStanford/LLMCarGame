from textual.message import Message
from typing import Any

class ModelLoadingSuccess(Message):
    """Posted when the model has loaded successfully."""
    def __init__(self, pipeline: Any) -> None:
        self.pipeline = pipeline
        super().__init__()

class ModelLoadingStatus(Message):
    """Posted to update the model loading status."""
    def __init__(self, status: str) -> None:
        self.status = status
        super().__init__()

class ModelLoadingFailed(Message):
    """Posted when model loading fails."""
    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__()
