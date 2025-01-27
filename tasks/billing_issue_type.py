from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor
from enum import Enum
from core.config import settings

class Categories(str, Enum):
    REFUND = "refund"
    SUMMARY = "summary"
    OTHER = "other"


class BillingIssue(BaseTask):
    class BillingIssueResponseModel(BaseModel):
        categories: Categories
        reason: str = Field(description="The reason for selecting a category")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = settings.OPENAI_MODEL
       
    def create_completion(self, query: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_model=self.BillingIssueResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You're a helpful assistant that classifies billing-related queries into one  categories"},
                {"role": "user", "content": query },
            ],
            )
            
        return completion
    
    def execute(self, event: Event) -> Event:
        print("Analyzing Billing issue...")
        issue_data = event.data
        result = self.create_completion(issue_data['content'])
        
        # Add to nodes with ProductIssue key
        event.data['nodes']['BillingIssue'] = result.model_dump()
        
        return event

