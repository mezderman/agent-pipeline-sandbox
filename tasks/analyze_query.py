from tasks.base_task import BaseTask
from core.event import Event
from pydantic import BaseModel, Field
from openai import OpenAI
import instructor
from enum import Enum

class Categories(str, Enum):
    """Enumeration of categories for incoming queries.
    - PRODUCT_ISSUE: If the query relates to a problem with a product.
    - BILLING_ISSUE: If the query relates to a billing or payment issue.
    - OTHER: If the query does not fit into product or billing issues.
    """
    PRODUCT_ISSUE = "product_issue"
    BILLING_ISSUE = "billing_issue"
    OTHER = "other"

class AnalyzeQuery(BaseTask):
    class AnalyzeResponseModel(BaseModel):
        intent: Categories
        reason: str = Field(description="The reason for selecting this category")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = "gpt-4o-2024-08-06"

    def analyze_query(self, query: str):
        choice = self.client.chat.completions.create(
            model=self.model,
            response_model=self.AnalyzeResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You're a helpful personal assistant that can classify incoming messages."},
                {"role": "user", "content": query },
            ],
            )
            
        return choice
    
    def execute(self, event: Event) -> Event:
        print("Analyzing issue...")
        issue_data = event.data
        result = self.analyze_query(issue_data['issue_description'])
        
        # Initialize nodes list if it doesn't exist
        if 'nodes' not in event.data:
            event.data['nodes'] = []
            
        # Add to nodes with AnalyzeQuery key
        event.data['nodes'].append({
            "AnalyzeQuery": result.model_dump()
        })
        
        # print(f"Analyzing issue with data: {issue_data}")
        return event

