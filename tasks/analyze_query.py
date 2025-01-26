from tasks.base_task import BaseTask
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor
from enum import Enum

class AnalyzeQuery(BaseTask):
    class Categories(str, Enum):
        """Enumeration of categories for incoming query.
        Pick specific if the query seeks detailed or pinpointed information
        Pick summary if the query seeks a broad overview or general understanding
        Pick other if the query if doesnt fit into specific or summary
        """
        SPECIFIC = "specific"
        SUMMARY = "summary"
        OTHER = "other"

    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.model = "gpt-4o-2024-08-06"

        self.response_model = create_model(
            'Choice',
            category=(self.Categories, ...),
            reason=(str, Field(description="The reason for selecting this category"))
        )
       
        
    def route(self, query: str):
       
        choice = self.client.chat.completions.create(
            model=self.model,
            response_model=self.response_model,
            max_retries=1, 
            messages=[
                {"role": "system", "content": "You're a helpful personal assistant that can classify incoming messages."},
                {"role": "user", "content": query },
            ],
            )
            
        return choice
    
    def execute(self, event: Event) -> Event:
        print("Analyzing issue...")
        # Access the event data
        issue_data = event.data
        result = self.route(issue_data['issue_description'])
        print(result)
        print(f"Analyzing issue with data: {issue_data}")
        
        # You can modify the data or add validation results
        event.data['validation_passed'] = True
        event.data['validation_timestamp'] = '2024-03-21'  # example
        
        return event 

