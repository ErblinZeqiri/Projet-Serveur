# routes_gestion_demandeurs.py
# EZ 2020.07.16 Gestions des "routes" FLASK pour les Personnes.

from flask import render_template, flash, redirect, url_for, request
from APP_Serveur import obj_mon_application
from APP_Serveur.Demandeurs.data_gestion_demandeurs import GestionPersonnes
from APP_Serveur.DATABASE.erreurs import *
# EZ 2020.07.11 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /personnes_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:5005/personnes_afficher
# order_by : ASC : Ascendant, DESC : Descendant
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/personnes_afficher/<string:order_by>/<int:ID_Personne_sel>", methods=['GET', 'POST'])
def personnes_afficher(order_by,ID_Personne_sel):
    # EZ 2020.07.19 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnes()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionpersonnes()
            # Fichier data_gestion_demandeurs.py
            # "order_by" permet de choisir l'ordre d'affichage des personnes.
            data_personnes = obj_actions_personnes.personnes_afficher_data(order_by,ID_Personne_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data personnes", data_personnes, "type ", type(data_personnes))

            # Différencier les messages si la table est vide.
            if not data_personnes and ID_Personne_sel == 0:
                flash("""La table "t_personne" est vide. !!""", "warning")
            elif not data_personnes and ID_Personne_sel > 0:
                # Si l'utilisateur change l'ID_Personne dans l'URL et que le personne n'existe pas,
                flash(f"Le demandeur demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "t_personne" est vide.
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données des demandeurs affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.17 Envoie la page "HTML" au serveur.
    return render_template("personnes/personnes_afficher.html", data=data_personnes)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /personnes_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "demandeurs_add.html"
# Pour la tester http://127.0.0.1:5005/personnes_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/personnes_add", methods=['GET', 'POST'])
def personnes_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnes()
            # EZ 2020.07.19 Récupère le contenu du champ dans le formulaire HTML "demandeurs_add.html"
            Nom_Pers = request.form['Nom_Pers_html']
            Prenom_Pers = request.form['Prenom_Pers_html']
            Date_Naissance_Pers = request.form['Date_Naissance_Pers_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            Nom_Pers):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")
                # On doit afficher à nouveau le formulaire "personnes_add.html" à cause des erreurs de "claviotage"
                return render_template("personnes/personnes_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_Nom_Pers": Nom_Pers,
                                                  "value_Prenom_Pers": Prenom_Pers,
                                                  "value_Date_Naissance_Pers": Date_Naissance_Pers}
                obj_actions_personnes.add_personne_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'personnes_afficher', car l'utilisateur
                # doit voir le nouveau personne qu'il vient d'insérer. Et on l'affiche de manière
                # à voir le dernier élément inséré.
                return redirect(url_for('personnes_afficher', order_by = 'DESC', ID_Personne_sel=0))

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
    return render_template("personnes/personnes_add.html")


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /personnes_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un personne de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/personnes_edit', methods=['POST', 'GET'])
def personnes_edit ():
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "personnes_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "ID_Personne" du formulaire html "personnes_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Personne"
            # grâce à la variable "ID_Personne_edit_html"
            # <a href="{{ url_for('personnes_edit', ID_Personne_edit_html=row.ID_Personne) }}">Edit</a>
            ID_Personne_edit = request.values['ID_Personne_edit_html']


            # Pour afficher dans la console la valeur de "ID_Personne_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(ID_Personne_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_ID_Personne": ID_Personne_edit}

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnes()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Personne = obj_actions_personnes.edit_personne_data(valeur_select_dictionnaire)
            print("dataIdPersonne ", data_ID_Personne, "type ", type(data_ID_Personne))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Modification d'un demandeur !!!", "success")

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

    return render_template("personnes/personnes_edit.html", data=data_ID_Personne)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /personnes_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un personne de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/personnes_update', methods=['POST', 'GET'])
def personnes_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # EZ 2020.07.17 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "personnes_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du personne alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "ID_Personne" du formulaire html "personnes_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "ID_Personne"
            # grâce à la variable "ID_Personne_edit_html"
            # <a href="{{ url_for('personnes_edit', ID_Personne_edit_html=row.ID_Personne) }}">Edit</a>
            ID_Personne_edit = request.values['ID_Personne_edit_html']

            # Récupère le contenu du champ "intitule_personne" dans le formulaire HTML "personnesEdit.html"
            Nom_Pers = request.values['name_edit_Nom_Pers_html']
            Prenom_Pers = request.values['name_edit_Prenom_Pers_html']
            Date_Naissance_Pers = request.values['name_edit_Date_Naissance_Pers_html']

            valeur_edit_list = [{'ID_Personne': ID_Personne_edit,
                                 'Nom_Pers': Nom_Pers,
                                 'Prenom_Pers': Prenom_Pers,
                                 'Date_Naissance_Pers': Date_Naissance_Pers}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            Nom_Pers):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_personne" dans le formulaire HTML "personnesEdit.html"
                # name_personne = request.values['name_edit_intitule_personne_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")

                # On doit afficher à nouveau le formulaire "personnes_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "personnes_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'ID_Personne': 13, 'intitule_personne': 'philosophique'}]
                valeur_edit_list = [{'ID_Personne': ID_Personne_edit,
                                     'Nom_Pers': Nom_Pers,
                                     'Prenom_Pers': Prenom_Pers,
                                     'Date_Naissance_Pers': Date_Naissance_Pers}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "personnes_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('personnes/personnes_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_ID_Personne": ID_Personne_edit,
                                              "value_Nom_Pers": Nom_Pers,
                                              "value_Prenom_Pers": Prenom_Pers,
                                              "value_Date_Naissance_Pers": Date_Naissance_Pers}

                # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_personnes = GestionPersonnes()

                # La commande MySql est envoyée à la BD
                data_ID_Personne = obj_actions_personnes.update_personne_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdPersonne ", data_ID_Personne, "type ", type(data_ID_Personne))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Valeur demandeur modifiée. ", "success")
                # On affiche les personnes avec celui qui vient d'être edité en tête de liste. (DESC)
                return redirect(url_for('personnes_afficher', order_by="ASC", ID_Personne_sel=ID_Personne_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème personnes ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_personne_html" alors on renvoie le formulaire "EDIT"
    return render_template('personnes/personnes_edit.html', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.17 Définition d'une "route" /personnes_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un personne de serveurs par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/personnes_select_delete', methods=['POST', 'GET'])
def personnes_select_delete ():
    if request.method == 'GET':
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnes()
            # OM 2019.04.04 Récupère la valeur de "idpersonneDeleteHTML" du formulaire html "personnesDelete.html"
            ID_Personne_delete = request.args.get('ID_Personne_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Personne": ID_Personne_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Personne = obj_actions_personnes.delete_select_personne_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur personnes_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur personnes_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('personnes/personnes_delete.html', data=data_ID_Personne)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /personnesUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un personne, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/personnes_delete', methods=['POST', 'GET'])
def personnes_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnes()
            # OM 2019.04.02 Récupère la valeur de "ID_Personne" du formulaire html "personnesAfficher.html"
            ID_Personne_delete = request.form['ID_Personne_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Personne": ID_Personne_delete}

            data_personnes = obj_actions_personnes.delete_personne_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des personnes des serveurs
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les personnes
            return redirect(url_for('personnes_afficher',order_by="ASC",ID_Personne_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.19 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "personne" de serveurs qui est associé dans "t_personnes_films".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des serveurs !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce personne est associé à des serveurs dans la t_personnes_films !!! : {erreur}")
                # Afficher la liste des personnes des serveurs
                return redirect(url_for('personnes_afficher', order_by="ASC", ID_Personne_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur personnes_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur personnes_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('personnes/personnes_afficher.html', data=data_personnes)
