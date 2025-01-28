from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from openai import OpenAI
import instructor
from enum import Enum
from core.config import settings
from typing import List
from datetime import datetime
from prompts.billing_summary_template import BILLING_SUMMARY_TEMPLATE, BILLING_SUMMARY_SYSTEM_PROMPT
from prompts.billing_refund_template import BILLING_REFUND_TEMPLATE, BILLING_REFUND_SYSTEM_PROMPT

class Categories(str, Enum):
    """Enumeration of categories that can be used to resolve billing issues.
    - SEND_EMAIL: Respond to user by email.
    - MORE_INFO: We dont have enough information to resolve the issue.
    - NO_ACTION_NEEDED: No action needed.
    """
    SEND_EMAIL = "send_email"
    REFUND = "refund"
    MORE_INFO = "more_info"
    NO_ACTION_NEEDED = "no_action_needed"

class BillingIssueResolution(BaseTask):
    class BillingIssueResolutionResponseModel(BaseModel):
        categories: Categories
        reason: str = Field(description="The reason for selecting a category. If you need more information, say what information you are missing")

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = settings.OPENAI_MODEL
        self.prompt_template = """"""
        self.system_prompt = """"""


    def create_completion(self, prompt: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_model=self.BillingIssueResolutionResponseModel,
            max_retries=1, 
            messages=[
                {"role": "system", "content":self.system_prompt},
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
                self.system_prompt = BILLING_SUMMARY_SYSTEM_PROMPT
                self.prompt_template = BILLING_SUMMARY_TEMPLATE

            case "refund":
                self.system_prompt = BILLING_REFUND_SYSTEM_PROMPT
                self.prompt_template = BILLING_REFUND_TEMPLATE
    
            case _:  # Default case
                self.system_prompt = BILLING_SUMMARY_SYSTEM_PROMPT
                self.prompt_template = BILLING_SUMMARY_TEMPLATE
                
        prompt = self.prompt_template.format(
                    content=event.data['content'],
                    user_record=user_record,
                    today=today
                )
        result = self.create_completion(prompt)
        
        # Add to nodes
        event.data['nodes']['BillingIssueResolution'] = result.model_dump()
        
        return event

