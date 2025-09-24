from app.services.groq_llm_service import GroqClient
from app.services.local_llm_service import LocalOllamaClient
from app.services.openai_llm_service import OpenAIClien


class LLMFactory():
    @staticmethod
    def create_client(
            client_name: str,
            image_analize_model: str = None,
            text_generate_model: str = None,
            stream_mode: bool = None
    ):
        if client_name == "ollama":
            return LocalOllamaClient(image_analize_model, text_generate_model, stream_mode)
        elif client_name == "groq":
            return GroqClient(image_analize_model, text_generate_model, stream_mode)
        elif client_name == "openai":
            return OpenAIClien(image_analize_model, text_generate_model, stream_mode)