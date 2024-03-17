import pytest
import random
import string
from src.classes import HH_API, Job_Search


# Generate random string
def random_query_string(size=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


# Test HH_API class
def test_fetch_jobs():
    hh_api = HH_API()
    query = random_query_string()
    response = hh_api.fetch_jobs(query)

    assert isinstance(response, list), "The response should be a list"


# Test Job_Search class
def test_salary_filter():
    simulated_response = [
        {"id": "1", "salary": {"from": 50000, "to": 70000}},
        {"id": "2", "salary": {"from": 30000, "to": 50000}},
        {"id": "3", "salary": None},
        {"id": "4", "salary": {"from": 100000, "to": 150000}}
    ]
    job_search = Job_Search(simulated_response)
    random_salary = random.randint(0, 150000)
    result = job_search.salary_filter(random_salary)
    assert isinstance(result, list), "The result should be a list"