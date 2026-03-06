STAGE_AWAITING_ERROR = "AWAITING_ERROR"
STAGE_AWAITING_CODE = "AWAITING_CODE"
STAGE_READY_FOR_ANALYSIS = "READY_FOR_ANALYSIS"


class ConversationManager:

    def __init__(self):
        self.stage = STAGE_AWAITING_ERROR
        self.error_message = None
        self.code_snippet = None

    def receive_error(self, error_text):
        self.error_message = error_text
        self.stage = STAGE_AWAITING_CODE
        return "Error received. Please paste the relevant code."

    def receive_code(self, code_text):
        self.code_snippet = code_text
        self.stage = STAGE_READY_FOR_ANALYSIS
        return "Code received. Ready to analyze."

    def get_stage(self):
        return self.stage