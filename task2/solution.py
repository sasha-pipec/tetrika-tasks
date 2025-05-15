import csv
from typing import Union
from collections import defaultdict

import requests


class WikipediaClient:
    BASE_API_URL = "https://ru.wikipedia.org/w/api.php"

    def request(self, method: str, params: dict[str, str]) -> dict[str, str]:
        return self._make_response(
            response=self._make_request(
                method=method, url=self.BASE_API_URL, params=params
            )
        )

    @staticmethod
    def _make_request(url: str, method: str, params: dict[str, str]) -> requests.Response:
        return requests.request(
            method=method.upper(),
            url=url,
            params=params
        )

    @staticmethod
    def _make_response(response: requests.Response) -> dict[str, str]:
        return response.json()


class WikipediaApi:

    def __init__(self, client: WikipediaClient):
        self.__client = client

    def all_animals_by_alphabet(self) -> list[dict[str, Union[int, str]]]:
        cmcontinue = None
        result = []

        while True:
            response = self.__client.request(
                method="get",
                params=(
                        {
                            "action": "query",
                            "list": "categorymembers",
                            "cmtitle": "Категория:Животные_по_алфавиту",
                            "cmlimit": "500",
                            "format": "json"
                        } |
                        (
                            {}
                            if cmcontinue is None
                            else {"cmcontinue": cmcontinue}
                        )
                )
            )

            result.extend(response['query']['categorymembers'])

            if 'continue' in response:
                cmcontinue = response['continue']['cmcontinue']
            else:
                break

        return result


def get_animals_by_alphabet_from_wikipedia():
    wiki_api = WikipediaApi(client=WikipediaClient())
    return wiki_api.all_animals_by_alphabet()


def build_csv_for_animals(animals: list[dict[str, Union[int, str]]], output_file: str):
    letter_counts = defaultdict(int)

    for item in animals:
        title = item["title"]
        first_letter = title[0].upper()
        letter_counts[first_letter] += 1

    with open(output_file, "w") as csvfile:
        writer = csv.writer(csvfile)

        for letter in sorted(letter_counts):
            writer.writerow([letter, letter_counts[letter]])


if __name__ == "__main__":
    animals = get_animals_by_alphabet_from_wikipedia()
    build_csv_for_animals(animals=animals, output_file="./result.csv")
