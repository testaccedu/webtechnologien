from webtechnologie_app import app
from webtechnologie_app import db
import sqlite3
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from webtechnologie_app.models import Mitarbeiter, Hallen, Inventar_status
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash


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
    return render_template('index.html')


@app.route('/erfassen')
def erfassen():
    return render_template('erfassen.html')


@app.route("/registrieren", methods=('GET', 'POST'))
def registrieren():
    if request.method == 'POST':
        vorname = request.form['vorname']
        name = request.form['name']
        passwort = request.form['passwort']
        user = Mitarbeiter.query.filter_by(name=name,
                                           vorname=vorname).first()  # if this returns a user, then the email already exists in database
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('registrieren'))

        neuer_benutzer = Mitarbeiter(vorname=vorname, name=name,
                                     passwort=generate_password_hash(passwort, method='sha256'))
        db.session.add(neuer_benutzer)
        db.session.commit()
        print(vorname + name + passwort)
    return render_template('registrieren.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        nutzer = request.form.get('nutzer')
        formpasswort = request.form.get('passwort')
        vorname = ""
        name = ""
        if "." in nutzer:
            vorname = str(nutzer).split(".")[0]
            name = str(nutzer).split(".")[1]

        # remember = True if request.form.get('remember') else False

        nutzer = Mitarbeiter.query.filter_by(name=name, vorname=vorname).first()
        print(nutzer)

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not nutzer or not check_password_hash(nutzer.passwort, formpasswort):
            flash('Login fehlerhaft. Bitte Benutzername und Passwort prüfen!')
            return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page
        login_user(nutzer, remember=1)
        return redirect(url_for('index'))
        # if the above check passes, then we know the user has the right credentials
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/anzeigen')
@login_required
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
    print(current_user.name)
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

        status = Inventar_status(inventar_id=id, standort_halle_id=halle, standort_feld=feld, standort_bemerkung=bemerkung, mitarbeiter_id=current_user.id)
        db.session.add(status)
        db.session.commit()
        print(status)
        return redirect(url_for('index'))

    return render_template('status_update.html', inventar_infos=get_inventar_infos(id),
                           status_info=get_status_infos(id))
