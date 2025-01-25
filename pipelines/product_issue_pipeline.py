from core.pipeline import Pipeline
from tasks.product_issue.analyze_product import analyze_product_issue
from tasks.product_issue.check_records import check_product_records

def create_product_issue_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(analyze_product_issue).add_task(check_product_records)
    return pipeline
