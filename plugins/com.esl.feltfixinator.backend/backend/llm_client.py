class LLMClient:
    def __init__(self, model_id=None):
        self.model_id = model_id

    def generate_fix(self, code, violations):
        return code

    def test_connection(self):
        return True
