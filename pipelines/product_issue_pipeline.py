from core.pipeline import Pipeline
from tasks.product_issue_priority import ProductIssuePriority
from tasks.product_issue_type import ProductIssueType

def create_product_issue_pipeline():
    pipeline = Pipeline(name="Product Issue")
    pipeline.add_task(ProductIssueType)
    pipeline.add_task(ProductIssuePriority)
    return pipeline