import toml
from typing import Dict
from dotenv import load_dotenv
import os


def load_project_env(working_dir: str = '') -> Dict:
    """Loads environment variables from .env file and api/db configuration values from config.toml in specified directory (current working directory by default).
    These files should be modeled after example-env and example-config.toml, Matching the keys in the files is required.

    :param working_dir: (optional) String, The path to the directory containing the .env and config.toml 
    :type working_dir: str

    :return: Nested Dictionaries, The values specified in the config.toml file
    :rtype: Dictionary
    """

    if not working_dir:
        working_dir = os.getcwd()
    load_dotenv(os.path.join(working_dir, '.env'))
    return toml.load(os.path.join(working_dir, 'config.toml'))
