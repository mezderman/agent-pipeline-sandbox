from core.pipeline import Pipeline
from tasks.router_issue_query import RouterQuery

def create_router_query_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(RouterQuery)
    pipeline.set_next_pipeline_options({
        "product_issue": "product_issue",
        "billing_issue": "billing_issue",
        "other": "default_issue"  # if you want a default pipeline
    })
    return pipeline