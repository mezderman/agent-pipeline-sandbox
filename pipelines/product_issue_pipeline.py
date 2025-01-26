from core.pipeline import Pipeline
from tasks.product_issue import ProductIssue

def create_product_issue_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(ProductIssue)
    return pipeline