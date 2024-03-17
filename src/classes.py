from dataclasses import dataclass

import json
import pandas as pd
import requests

from src.abs import Request_API, JobFileStorage
from src.cfg import HH_API_URL, PATH_DATA_JSON, PATH_DATA_CSV


# -------------------------- ЗАПРОС К API HH.RU --------------------------------
@dataclass
class HH_API(Request_API):
    """
    Класс для запроса к API HH.RU
    """
    base_url: str = HH_API_URL

    def fetch_jobs(self, query: str):
        try:
            response = requests.get(self.base_url, params={"text": query, "per_page": 100})
            response.raise_for_status()
            return response.json()['items']
        except requests.exceptions.HTTPError as http_err:
            # Обработка HTTP ошибок
            print(http_err)
        except requests.exceptions.ConnectionError as conn_err:
            # Обработка ошибок соединения
            print(conn_err)
        except requests.exceptions.Timeout as timeout_err:
            # Обработка ошибки тайм-аута
            print(timeout_err)
        except requests.exceptions.RequestException as req_err:
            # Обработка любых исключений, связанных с запросами
            print(req_err)
        except Exception as e:
            # Обработка всех остальных исключений
            print(f"Произошла ошибка: {e}")

        # Возвращение None в случае возникновения ошибки
        return None


# -------------------------- ВАЛИДАЦИЯ И ФИЛЬТРАЦИЯ --------------------------------
@dataclass
class Job_Search:
    """
    Класс для фильтрации вакансий
    """
    response: list

    def salary_filter(self, salary):
        salary_filtered_id = []
        if salary is None:
            return salary_filtered_id
        else:
            if salary == 0:
                for vacancy in self.response:
                    salary_filtered_id.append(vacancy["id"])
                return salary_filtered_id
            else:
                for vacancy in self.response:
                    if vacancy['salary'] is None or vacancy['salary']['from'] is None:
                        continue
                    if vacancy['salary']['from'] >= salary:
                        salary_filtered_id.append(vacancy["id"])
                return salary_filtered_id

    def location_filter(self, location):
        location_filtered_id = []
        if location is None:
            return location_filtered_id
        else:
            if location == "Не выбрано":
                for vacancy in self.response:
                    location_filtered_id.append(vacancy["id"])
                return location_filtered_id
            else:
                for vacancy in self.response:
                    if vacancy['area']['name'].lower() == location.lower():
                        location_filtered_id.append(vacancy["id"])
                return location_filtered_id

    def experience_filter(self, experience):
        experience_filtered_id = []
        if experience is None:
            return experience_filtered_id
        else:
            if experience == "Не выбрано":
                for vacancy in self.response:
                    experience_filtered_id.append(vacancy["id"])
                return experience_filtered_id
            else:
                for vacancy in self.response:
                    if vacancy['experience']['name'].lower() == experience.lower():
                        experience_filtered_id.append(vacancy["id"])
                return experience_filtered_id

    def intersection(self, salary=None, location=None, experience=None):
        search_output = []
        sets = [set(lst) for lst in [self.salary_filter(salary), self.location_filter(location), self.experience_filter(experience)] if lst]
        if sets:
            common_elements = set.intersection(*sets)
            for element in common_elements:
                for response in self.response:
                    if response["id"] == element:
                        search_output.append(response)
            return search_output
        else:
            return search_output


# -------------------------- JSON --------------------------------
@dataclass
class JSONJobStorage(JobFileStorage):
    """
    Сохранение ответа от API в файл и работа с файлом
    """
    filename = PATH_DATA_JSON

    def save_jobs(self, jobs):
        self._save_jobs(jobs)

    def add_job(self, job):
        jobs = self._load_jobs()
        jobs.append(job)
        self._save_jobs(jobs)

    def get_jobs(self, criteria: dict):
        jobs = self._load_jobs()
        for job in jobs:
            if self._match_criteria(job, criteria):
                return job

    def delete_jobs(self, criteria):
        jobs = self._load_jobs()
        jobs = [job for job in jobs if not self._match_criteria(job, criteria)]
        self._save_jobs(jobs)

    def _load_jobs(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_jobs(self, jobs):
        '''
        Сохранение в файл
        '''
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(jobs, file, indent=4, ensure_ascii=False, )

    def _match_criteria(self, data, criteria: dict):
        '''
        Сравнение данных с критериями
        '''
        def recursive_get(sub_data, keys, value):
            # Получаем первый ключ и оставшиеся ключи
            first_key, *remaining_keys = keys
            # Если ключей больше нет, сравниваем значение
            if not remaining_keys:
                return sub_data.get(first_key) == value
            # Если ключ существует и его значение - словарь, продолжаем поиск
            next_data = sub_data.get(first_key)
            if isinstance(next_data, dict):
                return recursive_get(next_data, remaining_keys, value)
            return False

        # Итерация по критериям и проверка каждого критерия
        for key, value in criteria.items():
            if not recursive_get(data, key.split('.'), value):
                return False
        return True


# -------------------------- CSV --------------------------------
@dataclass
class JSONToCSVConverter:
    """
    Класс для конвертации отевета от API в CSV
    """
    csv_file_path: str = PATH_DATA_CSV

    def create_csv(self, vacancies):
        data_for_table = []
        for vacancy in vacancies:
            try:
                name = vacancy.get('name', '')
                salary_from = vacancy.get('salary', {}).get('from', '') if vacancy.get('salary') else ''
                city = vacancy.get('area', {}).get('name', '') if vacancy.get('area') else ''
                experience = vacancy.get('experience', {}).get('name', '') if vacancy.get('experience') else ''
                alternate_url = vacancy.get('alternate_url', '')
            except AttributeError:
                continue
            data_for_table.append({
                'Название': name,
                'Зарплата от': salary_from,
                'Город': city,
                'Опыт': experience,
                'Ссылка': alternate_url
            })
        df = pd.DataFrame(data_for_table)
        df.to_csv(self.csv_file_path, index=False, encoding='utf-8-sig')

