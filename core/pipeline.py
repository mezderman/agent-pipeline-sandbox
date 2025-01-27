from core.event import Event
from core.task import Task
from tasks.base_task import BaseTask
from typing import Type, Union, Dict, Optional, Tuple

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

    def run(self, event: Event) -> Tuple[Event, Optional[str]]:
        """
        Run the pipeline and return the result and next pipeline key if any.
        """
        if not self.start_task:
            raise RuntimeError("Pipeline has no tasks")
        
        result = self.start_task.execute(event)
        
        # If this is a router pipeline, check for next pipeline
        next_pipeline_key = None
        if self.is_router and self.next_pipeline_options:
            decision_value = result.data['nodes']['RouterQuery']['intent']
            next_pipeline_key = self.get_next_pipeline_key(decision_value)
            
        return result, next_pipeline_key
