from mistralai import Mistral


class ModifiedMistral(Mistral):

    def message(
        self,
        messages: list[dict],
        temperature: int | float = None,
        response_format: dict = None,
        model: str = "mistral-large-latest",
    ) -> str:
        """Send message to model

        Args:
            messages (list[dict]): List of messages to model
            temperature (int | float, optional): 1 - more random, 0 - no random, 0.5 - between. Defaults to None.
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
        )
        return self.result.choices[0].message.content
