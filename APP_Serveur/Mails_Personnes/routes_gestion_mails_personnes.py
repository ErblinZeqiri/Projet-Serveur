# routes_gestion_mails_personnes.py
# EZ 2020.07 Gestions des "routes" FLASK pour la table intermédiaire qui associe les personnes et les mails.

from flask import render_template, request, flash, session
from APP_Serveur import obj_mon_application
from APP_Serveur.Mails.data_gestion_mails import GestionMails
from APP_Serveur.Mails_Personnes.data_gestion_mails_personnes import GestionMailsPersonnes


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /mails_personnes_afficher_concat
# Récupère la liste de tous les personnes et de tous les mails associés aux personnes.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/mails_personnes_afficher_concat/<int:ID_Personne_sel>", methods=['GET', 'POST'])
def mails_personnes_afficher_concat (ID_Personne_sel):
    print("ID_Personne_sel ", ID_Personne_sel)
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMailsPersonnes()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionMails()
            # Fichier data_gestion_mails.py
            data_mails_personnes_afficher_concat = obj_actions_mails.mails_personnes_afficher_data_concat(ID_Personne_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data mails", data_mails_personnes_afficher_concat, "type ", type(data_mails_personnes_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_mails_personnes_afficher_concat:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données mails affichés dans MailsPersonnes!!", "success")
            else:
                flash(f"""Le personne demandé n'existe pas. Ou la table "t_pers_a_mail" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("mails_personnes/mails_personnes_afficher.html",
                           data=data_mails_personnes_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.21 Définition d'une "route" /gf_edit_mail_personne_selected
# Récupère la liste de tous les mails du personne sélectionné.
# Nécessaire pour afficher tous les "TAGS" des mails, ainsi l'utilisateur voit les mails à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_mail_personne_selected", methods=['GET', 'POST'])
def gf_edit_mail_personne_selected ():
    if request.method == "GET":
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMails()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionMails()
            # Fichier data_gestion_mails.py
            # Pour savoir si la table "t_mails" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(locations_serveurs_modifier_tags_dropbox.html)
            data_mails_all = obj_actions_mails.mails_afficher_data('ASC', 0)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_mails = GestionMailsPersonnes()

            # EZ 2020.07.21 Récupère la valeur de "ID_Personne" du formulaire html "mails_personnes_afficher.html"
            # l'utilisateur clique sur le lien "Modifier mails de ce personne" et on récupère la valeur de "ID_Personne" grâce à la variable "ID_Personne_mails_edit_html"
            # <a href="{{ url_for('gf_edit_mail_personne_selected', ID_Personne_mails_edit_html=row.ID_Personne) }}">Modifier les mails de ce personne</a>
            ID_Personne_mails_edit = request.values['ID_Personne_mails_edit_html']

            # EZ 2020.07.21 Mémorise l'id du personne dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_ID_Personne_mails_edit'] = ID_Personne_mails_edit

            # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
            valeur_ID_Personne_selected_dictionnaire = {"value_ID_Personne_selected": ID_Personne_mails_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionMailsPersonnes()
            # 1) Sélection du personne choisi
            # 2) Sélection des mails "déjà" attribués pour le personne.
            # 3) Sélection des mails "pas encore" attribués pour le personne choisi.
            # Fichier data_gestion_mails_personnes.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "mails_personnes_afficher_data"
            data_mail_personne_selected, data_mails_personnes_non_attribues, data_mails_personnes_attribues = \
                obj_actions_mails.mails_personnes_afficher_data(valeur_ID_Personne_selected_dictionnaire)

            lst_data_personne_selected = [item['ID_Personne'] for item in data_mail_personne_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personne_selected  ", lst_data_personne_selected,
                  type(lst_data_personne_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les mails qui ne sont pas encore sélectionnés.
            lst_data_mails_personnes_non_attribues = [item['ID_Mail'] for item in data_mails_personnes_non_attribues]
            session['session_lst_data_mails_personnes_non_attribues'] = lst_data_mails_personnes_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_mails_personnes_non_attribues  ", lst_data_mails_personnes_non_attribues,
                  type(lst_data_mails_personnes_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les mails qui sont déjà sélectionnés.
            lst_data_mails_personnes_old_attribues = [item['ID_Mail'] for item in data_mails_personnes_attribues]
            session['session_lst_data_mails_personnes_old_attribues'] = lst_data_mails_personnes_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_mails_personnes_old_attribues  ", lst_data_mails_personnes_old_attribues,
                  type(lst_data_mails_personnes_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_mail_personne_selected", data_mail_personne_selected, "type ", type(data_mail_personne_selected))
            print(" data data_mails_personnes_non_attribues ", data_mails_personnes_non_attribues, "type ",
                  type(data_mails_personnes_non_attribues))
            print(" data_mails_personnes_attribues ", data_mails_personnes_attribues, "type ",
                  type(data_mails_personnes_attribues))

            # Extrait les valeurs contenues dans la table "t_mails", colonne "Adresse_Mail"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'ID_Mail
            lst_data_mails_personnes_non_attribues = [item['Adresse_Mail'] for item in data_mails_personnes_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_mails gf_edit_mail_personne_selected ", lst_data_mails_personnes_non_attribues,
                  type(lst_data_mails_personnes_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_personne_selected == [None]:
                flash(f"""Le personne demandé n'existe pas. Ou la table "t_pers_a_mail" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données mails affichées dans MailsPersonnes!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("mails_personnes/mails_personnes_modifier_tags_dropbox.html",
                           data_mails=data_mails_all,
                           data_personne_selected=data_mail_personne_selected,
                           data_mails_attribues=data_mails_personnes_attribues,
                           data_mails_non_attribues=data_mails_personnes_non_attribues)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /gf_update_mail_personne_selected
# Récupère la liste de tous les mails du personne sélectionné.
# Nécessaire pour afficher tous les "TAGS" des mails, ainsi l'utilisateur voit les mails à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_mail_personne_selected", methods=['GET', 'POST'])
def gf_update_mail_personne_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du personne sélectionné
            ID_Personne_selected = session['session_ID_Personne_mails_edit']
            print("session['session_ID_Personne_mails_edit'] ", session['session_ID_Personne_mails_edit'])

            # Récupère la liste des mails qui ne sont pas associés au personne sélectionné.
            old_lst_data_mails_personnes_non_attribues = session['session_lst_data_mails_personnes_non_attribues']
            print("old_lst_data_mails_personnes_non_attribues ", old_lst_data_mails_personnes_non_attribues)

            # Récupère la liste des mails qui sont associés au personne sélectionné.
            old_lst_data_mails_personnes_attribues = session['session_lst_data_mails_personnes_old_attribues']
            print("old_lst_data_mails_personnes_old_attribues ", old_lst_data_mails_personnes_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme mails dans le composant "tags-selector-tagselect"
            # dans le fichier "locations_serveurs_modifier_tags_dropbox.html"
            new_lst_str_mails_personnes = request.form.getlist('name_select_tags')
            print("new_lst_str_mails_personnes ", new_lst_str_mails_personnes)

            # EZ 2020.07.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_pers_a_mail_old = list(map(int, new_lst_str_mails_personnes))
            print("new_lst_pers_a_mail ", new_lst_int_pers_a_mail_old, "type new_lst_pers_a_mail ",
                  type(new_lst_int_pers_a_mail_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # EZ 2020.07.29 Une liste de "ID_Mail" qui doivent être effacés de la table intermédiaire "t_pers_a_mail".
            lst_diff_mails_delete_b = list(
                set(old_lst_data_mails_personnes_attribues) - set(new_lst_int_pers_a_mail_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_mails_delete_b ", lst_diff_mails_delete_b)

            # EZ 2020.07.29 Une liste de "ID_Mail" qui doivent être ajoutés à la BD
            lst_diff_mails_insert_a = list(
                set(new_lst_int_pers_a_mail_old) - set(old_lst_data_mails_personnes_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_mails_insert_a ", lst_diff_mails_insert_a)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_mails = GestionMailsPersonnes()

            # Pour le personne sélectionné, parcourir la liste des mails à INSÉRER dans la "t_pers_a_mail".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for ID_Mail_ins in lst_diff_mails_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
                # et "ID_Mail_ins" (l'id du mail dans la liste) associé à une variable.
                valeurs_personne_sel_mail_sel_dictionnaire = {"value_FK_Personne": ID_Personne_selected,
                                                           "value_FK_Mail": ID_Mail_ins}
                # Insérer une association entre un(des) mail(s) et le personne sélectionner.
                obj_actions_mails.mails_personnes_add(valeurs_personne_sel_mail_sel_dictionnaire)

            # Pour le personne sélectionné, parcourir la liste des mails à EFFACER dans la "t_pers_a_mail".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for ID_Mail_del in lst_diff_mails_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
                # et "ID_Mail_del" (l'id du mail dans la liste) associé à une variable.
                valeurs_personne_sel_mail_sel_dictionnaire = {"value_FK_Personne": ID_Personne_selected,
                                                           "value_FK_Mail": ID_Mail_del}
                # Effacer une association entre un(des) mail(s) et le personne sélectionner.
                obj_actions_mails.mails_personnes_delete(valeurs_personne_sel_mail_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe GestionMails()
            # Fichier data_gestion_mails.py
            # Afficher seulement le personne dont les mails sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_mails_personnes_afficher_concat = obj_actions_mails.mails_personnes_afficher_data_concat(ID_Personne_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data mails", data_mails_personnes_afficher_concat, "type ", type(data_mails_personnes_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_mails_personnes_afficher_concat == None:
                flash(f"""Le personne demandé n'existe pas. Ou la table "t_pers_a_mail" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données mails affichées dans MailsPersonnes!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_pers_a_mail",
    # on affiche les personnes et le(urs) mail(s) associé(s).
    return render_template("mails_personnes/mails_personnes_afficher.html",
                           data=data_mails_personnes_afficher_concat)
