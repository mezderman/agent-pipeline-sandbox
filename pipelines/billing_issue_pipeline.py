from core.pipeline import Pipeline
from tasks.billing_issue_type import BillingIssue

def create_billing_issue_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(BillingIssue)
    return pipeline