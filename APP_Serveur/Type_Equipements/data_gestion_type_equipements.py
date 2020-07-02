# data_gestion_type_equipements.py
# EZ 2020.07.19 Permet de gérer (CRUD) les données de la table "t_type_equipement"
from flask import flash
from APP_Serveur.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_Serveur.DATABASE.erreurs import *


class GestionType_Equipements():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions type_equipements")
            # EZ 2020.07 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash(f"Dans Gestion type_equipements ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionType_Equipements {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionType_Equipements ")

    def type_equipements_afficher_data(self, valeur_order_by, ID_Type_Equipement_sel):
        try:
            print("valeur_order_by ", valeur_order_by, type(valeur_order_by))

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Afficher soit la liste des type_equipements dans l'ordre inverse ou simplement le type_equipement sélectionné
                # par l'action edit
                if valeur_order_by == "ASC" and ID_Type_Equipement_sel == 0:
                    strsql_type_equipements_afficher = """SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement ORDER BY ID_Type_Equipement ASC"""
                    mc_afficher.execute(strsql_type_equipements_afficher)
                elif valeur_order_by == "ASC":
                    # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_type_equipement"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du type_equipement sélectionné avec un nom de variable
                    valeur_ID_Type_Equipement_selected_dictionnaire = {"value_ID_Type_Equipement_selected": ID_Type_Equipement_sel}
                    strsql_type_equipements_afficher = """SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement  WHERE ID_Type_Equipement = %(value_ID_Type_Equipement_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_type_equipements_afficher, valeur_ID_Type_Equipement_selected_dictionnaire)
                else:
                    strsql_type_equipements_afficher = """SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement ORDER BY ID_Type_Equipement ASC"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_type_equipements_afficher)
                # Récupère les données de la requête.
                data_type_equipements = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_type_equipements ", data_type_equipements, " Type : ", type(data_type_equipements))
                # Retourne les données du "SELECT"
                return data_type_equipements
        except pymysql.Error as erreur:
            print(f"DGG gad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGG gad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGG gad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def add_type_equipement_data (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            strsql_insert_type_equipement = """INSERT INTO t_type_equipement (ID_Type_Equipement,Type_Equipement) 
                                     VALUES (NULL,%(value_Type_Equipement)s)"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_type_equipement, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def edit_type_equipement_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le type_equipement sélectionné dans le tableau dans le formulaire HTML
            str_sql_ID_Type_Equipement = "SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement " \
                               "WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_ID_Type_Equipement, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_type_equipement_data Data Gestions Type_Equipements numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions type_equipements numéro de l'erreur : {erreur}", "danger")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_type_equipement_data d'un type_equipement Data Gestions Type_Equipements {erreur}")

    def update_type_equipement_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleType_EquipementHTML" du form HTML "type_equipementsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituletype_equipementHTML" value="{{ row.intitule_type_equipement }}"/></td>
            str_sql_update_type_equipement = "UPDATE t_type_equipement SET Type_Equipement = %(value_Type_Equipement)s " \
                                      "WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_type_equipement, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_type_equipement_data Data Gestions type_equipements numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions type_equipements numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_type_equipement_data d\'un type_equipement Data Gestions type_equipements {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"'Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_type_equipement_data Data Gestions type_equipements numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_type_equipement_data d'un type_equipement DataGestionstype_equipements {erreur}")

    def delete_select_type_equipement_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituletype_equipementHTML" du form HTML "type_equipementsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituletype_equipementHTML" value="{{ row.intitule_type_equipement }}"/></td>

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le type_equipement sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_ID_Type_Equipement = "SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_ID_Type_Equipement, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_select_type_equipement_data Gestions type_equipements numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_type_equipement_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_type_equipement_data d\'un type_equipement Data Gestions type_equipements {erreur}")

    def delete_type_equipement_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "type_equipementsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituletype_equipementHTML" value="{{ row.intitule_type_equipement }}"/></td>
            str_sql_delete_type_equipement = "DELETE FROM t_type_equipement WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_type_equipement, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_type_equipement_data Data Gestions type_equipements numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions type_equipements numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # EZ 2020.07.19 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un type_equipement qui est associé à une type_equipement dans la table intermédiaire "t_type_equipements_films"
                # il y a une contrainte sur les FK de la table intermédiaire "t_type_equipements_films"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce type_equipement est associé à des serveurs dans la t_type_equipements_films !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(
                    f"IMPOSSIBLE d'effacer !!! Ce type_equipement est associé à des films dans la t_type_equipements_films !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
