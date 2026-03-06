def generate_context_request(language, error_type):

    if language == "Python":

        if error_type == "NameError":
            return (
                "This usually happens when a variable is used before being defined.\n"
                "Please paste the code where the variable is referenced."
            )

        elif error_type == "TypeError":
            return (
                "This occurs when incompatible data types are used together.\n"
                "Please paste the code around the operation causing this error."
            )

        elif error_type == "SyntaxError":
            return (
                "This indicates a mistake in code structure.\n"
                "Please paste the code around the line where the error occurs."
            )

        else:
            return "Please paste the relevant section of your code."

    if language == "Java":

        if error_type == "NullPointerException":
            return (
                "This happens when an object reference is null.\n"
                "Please paste the code where this object is used."
            )

    if language == "JavaScript":

        if error_type == "ReferenceError":
            return (
                "This occurs when a variable is used before being defined.\n"
                "Please paste the code where the variable appears."
            )

    return "Please paste the relevant section of your code."