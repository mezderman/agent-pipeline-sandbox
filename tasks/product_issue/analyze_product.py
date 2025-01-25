def analyze_product_issue(event):
    print("Analyzing product issue...")
    # Access the event data
    product_issue_data = event.data
    print(f"Analyzing product issue with data: {product_issue_data}")
    
    # You can modify the data or add validation results
    event.data['validation_passed'] = True
    event.data['validation_timestamp'] = '2024-03-21'  # example
    
    return event 