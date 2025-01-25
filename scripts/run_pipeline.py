from pipelines.registry import register_all_pipelines
from core.registry import PipelineRegistry
from core.event import Event, EventFactory

if __name__ == "__main__":
    # Step 1: Register all pipelines
    register_all_pipelines()

    # Create sample product issue data
    product_issue_data = {
        'product_id': 'PROD-123',
        'customer_id': 'CUST-456',
        'issue_description': 'Product not working as expected',
        'severity': 'high'
    }
    
    # Create product issue event
    event = EventFactory.create_event(
        "product_issue",
        product_issue_data
    )

    # # Create sample billing issue data
    # billing_issue_data = {
    #     'customer_id': 'CUST-456',
    #     'amount': 299.99,
    #     'issue_type': 'overcharge',
    #     'description': 'Incorrect charges on invoice'
    # }
    
    # # Create billing issue event∏
    # event = EventFactory.create_event(
    #     "billing_issue",
    #     billing_issue_data
    # )
    
    # Get type-validated data
    validated_data = event.get_validated_data()  # Returns ProductIssueData instance

    # Get and run the appropriate pipeline
    pipeline = PipelineRegistry.get_pipeline(event)
    output = pipeline.run(event)

    output.model_dump()

    print("Pipeline execution output:", output.data)
