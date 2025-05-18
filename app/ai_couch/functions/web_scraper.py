from time import sleep

import requests
from bs4 import BeautifulSoup
from rich import print

from app.agents import analyze, summarizer
from app.config import config


def scraper(list_of_links: list[str], prompt: str, plan: str) -> list[str]:
    """Функция для парсинга и комплексной обработки данных из Интернета

    Args:
        list_of_links (list[str]): Список ссылок, которые нужно пропарсить и обработать.
        prompt (str): Тема курса для проверки пунктов на нужность.
        plan (str): План курса для дополнительной проверки.

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
        print(f"[yellow] * Data from {link} parsed successfully![/yellow]")
        return data

    list_of_processed_data = []
    for link in list_of_links:
        try:
            data = pars_data(
                link=link,
                BS4_CLASS=config.BS4_CLASS,
            )
            if analyze(
                data=data,
                prompt=prompt,
                plan=plan,
            ):
                sleep(1)
                list_of_processed_data.append(
                    summarizer(
                        data=data,
                        prompt=prompt,
                        plan=plan,
                    )
                )
                print(
                    f"[green] * Data from {link} summarized successfully![/green]"
                )
            else:
                print(f"[cyan] * {link} skipped.[cyan]")
        except Exception as e:
            print(
                f"[red] * Во время парсинга данных с {link} была вызвана ошибка: {e}[/red]"
            )
    print("[green] * All data is scraped successfully![/green]")
    return list_of_processed_data
