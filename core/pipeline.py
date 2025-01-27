from core.event import Event
from tasks.base_task import BaseTask
from typing import Type, Union, Dict, Optional, Tuple

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
        self.next_pipeline_options: Optional[Dict[str, str]] = None
        self.is_router = False

    def add_task(self, task_class: Union[Type[BaseTask], BaseTask]):
        task_wrapper = Task(task_class)
        if not self.start_task:
            self.start_task = task_wrapper
        if self.current_task:
            self.current_task.set_next(task_wrapper)
        self.current_task = task_wrapper
        return self

    def set_next_pipeline_options(self, options: Dict[str, str]):
        """Configure this pipeline as a router with next pipeline options.
        
        Args:
            options: Dictionary mapping decision values to pipeline names
                    e.g., {"product_issue": "product_pipeline"}
        """
        self.next_pipeline_options = options
        self.is_router = True
        return self

    def get_next_pipeline_key(self, decision_value: str) -> Optional[str]:
        """Get the next pipeline key based on the decision value."""
        if not self.is_router or not self.next_pipeline_options:
            return None
        return self.next_pipeline_options.get(decision_value)

    def run(self, event: Event) -> Union[Event, Tuple[Event, Optional[str]]]:
        """Run the pipeline and return either:
        - Just the event (for normal pipelines)
        - Tuple of (event, next_pipeline_key) for router pipelines
        """
        if not self.start_task:
            raise RuntimeError("Pipeline has no tasks")
        
        result = self.start_task.execute(event)
        
        # Only router pipelines return a tuple
        if self.is_router and self.next_pipeline_options:
            decision_value = result.data['nodes']['RouterQuery']['intent']
            next_pipeline_key = self.get_next_pipeline_key(decision_value)
            return result, next_pipeline_key
            
        # Normal pipelines just return the event
        return result
