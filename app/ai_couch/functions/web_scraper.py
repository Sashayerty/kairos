from time import sleep

import colorama
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

    def pars_data(link: str, BS4_CLASS: str) -> str:
        # flake8: noqa
        """Функция для парсинга данных

        Args:
            link (str): Ссылка, которую нужно пропарсить.
            BS4_CLASS (str, optional): Элемент, из которого извлекать данные на странице.

        Returns:
            str: Данные с страницы.
        """
        row_data = requests.get(url=link)
        bs4 = BeautifulSoup(
            row_data.text,
            "lxml",
        )
        data = bs4.find_all(name=BS4_CLASS)
        print(
            colorama.Fore.YELLOW + f" * Data from {link} parsed successfully!"
        )
        return data

    list_of_processed_data = []
    for link in list_of_links:
        try:
            data = pars_data(
                link=link,
                BS4_CLASS=config.BS4_CLASS,
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
                print(
                    colorama.Fore.GREEN
                    + f" * Data from {link} summarized successfully!"
                )
            else:
                print(colorama.Fore.CYAN + f" * {link} skipped.")
        except Exception as e:
            print(
                colorama.Fore.RED
                + f" * Во время парсинга данных с {link} была вызвана ошибка: {e}"
            )
    print(colorama.Fore.GREEN + " * All data is scraped successfully!")
    return list_of_processed_data
