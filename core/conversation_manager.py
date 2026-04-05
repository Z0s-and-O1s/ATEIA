class ConversationManager:
    def __init__(self):
        self.stage = "AWAITING_ERROR"
        self.error_message = None
        self.code_snippet = None

    def get_stage(self):
        return self.stage

    def receive_error(self, message):
        self.error_message = message
        self.stage = "AWAITING_CODE"

    def receive_code(self, code):
        self.code_snippet = code
        self.stage = "DONE"

    def reset(self):
        self.stage = "AWAITING_ERROR"
        self.error_message = None
        self.code_snippet = None