CREATE TABLE IF NOT EXISTS members(
    id integer PRIMARY KEY,
    metadata json,
    committee_membership json
);

CREATE TABLE IF NOT EXISTS hearings(
    id text PRIMARY KEY,
    transcript text,
    congress integer,
    session integer,
    chamber text,
    date date,
    committees text[],
    subcommittees text[],
    uri text,
    url text,
    sudoc text,
    number text,
    witness_meta json,
    member_meta json,
    parsed json
);

DO
$$
BEGIN
    IF NOT EXISTS (SELECT * 
                        FROM pg_type typ
                            INNER JOIN pg_namespace nsp
                                ON nsp.oid = typ.typnamespace
                        WHERE nsp.nspname = current_schema()
                            AND typ.typname = 'chamber' ) THEN
        CREATE TYPE chamber 
                    AS ENUM ('HOUSE', 'SENATE', 'JOINT', '');
    END IF;
END;
$$
LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS committees(
    id SERIAL PRIMARY KEY,
    name text,
    chamber chamber,
    code integer 
);

CREATE TABLE IF NOT EXISTS mongo_members(
    id SERIAL PRIMARY KEY,
    icspr integer,
    congress integer,
    biography text,
    birth_year integer,
    chamber chamber,
    congress_count integer,
    death_year integer,
    house_count integer,
    senate_count integer,
    district_code integer,
    name text,
    nabs_votes integer,
    nvotes_against_party integer,
    nvotes_party_split integer,
    nvotes_yea_nay integer,
    occupancy integer,
    party_code integer,
    served_as_speaker integer,
    state_abbrev text
);

CREATE TABLE IF NOT EXISTS nokken_poole(
    id SERIAL PRIMARY KEY,
    member_id integer,
    dim1 numeric,
    dim2 numeric,
    nvotes integer
);

CREATE TABLE IF NOT EXISTS nominate(
    id SERIAL PRIMARY KEY,
    member_id integer,
    dim1 numeric,
    dim2 numeric,
    geo_mean_probability numeric,
    log_likelihood numeric,
    nerrors integer,
    nvotes integer,
    ntotal_votes integer
);

CREATE TABLE IF NOT EXISTS commitee_assignments(
    id SERIAL PRIMARY KEY,
    icspr integer,
    code integer,
    congress integer,
    assign_date date,
    termination_date date,
    period_of_service integer,
    committee_status_congress_end integer,
    committee_continuity_next_congress integer,
    appointment_citation text,
    committee_name text,
    notes text
);
