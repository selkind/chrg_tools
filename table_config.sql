CREATE DATABASE hearings;
\c hearings;

CREATE TABLE members(
    id integer PRIMARY KEY,
    metadata json,
    committee_membership json
    );

CREATE TABLE hearings(
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

CREATE TYPE chamber AS ENUM ('HOUSE', 'SENATE', 'JOINT')

CREATE TABLE committees(
    id integer PRIMARY KEY,
    name text,
    chamber chamber,
    code integer
    );