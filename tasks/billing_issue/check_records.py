def check_billing_records(event):
    print("Checking billing records...")
    # Access the event data including any modifications from previous tasks
    billing_issue_data = event.data
    print(f"Checking billing records with data: {billing_issue_data}")
    
    # Add processing results to the data
    event.data['processed'] = True
    event.data['process_id'] = '12345'  # example
    
    return event 