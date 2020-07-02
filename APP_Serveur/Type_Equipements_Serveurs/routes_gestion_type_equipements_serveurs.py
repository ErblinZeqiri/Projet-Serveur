# routes_gestion_type_equipements_serveurs.py
# EZ 2020.07 Gestions des "routes" FLASK pour la table intermédiaire qui associe les serveurs et les type_equipements.

from flask import render_template, request, flash, session
from APP_Serveur import obj_mon_application
from APP_Serveur.Type_Equipements.data_gestion_type_equipements import GestionType_Equipements
from APP_Serveur.Type_Equipements_Serveurs.data_gestion_type_equipements_serveurs import GestionType_EquipementsServeurs


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /type_equipements_serveurs_afficher_concat
# Récupère la liste de tous les serveurs et de tous les type_equipements associés aux serveurs.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/type_equipements_serveurs_afficher_concat/<int:ID_Serveur_sel>", methods=['GET', 'POST'])
def type_equipements_serveurs_afficher_concat (ID_Serveur_sel):
    print("ID_Serveur_sel ", ID_Serveur_sel)
    if request.method == "GET":
        try:
            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_type_equipements = GestionType_EquipementsServeurs()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionType_Equipements()
            # Fichier data_gestion_type_equipements.py
            data_type_equipements_serveurs_afficher_concat = obj_actions_type_equipements.type_equipements_serveurs_afficher_data_concat(ID_Serveur_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data type_equipements", data_type_equipements_serveurs_afficher_concat, "type ", type(data_type_equipements_serveurs_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_type_equipements_serveurs_afficher_concat:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données type_equipements affichés dans Type_EquipementsServeurs!!", "success")
            else:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_pers_a_type_equipement" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("type_equipements_serveurs/type_equipements_serveurs_afficher.html",
                           data=data_type_equipements_serveurs_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.21 Définition d'une "route" /gf_edit_type_equipement_serveur_selected
# Récupère la liste de tous les type_equipements du serveur sélectionné.
# Nécessaire pour afficher tous les "TAGS" des type_equipements, ainsi l'utilisateur voit les type_equipements à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_type_equipement_serveur_selected", methods=['GET', 'POST'])
def gf_edit_type_equipement_serveur_selected ():
    if request.method == "GET":
        try:

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_type_equipements = GestionType_Equipements()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionType_Equipements()
            # Fichier data_gestion_type_equipements.py
            # Pour savoir si la table "t_type_equipements" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(type_equipements_serveurs_modifier_tags_dropbox.html)
            data_type_equipements_all = obj_actions_type_equipements.type_equipements_afficher_data('ASC', 0)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_type_equipements = GestionType_EquipementsServeurs()

            # EZ 2020.07.21 Récupère la valeur de "ID_Serveur" du formulaire html "type_equipements_serveurs_afficher.html"
            # l'utilisateur clique sur le lien "Modifier type_equipements de ce serveur" et on récupère la valeur de "ID_Serveur" grâce à la variable "ID_Serveur_type_equipements_edit_html"
            # <a href="{{ url_for('gf_edit_type_equipement_serveur_selected', ID_Serveur_type_equipements_edit_html=row.ID_Serveur) }}">Modifier les type_equipements de ce serveur</a>
            ID_Serveur_type_equipements_edit = request.values['ID_Serveur_type_equipements_edit_html']

            # EZ 2020.07.21 Mémorise l'id du serveur dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_ID_Serveur_type_equipements_edit'] = ID_Serveur_type_equipements_edit

            # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
            valeur_ID_Serveur_selected_dictionnaire = {"value_ID_Serveur_selected": ID_Serveur_type_equipements_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionType_EquipementsServeurs()
            # 1) Sélection du serveur choisi
            # 2) Sélection des type_equipements "déjà" attribués pour le serveur.
            # 3) Sélection des type_equipements "pas encore" attribués pour le serveur choisi.
            # Fichier data_gestion_type_equipements_serveurs.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "type_equipements_serveurs_afficher_data"
            data_type_equipement_serveur_selected, data_type_equipements_serveurs_non_attribues, data_type_equipements_serveurs_attribues = \
                obj_actions_type_equipements.type_equipements_serveurs_afficher_data(valeur_ID_Serveur_selected_dictionnaire)

            lst_data_serveur_selected = [item['ID_Serveur'] for item in data_type_equipement_serveur_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_serveur_selected  ", lst_data_serveur_selected,
                  type(lst_data_serveur_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les type_equipements qui ne sont pas encore sélectionnés.
            lst_data_type_equipements_serveurs_non_attribues = [item['ID_Type_Equipement'] for item in data_type_equipements_serveurs_non_attribues]
            session['session_lst_data_type_equipements_serveurs_non_attribues'] = lst_data_type_equipements_serveurs_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_type_equipements_serveurs_non_attribues  ", lst_data_type_equipements_serveurs_non_attribues,
                  type(lst_data_type_equipements_serveurs_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les type_equipements qui sont déjà sélectionnés.
            lst_data_type_equipements_serveurs_old_attribues = [item['ID_Type_Equipement'] for item in data_type_equipements_serveurs_attribues]
            session['session_lst_data_type_equipements_serveurs_old_attribues'] = lst_data_type_equipements_serveurs_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_type_equipements_serveurs_old_attribues  ", lst_data_type_equipements_serveurs_old_attribues,
                  type(lst_data_type_equipements_serveurs_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_type_equipement_serveur_selected", data_type_equipement_serveur_selected, "type ", type(data_type_equipement_serveur_selected))
            print(" data data_type_equipements_serveurs_non_attribues ", data_type_equipements_serveurs_non_attribues, "type ",
                  type(data_type_equipements_serveurs_non_attribues))
            print(" data_type_equipements_serveurs_attribues ", data_type_equipements_serveurs_attribues, "type ",
                  type(data_type_equipements_serveurs_attribues))

            # Extrait les valeurs contenues dans la table "t_type_equipements", colonne "Type_Equipement"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'ID_Type_Equipement
            lst_data_type_equipements_serveurs_non_attribues = [item['Type_Equipement'] for item in data_type_equipements_serveurs_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_type_equipements gf_edit_type_equipement_serveur_selected ", lst_data_type_equipements_serveurs_non_attribues,
                  type(lst_data_type_equipements_serveurs_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_serveur_selected == [None]:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_pers_a_type_equipement" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données type_equipements affichées dans Type_EquipementsServeurs!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # EZ 2020.07.21 Envoie la page "HTML" au serveur.
    return render_template("type_equipements_serveurs/type_equipements_serveurs_modifier_tags_dropbox.html",
                           data_type_equipements=data_type_equipements_all,
                           data_serveur_selected=data_type_equipement_serveur_selected,
                           data_type_equipements_attribues=data_type_equipements_serveurs_attribues,
                           data_type_equipements_non_attribues=data_type_equipements_serveurs_non_attribues)


# ---------------------------------------------------------------------------------------------------
# EZ 2020.07.26 Définition d'une "route" /gf_update_type_equipement_serveur_selected
# Récupère la liste de tous les type_equipements du serveur sélectionné.
# Nécessaire pour afficher tous les "TAGS" des type_equipements, ainsi l'utilisateur voit les type_equipements à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_type_equipement_serveur_selected", methods=['GET', 'POST'])
def gf_update_type_equipement_serveur_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du serveur sélectionné
            ID_Serveur_selected = session['session_ID_Serveur_type_equipements_edit']
            print("session['session_ID_Serveur_type_equipements_edit'] ", session['session_ID_Serveur_type_equipements_edit'])

            # Récupère la liste des type_equipements qui ne sont pas associés au serveur sélectionné.
            old_lst_data_type_equipements_serveurs_non_attribues = session['session_lst_data_type_equipements_serveurs_non_attribues']
            print("old_lst_data_type_equipements_serveurs_non_attribues ", old_lst_data_type_equipements_serveurs_non_attribues)

            # Récupère la liste des type_equipements qui sont associés au serveur sélectionné.
            old_lst_data_type_equipements_serveurs_attribues = session['session_lst_data_type_equipements_serveurs_old_attribues']
            print("old_lst_data_type_equipements_serveurs_old_attribues ", old_lst_data_type_equipements_serveurs_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme type_equipements dans le composant "tags-selector-tagselect"
            # dans le fichier "type_equipements_serveurs_modifier_tags_dropbox.html"
            new_lst_str_type_equipements_serveurs = request.form.getlist('name_select_tags')
            print("new_lst_str_type_equipements_serveurs ", new_lst_str_type_equipements_serveurs)

            # EZ 2020.07.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_pers_a_type_equipement_old = list(map(int, new_lst_str_type_equipements_serveurs))
            print("new_lst_pers_a_type_equipement ", new_lst_int_pers_a_type_equipement_old, "type new_lst_pers_a_type_equipement ",
                  type(new_lst_int_pers_a_type_equipement_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # EZ 2020.07.29 Une liste de "ID_Type_Equipement" qui doivent être effacés de la table intermédiaire "t_pers_a_type_equipement".
            lst_diff_type_equipements_delete_b = list(
                set(old_lst_data_type_equipements_serveurs_attribues) - set(new_lst_int_pers_a_type_equipement_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_type_equipements_delete_b ", lst_diff_type_equipements_delete_b)

            # EZ 2020.07.29 Une liste de "ID_Type_Equipement" qui doivent être ajoutés à la BD
            lst_diff_type_equipements_insert_a = list(
                set(new_lst_int_pers_a_type_equipement_old) - set(old_lst_data_type_equipements_serveurs_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_type_equipements_insert_a ", lst_diff_type_equipements_insert_a)

            # EZ 2020.07.19 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_type_equipements = GestionType_EquipementsServeurs()

            # Pour le serveur sélectionné, parcourir la liste des type_equipements à INSÉRER dans la "t_pers_a_type_equipement".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for ID_Type_Equipement_ins in lst_diff_type_equipements_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                # et "ID_Type_Equipement_ins" (l'id du type_equipement dans la liste) associé à une variable.
                valeurs_serveur_sel_type_equipement_sel_dictionnaire = {"value_FK_Serveur": ID_Serveur_selected,
                                                           "value_FK_Type_Equipement": ID_Type_Equipement_ins}
                # Insérer une association entre un(des) type_equipement(s) et le serveur sélectionner.
                obj_actions_type_equipements.type_equipements_serveurs_add(valeurs_serveur_sel_type_equipement_sel_dictionnaire)

            # Pour le serveur sélectionné, parcourir la liste des type_equipements à EFFACER dans la "t_pers_a_type_equipement".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for ID_Type_Equipement_del in lst_diff_type_equipements_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                # et "ID_Type_Equipement_del" (l'id du type_equipement dans la liste) associé à une variable.
                valeurs_serveur_sel_type_equipement_sel_dictionnaire = {"value_FK_Serveur": ID_Serveur_selected,
                                                           "value_FK_Type_Equipement": ID_Type_Equipement_del}
                # Effacer une association entre un(des) type_equipement(s) et le serveur sélectionner.
                obj_actions_type_equipements.type_equipements_serveurs_delete(valeurs_serveur_sel_type_equipement_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe GestionType_Equipements()
            # Fichier data_gestion_type_equipements.py
            # Afficher seulement le serveur dont les type_equipements sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_type_equipements_serveurs_afficher_concat = obj_actions_type_equipements.type_equipements_serveurs_afficher_data_concat(ID_Serveur_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data type_equipements", data_type_equipements_serveurs_afficher_concat, "type ", type(data_type_equipements_serveurs_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_type_equipements_serveurs_afficher_concat == None:
                flash(f"""Le serveur demandé n'existe pas. Ou la table "t_pers_a_type_equipement" est vide. !!""", "warning")
            else:
                # EZ 2020.07.19 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données type_equipements affichées dans Type_EquipementsServeurs!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_pers_a_type_equipement",
    # on affiche les serveurs et le(urs) type_equipement(s) associé(s).
    return render_template("type_equipements_serveurs/type_equipements_serveurs_afficher.html",
                           data=data_type_equipements_serveurs_afficher_concat)
