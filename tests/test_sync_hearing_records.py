import os
import pytest
import pickle
import sqlalchemy
from testcontainers.postgres import PostgresContainer
from hearings_lib.db_models import Base
from hearings_lib.db_handler import DB_Handler


class TestSyncHearingRecords:
    TEST_DATA_PATH = f'{os.path.abspath(os.path.dirname(__file__))}/summary_package_sample.pickle'

    @pytest.fixture
    def package_summaries(self):
        with open(self.TEST_DATA_PATH, 'rb') as f:
            data = pickle.load(f)
        return data

    @pytest.fixture
    def db(self):
        with PostgresContainer('postgres:latest') as db:
            e = sqlalchemy.create_engine(db.get_connection_url(), future=True)
            Base.metadata.create_all(e)
            yield e

    def test_sync_hearing_records_once(self, package_summaries, db):
        handler = DB_Handler(db)
        handler.sync_hearing_records(package_summaries)
        assert True
