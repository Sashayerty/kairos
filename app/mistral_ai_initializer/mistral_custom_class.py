from mistralai import Mistral


class ModifiedMistral(Mistral):
    """Создал кастомный класс для того, чтобы по вызову одной функции взаимодействовать с llm."""

    def message(
        self,
        messages: list[dict],
        temperature: int | float = None,
        response_format: dict = None,
        model: str = "mistral-large-latest",
        timeout: int = 300000,
    ) -> str:
        """Send message to model

        Args:
            messages (list[dict]): List of messages to model
            temperature (int | float, optional): 1 - more random, 0 - no random, 0.5 - between. Defaults to None.
            timeout (int, optional): Timeout of response in ms. Defaults to None.
            response_format (dict, optional): Format of response. May be json or else. Defaults to None.
            model (str, optional): Model to use. Defaults to "mistral-large-latest".


        Returns:
            str: Response from model.
        """
        self.result = self.chat.complete(
            model=model,
            response_format=response_format,
            temperature=temperature,
            messages=messages,
            timeout_ms=timeout,
        )
        return self.result.choices[0].message.content
