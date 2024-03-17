from src.classes import HH_API, Job_Search, JSONJobStorage, JSONToCSVConverter
from src.cfg import PATH_DATA_CSV
import requests
import pandas as pd



def fetch_and_parse_hh_ru_cities():
    """
    Функция для получения списка городов из API HH.RU
    """
    def parse_cities(areas, city_list):
        for area in areas:
            if area.get('parent_id') is not None:
                city_list.append(area['name'])
            if 'areas' in area and area['areas']:
                parse_cities(area['areas'], city_list)

    url = 'https://api.hh.ru/areas'
    response = requests.get(url)
    if response.status_code == 200:
        areas = response.json()
        city_list = []
        parse_cities(areas, city_list)
        return city_list
    else:
        return f"Failed to fetch areas. Status code: {response.status_code}"


def table(query, salary=None, location=None, experience=None):
    """
    Функция для вывода таблицы с вакансиями
    """
    api = HH_API()
    jobs = api.fetch_jobs(query)
    pars = Job_Search(jobs)
    out = pars.intersection(salary, location, experience)
    saver = JSONJobStorage()
    saver.save_jobs(out)
    converter = JSONToCSVConverter()
    converter.create_csv(out)
    df = pd.read_csv(PATH_DATA_CSV)
    return df


