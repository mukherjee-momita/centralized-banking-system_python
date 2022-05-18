class ApplicationError(Exception):

    def __init__(self, code, message):
        self.error_code = code
        self.error_message = message
        super().__init__(code, message)
