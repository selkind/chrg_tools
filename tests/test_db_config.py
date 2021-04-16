import sqlalchemy
from testcontainers.postgres import PostgresContainer
from hearings_lib.db_models import Base
import pytest


class TestDBConfig:

    @pytest.fixture
    def db(self):
        with PostgresContainer('postgres:9.5') as db:
            e = sqlalchemy.create_engine(db.get_connection_url())
            Base.metadata.create_all(e)
            return e
    
    def test_db_configures(self, db):
        assert True
