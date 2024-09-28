# A base class for API providers, defining the interface and common properties for subclasses.


class BaseAPIProvider(object):
    def set_model(self, model_name: str):
        raise NotImplementedError("Subclass must implement set_model")

    def get_models(self) -> dict:
        raise NotImplementedError("Subclass must implement get_models")

    def generate_response(self, prompt: str, system_content: str) -> str:
        raise NotImplementedError("Subclass must implement generate_response")
