from tasks.base_task import BaseTask
from pydantic import BaseModel, Field
from core.event import Event
from pydantic import Field, create_model
from openai import OpenAI
import instructor
from enum import Enum
from core.config import settings
from datetime import datetime, timedelta
from typing import List




class GetUserRecord(BaseTask):
    class UserRecordResponseModel(BaseModel):
        purchases: List[str] = Field(description="List of purchases made by the user")
        billing_history: List[str] = Field(description="List of billing history for the user")
        product_issues: List[str] = Field(description="List of product issues reported by the user")

        
    def get_mock_user_record(self, user_id: str) -> UserRecordResponseModel:
        """Create a mock user record for testing"""
        
        # Generate dates for the last 3 months
        today = datetime.now()
        three_months_ago = today - timedelta(days=90)
        
        mock_data = {
            'CUST-456': {
                'purchases': [
                    "Premium Plan Subscription (2024-01-15)",
                    "Smart Device X-1000 (2023-12-01)",
                    "Extended Warranty (2023-12-01)"
                ],
                'billing_history': [
                    f"$29.99 - Monthly subscription ({(today - timedelta(days=0)).strftime('%Y-%m-%d')})",
                    f"$29.99 - Monthly subscription ({(today - timedelta(days=30)).strftime('%Y-%m-%d')})",
                    f"$29.99 - Monthly subscription ({(today - timedelta(days=60)).strftime('%Y-%m-%d')})",
                    "$299.99 - Smart Device X-1000 (2023-12-01)"
                ],
                'product_issues': [
                    "Device connectivity issue (2024-02-15) - Resolved",
                    "Setup assistance request (2023-12-02) - Resolved"
                ]
            }
        }
        
        # Return mock data for the user, or empty data if user not found
        user_data = mock_data.get(user_id, {
            'purchases': [],
            'billing_history': [],
            'product_issues': []
        })
        
        return self.UserRecordResponseModel(**user_data)
    
    def execute(self, event: Event) -> Event:
        print("Getting user record...")
        user_id = event.data['user_id']
        result = self.get_mock_user_record(user_id)
        
        # Add to nodes with UserRecord key
        event.data['nodes']['UserRecord'] = result.model_dump()
        
        return event

