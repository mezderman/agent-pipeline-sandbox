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
            Given the following context:

            TODAY'S DATE: 
            {today}

            PURCHASES:
            {user_record}

            USER_QUERY:
            {content}

            ### Instructions:
            You are tasked with resolving the user's query by analyzing the provided data. Interpret time references date and provide a response accordingly. Solve this step by step:
            1. **Understand the query**: Identify the user's intent and resolve ambiguous time reference.
            2. **Review the data**: Analyze the records in PURCHASES SUMMARY that match the query, focusing on relevant purchases or issues.
            3. **Extract relevant details**: 
                - For purchases: Include item names, prices, purchase dates, and descriptions for the specified time frame.
            5. **Request clarification only if essential**: If the query is unclear or requires additional information that cannot be inferred, state what is missing and why it is needed.


            ### Example:
            If the query asks for "a summary of bills for December 2024," include:
            - A list of purchases from December 2024 with item names, dates, prices, and descriptions.
            - Any other relevant context (e.g., issues related to those purchases).
            - Reasons why some details might not be available, if applicable.
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

