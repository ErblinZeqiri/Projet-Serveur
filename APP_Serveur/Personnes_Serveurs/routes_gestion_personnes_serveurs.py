# routes_gestion_personnes_serveurs.py
# EZ 2020.07 Gestions des "routes" FLASK pour la table intermédiaire qui associe les serveurs et les personnes.

from flask import render_template, request, flash, session
from APP_Serveur import obj_mon_application
from APP_Serveur.Demandeurs.data_gestion_demandeurs import GestionPersonnes
from APP_Serveur.Personnes_Serveurs.data_gestion_personnes_serveurs import GestionPersonnesServeurs


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /personnes_serveurs_afficher_concat
# Récupère la liste de tous les serveurs et de tous les personnes associés aux serveurs.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/personnes_serveurs_afficher_concat/<int:ID_Serveur_sel>", methods=['GET', 'POST'])
def personnes_serveurs_afficher_concat (ID_Serveur_sel):
    print("ID_Serveur_sel ", ID_Serveur_sel)
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnesServeurs()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionpersonnes()
            # Fichier data_gestion_mails.py
            data_personnes_serveurs_afficher_concat = obj_actions_personnes.personnes_serveurs_afficher_data_concat(ID_Serveur_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data personnes", data_personnes_serveurs_afficher_concat, "type ", type(data_personnes_serveurs_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_personnes_serveurs_afficher_concat:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personnes affichés dans PersonnesServeurs!!", "success")
            else:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_personnes_serveurs" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("personnes_serveurs/personnes_serveurs_afficher.html",
                           data=data_personnes_serveurs_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.21 Définition d'une "route" /gf_edit_personne_serveur_selected
# Récupère la liste de tous les personnes du serveur sélectionné.
# Nécessaire pour afficher tous les "TAGS" des personnes, ainsi l'utilisateur voit les personnes à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_personne_serveur_selected", methods=['GET', 'POST'])
def gf_edit_personne_serveur_selected ():
    if request.method == "GET":
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnes()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionPersonne()
            # Fichier data_gestion_mails.py
            # Pour savoir si la table "t_personne" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(personnes_serveurs_modifier_tags_dropbox.html)
            data_personnes_all = obj_actions_personnes.personnes_afficher_data('ASC', 0)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_personnes = GestionPersonnesServeurs()

            # EZ 2020.07.21 Récupère la valeur de "ID_Serveur" du formulaire html "personnes_serveurs_afficher.html"
            # l'utilisateur clique sur le lien "Modifier personnes de ce serveur" et on récupère la valeur de "ID_Serveur" grâce à la variable "ID_Serveur_personnes_edit_html"
            # <a href="{{ url_for('gf_edit_personne_serveur_selected', ID_Serveur_personnes_edit_html=row.ID_Serveur) }}">Modifier les personnes de ce serveur</a>
            ID_Serveur_personnes_edit = request.values['ID_Serveur_personnes_edit_html']

            # EZ 2020.07.21 Mémorise l'id du serveur dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_ID_Serveur_personnes_edit'] = ID_Serveur_personnes_edit

            # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
            valeur_ID_Serveur_selected_dictionnaire = {"value_ID_Serveur_selected": ID_Serveur_personnes_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionPersonnesServeurs()
            # 1) Sélection du serveur choisi
            # 2) Sélection des personnes "déjà" attribués pour le serveur.
            # 3) Sélection des personnes "pas encore" attribués pour le serveur choisi.
            # Fichier data_gestion_personnes_serveurs.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "personnes_serveurs_afficher_data"
            data_personne_serveur_selected, data_personnes_serveurs_non_attribues, data_personnes_serveurs_attribues = \
                obj_actions_personnes.personnes_serveurs_afficher_data(valeur_ID_Serveur_selected_dictionnaire)

            lst_data_serveur_selected = [item['ID_Serveur'] for item in data_personne_serveur_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_serveur_selected  ", lst_data_serveur_selected,
                  type(lst_data_serveur_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personnes qui ne sont pas encore sélectionnés.
            lst_data_personnes_serveurs_non_attribues = [item['ID_Personne'] for item in data_personnes_serveurs_non_attribues]
            session['session_lst_data_personnes_serveurs_non_attribues'] = lst_data_personnes_serveurs_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personnes_serveurs_non_attribues  ", lst_data_personnes_serveurs_non_attribues,
                  type(lst_data_personnes_serveurs_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personnes qui sont déjà sélectionnés.
            lst_data_personnes_serveurs_old_attribues = [item['ID_Personne'] for item in data_personnes_serveurs_attribues]
            session['session_lst_data_personnes_serveurs_old_attribues'] = lst_data_personnes_serveurs_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personnes_serveurs_old_attribues  ", lst_data_personnes_serveurs_old_attribues,
                  type(lst_data_personnes_serveurs_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_personne_serveur_selected", data_personne_serveur_selected, "type ", type(data_personne_serveur_selected))
            print(" data data_personnes_serveurs_non_attribues ", data_personnes_serveurs_non_attribues, "type ",
                  type(data_personnes_serveurs_non_attribues))
            print(" data_personnes_serveurs_attribues ", data_personnes_serveurs_attribues, "type ",
                  type(data_personnes_serveurs_attribues))

            # Extrait les valeurs contenues dans la table "t_personne", colonne "intitule_personne"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_personne
            lst_data_personnes_serveurs_non_attribues = [item['Nom_Pers'] for item in data_personnes_serveurs_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_personnes gf_edit_personne_serveur_selected ", lst_data_personnes_serveurs_non_attribues,
                  type(lst_data_personnes_serveurs_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_serveur_selected == [None]:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_personnes_serveurs" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personnes affichées dans personnesserveurs!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("personnes_serveurs/personnes_serveurs_modifier_tags_dropbox.html",
                           data_personnes=data_personnes_all,
                           data_serveur_selected=data_personne_serveur_selected,
                           data_personnes_attribues=data_personnes_serveurs_attribues,
                           data_personnes_non_attribues=data_personnes_serveurs_non_attribues)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /gf_update_personne_serveur_selected
# Récupère la liste de tous les personnes du serveur sélectionné.
# Nécessaire pour afficher tous les "TAGS" des personnes, ainsi l'utilisateur voit les personnes à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_personne_serveur_selected", methods=['GET', 'POST'])
def gf_update_personne_serveur_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du serveur sélectionné
            ID_Serveur_selected = session['session_ID_Serveur_personnes_edit']
            print("session['session_ID_Serveur_personnes_edit'] ", session['session_ID_Serveur_personnes_edit'])

            # Récupère la liste des personnes qui ne sont pas associés au serveur sélectionné.
            old_lst_data_personnes_serveurs_non_attribues = session['session_lst_data_personnes_serveurs_non_attribues']
            print("old_lst_data_personnes_serveurs_non_attribues ", old_lst_data_personnes_serveurs_non_attribues)

            # Récupère la liste des personnes qui sont associés au serveur sélectionné.
            old_lst_data_personnes_serveurs_attribues = session['session_lst_data_personnes_serveurs_old_attribues']
            print("old_lst_data_personnes_serveurs_old_attribues ", old_lst_data_personnes_serveurs_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme personnes dans le composant "tags-selector-tagselect"
            # dans le fichier "personnes_serveurs_modifier_tags_dropbox.html"
            new_lst_str_personnes_serveurs = request.form.getlist('name_select_tags')
            print("new_lst_str_personnes_serveurs ", new_lst_str_personnes_serveurs)

            # EZ 2020.07.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_personnes_serveurs_old = list(map(int, new_lst_str_personnes_serveurs))
            print("new_lst_personnes_serveurs ", new_lst_int_personnes_serveurs_old, "type new_lst_personnes_serveurs ",
                  type(new_lst_int_personnes_serveurs_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # EZ 2020.07.29 Une liste de "id_personne" qui doivent être effacés de la table intermédiaire "t_personnes_serveurs".
            lst_diff_personnes_delete_b = list(
                set(old_lst_data_personnes_serveurs_attribues) - set(new_lst_int_personnes_serveurs_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_personnes_delete_b ", lst_diff_personnes_delete_b)

            # EZ 2020.07.29 Une liste de "id_personne" qui doivent être ajoutés à la BD
            lst_diff_personnes_insert_a = list(
                set(new_lst_int_personnes_serveurs_old) - set(old_lst_data_personnes_serveurs_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_personnes_insert_a ", lst_diff_personnes_insert_a)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnesServeurs()

            # Pour le serveur sélectionné, parcourir la liste des personnes à INSÉRER dans la "t_personnes_serveurs".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_personne_ins in lst_diff_personnes_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                # et "id_personne_ins" (l'id du personne dans la liste) associé à une variable.
                valeurs_serveur_sel_personne_sel_dictionnaire = {"value_fk_serveur": ID_Serveur_selected,
                                                           "value_fk_personne": id_personne_ins}
                # Insérer une association entre un(des) personne(s) et le serveur sélectionner.
                obj_actions_personnes.personnes_serveurs_add(valeurs_serveur_sel_personne_sel_dictionnaire)

            # Pour le serveur sélectionné, parcourir la liste des personnes à EFFACER dans la "t_personnes_serveurs".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_personne_del in lst_diff_personnes_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                # et "id_personne_del" (l'id du personne dans la liste) associé à une variable.
                valeurs_serveur_sel_personne_sel_dictionnaire = {"value_fk_serveur": ID_Serveur_selected,
                                                           "value_fk_personne": id_personne_del}
                # Effacer une association entre un(des) personne(s) et le serveur sélectionner.
                obj_actions_personnes.personnes_serveurs_delete(valeurs_serveur_sel_personne_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe GestionPersonne()
            # Fichier data_gestion_mails.py
            # Afficher seulement le serveur dont les personnes sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_personnes_serveurs_afficher_concat = obj_actions_personnes.personnes_serveurs_afficher_data_concat(ID_Serveur_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data personnes", data_personnes_serveurs_afficher_concat, "type ", type(data_personnes_serveurs_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_personnes_serveurs_afficher_concat == None:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_personnes_serveurs" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personnes affichées dans personnesserveurs!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_personnes_serveurs",
    # on affiche les serveurs et le(urs) personne(s) associé(s).
    return render_template("personnes_serveurs/personnes_serveurs_afficher.html",
                           data=data_personnes_serveurs_afficher_concat)
