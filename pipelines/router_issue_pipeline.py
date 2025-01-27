from core.pipeline import Pipeline
from tasks.router_issue_query import RouterQuery
from router_types.issue_types import IssueTypes  # Import the enum

def create_router_query_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(RouterQuery)
    pipeline.set_next_pipeline_options({
        IssueTypes.PRODUCT_ISSUE.value: "product_issue",
        IssueTypes.BILLING_ISSUE.value: "billing_issue",
        IssueTypes.OTHER.value: "default_issue"  # if you want a default pipeline
    })
    return pipeline