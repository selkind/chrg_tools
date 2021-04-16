import os
from load_project_env import ProjectEnv
from db_context_manager import cursor
from hearings_lib.gpo_tools.gpo_tools.scrape import Scraper


def main():
    ProjectEnv.load_env()
    config = ProjectEnv.get_config()
    db_config = config['database']

    old_scraper = Scraper(
        db=db_config['name'],
        user=db_config['user'],
        password=os.getenv('DB_POSTGRES_PW'),
        api_key=os.getenv('GPO_API_KEY'),
        host=db_config['host'],
        min_congress='113',
        max_congress='113'
    )
    old_scraper.scrape()


if __name__ == '__main__':
    main()