import os
import csv
from unittest.mock import patch, MagicMock
from solution import WikipediaClient, WikipediaApi, build_csv_for_animals


def test_wikipedia_client_request():
    mock_response = MagicMock()
    mock_response.json.return_value = {"query": "ok"}

    with patch("solution.requests.request", return_value=mock_response) as mock_request:
        client = WikipediaClient()
        result = client.request("get", {"a": "b"})

        assert result == {"query": "ok"}
        mock_request.assert_called_once()


def test_wikipedia_api_all_animals_by_alphabet():
    client = MagicMock()
    client.request.side_effect = [
        {
            "query": {
                "categorymembers": [{"title": "Аист"}, {"title": "Антилопа"}]
            },
            "continue": {"cmcontinue": "page2"}
        },
        {
            "query": {
                "categorymembers": [{"title": "Бобр"}]
            }
        }
    ]

    api = WikipediaApi(client)
    result = api.all_animals_by_alphabet()

    assert result == [{"title": "Аист"}, {"title": "Антилопа"}, {"title": "Бобр"}]


def test_build_csv_for_animals():
    animals = [
        {"title": "Акула"},
        {"title": "Аист"},
        {"title": "Бобр"},
    ]
    csv_file = "./test.csv"
    build_csv_for_animals(animals, str(csv_file))

    with open(csv_file, newline="") as f:
        reader = list(csv.reader(f))
        assert reader == [["А", "2"], ["Б", "1"]]

    os.remove(csv_file)


