from core.registry import PipelineRegistry
from pipelines.router_issue_pipeline import create_router_query_pipeline
from pipelines.product_issue_pipeline import create_product_issue_pipeline
from pipelines.billing_issue_pipeline import create_billing_issue_pipeline
def register_all_pipelines():
    # Register each pipeline with its event key
    PipelineRegistry.register_pipeline("product_issue", create_product_issue_pipeline())
    PipelineRegistry.register_pipeline("billing_issue", create_billing_issue_pipeline())
    PipelineRegistry.register_pipeline("router_query", create_router_query_pipeline())
