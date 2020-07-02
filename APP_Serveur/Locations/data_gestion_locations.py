# data_gestion_locations.py
# EZ 2020.07.19 Permet de gérer (CRUD) les données de la table "t_location"
from flask import flash
from APP_Serveur.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_Serveur.DATABASE.erreurs import *


class GestionLocations():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions locations")
            # EZ 2020.07.21 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash(f"Dans Gestion locations ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionLocations {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionLocations ")

    def locations_afficher_data(self, valeur_order_by, ID_Location_sel):
        try:
            print("valeur_order_by ", valeur_order_by, type(valeur_order_by))

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Afficher soit la liste des locations dans l'ordre inverse ou simplement le location sélectionné
                # par l'action edit
                if valeur_order_by == "ASC" and ID_Location_sel == 0:
                    strsql_locations_afficher = """SELECT ID_Location, Location FROM t_location ORDER BY ID_Location ASC"""
                    mc_afficher.execute(strsql_locations_afficher)
                elif valeur_order_by == "ASC":
                    # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_location"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du location sélectionné avec un nom de variable
                    valeur_ID_Location_selected_dictionnaire = {"value_ID_Location_selected": ID_Location_sel}
                    strsql_locations_afficher = """SELECT ID_Location, Location FROM t_location  WHERE ID_Location = %(value_ID_Location_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_locations_afficher, valeur_ID_Location_selected_dictionnaire)
                else:
                    strsql_locations_afficher = """SELECT ID_Location, Location FROM t_location ORDER BY ID_Location ASC"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_locations_afficher)
                # Récupère les données de la requête.
                data_locations = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_locations ", data_locations, " Type : ", type(data_locations))
                # Retourne les données du "SELECT"
                return data_locations
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

    def add_location_data (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            strsql_insert_location = """INSERT INTO t_location (ID_Location,Location) 
                                     VALUES (NULL,%(value_Location)s)"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_location, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def edit_location_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le location sélectionné dans le tableau dans le formulaire HTML
            str_sql_ID_Location = "SELECT ID_Location, Location FROM t_location " \
                               "WHERE ID_Location = %(value_ID_Location)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_ID_Location, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_location_data Data Gestions Locations numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions locations numéro de l'erreur : {erreur}", "danger")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_location_data d'un location Data Gestions Locations {erreur}")

    def update_location_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleLocationHTML" du form HTML "locationsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulelocationHTML" value="{{ row.intitule_location }}"/></td>
            str_sql_update_location = "UPDATE t_location SET Location = %(value_Location)s " \
                                      "WHERE ID_Location = %(value_ID_Location)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_location, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_location_data Data Gestions locations numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions locations numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_location_data d\'un location Data Gestions locations {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"'Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_location_data Data Gestions locations numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_location_data d'un location DataGestionslocations {erreur}")

    def delete_select_location_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulelocationHTML" du form HTML "locationsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulelocationHTML" value="{{ row.intitule_location }}"/></td>

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le location sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_ID_Location = "SELECT ID_Location, Location FROM t_location WHERE ID_Location = %(value_ID_Location)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_ID_Location, valeur_delete_dictionnaire)
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
            print(f"Problème delete_select_location_data Gestions locations numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_location_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_location_data d\'un location Data Gestions locations {erreur}")

    def delete_location_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "locationsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulelocationHTML" value="{{ row.intitule_location }}"/></td>
            str_sql_delete_location = "DELETE FROM t_location WHERE ID_Location = %(value_ID_Location)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_location, valeur_delete_dictionnaire)
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
            print(f"Problème delete_location_data Data Gestions locations numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions locations numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # EZ 2020.07.19 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un location qui est associé à une location dans la table intermédiaire "t_locations_films"
                # il y a une contrainte sur les FK de la table intermédiaire "t_locations_films"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce location est associé à des serveurs dans la t_locations_films !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(
                    f"IMPOSSIBLE d'effacer !!! Ce location est associé à des films dans la t_locations_films !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
