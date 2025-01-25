from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class EventData(BaseModel):
    """Base model for event data"""
    pass

class ProductIssueData(EventData):
    product_id: str = Field(..., description="ID of the product with issue")
    customer_id: str = Field(..., description="ID of the customer reporting the issue")
    issue_description: str = Field(..., description="Description of the product issue")
    severity: str = Field(..., description="Severity level of the issue")

class BillingIssueData(EventData):
    customer_id: str = Field(..., description="ID of the customer with billing issue")
    amount: float = Field(..., description="Amount involved in the billing issue")
    issue_type: str = Field(..., description="Type of billing issue")
    description: Optional[str] = Field(None, description="Detailed description of the billing issue")

class Event(BaseModel):
    event_key: str = Field(..., description="Key identifying the type of event")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")

    def get_validated_data(self) -> EventData:
        """Returns type-validated data based on event_key"""
        if self.event_key == "product_issue":
            return ProductIssueData(**self.data)
        elif self.event_key == "billing_issue":
            return BillingIssueData(**self.data)
        return EventData(**self.data)

class EventFactory:
    @staticmethod
    def create_event(event_key: str, data: Dict[str, Any]) -> Event:
        """Create and validate an event instance"""
        event = Event(event_key=event_key, data=data)
        # Validate the data based on event type
        event.get_validated_data()
        return event