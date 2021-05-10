from pymongo import MongoClient
from load_project_env import load_project_env 
import os


class MongoConnect():
    @staticmethod
    def get_connection():
        mongo_uri = load_project_env()['mongodb']['uri']

        return MongoClient(mongo_uri)
