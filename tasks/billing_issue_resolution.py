from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from openai import OpenAI
import instructor
from enum import Enum
from core.config import settings
from typing import List
from datetime import datetime

class Categories(str, Enum):
    """Enumeration of categories that can be used to resolve billing issues.
    - SEND_EMAIL: Respond to user by email.
    - MORE_INFO: We dont have enough information to resolve the issue.
    - NO_ACTION_NEEDED: No action needed.
    """
    SEND_EMAIL = "send_email"
    MORE_INFO = "more_info"
    NO_ACTION_NEEDED = "no_action_needed"

class BillingIssueResolution(BaseTask):
    class BillingIssueResolutionResponseModel(BaseModel):
        categories: Categories
        reason: str = Field(description="The reason for selecting a category. If you need more information, say what information you are missing")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = settings.OPENAI_MODEL
        self.prompt_template = """
            Given the following context:\n
            TODAY'S DATE: 
            {today}
            
            ISSUE_DISCOVERY:
            {user_record}

            USER_QUERY:
            {content}

            Recommend the appropriate action to take to resolve the issue from available categories.
            Solve it step by step:
            1. Identify the issue
            2. Make sure you have enough information to summarize for the timeframe requested
            3. Recommend the appropriate action
            4. Provide a reason for the action
        """

    def create_completion(self, prompt: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_model=self.BillingIssueResolutionResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes user queries and context to recommend actions. Based on the provided data, suggest one action only"},
                {"role": "user", "content": prompt},
            ],
        )
        return completion

    def execute(self, event: Event) -> Event:
        print("Resolving billing issue...")
        
        # Get user data and billing history
        user_record = event.data['nodes'].get('UserRecord', {})
        category = event.data['nodes'].get('BillingIssue', {}).get('category', '')
        today = datetime.now().strftime('%Y-%m-%d')
        match category:
            case "summary":
                prompt = self.prompt_template.format(
                    content=event.data['content'],
                    user_record=user_record,
                    today=today
                )
            case _:  # Default case
                prompt = self.prompt_template.format(
                    content=event.data['content'],
                    user_record=user_record,
                    today=today
                )
        
        # Get resolution
        result = self.create_completion(prompt)
        
        # Add to nodes
        event.data['nodes']['BillingIssueResolution'] = result.model_dump()
        
        return event

