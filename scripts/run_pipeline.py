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
    

    # First run the analysis pipeline
    test_case = "analyze_query"
    event = EventFactory.create_event("analyze_query", customer_inquiry)
    
    # Get and run the analysis pipeline
    pipeline = PipelineRegistry.get_pipeline(event)
    output = pipeline.run(event)
    
    # Get the intent from analysis
    analyze_result = output.data['nodes']['AnalyzeQuery']
    intent = analyze_result['intent']
    
    # Route to appropriate pipeline based on intent
    if intent == 'product_issue':
        print("\nRouting to Product Issue Pipeline...")
        product_event = EventFactory.create_event("product_issue", output.data)
        product_pipeline = PipelineRegistry.get_pipeline(product_event)
        final_output = product_pipeline.run(product_event)
    elif intent == 'billing_issue':
        print("\nRouting to Billing Issue Pipeline...")
        # billing_event = EventFactory.create_event("billing_issue", output.data)
        # billing_pipeline = PipelineRegistry.get_pipeline(billing_event)
        # final_output = billing_pipeline.run(billing_event)
    
    print("\nFinal Pipeline output:", final_output.data)
    
