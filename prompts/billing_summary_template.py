
BILLING_SUMMARY_SYSTEM_PROMPT = """
You are an assistant that analyzes user queries and context to recommend actions. Based on the provided data, suggest one action only
"""

BILLING_SUMMARY_TEMPLATE = """
Given the following context:

TODAY'S DATE: 
{today}

PURCHASES:
{user_record}

USER_QUERY:
{content}

### Instructions:
You are tasked with resolving the user's query by analyzing the provided data. Interpret time references date and provide a response accordingly. Solve this step by step:
1. **Understand the query**: Identify the user's intent and resolve ambiguous time reference.
2. **Review the data**: Analyze the records in PURCHASES that match the query, focusing on relevant purchases or issues.
3. **Extract relevant details**: 
    - For purchases: Include item names, prices, purchase dates, and descriptions for the specified time frame.
5. **Request clarification only if essential**: If the query is unclear or requires additional information that cannot be inferred, state what is missing and why it is needed.


### Example:
If the query asks for "a summary of bills for December 2024," include:
- A list of purchases from December 2024 with item names, dates, prices, and descriptions.
- Any other relevant context (e.g., issues related to those purchases).
- Reasons why some details might not be available, if applicable.
""" 