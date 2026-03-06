from core.error_parser.python_parser import parse_python_error
from core.error_parser.java_parser import parse_java_error
from core.error_parser.js_parser import parse_js_error
from core.error_parser.cpp_parser import parse_cpp_error


def detect_language_and_parse(error_text):

    if (
        "Traceback" in error_text
        or "TypeError" in error_text
        or "NameError" in error_text
        or "SyntaxError" in error_text
        or "IndentationError" in error_text
    ):
        return parse_python_error(error_text)

    elif "java.lang" in error_text or ".java" in error_text:
        return parse_java_error(error_text)

    elif ".js" in error_text or "ReferenceError" in error_text:
        return parse_js_error(error_text)

    elif ".cpp" in error_text or ".c:" in error_text:
        return parse_cpp_error(error_text)

    else:
        return {
            "language": "Unknown",
            "error_type": "Unknown"
        }