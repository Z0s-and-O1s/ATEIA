def generate_explanation(error, code):

    explanation = f"""
Error Analysis

Error:
{error}

Code:
{code}

Possible Explanation:
The error occurs because the code is using something incorrectly.

Suggested Fix:
Review the variable definitions, data types, or syntax around the error location.
"""

    return explanation