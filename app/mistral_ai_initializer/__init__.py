# Deprecated
from dotenv import dotenv_values

from app.mistral_ai_initializer.mistral_custom_class import ModifiedMistral


def mistral_ai_initializer() -> ModifiedMistral:
    """Create and return Mistral AI client.

    Returns:
        ModifiedMistral: returns client
    """
    api_key = dotenv_values(".env")["MISTRAL_AI_API_KEY"]
    client = ModifiedMistral(api_key=api_key)
    return client
