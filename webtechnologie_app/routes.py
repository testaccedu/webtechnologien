from webtechnologie_app import app
from webtechnologie_app import db
import sqlite3
from flask import render_template, request, url_for, flash, redirect
from webtechnologie_app.models import Mitarbeiter, Hallen


def get_db_connection():
    conn = sqlite3.connect('webtechnologie_app/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_inventar_infos(id):
    conn = get_db_connection()
    inventar = conn.execute('SELECT '
                            'inventar_typ.feld_1_bez, inventar_typ.feld_2_bez,inventar_typ.feld_3_bez, inventar_typ.feld_4_bez, inventar_typ.bezeichnung,'
                            'inventar.feld_1, inventar.feld_2, inventar.feld_3, inventar.feld_4, inventar.id '
                            'FROM inventar '
                            'LEFT JOIN inventar_typ on inventar.inventar_typ_id = inventar_typ.id '
                            ' WHERE inventar.id=' + str(id)).fetchall()
    conn.close()
    return inventar


def get_status_infos(id):
    conn = get_db_connection()
    status = conn.execute('SELECT * '
                          'FROM inventar_status '
                          'LEFT JOIN mitarbeiter on inventar_status.mitarbeiter_id = mitarbeiter.id'
                          ' WHERE inventar_status.inventar_id=' + str(
        id) + ' ORDER BY inventar_status.erstellt DESC').fetchmany()
    conn.close()
    print(len(status))

    if len(status) >= 1:
        status = status[0]
    else:
        status = {"id": 0, "vorname": "leer", "name": "leer", "erstellt": "leer"}

    print(status)
    return status


@app.route('/')
def index():

    user = Mitarbeiter(vorname="fragezeichen" , name="annabell")
    db.session.add(user)
    db.session.commit()
    user = Mitarbeiter.query.filter_by(name="Neurath").first()
    print(Mitarbeiter.query.get(2))
    print(Mitarbeiter.query.all())
    return render_template('index.html')


@app.route('/erfassen')
def erfassen():
    return render_template('erfassen.html')


@app.route('/registrieren')
def registrieren():
    return render_template('registrieren.html')


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


@app.route('/status_update', methods=('GET', 'POST'))
def status_update():
    if request.args.get('id'):
        id = request.args.get('id')
    else:
        id = 0

    if request.method == 'POST':
        halle = request.form['halle']
        ebene = request.form['ebene']
        feld = request.form['feld']
        bemerkung = request.form['bemerkung']

        if not feld:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO inventar_status (inventar_id, standort_halle_id, standort_feld, standort_bemerkung, mitarbeiter_id) VALUES (?, ?, ?, ?, ?)",
                (id, halle, ebene + feld, bemerkung, 1))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('status_update.html', inventar_infos=get_inventar_infos(id),
                           status_info=get_status_infos(id))


