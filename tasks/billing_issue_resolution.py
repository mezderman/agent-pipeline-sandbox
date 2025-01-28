from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from openai import OpenAI
import instructor
from enum import Enum
from core.config import settings
from typing import List

class Categories(str, Enum):
    COMPLETED = "completed"
    HUMAN_IN_LOOP = "human_in_loop"
    NO_ACTION_NEEDED = "no_action_needed"

class BillingIssueResolution(BaseTask):
    class BillingIssueResolutionResponseModel(BaseModel):
        resolution: str = Field(description="The resolution to the billing issue")
        email_response: str = Field(description="The email response to the user")
        category: Categories = Field(description="The category of the resolution")
        next_steps: List[str] = Field(description="List of recommended next steps")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = settings.OPENAI_MODEL
        self.prompt_template = """
Summarize the last 3 months of billing history and purchases.

USER INFORMATION:
{user_record}

Write an emailresponse to user query {content}. Please ensure your response is professional and empathetic.
"""

    def create_completion(self, prompt: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_model=self.BillingIssueResolutionResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You're a helpful billing support assistant that resolves billing issues."},
                {"role": "user", "content": prompt},
            ],
        )
        return completion

    def execute(self, event: Event) -> Event:
        print("Resolving billing issue...")
        
        # Get user data and billing history
        user_record = event.data['nodes'].get('UserRecord', {})
        
        # Format the prompt with user data
        prompt = self.prompt_template.format(
            content=event.data['content'],
            user_record=user_record  # Pass the user_record dict directly
        )
        
        # Get resolution
        result = self.create_completion(prompt)
        
        # Add to nodes
        event.data['nodes']['BillingIssueResolution'] = result.model_dump()
        
        return event

