# A base class for API providers, defining the interface and common properties for subclasses.


class BaseAPIProvider:
    MODELS = {}

    def __init__(self):
        self.api_key: str

    def set_model(self, model_name: str):
        raise NotImplementedError("Subclass must implement set_model")

    def get_models(self) -> dict:
        raise NotImplementedError("Subclass must implement get_model")

    def generate_response(prompt: str) -> str:
        raise NotImplementedError("Subclass must implement generate_response")
