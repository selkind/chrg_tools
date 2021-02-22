import toml
from dotenv import load_dotenv
import os
from gpo_tools.gpo_tools.scrape import Scraper


env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)


config = toml.load(os.path.join(os.path.dirname(__file__), 'config.toml'))
db_config = config['database']
MIN_CONGRESS = '112'
MAX_CONGRESS = '113'

scraper = Scraper(min_congress=MIN_CONGRESS, max_congress=MAX_CONGRESS,
                  api_key=os.getenv('GPO_API_KEY'), db=db_config['name'],
                  user=db_config['user'], password=os.getenv('DB_POSTGRES_PW'),
                  host=db_config['host'], update_stewart_meta=False
                  )
scraper.scrape()
