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
    code text
);

CREATE TABLE IF NOT EXISTS representatives(
    id integer PRIMARY KEY,
    congress integer,
    majority_code

);
CREATE TABLE IF NOT EXISTS commitee_assignments(
    id SERIAL PRIMARY KEY,
    congress integer,
    code integer REFERENCES committees,
    rep_id integer REFERENCES representatives,
    assign_date date,
    termination_date date,
    period_of_service integer,
    committee_status_congress_end integer,
    committee_continuity_next_congress integer,
    appointment_citation text,
    committee_name text,
    notes text
);
