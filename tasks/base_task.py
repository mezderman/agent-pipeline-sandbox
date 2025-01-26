from core.event import Event

class BaseTask:
    """Base class for all tasks"""
    def execute(self, event: Event) -> Event:
        raise NotImplementedError("Task must implement execute method") 