def parse_python_error(error_text):

    if "Traceback" in error_text:
        language = "Python"
    else:
        language = "Python"

    if "TypeError" in error_text:
        error_type = "TypeError"
    elif "NameError" in error_text:
        error_type = "NameError"
    elif "SyntaxError" in error_text:
        error_type = "SyntaxError"
    elif "IndentationError" in error_text:
        error_type = "IndentationError"
    else:
        error_type = "Unknown"

    return {
        "language": language,
        "error_type": error_type
    }