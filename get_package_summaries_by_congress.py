import os
import requests
from hearings_lib.hearings.load_project_env import load_project_env
from hearings_lib.api_client import APIClient


def get_package_ids_by_congress(congress: int, config_directory: str = ''):
    load_project_env(config_directory)
    # Python automatically concatenates strings within brackets that aren't comma-separated.
    # This string definition is broken up due to line-length

    with requests.Session() as s:
        client = APIClient(api_key=os.getenv('GPO_API_KEY'), session=s)
        new_or_modified_packages = client.get_package_ids_by_congress(congress)

        package_summaries = client.get_package_summaries(packages=new_or_modified_packages)
    return package_summaries
