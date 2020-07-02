-- EZ 2020.07.12
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: erblin_zeqiri_conf_serveur_1c_2020

-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS erblin_zeqiri_conf_serveur_1c_2020;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS erblin_zeqiri_conf_serveur_1c_2020;

-- Utilisation de cette base de donnée

USE erblin_zeqiri_conf_serveur_1c_2020;
-- --------------------------------------------------------
-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Jeu 02 Juillet 2020 à 18:56
-- Version du serveur :  5.7.11
-- Version de PHP :  5.6.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `erblin_zeqiri_conf_serveur_1c_2020`
--

-- --------------------------------------------------------

--
-- Structure de la table `t_location`
--

CREATE TABLE `t_location` (
  `ID_Location` int(11) NOT NULL,
  `Location` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_location`
--

INSERT INTO `t_location` (`ID_Location`, `Location`) VALUES
(5, 'Bureau 1'),
(6, 'Bureau 2'),
(7, 'Bureau 3'),
(8, 'Bureau 4'),
(9, 'Bureau 5');

-- --------------------------------------------------------

--
-- Structure de la table `t_mail`
--

CREATE TABLE `t_mail` (
  `ID_Mail` int(11) NOT NULL,
  `Adresse_Mail` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_mail`
--

INSERT INTO `t_mail` (`ID_Mail`, `Adresse_Mail`) VALUES
(1, 'fedsad@dsds.cj'),
(2, 'clowneriea'),
(4, 'Jean@dujardin.ch'),
(5, 'pierre@bourne.com'),
(9, 'nss@hotmail.com'),
(11, 'tttttt@ttt.ch'),
(13, 'asdas2@sadds.com');

-- --------------------------------------------------------

--
-- Structure de la table `t_personne`
--

CREATE TABLE `t_personne` (
  `ID_Personne` int(11) NOT NULL,
  `Nom_Pers` varchar(40) DEFAULT NULL,
  `Prenom_Pers` varchar(40) DEFAULT NULL,
  `Date_Naissance_Pers` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_personne`
--

INSERT INTO `t_personne` (`ID_Personne`, `Nom_Pers`, `Prenom_Pers`, `Date_Naissance_Pers`) VALUES
(1, 'Zeqiri', 'Erblin', '1998-09-17'),
(4, 'Jean', 'Dujardin', '1985-11-25'),
(6, 'Jhon', 'Ofthegarden', '1985-11-25'),
(8, 'Bite', 'Rivière', '2000-09-28'),
(10, 'Dick', 'River', '2004-10-20'),
(14, 'Bourn', 'Pierre', '1985-06-02'),
(15, 'NSs', 'Zeqiri', '2007-06-07'),
(16, 'ee', 'ee', '2004-11-30');

-- --------------------------------------------------------

--
-- Structure de la table `t_pers_a_mail`
--

CREATE TABLE `t_pers_a_mail` (
  `ID_Pers_A_Mail` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Mail` int(11) NOT NULL,
  `Date_Mail` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_pers_a_mail`
--

INSERT INTO `t_pers_a_mail` (`ID_Pers_A_Mail`, `FK_Personne`, `FK_Mail`, `Date_Mail`) VALUES
(1, 1, 1, '2020-03-10 17:05:59'),
(5, 4, 4, '2020-04-05 14:33:55'),
(6, 1, 4, '2020-06-22 23:12:14'),
(7, 1, 5, '2020-06-23 09:54:43'),
(8, 15, 9, '2020-06-23 13:46:24');

-- --------------------------------------------------------

--
-- Structure de la table `t_pers_a_serveur`
--

CREATE TABLE `t_pers_a_serveur` (
  `ID_Pers_A_Serveur` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Serveur` int(11) NOT NULL,
  `Date_Pers_Ask_Serveur` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_pers_a_serveur`
--

INSERT INTO `t_pers_a_serveur` (`ID_Pers_A_Serveur`, `FK_Personne`, `FK_Serveur`, `Date_Pers_Ask_Serveur`) VALUES
(2, 1, 1, '2020-03-10 17:06:27'),
(3, 1, 3, '2020-03-29 14:56:41'),
(4, 1, 3, '2020-04-05 13:15:25'),
(5, 1, 8, '2020-06-23 09:55:42'),
(7, 4, 8, '2020-06-23 09:55:42'),
(8, 6, 8, '2020-06-23 09:55:42'),
(9, 15, 7, '2020-06-23 13:49:31'),
(10, 4, 2, '2020-07-02 16:32:30'),
(11, 1, 10, '2020-07-02 16:36:32');

-- --------------------------------------------------------

--
-- Structure de la table `t_serveur`
--

CREATE TABLE `t_serveur` (
  `ID_Serveur` int(11) NOT NULL,
  `Nom_Serv` varchar(30) NOT NULL,
  `Nombre_Port` int(24) NOT NULL,
  `Nombre_U` int(42) NOT NULL,
  `Date_Conf_Serv` date NOT NULL,
  `Description` text NOT NULL,
  `Puissance` int(11) NOT NULL,
  `Date_Serveur` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serveur`
--

INSERT INTO `t_serveur` (`ID_Serveur`, `Nom_Serv`, `Nombre_Port`, `Nombre_U`, `Date_Conf_Serv`, `Description`, `Puissance`, `Date_Serveur`) VALUES
(1, 'rtzdfdrtzz', 2, 4, '2020-07-24', 'voila voila', 51, '2020-03-10 15:13:24'),
(2, 'bvcxbcvbvbvc', 31121231, 2111, '2020-07-24', 'qweweqewq', 21321321, '2020-03-10 17:05:29'),
(3, 'fdgdfdfg', 65, 45, '2020-07-15', 'voilà c\'est tellement rose', 0, '2020-03-24 19:42:46'),
(5, 'serveur23', 234, 2111, '2020-05-15', 'werew', 323223, '2020-04-05 13:30:49'),
(6, 'serveur23', 20, 12, '2020-05-15', 'wesh bien ou quoi', 2500, '2020-04-05 13:33:05'),
(7, 'tg', 27, 27, '2020-05-20', 'tg bouffon\r\n', 5345, '2020-05-20 12:36:49'),
(8, 'tg', 27, 27, '2020-07-24', 'tg bouffon', 5345, '2020-05-27 12:04:47'),
(9, 'rterr45dewe', 5, 5, '2020-07-16', 'reterege', 4, '2020-07-02 15:48:16'),
(10, 'Serveur', 26, 26, '2020-07-30', 'Serveur', 2500, '2020-07-02 16:36:22');

-- --------------------------------------------------------

--
-- Structure de la table `t_serv_a_location`
--

CREATE TABLE `t_serv_a_location` (
  `ID_Serv_A_Location` int(11) NOT NULL,
  `FK_Serveur` int(11) NOT NULL,
  `FK_Location` int(11) NOT NULL,
  `Date_Serv_A_Location` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serv_a_location`
--

INSERT INTO `t_serv_a_location` (`ID_Serv_A_Location`, `FK_Serveur`, `FK_Location`, `Date_Serv_A_Location`) VALUES
(7, 1, 5, '2020-07-02 16:40:33');

-- --------------------------------------------------------

--
-- Structure de la table `t_serv_a_status`
--

CREATE TABLE `t_serv_a_status` (
  `ID_Serv_A_Status` int(11) NOT NULL,
  `FK_Serveur` int(11) NOT NULL,
  `FK_Status` int(11) NOT NULL,
  `Date_Serv_A_Status` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serv_a_status`
--

INSERT INTO `t_serv_a_status` (`ID_Serv_A_Status`, `FK_Serveur`, `FK_Status`, `Date_Serv_A_Status`) VALUES
(1, 2, 1, '2020-03-10 17:07:07'),
(4, 1, 1, '2020-06-23 11:50:58'),
(6, 7, 1, '2020-07-02 16:14:03'),
(7, 6, 7, '2020-07-02 16:28:44');

-- --------------------------------------------------------

--
-- Structure de la table `t_serv_a_type_equipement`
--

CREATE TABLE `t_serv_a_type_equipement` (
  `ID_Serv_A_Type_Equipement` int(11) NOT NULL,
  `Fk_Serveur` int(11) NOT NULL,
  `FK_Type_Equipement` int(11) NOT NULL,
  `Date_Serv_A_Type_Equipement` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serv_a_type_equipement`
--

INSERT INTO `t_serv_a_type_equipement` (`ID_Serv_A_Type_Equipement`, `Fk_Serveur`, `FK_Type_Equipement`, `Date_Serv_A_Type_Equipement`) VALUES
(3, 6, 3, '2020-04-05 14:52:33'),
(4, 1, 1, '2020-07-02 16:30:43'),
(5, 2, 3, '2020-07-02 16:30:50'),
(6, 2, 6, '2020-07-02 16:30:50');

-- --------------------------------------------------------

--
-- Structure de la table `t_status`
--

CREATE TABLE `t_status` (
  `ID_Status` int(11) NOT NULL,
  `Status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_status`
--

INSERT INTO `t_status` (`ID_Status`, `Status`) VALUES
(1, 'Traité'),
(7, 'Désangager'),
(8, 'Traité'),
(9, 'A traité'),
(10, 'asdew3');

-- --------------------------------------------------------

--
-- Structure de la table `t_type_equipement`
--

CREATE TABLE `t_type_equipement` (
  `ID_Type_Equipement` int(11) NOT NULL,
  `Type_Equipement` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_type_equipement`
--

INSERT INTO `t_type_equipement` (`ID_Type_Equipement`, `Type_Equipement`) VALUES
(1, 'cxvxvxcv'),
(3, 'voilà c\'est tellement rose'),
(6, 'fdgfdgdfgdfgfdgdfdf'),
(7, 'asdw2asdas22');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_location`
--
ALTER TABLE `t_location`
  ADD PRIMARY KEY (`ID_Location`);

--
-- Index pour la table `t_mail`
--
ALTER TABLE `t_mail`
  ADD PRIMARY KEY (`ID_Mail`);

--
-- Index pour la table `t_personne`
--
ALTER TABLE `t_personne`
  ADD PRIMARY KEY (`ID_Personne`);

--
-- Index pour la table `t_pers_a_mail`
--
ALTER TABLE `t_pers_a_mail`
  ADD PRIMARY KEY (`ID_Pers_A_Mail`),
  ADD KEY `FK_Mail` (`FK_Mail`),
  ADD KEY `FK_Personne` (`FK_Personne`);

--
-- Index pour la table `t_pers_a_serveur`
--
ALTER TABLE `t_pers_a_serveur`
  ADD PRIMARY KEY (`ID_Pers_A_Serveur`),
  ADD KEY `FK_Personne` (`FK_Personne`),
  ADD KEY `FK_Serveur` (`FK_Serveur`);

--
-- Index pour la table `t_serveur`
--
ALTER TABLE `t_serveur`
  ADD PRIMARY KEY (`ID_Serveur`);

--
-- Index pour la table `t_serv_a_location`
--
ALTER TABLE `t_serv_a_location`
  ADD PRIMARY KEY (`ID_Serv_A_Location`),
  ADD KEY `FK_Serveur` (`FK_Serveur`),
  ADD KEY `FK_Location` (`FK_Location`);

--
-- Index pour la table `t_serv_a_status`
--
ALTER TABLE `t_serv_a_status`
  ADD PRIMARY KEY (`ID_Serv_A_Status`),
  ADD KEY `FK_Serveur` (`FK_Serveur`),
  ADD KEY `FK_Status` (`FK_Status`);

--
-- Index pour la table `t_serv_a_type_equipement`
--
ALTER TABLE `t_serv_a_type_equipement`
  ADD PRIMARY KEY (`ID_Serv_A_Type_Equipement`),
  ADD KEY `Fk_Serveur` (`Fk_Serveur`),
  ADD KEY `FK_Type_Equipement` (`FK_Type_Equipement`);

--
-- Index pour la table `t_status`
--
ALTER TABLE `t_status`
  ADD PRIMARY KEY (`ID_Status`);

--
-- Index pour la table `t_type_equipement`
--
ALTER TABLE `t_type_equipement`
  ADD PRIMARY KEY (`ID_Type_Equipement`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_location`
--
ALTER TABLE `t_location`
  MODIFY `ID_Location` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT pour la table `t_mail`
--
ALTER TABLE `t_mail`
  MODIFY `ID_Mail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT pour la table `t_personne`
--
ALTER TABLE `t_personne`
  MODIFY `ID_Personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT pour la table `t_pers_a_mail`
--
ALTER TABLE `t_pers_a_mail`
  MODIFY `ID_Pers_A_Mail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `t_pers_a_serveur`
--
ALTER TABLE `t_pers_a_serveur`
  MODIFY `ID_Pers_A_Serveur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT pour la table `t_serveur`
--
ALTER TABLE `t_serveur`
  MODIFY `ID_Serveur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `t_serv_a_location`
--
ALTER TABLE `t_serv_a_location`
  MODIFY `ID_Serv_A_Location` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT pour la table `t_serv_a_status`
--
ALTER TABLE `t_serv_a_status`
  MODIFY `ID_Serv_A_Status` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT pour la table `t_serv_a_type_equipement`
--
ALTER TABLE `t_serv_a_type_equipement`
  MODIFY `ID_Serv_A_Type_Equipement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT pour la table `t_status`
--
ALTER TABLE `t_status`
  MODIFY `ID_Status` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `t_type_equipement`
--
ALTER TABLE `t_type_equipement`
  MODIFY `ID_Type_Equipement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_pers_a_mail`
--
ALTER TABLE `t_pers_a_mail`
  ADD CONSTRAINT `t_pers_a_mail_ibfk_1` FOREIGN KEY (`FK_Personne`) REFERENCES `t_personne` (`ID_Personne`),
  ADD CONSTRAINT `t_pers_a_mail_ibfk_2` FOREIGN KEY (`FK_Mail`) REFERENCES `t_mail` (`ID_Mail`);

--
-- Contraintes pour la table `t_pers_a_serveur`
--
ALTER TABLE `t_pers_a_serveur`
  ADD CONSTRAINT `t_pers_a_serveur_ibfk_1` FOREIGN KEY (`FK_Personne`) REFERENCES `t_personne` (`ID_Personne`),
  ADD CONSTRAINT `t_pers_a_serveur_ibfk_2` FOREIGN KEY (`FK_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`);

--
-- Contraintes pour la table `t_serv_a_location`
--
ALTER TABLE `t_serv_a_location`
  ADD CONSTRAINT `t_serv_a_location_ibfk_1` FOREIGN KEY (`FK_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`),
  ADD CONSTRAINT `t_serv_a_location_ibfk_2` FOREIGN KEY (`FK_Location`) REFERENCES `t_location` (`ID_Location`);

--
-- Contraintes pour la table `t_serv_a_status`
--
ALTER TABLE `t_serv_a_status`
  ADD CONSTRAINT `t_serv_a_status_ibfk_1` FOREIGN KEY (`FK_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`),
  ADD CONSTRAINT `t_serv_a_status_ibfk_2` FOREIGN KEY (`FK_Status`) REFERENCES `t_status` (`ID_Status`);

--
-- Contraintes pour la table `t_serv_a_type_equipement`
--
ALTER TABLE `t_serv_a_type_equipement`
  ADD CONSTRAINT `t_serv_a_type_equipement_ibfk_1` FOREIGN KEY (`Fk_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`),
  ADD CONSTRAINT `t_serv_a_type_equipement_ibfk_2` FOREIGN KEY (`FK_Type_Equipement`) REFERENCES `t_type_equipement` (`ID_Type_Equipement`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
