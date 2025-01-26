from tasks.base_task import BaseTask
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor
from enum import Enum

class AnalyzeQuery(BaseTask):
    class Categories(str, Enum):
        """Enumeration of categories for incoming queries.
        - PRODUCT_ISSUE: If the query relates to a problem with a product.
        - BILLING_ISSUE: If the query relates to a billing or payment issue.
        - OTHER: If the query does not fit into product or billing issues.
        """
        PRODUCT_ISSUE = "product_issue"
        BILLING_ISSUE = "billing_issue"
        OTHER = "other"

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = "gpt-4o-2024-08-06"

        self.response_model = create_model(
            'Choice',
            category=(self.Categories, ...),
            reason=(str, Field(description="The reason for selecting this category"))
        )
       
        
    def route(self, query: str):
       
        choice = self.client.chat.completions.create(
            model=self.model,
            response_model=self.response_model,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You're a helpful personal assistant that can classify incoming messages."},
                {"role": "user", "content": query },
            ],
            )
            
        return choice
    
    def execute(self, event: Event) -> Event:
        print("Analyzing issue...")
        # Access the event data
        issue_data = event.data
        result = self.route(issue_data['issue_description'])
        print(result)
        print(f"Analyzing issue with data: {issue_data}")
        
        # You can modify the data or add validation results
        event.data['validation_passed'] = True
        event.data['validation_timestamp'] = '2024-03-21'  # example
        
        return event 

