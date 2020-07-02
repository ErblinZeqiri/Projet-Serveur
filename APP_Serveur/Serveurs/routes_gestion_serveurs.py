# routes_gestion_serveurs.py
# EZ 2020.07.16 Gestions des "routes" FLASK pour les serveurs.
import re

import pymysql
from flask import render_template, flash, request, url_for
from werkzeug.utils import redirect
from APP_Serveur.DATABASE.erreurs import *

from APP_Serveur import obj_mon_application
from APP_Serveur.Serveurs.data_gestion_serveurs import GestionServeurs, MaBdErreurConnexion


# EZ 2020.07 Afficher les serveurs
# Pour la tester http://127.0.0.1:5005/serveurs_afficher
@obj_mon_application.route("/serveurs_afficher")
def serveurs_afficher():
    # EZ 2020.07.19 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_serveurs = GestionServeurs()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionserveurs()
            # Fichier data_gestion_serveurs.py
            data_serveurs = obj_actions_serveurs.serveurs_afficher_data()
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data serveurs", data_serveurs, "type ", type(data_serveurs))
            # Différencier les messages si la table est vide.
            if data_serveurs:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash("Données des serveurs affichées !!", "success")
            else:
                flash("""La table "t_serveurs" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGF Erreur générale. {erreur}","danger")

    # EZ 2020.07.17 Envoie la page "HTML" au serveur.
    return render_template("serveurs/serveurs_afficher.html", data=data_serveurs)

# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /serveurs_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "serveurs_add.html"
# Pour la tester http://127.0.0.1:5005/serveurs_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/serveurs_add", methods=['GET', 'POST'])
def serveurs_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_serveurs = GestionServeurs()
            # EZ 2020.07.19 Récupère le contenu du champ dans le formulaire HTML "serveurs_add.html"
            Nom_Serv = request.form['Nom_Serv_html']
            Nombre_Port = request.form['Nombre_Port_html']
            Nombre_U = request.form['Nombre_U_html']
            Date_Conf_Serv = request.form['Date_Conf_Serv_html']
            Description = request.form['Description_html']
            Puissance = request.form['Puissance_html']
            Date_Serveur = request.form['Date_Serveur_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.


            # Constitution d'un dictionnaire et insertion dans la BD
            valeurs_insertion_dictionnaire = {"value_Nom_Serv": Nom_Serv,
                                              "value_Nombre_Port": Nombre_Port,
                                              "value_Nombre_U": Nombre_U,
                                              "value_Date_Conf_Serv": Date_Conf_Serv,
                                              "value_Description": Description,
                                              "value_Puissance": Puissance,
                                              "value_Date_Serveur": Date_Serveur}
            obj_actions_serveurs.add_serveur_data(valeurs_insertion_dictionnaire)

            # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Données insérées !!", "success")
            print(f"Données insérées !!")
            # On va interpréter la "route" 'serveurs_afficher', car l'utilisateur
            # doit voir le nouveau serveur qu'il vient d'insérer. Et on l'affiche de manière
            # à voir le dernier élément inséré.
            return redirect(url_for('serveurs_afficher', order_by = 'DESC', ID_Serveur_sel=0))

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
    return render_template("serveurs/serveurs_add.html")

# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /serveurs_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un serveur de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/serveurs_edit', methods=['POST', 'GET'])
def serveurs_edit ():
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "serveurs_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "ID_Serveur" du formulaire html "serveurs_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Serveur"
            # grâce à la variable "ID_Serveur_edit_html"
            # <a href="{{ url_for('serveurs_edit', ID_Serveur_edit_html=row.ID_Serveur) }}">Edit</a>
            ID_Serveur_edit = request.values['ID_Serveur_edit_html']

            # Pour afficher dans la console la valeur de "ID_Serveur_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(ID_Serveur_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_ID_Serveur": ID_Serveur_edit}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_serveurs = GestionServeurs()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Serveur = obj_actions_serveurs.edit_serveur_data(valeur_select_dictionnaire)
            print("dataIdserveur ", data_ID_Serveur, "type ", type(data_ID_Serveur))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Affichage du serveur à modifier!!!", "success")

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

    return render_template("serveurs/serveurs_edit.html", data=data_ID_Serveur)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /serveurs_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un serveur de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/serveurs_update', methods=['POST', 'GET'])
def serveurs_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "serveurs_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du serveur alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "ID_Serveur" du formulaire html "serveurs_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Serveur"
            # grâce à la variable "ID_Serveur_edit_html"
            # <a href="{{ url_for('serveurs_edit', ID_Serveur_edit_html=row.ID_Serveur) }}">Edit</a>
            ID_Serveur_edit = request.values['ID_Serveur_edit_html']

            # Récupère le contenu du champ "intitule_serveur" dans le formulaire HTML "serveursEdit.html"
            Nom_Serv = request.values['name_edit_Nom_Serv_html']
            Nombre_Port = request.values['name_edit_Nombre_Port_html']
            Nombre_U = request.values['name_edit_Nombre_U_html']
            Date_Conf_Serv = request.values['name_edit_Date_Conf_Serv_html']
            Description = request.values['name_edit_Description_html']
            Puissance = request.values['name_edit_Puissance_html']

            valeur_edit_list = [{'ID_Serveur': ID_Serveur_edit,
                                 'Nom_Serv': Nom_Serv,
                                 'Nombre_Port': Nombre_Port,
                                 'Nombre_U': Nombre_U,
                                 'Date_Conf_Serv': Date_Conf_Serv,
                                 'Description': Description,
                                 'Puissance': Puissance}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.v

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_update_dictionnaire = {"value_ID_Serveur": ID_Serveur_edit,
                                          "value_Nom_Serv": Nom_Serv,
                                          "value_Nombre_Port": Nombre_Port,
                                          "value_Nombre_U": Nombre_U,
                                          "value_Date_Conf_Serv": Date_Conf_Serv,
                                          "value_Description": Description,
                                          "value_Puissance": Puissance}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_serveurs = GestionServeurs()

            # La commande MySql est envoyée à la BD
            data_ID_Serveur = obj_actions_serveurs.update_serveur_data(valeur_update_dictionnaire)
            # DEBUG bon marché :
            print("dataIdserveur ", data_ID_Serveur, "type ", type(data_ID_Serveur))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Valeur serveur modifiée. ", "success")
            # On affiche les serveurs avec celui qui vient d'être edité en tête de liste. (DESC)
            return redirect(url_for('serveurs_afficher', order_by="ASC", ID_Serveur_sel=ID_Serveur_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème serveurs ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_serveur_html" alors on renvoie le formulaire "EDIT"
    return render_template('serveurs/serveurs_edit.html', data=valeur_edit_list)

# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /serveurs_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un serveur de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/serveurs_select_delete', methods=['POST', 'GET'])
def serveurs_select_delete ():
    if request.method == 'GET':
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_serveurs = GestionServeurs()
            # OM 2019.04.04 Récupère la valeur de "idserveurDeleteHTML" du formulaire html "serveursDelete.html"
            ID_Serveur_delete = request.args.get('ID_Serveur_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Serveur": ID_Serveur_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Serveur = obj_actions_serveurs.delete_select_serveur_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur serveurs_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur serveurs_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('serveurs/serveurs_delete.html', data=data_ID_Serveur)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /serveursUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un serveur, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/serveurs_delete', methods=['POST', 'GET'])
def serveurs_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_serveurs = GestionServeurs()
            # OM 2019.04.02 Récupère la valeur de "ID_Serveur" du formulaire html "serveursAfficher.html"
            ID_Serveur_delete = request.form['ID_Serveur_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Serveur": ID_Serveur_delete}

            data_serveurs = obj_actions_serveurs.delete_serveur_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des serveurs des serveurs
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les serveurs
            return redirect(url_for('serveurs_afficher',order_by="ASC",ID_Serveur_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.19 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "serveur" de serveurs qui est associé dans "t_serveurs_serveurs".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des serveurs !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce serveur est associé à des serveurs dans la t_serveurs_serveurs !!! : {erreur}")
                # Afficher la liste des serveurs des serveurs
                return redirect(url_for('serveurs_afficher', order_by="ASC", ID_Serveur_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur serveurs_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur serveurs_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('serveurs/serveurs_afficher.html', data=data_serveurs)
