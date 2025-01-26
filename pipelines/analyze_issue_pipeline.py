from core.pipeline import Pipeline
from tasks.analyze_query import AnalyzeQuery

def create_analyze_query_pipeline():
    pipeline = Pipeline()
    pipeline.add_task(AnalyzeQuery)
    return pipeline