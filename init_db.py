import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


cur.execute("INSERT INTO inventar_typ (bezeichnung, feld_1_bez, feld_2_bez) VALUES (?, ?, ?)",
            ('Leiter', 'Art', 'Anzahl Sprossen')
            )

cur.execute("INSERT INTO inventar_typ (bezeichnung, feld_1_bez, feld_2_bez) VALUES (?, ?, ?)",
            ('Hebebühne', 'Art', 'Arbeitshöhe (max)')
            )

cur.execute("INSERT INTO inventar (inventar_typ_id, feld_1, feld_2) VALUES (?, ?, ?)",
            (1, 'Anlegeleiter', '12')
            )

cur.execute("INSERT INTO inventar (inventar_typ_id, feld_1, feld_2) VALUES (?, ?, ?)",
            (2, 'Gelenkteleskop', '9,80 m')
            )

cur.execute("INSERT INTO inventar (inventar_typ_id, feld_1, feld_2) VALUES (?, ?, ?)",
            (2, 'Scheren-Bühne', '10 m')
            )

cur.execute("INSERT INTO mitarbeiter (name, vorname, passwort) VALUES (?, ?, ?)",
            ('Neurath', 'Tobias', 'xxxxx')
            )

cur.execute("INSERT INTO hallen (bezeichnung) VALUES ('Halle 1')")
cur.execute("INSERT INTO hallen (bezeichnung) VALUES ('Halle 2')")
cur.execute("INSERT INTO hallen (bezeichnung) VALUES ('Halle 3')")
cur.execute("INSERT INTO hallen (bezeichnung) VALUES ('Halle 4')")


cur.execute("INSERT INTO inventar_status (inventar_id, standort_halle_id, standort_feld, standort_bemerkung, mitarbeiter_id) VALUES (?, ?, ?, ?, ?)",
            (2, 2, 'EG F118', 'Unter Bühne', 1)
            )

connection.commit()
connection.close()
