from core.event import Event
from tasks.base_task import BaseTask
from typing import Type

class Task:
    def __init__(self, task_class: Type[BaseTask]):
        # Always instantiate the task class
        self.task = task_class() if isinstance(task_class, type) else task_class
        self.next_task = None

        if not isinstance(self.task, BaseTask):
            raise TypeError(f"Task must be a BaseTask class or instance, got {type(task_class)}")

    def set_next(self, task):
        self.next_task = task

    def execute(self, event: Event):
        result = self.task.execute(event)
        if self.next_task:
            return self.next_task.execute(event)
        return result 