from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor
from enum import Enum
from core.config import settings

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProductIssuePriority(BaseTask):
    class ProductResponseModel(BaseModel):
        priority: Priority
        reason: str = Field(description="The reason for selecting priority")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = settings.OPENAI_MODEL
       
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
        print("Analyzing product priority...")
        issue_data = event.data
        result = self.create_completion(issue_data['content'])
        
        # Add to nodes with ProductIssue key
        event.data['nodes']['ProductIssue'] = result.model_dump()
        
        return event

