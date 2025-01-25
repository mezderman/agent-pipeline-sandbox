def check_product_records(event):
    print("Checking product records...")
    # Access the event data including any modifications from previous tasks
    product_issue_data = event.data
    print(f"Checking product records with data: {product_issue_data}")
    
    # Add processing results to the data
    event.data['processed'] = True
    event.data['process_id'] = '12345'  # example
    
    return event 