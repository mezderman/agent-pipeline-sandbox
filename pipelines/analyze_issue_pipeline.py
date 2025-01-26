from core.pipeline import Pipeline
from tasks.analyze_query import analyze_query

def create_analyze_query_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(analyze_query)
    return pipeline