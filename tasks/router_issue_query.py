from tasks.base_task import BaseTask
from core.event import Event
from pydantic import BaseModel, Field
from openai import OpenAI
import instructor
from core.config import settings
from router_types.issue_types import IssueTypes

class RouterQuery(BaseTask):
    class RouterResponseModel(BaseModel):
        intent: IssueTypes
        reason: str = Field(description="The reason for selecting this category")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = settings.OPENAI_MODEL

    def create_completion(self, query: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_model=self.RouterResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You're a helpful personal assistant that can classify incoming messages."},
                {"role": "user", "content": query },
            ],
            )
            
        return completion
    
    def execute(self, event: Event) -> Event:
        print("Routing issue to the right department...")
        issue_data = event.data
        result = self.create_completion(issue_data['issue_description'])
        
        # Initialize nodes dict if it doesn't exist
        if 'nodes' not in event.data:
            event.data['nodes'] = {}
            
        # Add to nodes with RouterQuery key
        event.data['nodes']['RouterQuery'] = result.model_dump()
        
        return event

