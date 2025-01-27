from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor
from enum import Enum
from core.config import settings

class Categories(str, Enum):
    """
    Enumeration of categories for incoming customer queries.
    - OPERATIONAL_ISSUE: Issues related to understanding or using the product.
    - TECHNICAL_MALFUNCTION: Issues related to product malfunctions or defects.
    - WARRANTY: Queries related to warranty coverage or claims.
    - USER_ERROR: Issues caused by user mistakes or improper usage.
    - OTHERS: General queries or issues that do not fit into other categories.
    """
    OPERATIONAL_ISSUE = "operational_issue"
    TECHNICAL_MALFUNCTION = "technical_malfunction"
    WARRANTY = "warranty"
    USER_ERROR = "user_error"
    OTHERS = "others"



class ProductIssueType(BaseTask):
    class ProductIssueTypeResponseModel(BaseModel):
        issue_type: Categories
        reason: str = Field(description="The reason for selecting this category")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = settings.OPENAI_MODEL
       
    def create_completion(self, query: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_model=self.ProductIssueTypeResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant. Your task is to analyze the user's query and classify it into one of the categories types"},
                {"role": "user", "content": query },
            ],
            )
            
        return completion
    
    def execute(self, event: Event) -> Event:
        print("Analyzing Product issue type...")
        issue_data = event.data
        result = self.create_completion(issue_data['issue_description'])
        
        # Add to nodes with ProductIssue key
        event.data['nodes']['ProductIssueType'] = result.model_dump()
        
        return event

