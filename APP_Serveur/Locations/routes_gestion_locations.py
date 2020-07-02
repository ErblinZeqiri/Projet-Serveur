# routes_gestion_locations.py
# EZ 2020.07.16 Gestions des "routes" FLASK pour les Locations.

from flask import render_template, flash, redirect, url_for, request
from APP_Serveur import obj_mon_application
from APP_Serveur.Locations.data_gestion_locations import GestionLocations
from APP_Serveur.DATABASE.erreurs import *
# EZ 2020.07.11 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /locations_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:5005/locations_afficher
# order_by : ASC : Ascendant, DESC : Descendant
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/locations_afficher/<string:order_by>/<int:ID_Location_sel>", methods=['GET', 'POST'])
def locations_afficher(order_by,ID_Location_sel):
    # EZ 2020.07.19 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocations()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionlocations()
            # Fichier data_gestion_locations.py
            # "order_by" permet de choisir l'ordre d'affichage des locations.
            data_locations = obj_actions_locations.locations_afficher_data(order_by,ID_Location_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data locations", data_locations, "type ", type(data_locations))

            # Différencier les messages si la table est vide.
            if not data_locations and ID_Location_sel == 0:
                flash("""La table "t_location" est vide. !!""", "warning")
            elif not data_locations and ID_Location_sel > 0:
                # Si l'utilisateur change l'ID_Location dans l'URL et que le location n'existe pas,
                flash(f"Le location demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "t_location" est vide.
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données des locations affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.17 Envoie la page "HTML" au serveur.
    return render_template("locations/locations_afficher.html", data=data_locations)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /locations_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "locations_add.html"
# Pour la tester http://127.0.0.1:5005/locations_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/locations_add", methods=['GET', 'POST'])
def locations_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocations()
            # EZ 2020.07.19 Récupère le contenu du champ dans le formulaire HTML "locations_add.html"
            Location = request.form['Location_html']

            # Constitution d'un dictionnaire et insertion dans la BD
            valeurs_insertion_dictionnaire = {"value_Location": Location}
            obj_actions_locations.add_location_data(valeurs_insertion_dictionnaire)

            # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Données insérées !!", "success")
            print(f"Données insérées !!")
            # On va interpréter la "route" 'locations_afficher', car l'utilisateur
            # doit voir le nouveau location qu'il vient d'insérer. Et on l'affiche de manière
            # à voir le dernier élément inséré.
            return redirect(url_for('locations_afficher', order_by = 'DESC', ID_Location_sel=0))

        # EZ 2020.07 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"RGG pei {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

        # EZ 2020.07 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur:
            flash(f"Autre erreur {erreur}", "danger")
            raise MonErreur(f"Autre erreur")

        # EZ 2020.07 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except Exception as erreur:
            # EZ 2020.07.19 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(
                f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")
    # EZ 2020.07.17 Envoie la page "HTML" au serveur.
    return render_template("locations/locations_add.html")


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /locations_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un location de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/locations_edit', methods=['POST', 'GET'])
def locations_edit ():
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "locations_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "ID_Location" du formulaire html "locations_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Location"
            # grâce à la variable "ID_Location_edit_html"
            # <a href="{{ url_for('locations_edit', ID_Location_edit_html=row.ID_Location) }}">Edit</a>
            ID_Location_edit = request.values['ID_Location_edit_html']


            # Pour afficher dans la console la valeur de "ID_Location_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(ID_Location_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_ID_Location": ID_Location_edit}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocations()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Location = obj_actions_locations.edit_location_data(valeur_select_dictionnaire)
            print("dataIdLocation ", data_ID_Location, "type ", type(data_ID_Location))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Modification d'un location !!!", "success")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            # On indique un problème, mais on ne dit rien en ce qui concerne la résolution.
            print("Problème avec la BD ! : %s", erreur)
            # EZ 2020.07.19 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']}"
                                      f"et son status {msg_erreurs['ErreurConnexionBD']['status']}")

    return render_template("locations/locations_edit.html", data=data_ID_Location)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /locations_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un location de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/locations_update', methods=['POST', 'GET'])
def locations_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "locations_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du location alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "ID_Location" du formulaire html "locations_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Location"
            # grâce à la variable "ID_Location_edit_html"
            # <a href="{{ url_for('locations_edit', ID_Location_edit_html=row.ID_Location) }}">Edit</a>
            ID_Location_edit = request.values['ID_Location_edit_html']

            # Récupère le contenu du champ "intitule_location" dans le formulaire HTML "locationsEdit.html"
            Location = request.values['name_edit_Location_html']

            valeur_edit_list = [{'ID_Location': ID_Location_edit,
                                 'Location': Location}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_update_dictionnaire = {"value_ID_Location": ID_Location_edit,
                                          "value_Location": Location}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocations()

            # La commande MySql est envoyée à la BD
            data_ID_Location = obj_actions_locations.update_location_data(valeur_update_dictionnaire)
            # DEBUG bon marché :
            print("dataIdLocation ", data_ID_Location, "type ", type(data_ID_Location))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Valeur location modifiée. ", "success")
            # On affiche les locations avec celui qui vient d'être edité en tête de liste. (DESC)
            return redirect(url_for('locations_afficher', order_by="ASC", ID_Location_sel=ID_Location_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème locations ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_location_html" alors on renvoie le formulaire "EDIT"
    return render_template('locations/locations_edit.html', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /locations_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un location de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/locations_select_delete', methods=['POST', 'GET'])
def locations_select_delete ():
    if request.method == 'GET':
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocations()
            # OM 2019.04.04 Récupère la valeur de "idlocationDeleteHTML" du formulaire html "locationsDelete.html"
            ID_Location_delete = request.args.get('ID_Location_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Location": ID_Location_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Location = obj_actions_locations.delete_select_location_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur locations_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur locations_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('locations/locations_delete.html', data=data_ID_Location)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /locationsUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un location, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/locations_delete', methods=['POST', 'GET'])
def locations_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocations()
            # OM 2019.04.02 Récupère la valeur de "ID_Location" du formulaire html "locationsAfficher.html"
            ID_Location_delete = request.form['ID_Location_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Location": ID_Location_delete}

            data_locations = obj_actions_locations.delete_location_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des locations des serveurs
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les locations
            return redirect(url_for('locations_afficher',order_by="ASC",ID_Location_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.19 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "location" de serveurs qui est associé dans "t_locations_films".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des serveurs !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce location est associé à des serveurs dans la t_locations_films !!! : {erreur}")
                # Afficher la liste des locations des serveurs
                return redirect(url_for('locations_afficher', order_by="ASC", ID_Location_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur locations_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur locations_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('locations/locations_afficher.html', data=data_locations)
