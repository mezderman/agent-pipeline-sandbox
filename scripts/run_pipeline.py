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
    
    product_issue_data = {
        'product_id': 'PROD-123',
        'customer_id': 'CUST-456',
        'issue_description': 'What are the highlights of this article?',
        'severity': 'high'
    }
    
    # Test Case 2: Billing Issue
    billing_issue_data = {
        'customer_id': 'CUST-789',
        'amount': 299.99,
        'issue_type': 'overcharge',
        'description': 'Double charged for monthly subscription'
    }
    
   

    # Choose which test to run
    test_case = "analyze_query"  # Change this to test different scenarios
    
    if test_case == "product_issue":
        event = EventFactory.create_event("product_issue", product_issue_data)
    elif test_case == "billing_issue":
        event = EventFactory.create_event("billing_issue", billing_issue_data)
    elif test_case == "analyze_query":
        event = EventFactory.create_event("analyze_query", customer_inquiry)
    
    # Get type-validated data
    validated_data = event.get_validated_data()

    # Get and run the appropriate pipeline
    pipeline = PipelineRegistry.get_pipeline(event)
    output = pipeline.run(event)

    output.model_dump()

    print("Pipeline execution output:", output.data)
