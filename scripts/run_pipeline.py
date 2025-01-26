from pipelines.registry import register_all_pipelines
from core.registry import PipelineRegistry
from core.event import EventFactory
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Step 1: Register all pipelines
    register_all_pipelines()


    #TESTING

    # Test Case 1: Product Issue
    customer_inquiry = {
        "customer_id": "CUST-456",
        "issue_description": "The device I purchased is not charging properly. What should I do?",
    }
    
   
    
   

    # Choose which test to run
    test_case = "analyze_query"  # Change this to test different scenarios
    
    if test_case == "product_issue":
        event = EventFactory.create_event("product_issue", customer_inquiry)
    elif test_case == "billing_issue":
        event = EventFactory.create_event("billing_issue", customer_inquiry)
    elif test_case == "analyze_query":
        event = EventFactory.create_event("analyze_query", customer_inquiry)
    
    # Get type-validated data
    validated_data = event.get_validated_data()

    # Get and run the appropriate pipeline
    pipeline = PipelineRegistry.get_pipeline(event)
    output = pipeline.run(event)
    print("Pipeline execution output:", output.data)
    # print(output.data['nodes'][0]['AnalyzeQuery'].name)
    
