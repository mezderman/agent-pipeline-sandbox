from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor

class TaskResultEvent(BaseModel):
    name: str = "ProductIssue"
    processed: bool = True

class ProductIssue(BaseTask):

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = "gpt-4o-2024-08-06"
        self.response_model = create_model(
            'ResponseModel',
            processed=(bool, Field(description="Indicates if the product issue was processed"))
        )

       
    
    def execute(self, event: Event) -> Event:
        print("Analyzing Product issue...")
        issue_data = event.data
        
        task = TaskResultEvent()
        
        # Initialize nodes list if it doesn't exist
        if 'nodes' not in event.data:
            event.data['nodes'] = []
            
        event.data['nodes'].append(task.model_dump())
        
        # print(f"Analyzing issue with data: {issue_data}")
        return event

