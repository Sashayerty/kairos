import openai


class ModifiedOpenai(openai.OpenAI):
    """Модифицированный класс openai.OpenAI. Добавлена функция message."""

    def message(
        self,
        messages: list,
        model: str,
        response_format: dict[str, str] | openai.NotGiven = openai.NOT_GIVEN,
        timeout: float | openai.NotGiven = openai.NOT_GIVEN,
        temperature: float | openai.NotGiven = 0.7,
    ) -> str:
        result = self.chat.completions.create(
            model=model,
            response_format=response_format,
            temperature=temperature,
            messages=messages,
            timeout=timeout,
        )
        return result.choices[0].message.content
