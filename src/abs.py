from abc import ABC, abstractmethod


class Request_API(ABC):
    @abstractmethod
    def fetch_jobs(self, query):
        pass


class JobFileStorage(ABC):
    @abstractmethod
    def add_job(self, job):
        pass

    @abstractmethod
    def get_jobs(self, criteria):
        pass

    @abstractmethod
    def delete_jobs(self, criteria):
        pass