DROP TABLE IF EXISTS inventar;
DROP TABLE IF EXISTS inventar_typ;
DROP TABLE IF EXISTS inventar_status;
DROP TABLE IF EXISTS mitarbeiter;
DROP TABLE IF EXISTS hallen;

CREATE TABLE inventar (
	id integer PRIMARY KEY AUTOINCREMENT,
	inventar_typ_id integer,
	feld_1 varchar,
	feld_2 varchar,
	feld_3 varchar,
	feld_4 varchar,
    erstellt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventar_typ (
	id integer PRIMARY KEY AUTOINCREMENT,
	bezeichnung varchar,
	feld_1_bez varchar,
	feld_2_bez varchar,
	feld_3_bez varchar,
	feld_4_bez varchar,
	erstellt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventar_status (
	id integer PRIMARY KEY AUTOINCREMENT,
	inventar_id integer,
	standort_halle_id integer,
	standort_feld varchar,
	standort_bemerkung varchar,
	mitarbeiter_id integer,
	erstellt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mitarbeiter (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	vorname varchar,
	passwort varchar,
	previligiert integer,
    erstellt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hallen (
	id integer PRIMARY KEY AUTOINCREMENT,
	bezeichnung varchar
);




