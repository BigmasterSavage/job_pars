import pytest
import requests_mock
from src.func import fetch_and_parse_hh_ru_cities


# Тест успешного получения списка городов
def test_fetch_and_parse_success():
    mock_data = [
        {'id': '1', 'parent_id': None, 'name': 'Russia', 'areas': [
            {'id': '2', 'parent_id': '1', 'name': 'Moscow', 'areas': []},
            {'id': '3', 'parent_id': '1', 'name': 'Saint Petersburg', 'areas': []}
        ]}
    ]
    with requests_mock.Mocker() as m:
        m.get('https://api.hh.ru/areas', json=mock_data)
        result = fetch_and_parse_hh_ru_cities()
        assert result == ['Moscow', 'Saint Petersburg']


# Тест неудачного запроса
def test_fetch_failure():
    with requests_mock.Mocker() as m:
        m.get('https://api.hh.ru/areas', status_code=500)
        result = fetch_and_parse_hh_ru_cities()
        assert result == "Failed to fetch areas. Status code: 500"


