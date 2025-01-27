from core.pipeline import Pipeline
from tasks.analyze_query import AnalyzeQuery

def create_analyze_query_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(AnalyzeQuery)
    pipeline.set_next_pipeline_options({
        "product_issue": "product_issue",
        "billing_issue": "billing_issue",
        "other": "default_issue"  # if you want a default pipeline
    })
    return pipeline