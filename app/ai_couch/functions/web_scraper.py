from time import sleep

import requests
from bs4 import BeautifulSoup

from app.ai_core import analyze, summarizer
from app.config import config


def scraper(
    list_of_links: list[str], prompt: str, plan_of_course: str
) -> list[str]:
    """Функция для парсинга и комплексной обработки данных из Интернета

    Args:
        list_of_links (list[str]): Список ссылок, которые нужно пропарсить и обработать.
        prompt (str): Тема курса для проверки пунктов на нужность.
        plan_of_course (str): План курса для дополнительной проверки.

    Returns:
        list[str]: Список обработанных данных по каждой ссылке.
    """

    def pars_data(
        link: str, class_of_element: str = config.class_of_element
    ) -> str:
        # flake8: noqa
        """Функция для парсинга данных

        Args:
            link (str): Ссылка, которую нужно пропарсить.
            class_of_element (str, optional): Элемент, из которого извлекать данные на странице. Defaults to config.class_of_element.

        Returns:
            str: Данные с страницы.
        """
        row_data = requests.get(url=link)
        bs4 = BeautifulSoup(
            row_data.text,
            "lxml",
        )
        data = bs4.find_all(name=class_of_element)
        print(f" * Data from {link} parsed successfully!")
        return data

    list_of_processed_data = []
    for link in list_of_links:
        try:
            data = pars_data(
                link=link,
            )
            if analyze(
                data_from_internet=data,
                prompt=prompt,
                plan_of_course=plan_of_course,
            ):
                sleep(1)
                list_of_processed_data.append(
                    summarizer(
                        data=data,
                        prompt=prompt,
                        plan_of_course=plan_of_course,
                    )
                )
                print(f" * Data from {link} summarized successfully!")
            else:
                print(f" * {link} skipped.")
        except Exception as e:
            print(
                f" * Во время парсинга данных с {link} была вызвана ошибка: {e}"
            )
    print(" * All data is scraped successfully!")
    return list_of_processed_data
