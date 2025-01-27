from pipelines.registry import register_all_pipelines
from core.registry import PipelineRegistry
from core.event import EventFactory
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Step 1: Register all pipelines
    register_all_pipelines()


    #TESTING
    #billing issues
    #I was charged twice for my subscription. Can I get a refund for the extra charge?
    # Can you provide me with a detailed summary of my last three months' bills?

    #product issues
    #The device I purchased is not charging properly. What should I do?
    customer_inquiry = {
        "customer_id": "CUST-456",
        "issue_description": "I was charged twice for my subscription. Can I get a refund for the extra charge?",
    }
    

    # First run the router pipeline
    event = EventFactory.create_event("router_query", customer_inquiry)
    pipeline = PipelineRegistry.get_pipeline(event)
    output, next_pipeline_key = pipeline.run(event)  # This is a router pipeline
    
    if next_pipeline_key:
        print(f"\nRouting to {next_pipeline_key} Pipeline...")
        # Create new event while preserving the nodes data
        next_event = EventFactory.create_event(next_pipeline_key, {
            "customer_id": customer_inquiry["customer_id"],
            "issue_description": customer_inquiry["issue_description"],
            "nodes": output.data["nodes"]  # Preserve the nodes data
        })
        next_pipeline = PipelineRegistry.get_pipeline(next_event)
        final_output = next_pipeline.run(next_event)
        print("\nFinal Pipeline output:", final_output.data)
    else:
        print("\nNo next pipeline specified")
    
