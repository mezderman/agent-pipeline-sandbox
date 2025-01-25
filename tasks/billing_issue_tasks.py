def analyze_billing_issue(event):
    print("Analyzing billing issue...")
    # Access the event data
    billing_issue_data = event.data
    print(f"Analyzing billing issue with data: {billing_issue_data}")
    
    # You can modify the data or add validation results
    event.data['validation_passed'] = True
    event.data['validation_timestamp'] = '2024-03-21'  # example
    
    return event

def check_billing_records(event):
    print("Checking billing records...")
    # Access the event data including any modifications from previous tasks
    billing_issue_data = event.data
    print(f"Checking billing records with data: {billing_issue_data}")
    
    # Add processing results to the data
    event.data['processed'] = True
    event.data['process_id'] = '12345'  # example
    
    return event
