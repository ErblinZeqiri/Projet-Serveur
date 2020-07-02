# data_gestion_type_equipements_serveur.py
# EZ 2020.07.22 Permet de gérer (CRUD) les données de la table intermédiaire "t_serv_a_type_equipement"

from flask import flash
from APP_Serveur.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_Serveur.DATABASE.erreurs import *


class GestionType_EquipementsServeurs():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions type_equipements")
            # EZ 2020.07 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion type_equipements serveurs ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionType_EquipementsServeurs {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionType_EquipementsServeurs ")

    def type_equipements_afficher_data (self):
        try:
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_type_equipement"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_type_equipements_afficher = """SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement ORDER BY ID_Type_Equipement ASC"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
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

    def type_equipements_serveurs_afficher_data (self, valeur_ID_Serveur_selected_dict):
        print("valeur_ID_Serveur_selected_dict...", valeur_ID_Serveur_selected_dict)
        try:

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_type_equipement"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_serveur_selected = """SELECT ID_Serveur, Nom_Serv, Nombre_Port, Nombre_U, Date_Conf_Serv, Description, Puissance, Date_Serveur,
                                        GROUP_CONCAT(ID_Type_Equipement) as Type_EquipementsServeurs FROM t_serv_a_type_equipement AS T1
                                        INNER JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                        INNER JOIN t_type_equipement AS T3 ON T3.ID_Type_Equipement = T1.FK_Type_Equipement
                                        WHERE ID_Serveur = %(value_ID_Serveur_selected)s"""

            strsql_type_equipements_serveurs_non_attribues = """SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement
                                                    WHERE ID_Type_Equipement not in(SELECT ID_Type_Equipement as idType_EquipementsServeurs FROM t_serv_a_type_equipement AS T1
                                                    INNER JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                                    INNER JOIN t_type_equipement AS T3 ON T3.ID_Type_Equipement = T1.FK_Type_Equipement
                                                    WHERE ID_Serveur = %(value_ID_Serveur_selected)s)"""

            strsql_type_equipements_serveurs_attribues = """SELECT ID_Serveur, ID_Type_Equipement, Type_Equipement FROM t_serv_a_type_equipement AS T1
                                            INNER JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                            INNER JOIN t_type_equipement AS T3 ON T3.ID_Type_Equipement = T1.FK_Type_Equipement
                                            WHERE ID_Serveur = %(value_ID_Serveur_selected)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_type_equipements_serveurs_non_attribues, valeur_ID_Serveur_selected_dict)
                # Récupère les données de la requête.
                data_type_equipements_serveurs_non_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("dfad data_type_equipements_serveurs_non_attribues ", data_type_equipements_serveurs_non_attribues, " Type : ",
                      type(data_type_equipements_serveurs_non_attribues))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_serveur_selected, valeur_ID_Serveur_selected_dict)
                # Récupère les données de la requête.
                data_serveur_selected = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_serveur_selected  ", data_serveur_selected, " Type : ", type(data_serveur_selected))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_type_equipements_serveurs_attribues, valeur_ID_Serveur_selected_dict)
                # Récupère les données de la requête.
                data_type_equipements_serveurs_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_type_equipements_serveurs_attribues ", data_type_equipements_serveurs_attribues, " Type : ",
                      type(data_type_equipements_serveurs_attribues))

                # Retourne les données du "SELECT"
                return data_serveur_selected, data_type_equipements_serveurs_non_attribues, data_type_equipements_serveurs_attribues
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

    def type_equipements_serveurs_afficher_data_concat (self, ID_Serveur_selected):
        print("ID_Serveur_selected  ", ID_Serveur_selected)
        try:
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_type_equipement"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_type_equipements_serveurs_afficher_data_concat = """SELECT ID_Serveur, Nom_Serv, Nombre_Port, Nombre_U, Date_Conf_Serv, Description, Puissance, Date_Serveur,
                                                            GROUP_CONCAT(Type_Equipement) as Type_EquipementsServeurs FROM t_serv_a_type_equipement AS T1
                                                            RIGHT JOIN t_serveur AS T2 ON T2.ID_Serveur = T1.FK_Serveur
                                                            LEFT JOIN t_type_equipement AS T3 ON T3.ID_Type_Equipement = T1.FK_Type_Equipement
                                                            GROUP BY ID_Serveur"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # le paramètre 0 permet d'afficher tous les serveurs
                # Sinon le paramètre représente la valeur de l'id du serveur
                if ID_Serveur_selected == 0:
                    mc_afficher.execute(strsql_type_equipements_serveurs_afficher_data_concat)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du serveur sélectionné avec un nom de variable
                    valeur_ID_Serveur_selected_dictionnaire = {"value_ID_Serveur_selected": ID_Serveur_selected}
                    strsql_type_equipements_serveurs_afficher_data_concat += """ HAVING ID_Serveur= %(value_ID_Serveur_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_type_equipements_serveurs_afficher_data_concat, valeur_ID_Serveur_selected_dictionnaire)

                # Récupère les données de la requête.
                data_type_equipements_serveurs_afficher_concat = mc_afficher.fetchall()
                # Affichage dans la console
                print("dggf data_type_equipements_serveurs_afficher_concat ", data_type_equipements_serveurs_afficher_concat, " Type : ",
                      type(data_type_equipements_serveurs_afficher_concat))

                # Retourne les données du "SELECT"
                return data_type_equipements_serveurs_afficher_concat


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

    def type_equipements_serveurs_add (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Insérer une (des) nouvelle(s) association(s) entre "ID_Serveur" et "id_type_equipement" dans la "t_serv_a_type_equipement"
            strsql_insert_serv_a_type_equipement = """INSERT INTO t_serv_a_type_equipement (ID_Serv_A_Type_Equipement, FK_Type_Equipement, FK_Serveur)
                                            VALUES (NULL, %(value_FK_Type_Equipement)s, %(value_FK_Serveur)s)"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_serv_a_type_equipement, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def type_equipements_serveurs_delete (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Effacer une (des) association(s) existantes entre "ID_Serveur" et "id_type_equipement" dans la "t_serv_a_type_equipement"
            strsql_delete_type_equipement_serveur = """DELETE FROM t_serv_a_type_equipement WHERE FK_Type_Equipement = %(value_FK_Type_Equipement)s AND FK_Serveur = %(value_FK_Serveur)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_delete_type_equipement_serveur, valeurs_insertion_dictionnaire)
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème type_equipements_serveurs_delete Gestions type_equipements serveurs numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème type_equipements_serveurs_delete Gestions type_equipements serveurs  numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème type_equipements_serveurs_delete Gestions type_equipements serveurs  {erreur}")

    def edit_type_equipement_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le type_equipement sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_type_equipement = "SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_type_equipement, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_type_equipement_data Data Gestions type_equipements numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions type_equipements numéro de l'erreur : {erreur}", "danger")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_type_equipement_data d'un type_equipement Data Gestions type_equipements {erreur}")

    def update_type_equipement_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditType_EquipementHTML" du form HTML "type_equipementsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditType_EquipementHTML" value="{{ row.Type_Equipement }}"/></td>
            str_sql_update_Type_Equipement = "UPDATE t_type_equipement SET Type_Equipement = %(value_Type_Equipement)s WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_Type_Equipement, valeur_update_dictionnaire)

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
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "warning")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_type_equipement_data Data Gestions type_equipements numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_type_equipement_data d'un type_equipement DataGestionstype_equipements {erreur}")

    def delete_select_type_equipement_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditType_EquipementHTML" du form HTML "type_equipementsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditType_EquipementHTML" value="{{ row.Type_Equipement }}"/></td>

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le type_equipement sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_type_equipement = "SELECT ID_Type_Equipement, Type_Equipement FROM t_type_equipement WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode"mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_type_equipement, valeur_delete_dictionnaire)
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
            # <td><input type = "text" name = "nameEditType_EquipementHTML" value="{{ row.Type_Equipement }}"/></td>
            str_sql_delete_Type_Equipement = "DELETE FROM t_type_equipement WHERE ID_Type_Equipement = %(value_ID_Type_Equipement)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_Type_Equipement, valeur_delete_dictionnaire)
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
            flash(f"Flash. Problèmes Data Gestions type_equipements numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # EZ 2020.07.19 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un type_equipement qui est associé à un serveur dans la table intermédiaire "t_serv_a_type_equipements"
                # il y a une contrainte sur les FK de la table intermédiaire "t_serv_a_type_equipements"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce type_equipement est associé à des serveurs dans la t_serv_a_type_equipements !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce type_equipement est associé à des serveurs dans la t_serv_a_type_equipements !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
