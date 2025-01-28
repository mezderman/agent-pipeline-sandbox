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
    class PurchaseModel(BaseModel):
        item: str = Field(description="Name of the purchased item")
        date: str = Field(description="Purchase date in YYYY-MM-DD format")
        price: str = Field(description="Price of the item")
        description: str = Field(description="Detailed description of the item")
        
    class UserRecordResponseModel(BaseModel):
        purchases: List["GetUserRecord.PurchaseModel"] = Field(description="List of purchases made by the user")
        product_issues: List[str] = Field(description="List of product issues reported by the user")

        
    def get_mock_user_record(self, user_id: str) -> UserRecordResponseModel:
        """Create a mock user record for testing"""
        
        # Generate dates for the last 3 months
        today = datetime.now()
        three_months_ago = today - timedelta(days=90)
        
        mock_data = {
            'CUST-456': {
                'purchases': [
                    self.PurchaseModel(
                        item="Premium Plan Subscription",
                        date=(today - timedelta(days=30)).strftime('%Y-%m-%d'),
                        price="$99.99",
                        description="Annual subscription to the premium service plan with access to exclusive features and priority support."
                    ),
                    self.PurchaseModel(
                        item="Smart Device X-1000",
                        date=(today - timedelta(days=40)).strftime('%Y-%m-%d'),
                        price="$499.99",
                        description="High-performance smart device featuring voice recognition, AI-powered assistant, and home automation capabilities."
                    ),
                    self.PurchaseModel(
                        item="Extended Warranty",
                        date=(today - timedelta(days=41)).strftime('%Y-%m-%d'),
                        price="$59.99",
                        description="Two-year extended warranty for Smart Device X-1000 covering repairs and replacement for manufacturing defects."
                    )
                ],
                'product_issues': [
                    "Device connectivity issue (2024-02-15) - Resolved",
                    "Setup assistance request (2023-12-02) - Resolved"
                ]
            }
        }
        
        # Return mock data for the user, or empty data if user not found
        user_data = mock_data.get(user_id, {
            'purchases_summaries': [],
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

