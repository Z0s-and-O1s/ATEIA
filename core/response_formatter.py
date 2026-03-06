def format_debug_response(language, error_type, explanation):

    response = f"""
Error Detected
--------------

Language: {language}
Error Type: {error_type}

Explanation
-----------

{explanation}

Next Step
---------

Review the code and apply the suggested fix.
"""

    return response