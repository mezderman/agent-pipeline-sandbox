from core.event import Event, EventFactory
from core.registry import PipelineRegistry

class PipelineRunner:
    def __init__(self, registry: PipelineRegistry):
        self.registry = registry

    def run_pipeline(self, event: Event) -> Event:
        """
        Run a pipeline and any subsequent chained pipelines.
        Returns the final result from the last pipeline in the chain.
        """
        pipeline = self.registry.get_pipeline(event)
        result, next_pipeline_key = pipeline.run(event)

        if next_pipeline_key:
            next_event = EventFactory.create_event(
                next_pipeline_key,
                {
                    "customer_id": event.data.get("customer_id"),
                    "issue_description": event.data.get("issue_description"),
                    "nodes": result.data.get("nodes", {})  # result is the Event object
                }
            )
            return self.run_pipeline(next_event)  # Recursive call for next pipeline
        
        return result  # Return the Event object directly 