from core.pipeline import Pipeline
from tasks.product_issue import ProductIssue
from tasks.product_issue_type import ProductIssueType

def create_product_issue_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(ProductIssue)
    pipeline.add_task(ProductIssueType)
    return pipeline