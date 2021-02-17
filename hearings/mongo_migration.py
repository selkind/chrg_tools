import os
import psycopg2
import psycopg2.extras
from mongo_connect import MongoConnect
from load_project_env import ProjectEnv


def main():
    mdb_connection = MongoConnect.get_connection()
    mdb = connection.test
    mdb_cursor = mdb.voteview_members.find()
    unique_keys = {}
    member_values = []
    nokken_values = []
    nominate_values = []
    # handle inconsistencies in field names between mongo and postgres schemas
    member_schema_map = {
        'icspr': 'icspr', 'congress': 'congress', 'biography': 'biography', 'born': 'birth_year',
        'chamber': 'chamber', 'congresses': 'congress_count', 'congresses_house': 'house_count',
        'congresses_senate': 'senate_count', 'death_year': 'death_year', 'district_code': 'district_code',
        'fname': 'name', 'nvotes_abs': 'nvotes_abs', 'nvotes_against_party': 'nvotes_against_party',
        'nvotes_party_split': 'nvotes_party_split', 'nvotes_yea_nay': 'nvotes_yea_nay', 'occupancy': 'occupancy',
        'party_code': 'party_code', 'served_as_speaker': 'served_as_speaker', 'state_abbrev': 'state_abbrev'
        }
    nokken_schema_map = {'number_of_votes': 'nvotes', 'dim1': 'dim1', 'dim2': 'dim2'}
    nominate_schema_map = {'number_of_votes': 'nvotes', 'dim1': 'dim1', 'dim2': 'dim2'}
    for i in mdb_cursor:
        member = {member_schema_map[k]: i.get(k, None) for k in [
            'icspr', 'congress', 'biography', 'born', 'chamber', 'congresses', 'congresses_house', 'congresses_senate',
            'death_year', 'district_code', 'fname', 'nvotes_abs', 'nvotes_against_party', 'nvotes_party_split',
            'nvotes_yea_nay', 'occupancy', 'party_code', 'served_as_speaker', 'state_abbrev']}
        member_id = int(str(member['icspr']) + str(member['congress']))
        member_values.append(member)
        if 'nokken' in i:
            nokken = {nokken_schema_map[k]: i['nokken'].get(k, None) for k in nokken_schema_map.keys()}
            nokken['member_id'] = member_id
        if 'nominate' in i:
            nominate =


    config = ProjectEnv.get_config()
    ProjectEnv.load_env()
    db_config = config['database']

    conn = psycopg2.connect(database=db_config['name'],
                            user=db_config['user'],
                            host=db_config['host'],
                            password=os.getenv('DB_POSTGRES_PW'),
                            cursor_factory=psycopg2.extras.RealDictCursor
                            )

    try:
        crs = conn.cursor()
        psycopg2.extras.execute_values(crs, member_query, member_values)
        psycopg2.extras.execute_values(crs, nokken_query, nokken_values)
        psycopg2.extras.execute_values(crs, nominate_query, nominate_values)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
