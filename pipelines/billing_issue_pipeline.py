from core.pipeline import Pipeline
from tasks.billing_issue_type import BillingIssue
from tasks.get_user_record import GetUserRecord
from tasks.billing_issue_resolution import BillingIssueResolution

def create_billing_issue_pipeline():
    pipeline = Pipeline(name="Billing Issue")
    pipeline.add_task(BillingIssue)
    pipeline.add_task(GetUserRecord)
    pipeline.add_task(BillingIssueResolution)
    return pipeline
