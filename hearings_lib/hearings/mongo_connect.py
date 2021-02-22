from pymongo import MongoClient
from load_project_env import ProjectEnv
import os


class MongoConnect():
    @staticmethod
    def get_connection():
        ProjectEnv.load_env()

        return MongoClient(os.getenv('MONGOSTRING'))
