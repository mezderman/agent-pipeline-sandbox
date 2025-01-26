from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class EventData(BaseModel):
    """Base model for event data"""
    nodes: List['EventData'] = Field(
        default_factory=list, 
        description="List of pipeline processing nodes"
    )

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

class AnalyzeIssueData(EventData):
    customer_id: str = Field(..., description="ID of the customer")
    issue_description: str = Field(..., description="Description of the issue")

class Event(BaseModel):
    event_key: str = Field(..., description="Key identifying the type of event")
    data: Dict[str, Any] = Field(default_factory=lambda: {"nodes": []})

    def get_validated_data(self) -> EventData:
        """Returns type-validated data based on event_key"""
        if self.event_key == "product_issue":
            return AnalyzeIssueData(**self.data)  # Strict validation
        elif self.event_key == "billing_issue":
            return BillingIssueData(**self.data)
        elif self.event_key == "analyze_issue":
            return AnalyzeIssueData(**self.data)
        return EventData(**self.data)  # Basic validation

class EventFactory:
    @staticmethod
    def create_event(event_key: str, data: Dict[str, Any]) -> Event:
        """Create and validate an event instance"""
        # Merge input data with EventData defaults
        base_data = EventData().model_dump()
        base_data.update(data)
        
        event = Event(event_key=event_key, data=base_data)
        # Validate the data based on event type
        event.get_validated_data()
        return event