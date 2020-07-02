# data_gestion_status_serveurs.py
# EZ 2020.07.22 Permet de gérer (CRUD) les données de la table intermédiaire "t_serv_a_status"

from flask import flash
from APP_Serveur.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_Serveur.DATABASE.erreurs import *


class GestionStatusServeurs():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions status")
            # EZ 2020.07 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion status serveurs ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionStatusServeurs {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionStatusServeurs ")

    def status_afficher_data (self):
        try:
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_status"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_status_afficher = """SELECT ID_Status, Status FROM t_status ORDER BY ID_Status ASC"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_status_afficher)
                # Récupère les données de la requête.
                data_status = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_status ", data_status, " Type : ", type(data_status))
                # Retourne les données du "SELECT"
                return data_status
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

    def status_serveurs_afficher_data (self, valeur_ID_Serveur_selected_dict):
        print("valeur_ID_Serveur_selected_dict...", valeur_ID_Serveur_selected_dict)
        try:

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_status"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_serveur_selected = """SELECT ID_Serveur, Nom_Serv, Nombre_Port, Nombre_U, Date_Conf_Serv, Description, Puissance, Date_Serveur, 
                                        GROUP_CONCAT(ID_Status) as StatusServeurs FROM t_serv_a_status AS T1
                                        INNER JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                        INNER JOIN t_status AS T3 ON T3.ID_Status = T1.FK_Status
                                        WHERE ID_Serveur = %(value_ID_Serveur_selected)s"""

            strsql_status_serveurs_non_attribues = """SELECT ID_Status, Status FROM t_status
                                                    WHERE ID_Status not in(SELECT ID_Status as idStatusServeurs FROM t_serv_a_status AS T1
                                                    INNER JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                                    INNER JOIN t_status AS T3 ON T3.ID_Status = T1.FK_Status
                                                    WHERE ID_Serveur = %(value_ID_Serveur_selected)s)"""

            strsql_status_serveurs_attribues = """SELECT ID_Serveur, ID_Status, Status FROM t_serv_a_status AS T1
                                            INNER JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                            INNER JOIN t_status AS T3 ON T3.ID_Status = T1.FK_Status
                                            WHERE ID_Serveur = %(value_ID_Serveur_selected)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_status_serveurs_non_attribues, valeur_ID_Serveur_selected_dict)
                # Récupère les données de la requête.
                data_status_serveurs_non_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("dfad data_status_serveurs_non_attribues ", data_status_serveurs_non_attribues, " Type : ",
                      type(data_status_serveurs_non_attribues))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_serveur_selected, valeur_ID_Serveur_selected_dict)
                # Récupère les données de la requête.
                data_serveur_selected = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_serveur_selected  ", data_serveur_selected, " Type : ", type(data_serveur_selected))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_status_serveurs_attribues, valeur_ID_Serveur_selected_dict)
                # Récupère les données de la requête.
                data_status_serveurs_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_status_serveurs_attribues ", data_status_serveurs_attribues, " Type : ",
                      type(data_status_serveurs_attribues))

                # Retourne les données du "SELECT"
                return data_serveur_selected, data_status_serveurs_non_attribues, data_status_serveurs_attribues
        except pymysql.Error as erreur:
            print(f"DGGF gfad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGGF gfad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGGF gfad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def status_serveurs_afficher_data_concat (self, ID_Serveur_selected):
        print("ID_Serveur_selected  ", ID_Serveur_selected)
        try:
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_status"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_status_serveurs_afficher_data_concat = """SELECT ID_Serveur, Nom_Serv, Nombre_Port, Nombre_U, Date_Conf_Serv, Description, Puissance, Date_Serveur, 
                                                            GROUP_CONCAT(Status) as StatusServeurs FROM t_serv_a_status AS T1
                                                            RIGHT JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                                            LEFT JOIN t_status AS T3 ON T3.ID_Status = T1.FK_Status
                                                            GROUP BY ID_Serveur"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # le paramètre 0 permet d'afficher tous les serveurs
                # Sinon le paramètre représente la valeur de l'id du serveur
                if ID_Serveur_selected == 0:
                    mc_afficher.execute(strsql_status_serveurs_afficher_data_concat)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                    valeur_ID_Serveur_selected_dictionnaire = {"value_ID_Serveur_selected": ID_Serveur_selected}
                    strsql_status_serveurs_afficher_data_concat += """ HAVING ID_Serveur= %(value_ID_Serveur_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_status_serveurs_afficher_data_concat, valeur_ID_Serveur_selected_dictionnaire)

                # Récupère les données de la requête.
                data_status_serveurs_afficher_concat = mc_afficher.fetchall()
                # Affichage dans la console
                print("dggf data_status_serveurs_afficher_concat ", data_status_serveurs_afficher_concat, " Type : ",
                      type(data_status_serveurs_afficher_concat))

                # Retourne les données du "SELECT"
                return data_status_serveurs_afficher_concat


        except pymysql.Error as erreur:
            print(f"DGGF gfadc pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGGF gfadc Exception {erreur.args}")
            raise MaBdErreurConnexion(
                f"DGG gfadc Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGGF gfadc pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def status_serveurs_add (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Insérer une (des) nouvelle(s) association(s) entre "ID_Serveur" et "ID_Status" dans la "t_status_serveur"
            strsql_insert_status_serveur = """INSERT INTO t_serv_a_status (ID_Serv_A_Status, FK_Status, FK_Serveur)
                                            VALUES (NULL, %(value_FK_Status)s, %(value_FK_Serveur)s)"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_status_serveur, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def status_serveurs_delete (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Effacer une (des) association(s) existantes entre "ID_Serveur" et "ID_Status" dans la "t_status_serveur"
            strsql_delete_status_serveur = """DELETE FROM t_serv_a_status WHERE FK_Status = %(value_FK_Status)s AND FK_Serveur = %(value_FK_Serveur)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_delete_status_serveur, valeurs_insertion_dictionnaire)
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème status_serveurs_delete Gestions status serveurs numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème status_serveurs_delete Gestions status serveurs  numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème status_serveurs_delete Gestions status serveurs  {erreur}")

    def edit_status_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le status sélectionné dans le tableau dans le formulaire HTML
            str_sql_ID_Status = "SELECT ID_Status, Status FROM t_status WHERE ID_Status = %(value_ID_Status)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_ID_Status, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_status_data Data Gestions status numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions status numéro de l'erreur : {erreur}", "danger")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_status_data d'un status Data Gestions status {erreur}")

    def update_status_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditstatusHTML" du form HTML "statusEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditstatusHTML" value="{{ row.intitule_status }}"/></td>
            str_sql_update_status = "UPDATE t_status SET Status = %(value_status)s WHERE ID_Status = %(value_ID_Status)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_status, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_status_data Data Gestions status numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions status numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_status_data d\'un status Data Gestions status {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "warning")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_status_data Data Gestions status numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_status_data d'un status DataGestionsstatus {erreur}")

    def delete_select_status_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulestatusHTML" du form HTML "statusEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulestatusHTML" value="{{ row.intitule_status }}"/></td>

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le status sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_ID_Status = "SELECT ID_Status, Status FROM t_status WHERE ID_Status = %(value_ID_Status)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode"mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_ID_Status, valeur_delete_dictionnaire)
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
            print(f"Problème delete_select_status_data Gestions status numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_status_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_status_data d\'un status Data Gestions status {erreur}")

    def delete_status_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "statusEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulestatusHTML" value="{{ row.intitule_status }}"/></td>
            str_sql_delete_status = "DELETE FROM t_status WHERE ID_Status = %(value_ID_Status)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_status, valeur_delete_dictionnaire)
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
            print(f"Problème delete_status_data Data Gestions status numéro de l'erreur : {erreur}")
            flash(f"Flash. Problèmes Data Gestions status numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # EZ 2020.07.19 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un status qui est associé à un serveur dans la table intermédiaire "t_status_serveurs"
                # il y a une contrainte sur les FK de la table intermédiaire "t_status_serveurs"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce status est associé à des serveurs dans la t_status_serveurs !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce status est associé à des serveurs dans la t_status_serveurs !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
