from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor
from enum import Enum

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProductIssue(BaseTask):
    class ProductResponseModel(BaseModel):
        priority: Priority
        reason: str = Field(description="The reason for selecting priority")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = "gpt-4o-2024-08-06"
       
    def create_completion(self, query: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_model=self.ProductResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You're a helpful personal assistant that can prioritize product issue."},
                {"role": "user", "content": query },
            ],
            )
            
        return completion
    
    def execute(self, event: Event) -> Event:
        print("Analyzing Product issue...")
        issue_data = event.data
        result = self.create_completion(issue_data['issue_description'])
        
        # Add to nodes with ProductIssue key
        event.data['nodes'].append({
            "ProductIssue": result.model_dump()
        })
        
        return event

