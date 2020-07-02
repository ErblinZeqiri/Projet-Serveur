# data_gestion_mails_personne.py
# EZ 2020.07.22 Permet de gérer (CRUD) les données de la table intermédiaire "t_pers_a_mail"

from flask import flash
from APP_Serveur.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_Serveur.DATABASE.erreurs import *


class GestionMailsPersonnes():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions mails")
            # EZ 2020.07 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion mails personnes ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionMailsPersonnes {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionMailsPersonnes ")

    def mails_afficher_data (self):
        try:
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_mail"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_mails_afficher = """SELECT ID_Mail, Adresse_Mail FROM t_mail ORDER BY ID_Mail ASC"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_mails_afficher)
                # Récupère les données de la requête.
                data_mails = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_mails ", data_mails, " Type : ", type(data_mails))
                # Retourne les données du "SELECT"
                return data_mails
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

    def mails_personnes_afficher_data (self, valeur_ID_Personne_selected_dict):
        print("valeur_ID_Personne_selected_dict...", valeur_ID_Personne_selected_dict)
        try:

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_mail"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_personne_selected = """SELECT ID_Personne, Nom_Pers, Prenom_Pers, Date_Naissance_Pers, GROUP_CONCAT(ID_Mail) as MailsPersonnes FROM t_pers_a_mail AS T1
                                        INNER JOIN t_personne AS T2 ON T2.ID_Personne = T1.FK_Personne
                                        INNER JOIN t_mail AS T3 ON T3.ID_Mail = T1.FK_Mail
                                        WHERE ID_Personne = %(value_ID_Personne_selected)s"""

            strsql_mails_personnes_non_attribues = """SELECT ID_Mail, Adresse_Mail FROM t_mail
                                                    WHERE ID_Mail not in(SELECT ID_Mail as idMailsPersonnes FROM t_pers_a_mail AS T1
                                                    INNER JOIN t_personne AS T2 ON T2.ID_Personne = T1.FK_Personne
                                                    INNER JOIN t_mail AS T3 ON T3.ID_Mail = T1.FK_Mail
                                                    WHERE ID_Personne = %(value_ID_Personne_selected)s)"""

            strsql_mails_personnes_attribues = """SELECT ID_Personne, ID_Mail, Adresse_Mail FROM t_pers_a_mail AS T1
                                            INNER JOIN t_personne AS T2 ON T2.ID_Personne = T1.FK_Personne
                                            INNER JOIN t_mail AS T3 ON T3.ID_Mail = T1.FK_Mail
                                            WHERE ID_Personne = %(value_ID_Personne_selected)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_mails_personnes_non_attribues, valeur_ID_Personne_selected_dict)
                # Récupère les données de la requête.
                data_mails_personnes_non_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("dfad data_mails_personnes_non_attribues ", data_mails_personnes_non_attribues, " Type : ",
                      type(data_mails_personnes_non_attribues))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_personne_selected, valeur_ID_Personne_selected_dict)
                # Récupère les données de la requête.
                data_personne_selected = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_personne_selected  ", data_personne_selected, " Type : ", type(data_personne_selected))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_mails_personnes_attribues, valeur_ID_Personne_selected_dict)
                # Récupère les données de la requête.
                data_mails_personnes_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_mails_personnes_attribues ", data_mails_personnes_attribues, " Type : ",
                      type(data_mails_personnes_attribues))

                # Retourne les données du "SELECT"
                return data_personne_selected, data_mails_personnes_non_attribues, data_mails_personnes_attribues
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

    def mails_personnes_afficher_data_concat (self, ID_Personne_selected):
        print("ID_Personne_selected  ", ID_Personne_selected)
        try:
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_mail"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_mails_personnes_afficher_data_concat = """SELECT ID_Personne, Nom_Pers, Prenom_Pers, Date_Naissance_Pers,
                                                            GROUP_CONCAT(Adresse_Mail) as MailsPersonnes FROM t_pers_a_mail AS T1
                                                            RIGHT JOIN t_personne AS T2 ON T2.ID_Personne = T1.FK_Personne
                                                            LEFT JOIN t_mail AS T3 ON T3.ID_Mail = T1.FK_Mail
                                                            GROUP BY ID_Personne"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # le paramètre 0 permet d'afficher tous les personnes
                # Sinon le paramètre représente la valeur de l'id du personne
                if ID_Personne_selected == 0:
                    mc_afficher.execute(strsql_mails_personnes_afficher_data_concat)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
                    valeur_ID_Personne_selected_dictionnaire = {"value_ID_Personne_selected": ID_Personne_selected}
                    strsql_mails_personnes_afficher_data_concat += """ HAVING ID_Personne= %(value_ID_Personne_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_mails_personnes_afficher_data_concat, valeur_ID_Personne_selected_dictionnaire)

                # Récupère les données de la requête.
                data_mails_personnes_afficher_concat = mc_afficher.fetchall()
                # Affichage dans la console
                print("dggf data_mails_personnes_afficher_concat ", data_mails_personnes_afficher_concat, " Type : ",
                      type(data_mails_personnes_afficher_concat))

                # Retourne les données du "SELECT"
                return data_mails_personnes_afficher_concat


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

    def mails_personnes_add (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Insérer une (des) nouvelle(s) association(s) entre "ID_Personne" et "id_mail" dans la "t_pers_a_mail"
            strsql_insert_pers_a_mail = """INSERT INTO t_pers_a_mail (ID_Pers_A_Mail, FK_Mail, FK_Personne)
                                            VALUES (NULL, %(value_FK_Mail)s, %(value_FK_Personne)s)"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_pers_a_mail, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # EZ 2020.07.19 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def mails_personnes_delete (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Effacer une (des) association(s) existantes entre "ID_Personne" et "id_mail" dans la "t_pers_a_mail"
            strsql_delete_mail_personne = """DELETE FROM t_pers_a_mail WHERE FK_Mail = %(value_FK_Mail)s AND FK_Personne = %(value_FK_Personne)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_delete_mail_personne, valeurs_insertion_dictionnaire)
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème mails_personnes_delete Gestions mails personnes numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème mails_personnes_delete Gestions mails personnes  numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème mails_personnes_delete Gestions mails personnes  {erreur}")

    def edit_mail_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le mail sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_mail = "SELECT ID_Mail, Adresse_Mail FROM t_mail WHERE ID_Mail = %(value_ID_Mail)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_mail, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_mail_data Data Gestions mails numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions mails numéro de l'erreur : {erreur}", "danger")
            # EZ 2020.07.19 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_mail_data d'un mail Data Gestions mails {erreur}")

    def update_mail_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditAdresse_MailHTML" du form HTML "mailsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditAdresse_MailHTML" value="{{ row.Adresse_Mail }}"/></td>
            str_sql_update_Adresse_Mail = "UPDATE t_mail SET Adresse_Mail = %(value_Adresse_Mail)s WHERE ID_Mail = %(value_ID_Mail)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_Adresse_Mail, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # EZ 2020.07.11 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_mail_data Data Gestions mails numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions mails numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_mail_data d\'un mail Data Gestions mails {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "warning")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_mail_data Data Gestions mails numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_mail_data d'un mail DataGestionsmails {erreur}")

    def delete_select_mail_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditAdresse_MailHTML" du form HTML "mailsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditAdresse_MailHTML" value="{{ row.Adresse_Mail }}"/></td>

            # EZ 2020.07.17 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le mail sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_mail = "SELECT ID_Mail, Adresse_Mail FROM t_mail WHERE ID_Mail = %(value_ID_Mail)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode"mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_mail, valeur_delete_dictionnaire)
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
            print(f"Problème delete_select_mail_data Gestions mails numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_mail_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_mail_data d\'un mail Data Gestions mails {erreur}")

    def delete_mail_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "mailsEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditAdresse_MailHTML" value="{{ row.Adresse_Mail }}"/></td>
            str_sql_delete_Adresse_Mail = "DELETE FROM t_mail WHERE ID_Mail = %(value_ID_Mail)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_Adresse_Mail, valeur_delete_dictionnaire)
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
            print(f"Problème delete_mail_data Data Gestions mails numéro de l'erreur : {erreur}")
            flash(f"Flash. Problèmes Data Gestions mails numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # EZ 2020.07.19 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un mail qui est associé à un personne dans la table intermédiaire "t_pers_a_mails"
                # il y a une contrainte sur les FK de la table intermédiaire "t_pers_a_mails"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce mail est associé à des personnes dans la t_pers_a_mails !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce mail est associé à des personnes dans la t_pers_a_mails !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
