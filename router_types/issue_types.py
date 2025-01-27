from enum import Enum

class IssueTypes(str, Enum):
    """Enumeration of categories for incoming queries.
    - PRODUCT_ISSUE: If the query relates to a problem with a product.
    - BILLING_ISSUE: If the query relates to a billing or payment issue.
    - OTHER: If the query does not fit into product or billing issues.
    """
    PRODUCT_ISSUE = "product_issue"
    BILLING_ISSUE = "billing_issue"
    OTHER = "other" 