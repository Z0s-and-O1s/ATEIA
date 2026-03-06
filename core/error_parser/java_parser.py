def parse_java_error(error_text):

    if "java.lang" in error_text:
        language = "Java"
    else:
        language = "Java"

    if "NullPointerException" in error_text:
        error_type = "NullPointerException"
    elif "ArrayIndexOutOfBoundsException" in error_text:
        error_type = "ArrayIndexOutOfBoundsException"
    else:
        error_type = "Unknown"

    return {
        "language": language,
        "error_type": error_type
    }