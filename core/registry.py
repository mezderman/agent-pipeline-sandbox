from core.pipeline import Pipeline
from core.event import Event

class PipelineRegistry:
    _pipelines = {}

    @classmethod
    def register_pipeline(cls, event_key: str, pipeline: Pipeline):
        cls._pipelines[event_key] = pipeline

    @classmethod
    def get_pipeline(cls, event: Event) -> Pipeline:
        pipeline = cls._pipelines.get(event.event_key)
        if not pipeline:
            raise ValueError(f"No pipeline registered for event key: {event.event_key}")
        return pipeline
