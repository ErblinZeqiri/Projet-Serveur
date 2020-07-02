# routes_gestion_status.py
# EZ 2020.07.16 Gestions des "routes" FLASK pour les status.

from flask import render_template, flash, redirect, url_for, request
from APP_Serveur import obj_mon_application
from APP_Serveur.Status.data_gestion_status import GestionStatus
from APP_Serveur.DATABASE.erreurs import *
# EZ 2020.07.11 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /status_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:5005/status_afficher
# order_by : ASC : Ascendant, DESC : Descendant
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/status_afficher/<string:order_by>/<int:ID_Status_sel>", methods=['GET', 'POST'])
def status_afficher(order_by,ID_Status_sel):
    # EZ 2020.07.19 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_status = GestionStatus()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionstatus()
            # Fichier data_gestion_status.py
            # "order_by" permet de choisir l'ordre d'affichage des status.
            data_status = obj_actions_status.status_afficher_data(order_by,ID_Status_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data status", data_status, "type ", type(data_status))

            # Différencier les messages si la table est vide.
            if not data_status and ID_Status_sel == 0:
                flash("""La table "t_status" est vide. !!""", "warning")
            elif not data_status and ID_Status_sel > 0:
                # Si l'utilisateur change l'ID_Status dans l'URL et que le status n'existe pas,
                flash(f"Le status demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "t_status" est vide.
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données des status affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.17 Envoie la page "HTML" au serveur.
    return render_template("status/status_afficher.html", data=data_status)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /status_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "status_add.html"
# Pour la tester http://127.0.0.1:5005/status_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/status_add", methods=['GET', 'POST'])
def status_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_status = GestionStatus()
            # EZ 2020.07.19 Récupère le contenu du champ dans le formulaire HTML "status_add.html"
            Status = request.form['Status_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.

            # Constitution d'un dictionnaire et insertion dans la BD
            valeurs_insertion_dictionnaire = {"value_Status": Status}
            obj_actions_status.add_status_data(valeurs_insertion_dictionnaire)

            # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Données insérées !!", "success")
            print(f"Données insérées !!")
            # On va interpréter la "route" 'status_afficher', car l'utilisateur
            # doit voir le nouveau status qu'il vient d'insérer. Et on l'affiche de manière
            # à voir le dernier élément inséré.
            return redirect(url_for('status_afficher', order_by = 'DESC', ID_Status_sel=0))

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
    return render_template("status/status_add.html")


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /status_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un status de status par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/status_edit', methods=['POST', 'GET'])
def status_edit ():
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "status_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "ID_Status" du formulaire html "status_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Status"
            # grâce à la variable "ID_Status_edit_html"
            # <a href="{{ url_for('status_edit', ID_Status_edit_html=row.ID_Status) }}">Edit</a>
            ID_Status_edit = request.values['ID_Status_edit_html']


            # Pour afficher dans la console la valeur de "ID_Status_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(ID_Status_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_ID_Status": ID_Status_edit}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_status = GestionStatus()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Status = obj_actions_status.edit_status_data(valeur_select_dictionnaire)
            print("dataIdstatus ", data_ID_Status, "type ", type(data_ID_Status))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Modification d'un status !!!", "success")

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

    return render_template("status/status_edit.html", data=data_ID_Status)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /status_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un status de status par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/status_update', methods=['POST', 'GET'])
def status_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "status_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du status alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "ID_Status" du formulaire html "status_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Status"
            # grâce à la variable "ID_Status_edit_html"
            # <a href="{{ url_for('status_edit', ID_Status_edit_html=row.ID_Status) }}">Edit</a>
            ID_Status_edit = request.values['ID_Status_edit_html']

            # Récupère le contenu du champ "Status" dans le formulaire HTML "statusEdit.html"
            Status = request.values['name_edit_Status_html']

            valeur_edit_list = [{'ID_Status': ID_Status_edit, 'Status': Status}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_update_dictionnaire = {"value_ID_Status": ID_Status_edit, "value_Status": Status}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_status = GestionStatus()

            # La commande MySql est envoyée à la BD
            data_ID_Status = obj_actions_status.update_status_data(valeur_update_dictionnaire)
            # DEBUG bon marché :
            print("dataIdStatus ", data_ID_Status, "type ", type(data_ID_Status))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Valeur status modifiée. ", "success")
            # On affiche les status avec celui qui vient d'être edité en tête de liste. (DESC)
            return redirect(url_for('status_afficher', order_by="ASC", ID_Status_sel=ID_Status_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème status ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_status_html" alors on renvoie le formulaire "EDIT"
    return render_template('status/status_edit.html', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /status_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un status de status par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/status_select_delete', methods=['POST', 'GET'])
def status_select_delete ():
    if request.method == 'GET':
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_status = GestionStatus()
            # OM 2019.04.04 Récupère la valeur de "idstatusDeleteHTML" du formulaire html "statusDelete.html"
            ID_Status_delete = request.args.get('ID_Status_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Status": ID_Status_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Status = obj_actions_status.delete_select_status_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur status_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur status_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('status/status_delete.html', data=data_ID_Status)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /statusUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un status, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/status_delete', methods=['POST', 'GET'])
def status_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_status = GestionStatus()
            # OM 2019.04.02 Récupère la valeur de "ID_Status" du formulaire html "statusAfficher.html"
            ID_Status_delete = request.form['ID_Status_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Status": ID_Status_delete}

            data_status = obj_actions_status.delete_status_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des status des status
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les status
            return redirect(url_for('status_afficher',order_by="ASC",ID_Status_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.19 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "status" de status qui est associé dans "t_status_status".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des status !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce status est associé à des status dans la t_status_status !!! : {erreur}")
                # Afficher la liste des status des status
                return redirect(url_for('status_afficher', order_by="ASC", ID_Status_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur status_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur status_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('status/status_afficher.html', data=data_status)
