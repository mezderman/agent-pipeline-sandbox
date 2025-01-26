from core.event import Event
from tasks.base_task import BaseTask
from typing import Type, Union

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

class Pipeline:
    def __init__(self):
        self.start_task = None
        self.current_task = None

    def add_task(self, task_class: Union[Type[BaseTask], BaseTask]):
        task_wrapper = Task(task_class)
        if not self.start_task:
            self.start_task = task_wrapper
        if self.current_task:
            self.current_task.set_next(task_wrapper)
        self.current_task = task_wrapper
        return self

    def run(self, event: Event):
        if not self.start_task:
            raise RuntimeError("Pipeline has no tasks")
        return self.start_task.execute(event)
