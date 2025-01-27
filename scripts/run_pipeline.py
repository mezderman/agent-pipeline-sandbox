from pipelines.registry import register_all_pipelines
from core.registry import PipelineRegistry
from core.event import EventFactory
from dotenv import load_dotenv
from core.pipeline_runner import PipelineRunner

load_dotenv()

if __name__ == "__main__":
    #TESTING
    #billing issues
    #I was charged twice for my subscription. Can I get a refund for the extra charge?
    # Can you provide me with a detailed summary of my last three months' bills?

    #product issues
    #The device I purchased is not charging properly. What should I do?
    customer_inquiry = {
        "user_id": "CUST-456",
        "content": "The device I purchased is not charging properly. What should I do?",
    }
    # Step 1: Register all pipelines
    register_all_pipelines()
    
    # start the entry point pipeline
    event = EventFactory.create_event("router_query", customer_inquiry)
    
    # Create registry and runner
    registry = PipelineRegistry()
    runner = PipelineRunner(registry)
    
    # Run the pipeline chain
    final_output = runner.run_pipeline(event)
    print("\nFinal Pipeline output:", final_output.data)
    
