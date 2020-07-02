# routes_gestion_mails.py
# EZ 2020.07.16 Gestions des "routes" FLASK pour les mails.

from flask import render_template, flash, redirect, url_for, request
from APP_Serveur import obj_mon_application
from APP_Serveur.Mails.data_gestion_mails import GestionMails
from APP_Serveur.DATABASE.erreurs import *
# EZ 2020.07.11 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /mails_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:5005/mails_afficher
# order_by : ASC : Ascendant, DESC : Descendant
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/mails_afficher/<string:order_by>/<int:ID_Mail_sel>", methods=['GET', 'POST'])
def mails_afficher(order_by,ID_Mail_sel):
    # EZ 2020.07.19 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMails()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionMails()
            # Fichier data_gestion_mails.py
            # "order_by" permet de choisir l'ordre d'affichage des mails.
            data_mails = obj_actions_mails.mails_afficher_data(order_by,ID_Mail_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data mails", data_mails, "type ", type(data_mails))

            # Différencier les messages si la table est vide.
            if not data_mails and ID_Mail_sel == 0:
                flash("""La table "t_mail" est vide. !!""", "warning")
            elif not data_mails and ID_Mail_sel > 0:
                # Si l'utilisateur change l'ID_Mail dans l'URL et que le mail n'existe pas,
                flash(f"Le mail demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "t_mails" est vide.
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données des mails affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.17 Envoie la page "HTML" au serveur.
    return render_template("mails/mails_afficher.html", data=data_mails)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /mails_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "mails_add.html"
# Pour la tester http://127.0.0.1:5005/mails_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/mails_add", methods=['GET', 'POST'])
def mails_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMails()
            # EZ 2020.07.19 Récupère le contenu du champ dans le formulaire HTML "mails_add.html"
            Adresse_Mail = request.form['Adresse_Mail_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$",
                            Adresse_Mail):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de caractères spéciaux, d'espace, "
                      f"d'apostrophe, de double trait union et ne doit pas être vide. "
                      f"Il doit contenir un point et un @ au minimum.", "danger")
                # On doit afficher à nouveau le formulaire "mails_add.html" à cause des erreurs de "claviotage"
                return render_template("mails/mails_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_Adresse_Mail": Adresse_Mail}
                obj_actions_mails.add_mail_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'mails_afficher', car l'utilisateur
                # doit voir le nouveau mail qu'il vient d'insérer. Et on l'affiche de manière
                # à voir le dernier élément inséré.
                return redirect(url_for('mails_afficher', order_by = 'DESC', ID_Mail_sel=0))

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
    return render_template("mails/mails_add.html")


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /mails_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un mail de mails par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/mails_edit', methods=['POST', 'GET'])
def mails_edit ():
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "mails_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "ID_Mail" du formulaire html "mails_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Mail"
            # grâce à la variable "ID_Mail_edit_html"
            # <a href="{{ url_for('mails_edit', ID_Mail_edit_html=row.ID_Mail) }}">Edit</a>
            ID_Mail_edit = request.values['ID_Mail_edit_html']


            # Pour afficher dans la console la valeur de "ID_Mail_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(ID_Mail_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_ID_Mail": ID_Mail_edit}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMails()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Mail = obj_actions_mails.edit_mail_data(valeur_select_dictionnaire)
            print("dataIdmail ", data_ID_Mail, "type ", type(data_ID_Mail))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Modification d'un mail !!!", "success")

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

    return render_template("mails/mails_edit.html", data=data_ID_Mail)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /mails_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un mail de mails par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/mails_update', methods=['POST', 'GET'])
def mails_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "mails_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du mail alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "ID_Mail" du formulaire html "mails_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Mail"
            # grâce à la variable "ID_Mail_edit_html"
            # <a href="{{ url_for('mails_edit', ID_Mail_edit_html=row.ID_Mail) }}">Edit</a>
            ID_Mail_edit = request.values['ID_Mail_edit_html']

            # Récupère le contenu du champ "intitule_mail" dans le formulaire HTML "mailsEdit.html"
            Adresse_Mail = request.values['name_edit_Adresse_Mail_html']

            valeur_edit_list = [{'ID_Mail': ID_Mail_edit, 'Adresse_Mail': Adresse_Mail}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match(r"[^@]+@[^@]+\.[^@]+",
                            Adresse_Mail):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_mail" dans le formulaire HTML "mailsEdit.html"
                # name_mail = request.values['name_edit_intitule_mail_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de caractères spéciaux, d'espace, "
                      f"d'apostrophe, de double trait union et ne doit pas être vide. "
                      f"Il doit contenir un point et un @ au minimum.", "danger")

                # On doit afficher à nouveau le formulaire "mails_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "mails_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'ID_Mail': 13, 'intitule_mail': 'philosophique'}]
                valeur_edit_list = [{'ID_Mail': ID_Mail_edit,'Adresse_Mail': Adresse_Mail}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "mails_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('mails/mails_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_ID_Mail": ID_Mail_edit, "value_Adresse_Mail": Adresse_Mail}

                # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_mails = GestionMails()

                # La commande MySql est envoyée à la BD
                data_ID_Mail = obj_actions_mails.update_mail_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdmail ", data_ID_Mail, "type ", type(data_ID_Mail))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Valeur mail modifiée. ", "success")
                # On affiche les mails avec celui qui vient d'être edité en tête de liste. (DESC)
                return redirect(url_for('mails_afficher', order_by="ASC", ID_Mail_sel=ID_Mail_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème mails ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_mail_html" alors on renvoie le formulaire "EDIT"
    return render_template('mails/mails_edit.html', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /mails_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un mail de mails par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/mails_select_delete', methods=['POST', 'GET'])
def mails_select_delete ():
    if request.method == 'GET':
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMails()
            # OM 2019.04.04 Récupère la valeur de "idmailDeleteHTML" du formulaire html "mailsDelete.html"
            ID_Mail_delete = request.args.get('ID_Mail_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Mail": ID_Mail_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Mail = obj_actions_mails.delete_select_mail_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur mails_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur mails_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('mails/mails_delete.html', data=data_ID_Mail)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /mailsUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un mail, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/mails_delete', methods=['POST', 'GET'])
def mails_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMails()
            # OM 2019.04.02 Récupère la valeur de "ID_Mail" du formulaire html "mailsAfficher.html"
            ID_Mail_delete = request.form['ID_Mail_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Mail": ID_Mail_delete}

            data_mails = obj_actions_mails.delete_mail_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des mails des mails
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les mails
            return redirect(url_for('mails_afficher',order_by="ASC",ID_Mail_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.19 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "mail" de mails qui est associé dans "t_mails_mails".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des mails !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce mail est associé à des mails dans la t_mails_mails !!! : {erreur}")
                # Afficher la liste des mails des mails
                return redirect(url_for('mails_afficher', order_by="ASC", ID_Mail_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur mails_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur mails_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('mails/mails_afficher.html', data=data_mails)
