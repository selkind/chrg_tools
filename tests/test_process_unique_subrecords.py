import os
import pytest
import pickle
import sqlalchemy
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer
from hearings_lib.db_models import Base
from hearings_lib.db_handler import DB_Handler


class TestProcessUniqueSubrecords:

    TEST_DATA_PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'api_client_data_pickles',
        'summary_package_sample.pickle'
    )

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

    def test_process_unique_witnesses(self, package_summaries, db):
        handler = DB_Handler(db)
        with Session(handler.engine) as session:
            for i in package_summaries:
                if i.metadata:
                    witnesses = i.metadata.witnesses
                    orm_witnesses = handler._process_unique_witnesses(witnesses, session)
                    assert len(witnesses) == len(orm_witnesses)
