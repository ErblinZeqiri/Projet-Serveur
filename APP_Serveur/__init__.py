# Un objet "obj_mon_application" pour utiliser la classe Flask
# Pour les personnes qui veulent savoir ce que signifie __name__ une démonstration se trouve ici :
# https://www.studytonight.com/python/_name_-as-main-method-in-python
# __name__ garantit que la méthode run() est appelée uniquement lorsque main.py est exécuté en tant que programme principal.
# La méthode run() ne sera pas appelée si vous importez main.py dans un autre module Python.
from flask import Flask
from APP_Serveur.DATABASE import connect_db_context_manager


# Objet qui fait "exister" notre application
obj_mon_application = Flask(__name__, template_folder="templates")
# Flask va pouvoir crypter les cookies
obj_mon_application.secret_key = '_vogonAmiral_)?^'

# Doit se trouver ici... soit après l'instanciation de la classe "Flask"
# EZ 2020.07.25 Tout commence ici par "indiquer" les routes de l'application.
from APP_Serveur import routes
from APP_Serveur.Serveurs import routes_gestion_serveurs
from APP_Serveur.Demandeurs import routes_gestion_demandeurs
from APP_Serveur.Personnes_Serveurs import routes_gestion_personnes_serveurs
from APP_Serveur.Mails import routes_gestion_mails
from APP_Serveur.Mails_Personnes import routes_gestion_mails_personnes
from APP_Serveur.Status import routes_gestion_status
from APP_Serveur.Status_Serveurs import routes_gestion_status_serveurs
from APP_Serveur.Locations import routes_gestion_locations
from APP_Serveur.Locations_Serveurs import routes_gestion_locations_serveurs
from APP_Serveur.Type_Equipements import routes_gestion_type_equipements
from APP_Serveur.Type_Equipements_Serveurs import routes_gestion_type_equipements_serveurs

