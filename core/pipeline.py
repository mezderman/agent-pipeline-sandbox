from core.event import Event

class Task:
    def __init__(self, func):
        self.func = func
        self.next_task = None

    def set_next(self, task):
        self.next_task = task

    def execute(self, event: Event):
        # Execute the current task
        result = self.func(event)
        # Pass to the next task, if exists
        if self.next_task:
            return self.next_task.execute(event)
        return result

class Pipeline:
    def __init__(self):
        self.start_task = None
        self.current_task = None

    def add_task(self, func):
        task = Task(func)
        if not self.start_task:
            self.start_task = task
        if self.current_task:
            self.current_task.set_next(task)
        self.current_task = task
        return self

    def run(self, event: Event):
        if not self.start_task:
            raise RuntimeError("Pipeline has no tasks")
        return self.start_task.execute(event)
