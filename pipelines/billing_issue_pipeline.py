from core.pipeline import Pipeline
from tasks.billing_issue.analyze_billing import analyze_billing_issue
from tasks.billing_issue.check_records import check_billing_records

def create_billing_issue_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(analyze_billing_issue).add_task(check_billing_records)
    return pipeline
