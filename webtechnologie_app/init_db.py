from webtechnologie_app.models import Mitarbeiter, Hallen,Inventar, Inventar_status, Inventar_typ
from werkzeug.security import generate_password_hash, check_password_hash
from webtechnologie_app.models import db

db.create_all()

typ = Inventar_typ(bezeichnung="Leiter", feld_1_bez="Art", feld_2_bez="Sprossen")
db.session.add(typ)
db.session.commit()

inventar = Inventar(inventar_typ_id="1", feld_1="Anlegeleiter", feld_2="10 Sprossen")
db.session.add(inventar)
db.session.commit()

neuer_benutzer = Mitarbeiter(vorname="Tobias", name="Neurath",
                             passwort=generate_password_hash("123", method='sha256'))
db.session.add(neuer_benutzer)
db.session.commit()



halle = Hallen(bezeichnung="Halle 1")
db.session.add(halle)
db.session.commit()
