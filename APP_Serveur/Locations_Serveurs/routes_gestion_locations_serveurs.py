# routes_gestion_locations_serveurs.py
# EZ 2020.07 Gestions des "routes" FLASK pour la table intermédiaire qui associe les serveurs et les locations.

from flask import render_template, request, flash, session
from APP_Serveur import obj_mon_application
from APP_Serveur.Locations.data_gestion_locations import GestionLocations
from APP_Serveur.Locations_Serveurs.data_gestion_locations_serveurs import GestionLocationsServeurs


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /locations_serveurs_afficher_concat
# Récupère la liste de tous les serveurs et de tous les locations associés aux serveurs.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/locations_serveurs_afficher_concat/<int:ID_Serveur_sel>", methods=['GET', 'POST'])
def locations_serveurs_afficher_concat (ID_Serveur_sel):
    print("ID_Serveur_sel ", ID_Serveur_sel)
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocationsServeurs()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionLocations()
            # Fichier data_gestion_locations.py
            data_locations_serveurs_afficher_concat = obj_actions_locations.locations_serveurs_afficher_data_concat(ID_Serveur_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data locations", data_locations_serveurs_afficher_concat, "type ", type(data_locations_serveurs_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_locations_serveurs_afficher_concat:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données locations affichés dans LocationsServeurs!!", "success")
            else:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_pers_a_location" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("locations_serveurs/locations_serveurs_afficher.html",
                           data=data_locations_serveurs_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.21 Définition d'une "route" /gf_edit_location_serveur_selected
# Récupère la liste de tous les locations du serveur sélectionné.
# Nécessaire pour afficher tous les "TAGS" des locations, ainsi l'utilisateur voit les locations à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_location_serveur_selected", methods=['GET', 'POST'])
def gf_edit_location_serveur_selected ():
    if request.method == "GET":
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocations()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionLocations()
            # Fichier data_gestion_locations.py
            # Pour savoir si la table "t_locations" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(locations_serveurs_modifier_tags_dropbox.html)
            data_locations_all = obj_actions_locations.locations_afficher_data('ASC', 0)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_locations = GestionLocationsServeurs()

            # EZ 2020.07.21 Récupère la valeur de "ID_Serveur" du formulaire html "locations_serveurs_afficher.html"
            # l'utilisateur clique sur le lien "Modifier locations de ce serveur" et on récupère la valeur de "ID_Serveur" grâce à la variable "ID_Serveur_locations_edit_html"
            # <a href="{{ url_for('gf_edit_location_serveur_selected', ID_Serveur_locations_edit_html=row.ID_Serveur) }}">Modifier les locations de ce serveur</a>
            ID_Serveur_locations_edit = request.values['ID_Serveur_locations_edit_html']

            # EZ 2020.07.21 Mémorise l'id du serveur dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_ID_Serveur_locations_edit'] = ID_Serveur_locations_edit

            # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
            valeur_ID_Serveur_selected_dictionnaire = {"value_ID_Serveur_selected": ID_Serveur_locations_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionLocationsServeurs()
            # 1) Sélection du serveur choisi
            # 2) Sélection des locations "déjà" attribués pour le serveur.
            # 3) Sélection des locations "pas encore" attribués pour le serveur choisi.
            # Fichier data_gestion_locations_serveurs.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "locations_serveurs_afficher_data"
            data_location_serveur_selected, data_locations_serveurs_non_attribues, data_locations_serveurs_attribues = \
                obj_actions_locations.locations_serveurs_afficher_data(valeur_ID_Serveur_selected_dictionnaire)

            lst_data_serveur_selected = [item['ID_Serveur'] for item in data_location_serveur_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_serveur_selected  ", lst_data_serveur_selected,
                  type(lst_data_serveur_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les locations qui ne sont pas encore sélectionnés.
            lst_data_locations_serveurs_non_attribues = [item['ID_Location'] for item in data_locations_serveurs_non_attribues]
            session['session_lst_data_locations_serveurs_non_attribues'] = lst_data_locations_serveurs_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_locations_serveurs_non_attribues  ", lst_data_locations_serveurs_non_attribues,
                  type(lst_data_locations_serveurs_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les locations qui sont déjà sélectionnés.
            lst_data_locations_serveurs_old_attribues = [item['ID_Location'] for item in data_locations_serveurs_attribues]
            session['session_lst_data_locations_serveurs_old_attribues'] = lst_data_locations_serveurs_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_locations_serveurs_old_attribues  ", lst_data_locations_serveurs_old_attribues,
                  type(lst_data_locations_serveurs_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_location_serveur_selected", data_location_serveur_selected, "type ", type(data_location_serveur_selected))
            print(" data data_locations_serveurs_non_attribues ", data_locations_serveurs_non_attribues, "type ",
                  type(data_locations_serveurs_non_attribues))
            print(" data_locations_serveurs_attribues ", data_locations_serveurs_attribues, "type ",
                  type(data_locations_serveurs_attribues))

            # Extrait les valeurs contenues dans la table "t_locations", colonne "Location"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'ID_Location
            lst_data_locations_serveurs_non_attribues = [item['Location'] for item in data_locations_serveurs_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_locations gf_edit_location_serveur_selected ", lst_data_locations_serveurs_non_attribues,
                  type(lst_data_locations_serveurs_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_serveur_selected == [None]:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_pers_a_location" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données locations affichées dans LocationsServeurs!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("locations_serveurs/locations_serveurs_modifier_tags_dropbox.html",
                           data_locations=data_locations_all,
                           data_serveur_selected=data_location_serveur_selected,
                           data_locations_attribues=data_locations_serveurs_attribues,
                           data_locations_non_attribues=data_locations_serveurs_non_attribues)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /gf_update_location_serveur_selected
# Récupère la liste de tous les locations du serveur sélectionné.
# Nécessaire pour afficher tous les "TAGS" des locations, ainsi l'utilisateur voit les locations à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_location_serveur_selected", methods=['GET', 'POST'])
def gf_update_location_serveur_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du serveur sélectionné
            ID_Serveur_selected = session['session_ID_Serveur_locations_edit']
            print("session['session_ID_Serveur_locations_edit'] ", session['session_ID_Serveur_locations_edit'])

            # Récupère la liste des locations qui ne sont pas associés au serveur sélectionné.
            old_lst_data_locations_serveurs_non_attribues = session['session_lst_data_locations_serveurs_non_attribues']
            print("old_lst_data_locations_serveurs_non_attribues ", old_lst_data_locations_serveurs_non_attribues)

            # Récupère la liste des locations qui sont associés au serveur sélectionné.
            old_lst_data_locations_serveurs_attribues = session['session_lst_data_locations_serveurs_old_attribues']
            print("old_lst_data_locations_serveurs_old_attribues ", old_lst_data_locations_serveurs_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme locations dans le composant "tags-selector-tagselect"
            # dans le fichier "locations_serveurs_modifier_tags_dropbox.html"
            new_lst_str_locations_serveurs = request.form.getlist('name_select_tags')
            print("new_lst_str_locations_serveurs ", new_lst_str_locations_serveurs)

            # EZ 2020.07.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_pers_a_location_old = list(map(int, new_lst_str_locations_serveurs))
            print("new_lst_pers_a_location ", new_lst_int_pers_a_location_old, "type new_lst_pers_a_location ",
                  type(new_lst_int_pers_a_location_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # EZ 2020.07.29 Une liste de "ID_Location" qui doivent être effacés de la table intermédiaire "t_pers_a_location".
            lst_diff_locations_delete_b = list(
                set(old_lst_data_locations_serveurs_attribues) - set(new_lst_int_pers_a_location_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_locations_delete_b ", lst_diff_locations_delete_b)

            # EZ 2020.07.29 Une liste de "ID_Location" qui doivent être ajoutés à la BD
            lst_diff_locations_insert_a = list(
                set(new_lst_int_pers_a_location_old) - set(old_lst_data_locations_serveurs_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_locations_insert_a ", lst_diff_locations_insert_a)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_locations = GestionLocationsServeurs()

            # Pour le serveur sélectionné, parcourir la liste des locations à INSÉRER dans la "t_pers_a_location".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for ID_Location_ins in lst_diff_locations_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                # et "ID_Location_ins" (l'id du location dans la liste) associé à une variable.
                valeurs_serveur_sel_location_sel_dictionnaire = {"value_FK_Serveur": ID_Serveur_selected,
                                                           "value_FK_Location": ID_Location_ins}
                # Insérer une association entre un(des) location(s) et le serveur sélectionner.
                obj_actions_locations.locations_serveurs_add(valeurs_serveur_sel_location_sel_dictionnaire)

            # Pour le serveur sélectionné, parcourir la liste des locations à EFFACER dans la "t_pers_a_location".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for ID_Location_del in lst_diff_locations_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                # et "ID_Location_del" (l'id du location dans la liste) associé à une variable.
                valeurs_serveur_sel_location_sel_dictionnaire = {"value_FK_Serveur": ID_Serveur_selected,
                                                           "value_FK_Location": ID_Location_del}
                # Effacer une association entre un(des) location(s) et le serveur sélectionner.
                obj_actions_locations.locations_serveurs_delete(valeurs_serveur_sel_location_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe GestionLocations()
            # Fichier data_gestion_locations.py
            # Afficher seulement le serveur dont les locations sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_locations_serveurs_afficher_concat = obj_actions_locations.locations_serveurs_afficher_data_concat(ID_Serveur_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data locations", data_locations_serveurs_afficher_concat, "type ", type(data_locations_serveurs_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_locations_serveurs_afficher_concat == None:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_pers_a_location" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données locations affichées dans LocationsServeurs!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_pers_a_location",
    # on affiche les serveurs et le(urs) location(s) associé(s).
    return render_template("locations_serveurs/locations_serveurs_afficher.html",
                           data=data_locations_serveurs_afficher_concat)
