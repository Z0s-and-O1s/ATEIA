def parse_js_error(error_text):

    language = "JavaScript"

    if "ReferenceError" in error_text:
        error_type = "ReferenceError"
    elif "TypeError" in error_text:
        error_type = "TypeError"
    else:
        error_type = "Unknown"

    return {
        "language": language,
        "error_type": error_type
    }