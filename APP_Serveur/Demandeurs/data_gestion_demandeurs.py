# data_gestion_demandeur.py
# EZ 2020.07.19 Permet de gérer (CRUD) les données de la table "t_personne"
from flask import flash
from APP_Serveur.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_Serveur.DATABASE.erreurs import *


class GestionPersonnes():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions Personnes")
            # EZ 2020.07 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash(f"Dans Gestion personnes ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionPersonnes {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionPersonnes ")

    def personnes_afficher_data (self, valeur_order_by, ID_Personne_sel):
        try:
            print("valeur_order_by ", valeur_order_by, type(valeur_order_by))

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Afficher soit la liste des personnes dans l'ordre inverse ou simplement le personne sélectionné
                # par l'action edit
                if valeur_order_by == "ASC" and ID_Personne_sel == 0:
                    strsql_personnes_afficher = """SELECT ID_Personne, Nom_Pers, Prenom_Pers, Date_Naissance_Pers FROM t_personne ORDER BY ID_Personne ASC"""
                    mc_afficher.execute(strsql_personnes_afficher)
                elif valeur_order_by == "ASC":
                    # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_personne"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
                    valeur_ID_Personne_selected_dictionnaire = {"value_ID_Personne_selected": ID_Personne_sel}
                    strsql_personnes_afficher = """SELECT ID_Personne, Nom_Pers, Prenom_Pers, Date_Naissance_Pers FROM t_personne  WHERE ID_Personne = %(value_ID_Personne_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_personnes_afficher, valeur_ID_Personne_selected_dictionnaire)
                else:
                    strsql_personnes_afficher = """SELECT ID_Personne, Nom_Pers, Prenom_Pers, Date_Naissance_Pers FROM t_personne ORDER BY ID_Personne ASC"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_personnes_afficher)
                # Récupère les données de la requête.
                data_personnes = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_personnes ", data_personnes, " Type : ", type(data_personnes))
                # Retourne les données du "SELECT"
                return data_personnes
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

    def add_personne_data (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            strsql_insert_personne = """INSERT INTO t_personne (ID_Personne,Nom_Pers, Prenom_Pers, Date_Naissance_Pers) 
                                     VALUES (NULL,%(value_Nom_Pers)s,%(value_Prenom_Pers)s,%(value_Date_Naissance_Pers)s)"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_personne, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def edit_personne_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le personne sélectionné dans le tableau dans le formulaire HTML
            str_sql_ID_Personne = "SELECT ID_Personne, Nom_Pers, Prenom_Pers, Date_Naissance_Pers FROM t_personne " \
                               "WHERE ID_Personne = %(value_ID_Personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_ID_Personne, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_personne_data Data Gestions Personnes numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions personnes numéro de l'erreur : {erreur}", "danger")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_personne_data d'un personne Data Gestions Personnes {erreur}")

    def update_personne_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulePersonneHTML" du form HTML "personnesEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulepersonneHTML" value="{{ row.intitule_personne }}"/></td>
            str_sql_update_personne = "UPDATE t_personne SET Nom_Pers = %(value_Nom_Pers)s, Prenom_Pers = %(value_Prenom_Pers)s, " \
                                           "Date_Naissance_Pers = %(value_Date_Naissance_Pers)s" \
                                           "WHERE ID_Personne = %(value_ID_Personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_personne, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_personne_data Data Gestions personnes numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions personnes numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_personne_data d\'un personne Data Gestions personnes {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"'Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_personne_data Data Gestions personnes numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_personne_data d'un personne DataGestionspersonnes {erreur}")

    def delete_select_personne_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulepersonneHTML" du form HTML "personnesEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulepersonneHTML" value="{{ row.intitule_personne }}"/></td>

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le personne sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_ID_Personne = "SELECT ID_Personne, Nom_Pers FROM t_personne WHERE ID_Personne = %(value_ID_Personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_ID_Personne, valeur_delete_dictionnaire)
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
            print(f"Problème delete_select_personne_data Gestions personnes numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_personne_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_personne_data d\'un personne Data Gestions personnes {erreur}")

    def delete_personne_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "personnesEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulepersonneHTML" value="{{ row.intitule_personne }}"/></td>
            str_sql_delete_personne = "DELETE FROM t_personne WHERE ID_Personne = %(value_ID_Personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_personne, valeur_delete_dictionnaire)
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
            print(f"Problème delete_personne_data Data Gestions personnes numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions personnes numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # EZ 2020.07.19 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un personne qui est associé à une personne dans la table intermédiaire "t_personnes_films"
                # il y a une contrainte sur les FK de la table intermédiaire "t_personnes_films"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce personne est associé à des serveurs dans la t_personnes_films !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(
                    f"IMPOSSIBLE d'effacer !!! Ce personne est associé à des films dans la t_personnes_films !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
