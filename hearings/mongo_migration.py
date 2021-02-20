import os
import psycopg2
import psycopg2.extras
from mongo_connect import MongoConnect
from load_project_env import ProjectEnv


def main():
    member_values = []
    nokken_values = []
    nominate_values = []
    # handle inconsistencies in field names between mongo and postgres schemas
    member_schema_map = {
        'icpsr': 'icpsr', 'congress': 'congress', 'biography': 'biography', 'born': 'birth_year',
        'chamber': 'chamber', 'death_year': 'death_year', 'district_code': 'district_code',
        'fname': 'name', 'nvotes_abs': 'nvotes_abs', 'nvotes_against_party': 'nvotes_against_party',
        'nvotes_party_split': 'nvotes_party_split', 'nvotes_yea_nay': 'nvotes_yea_nay', 'occupancy': 'occupancy',
        'party_code': 'party_code', 'served_as_speaker': 'served_as_speaker', 'state_abbrev': 'state_abbrev'
    }

    nokken_schema_map = {'number_of_votes': 'nvotes', 'dim1': 'dim1', 'dim2': 'dim2'}

    nominate_schema_map = {
        'geo_mean_probability': 'geo_mean_probability', 'dim1': 'dim1',
        'dim2': 'dim2', 'log_likelihood': 'log_likelihood', 'number_of_errors': 'nerrors', 'number_of_votes': 'nvotes',
        'total_number_of_votes': 'ntotal_votes'
    }
    member_fields = sorted(list(member_schema_map.values()))
    nokken_fields = list(nokken_schema_map.values())
    nokken_fields.append('member_id')
    nokken_fields = sorted(nokken_fields)
    nominate_fields = list(nokken_schema_map.values())
    nominate_fields.append('member_id')
    nominate_fields = sorted(nominate_fields)

    mdb_connection = MongoConnect.get_connection()
    mdb = mdb_connection.test
    mdb_cursor = mdb.voteview_members.find()

    for i in mdb_cursor:
        member = {member_schema_map[k]: i.get(k, None) for k in member_schema_map.keys()}
        member_id = int(str(member['icpsr']) + str(member['congress']))
        member_values.append([member[k] for k in member_fields])
        if 'nokken_poole' in i:
            nokken = {nokken_schema_map[k]: i['nokken_poole'].get(k, None) for k in nokken_schema_map.keys()}
            nokken['member_id'] = member_id
            nokken_values.append([nokken[k] for k in nokken_fields])
        if 'nominate' in i:
            nominate = {nominate_schema_map[k]: i['nominate'].get(k, None) for k in nominate_schema_map.keys()}
            nominate['member_id'] = member_id
            nominate_values.append([nominate[k] for k in nominate_fields])

    config = ProjectEnv.get_config()
    ProjectEnv.load_env()
    db_config = config['database']

    conn = psycopg2.connect(database=db_config['name'],
                            user=db_config['user'],
                            host=db_config['host'],
                            password=os.getenv('DB_POSTGRES_PW'),
                            cursor_factory=psycopg2.extras.RealDictCursor
                            )

    member_query = f"INSERT INTO mongo_members ({','.join(member_fields)}) VALUES %s"
    nokken_query = f"INSERT INTO nokken_poole ({','.join(nokken_fields)}) VALUES %s"
    nominate_query = f"INSERT INTO nominate ({','.join(nominate_fields)}) VALUES %s"

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
