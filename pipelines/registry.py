from core.registry import PipelineRegistry
from pipelines.analyze_issue_pipeline import create_analyze_query_pipeline
def register_all_pipelines():
    # Register each pipeline with its event key
    # PipelineRegistry.register_pipeline("product_issue", create_product_issue_pipeline())
    # PipelineRegistry.register_pipeline("billing_issue", create_billing_issue_pipeline())
    PipelineRegistry.register_pipeline("analyze_query", create_analyze_query_pipeline())
