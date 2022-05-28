from webtechnologie_app.models import Mitarbeiter, Hallen,Inventar, Inventar_status, Inventar_typ
from werkzeug.security import generate_password_hash, check_password_hash
from webtechnologie_app.models import db

db.create_all()


db.session.add(Inventar_typ(bezeichnung="Leiter", feld_1_bez="Art", feld_2_bez="Sprossen"))
db.session.add(Inventar_typ(bezeichnung="Hebebühne", feld_1_bez="Bezeichnung / Firma", feld_2_bez="Art", feld_3_bez="Arbeitshöhe"))
db.session.commit()


db.session.add(Inventar(inventar_typ_id="1", feld_1="Anlegeleiter", feld_2="10 Sprossen"))
db.session.add(Inventar(inventar_typ_id="1", feld_1="Stehleiter", feld_2="8 Sprossen"))
db.session.add(Inventar(inventar_typ_id="2", feld_1="Nifty", feld_2="Gelenkteleskop", feld_3="14,80 m"))
db.session.commit()

neuer_benutzer = Mitarbeiter(vorname="Tobias", name="Neurath",
                             passwort=generate_password_hash("123", method='sha256'))
db.session.add(neuer_benutzer)
db.session.commit()



halle = Hallen(bezeichnung="Halle 1")
db.session.add(halle)
db.session.commit()
