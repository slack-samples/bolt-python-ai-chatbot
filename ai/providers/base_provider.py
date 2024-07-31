class BaseProvider:
    MODELS = {}
    BASELINE_MAX_TOKENS: int
    API_NAME: str

    def __init__(self):
        self.current_model = None
        self.api_key: str

    def set_model(self, model_name: str):
        raise NotImplementedError("Subclass must implement set_model")

    def get_models(self):
        raise NotImplementedError("Subclass must implement get_model")

    def generate_response(prompt: str) -> str:
        raise NotImplementedError("Subclass must implement generate_response")
