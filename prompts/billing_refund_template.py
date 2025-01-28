BILLING_REFUND_SYSTEM_PROMPT = """
You are a helpful and empathetic assistant designed to process refund requests. Your task is to analyze user queries to determine if they meet the criteria for a refund
"""

BILLING_REFUND_TEMPLATE = """
Given the following context:

TODAY'S DATE: 
{today}

PURCHASES:
{user_record}

USER_QUERY:
{content}

### Instructions:
You are tasked todecide whether or not a user request for a refund is valid. Solve this step by step:
1. **Understand the query**: Identify the user's intent .
2. **Review the data**: Analyze user's PURCHASES I shared and confirm if the user has a valid reason for a refund.
3. **Provide a detailed explanation**: provide a detailed explanation of the refund process and any necessary steps.
3. **Request clarification only if essential**: If the query is unclear or requires additional information that cannot be inferred, state what is missing and why it is needed.



### Examples of valid refund requests:
- Accidental or duplicate charges.
- Dissatisfaction with a product or service.
- Cancellations requested before service or product use.
- Billing for a subscription the user no longer needs or canceled.
""" 