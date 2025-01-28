from pipelines.registry import register_all_pipelines
from core.registry import PipelineRegistry
from core.event import EventFactory
from dotenv import load_dotenv
from core.pipeline_runner import PipelineRunner
import json
import sys

load_dotenv()

if __name__ == "__main__":
    #TESTING
    #billing issues
    #I was charged twice for my subscription. Can I get a refund for the extra charge?
    # Can you provide me with a detailed summary of my last three months' bills?
    #Please summarize all my purchases and transactions from Decmber 2024 with itemized details.
    # Can you give me a comprehensive report of the bills I was charged last month?
    # I was charged twice for my Premium Plan subscription. Can I get a refund for the extra charge

    #product issues
    #The device I purchased is not charging properly. What should I do?


    customer_inquiry = {
        "user_id": "CUST-456",
        "content": "I was charged twice for my Premium Plan subscription. Can I get a refund for the extra charge",
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

    # Increase d

    print("\nFinal Pipeline output:")

    json.dump(final_output.data, sys.stdout, indent=4, ensure_ascii=False)
print()  # Ad
    
