import sqlite3
from flask import Flask, render_template

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/erfassen')
def erfassen():
    return render_template('erfassen.html')

@app.route('/anzeigen')
def anzeigen():
    conn = get_db_connection()
    inventar = conn.execute('SELECT '
                            'inventar_typ.feld_1_bez, inventar_typ.feld_2_bez,inventar_typ.feld_3_bez, inventar_typ.feld_4_bez, inventar_typ.bezeichnung,'
                            'inventar.feld_1, inventar.feld_2, inventar.feld_3, inventar.feld_4, inventar.id,'
                            'mitarbeiter.vorname, mitarbeiter.name, '
                            'hallen.bezeichnung, '
                            'inventar_status.standort_feld, inventar_status.standort_bemerkung, inventar_status.erstellt AS status_erstellt '
                            'FROM inventar '
                            'LEFT JOIN inventar_typ on inventar.inventar_typ_id = inventar_typ.id '
                            'LEFT JOIN inventar_status on inventar_status.inventar_id = inventar.id '
                            'LEFT JOIN hallen on inventar_status.standort_halle_id = hallen.id '
                            'LEFT JOIN mitarbeiter on inventar_status.mitarbeiter_id = mitarbeiter.id').fetchall()
    conn.close()
    return render_template('anzeigen.html', inventar=inventar)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5005')
