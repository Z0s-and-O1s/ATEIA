def parse_cpp_error(error_text):

    language = "C/C++"

    if "expected" in error_text:
        error_type = "SyntaxError"
    else:
        error_type = "Unknown"

    return {
        "language": language,
        "error_type": error_type
    }