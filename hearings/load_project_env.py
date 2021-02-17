import toml
from dotenv import load_dotenv
import os


class ProjectEnv:
    @staticmethod
    def load_env() -> None:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)

    @staticmethod
    def get_congfig() -> dict:
        return toml.load(os.path.join(os.path.dirname(__file__), 'config.toml'))
