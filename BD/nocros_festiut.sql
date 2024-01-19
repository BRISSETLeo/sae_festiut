-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql-nocros.alwaysdata.net
-- Generation Time: Jan 19, 2024 at 08:20 AM
-- Server version: 10.6.14-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nocros_festiut`
--

-- --------------------------------------------------------

--
-- Table structure for table `artiste`
--

CREATE TABLE `artiste` (
  `nomArtiste` varchar(50) NOT NULL,
  `groupeArtiste` varchar(50) DEFAULT NULL,
  `styleArtiste` varchar(50) NOT NULL,
  `imageArtiste` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `billet`
--

CREATE TABLE `billet` (
  `idAchat` int(11) NOT NULL,
  `typeBillet` varchar(50) NOT NULL,
  `nomUser` varchar(25) NOT NULL,
  `dateAchat` datetime NOT NULL,
  `dateDebut` datetime NOT NULL,
  `dateFin` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `idEvent` int(11) NOT NULL,
  `nomEvent` varchar(50) NOT NULL,
  `typeEvent` varchar(50) NOT NULL,
  `lieuEvent` varchar(50) NOT NULL,
  `heureDebutEvent` time NOT NULL,
  `heureFinEvent` time NOT NULL,
  `descriptionEvent` varchar(500) NOT NULL,
  `imageEvent` longblob DEFAULT NULL,
  `estGratuit` tinyint(1) NOT NULL,
  `journeeEvent` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Je veux un délimiter pour pas que heureDebutEvent soit supérieur ou égal à heureFinEvent

DELIMITER | 

CREATE TRIGGER `event_before_insert` BEFORE INSERT ON `event` FOR EACH ROW BEGIN
    IF NEW.`heureDebutEvent` >= NEW.`heureFinEvent` THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "L'heure de début doit être strictement inférieure à l'heure de fin";
    END IF;
END |

DELIMITER ;

DELIMITER | 

CREATE TRIGGER `event_before_insert` BEFORE UPDATE ON `event` FOR EACH ROW BEGIN
    IF NEW.`heureDebutEvent` >= NEW.`heureFinEvent` THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "L'heure de début doit être strictement inférieure à l'heure de fin";
    END IF;
END |

DELIMITER ;

-- Je veux un délimiter qui permet d'éviter les chevauchements de date et d'heure d'un event de même salle et de même jour
DELIMITER |

CREATE TRIGGER prevent_overlap_dates
BEFORE INSERT ON event
FOR EACH ROW
BEGIN
    DECLARE overlap_count INT;
    SELECT COUNT(*)
    INTO overlap_count
    FROM event
    WHERE lieuEvent = NEW.lieuEvent
        AND journeeEvent = NEW.journeeEvent
        AND (
            (NEW.heureDebutEvent < heureFinEvent AND NEW.heureFinEvent > heureDebutEvent)
            OR (heureDebutEvent < NEW.heureFinEvent AND heureFinEvent > NEW.heureDebutEvent)
            OR (heureDebutEvent = NEW.heureDebutEvent AND heureFinEvent = NEW.heureFinEvent)
        );
    IF overlap_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Chevauchement de dates détecté pour le même lieu et la même journée';
    END IF;
END |

DELIMITER ;

-- Je veux un délimiter qui permet d'éviter les chevauchements de date et d'heure d'un event de même salle et de même jour
DELIMITER |

CREATE TRIGGER prevent_overlap_dates_on_update
BEFORE UPDATE ON event
FOR EACH ROW
BEGIN
    DECLARE overlap_count INT;

    -- Vérifier s'il y a des chevauchements de dates pour le même lieu et la même journée
    SELECT COUNT(*)
    INTO overlap_count
    FROM event
    WHERE lieuEvent = NEW.lieuEvent
        AND journeeEvent = NEW.journeeEvent
        AND idEvent != NEW.idEvent
        AND (
            (NEW.heureDebutEvent < heureFinEvent AND NEW.heureFinEvent > heureDebutEvent)
            OR (heureDebutEvent < NEW.heureFinEvent AND heureFinEvent > NEW.heureDebutEvent)
            OR (heureDebutEvent = NEW.heureDebutEvent AND heureFinEvent = NEW.heureFinEvent)
        );

    -- Si des chevauchements sont détectés, signaler une erreur
    IF overlap_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Chevauchement de dates détecté pour le même lieu et la même journée lors de la mise à jour';
    END IF;
END |

DELIMITER ;



--
-- Dumping data for table `event`
--

INSERT INTO `event` (`idEvent`, `nomEvent`, `typeEvent`, `lieuEvent`, `heureDebutEvent`, `heureFinEvent`, `descriptionEvent`, `imageEvent`, `estGratuit`, `journeeEvent`) VALUES
(5, 'test', 'Concert', 'Zenith', '10:10:00', '20:10:00', 'test', NULL, 1, 1),
(6, 'test', 'Concert', 'Zenith', '08:08:00', '09:09:00', 'test', NULL, 1, 1),
(7, 'test', 'Atelier', 'Comet', '08:08:00', '09:09:00', 'test', NULL, 1, 2),
(8, 'test', 'Atelier', 'Comet', '08:09:00', '10:10:00', 'test', NULL, 1, 2),
(9, 'test', 'Concert', 'Zenith', '08:09:00', '08:09:00', 'test', NULL, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `festival`
--

CREATE TABLE `festival` (
  `nomFestival` varchar(50) NOT NULL,
  `villeFestival` varchar(50) NOT NULL,
  `codePostalFestival` varchar(5) NOT NULL,
  `dateDebutFestival` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `festival`
--

INSERT INTO `festival` (`nomFestival`, `villeFestival`, `codePostalFestival`, `dateDebutFestival`) VALUES
('FestIUT\'O 2ème édition', 'Orléans', '45000', '2024-01-19');

-- --------------------------------------------------------

--
-- Table structure for table `groupe`
--

CREATE TABLE `groupe` (
  `nomGroupe` varchar(50) NOT NULL,
  `styleGroupe` varchar(50) NOT NULL,
  `imageGroupe` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `journee`
--

CREATE TABLE `journee` (
  `idJournee` int(11) NOT NULL,
  `nomFestivalJournee` varchar(50) NOT NULL,
  `dateJournee` date NOT NULL,
  `lieuJournee` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `journee`
--

INSERT INTO `journee` (`idJournee`, `nomFestivalJournee`, `dateJournee`, `lieuJournee`) VALUES
(1, 'FestIUT\'O 2ème édition', '2024-01-19', 'Zenith'),
(2, 'FestIUT\'O 2ème édition', '2024-01-20', 'Comet'),
(3, 'FestIUT\'O 2ème édition', '2024-01-21', 'Zenith');

-- --------------------------------------------------------

--
-- Table structure for table `lien`
--

CREATE TABLE `lien` (
  `idLien` int(11) NOT NULL,
  `typeLien` varchar(50) NOT NULL,
  `urlLien` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lien_artiste`
--

CREATE TABLE `lien_artiste` (
  `nomArtiste` varchar(50) NOT NULL,
  `idLien` int(11) NOT NULL,
  `dateLien` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lien_groupe`
--

CREATE TABLE `lien_groupe` (
  `nomGroupe` varchar(50) NOT NULL,
  `idLien` int(11) NOT NULL,
  `dateLien` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lieu`
--

CREATE TABLE `lieu` (
  `nomLieu` varchar(50) NOT NULL,
  `adresseLieu` varchar(50) NOT NULL,
  `nbPlaceLieu` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lieu`
--

INSERT INTO `lieu` (`nomLieu`, `adresseLieu`, `nbPlaceLieu`) VALUES
('Comet', '4 rue commet', 120),
('Zenith', '1 rue des Zeniths', 600);

-- --------------------------------------------------------

--
-- Table structure for table `logement`
--

CREATE TABLE `logement` (
  `idLogement` int(11) NOT NULL,
  `nomLogement` varchar(50) NOT NULL,
  `adresseLogement` varchar(50) NOT NULL,
  `codePostalLogement` varchar(5) NOT NULL,
  `villeLogement` varchar(50) NOT NULL,
  `nbPlaceLogement` int(11) NOT NULL,
  `prixLogement` int(11) NOT NULL,
  `descriptionLogement` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `participer_artiste`
--

CREATE TABLE `participer_artiste` (
  `nomArtiste` varchar(50) NOT NULL,
  `idEvent` int(11) NOT NULL,
  `idLogement` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `participer_groupe`
--

CREATE TABLE `participer_groupe` (
  `nomGroupe` varchar(50) NOT NULL,
  `idEvent` int(11) NOT NULL,
  `idLogement` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `nomRole` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`nomRole`) VALUES
('Administrateur'),
('Utilisateur');

-- --------------------------------------------------------

--
-- Table structure for table `style_musique`
--

CREATE TABLE `style_musique` (
  `nomStyleMusique` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `style_musique`
--

INSERT INTO `style_musique` (`nomStyleMusique`) VALUES
('Classique'),
('Country'),
('Electro'),
('Folk'),
('Jazz'),
('Metal'),
('Pop'),
('Rap'),
('Reggae'),
('Rock'),
('Variété');

-- --------------------------------------------------------

--
-- Table structure for table `type_billet`
--

CREATE TABLE `type_billet` (
  `nomTypeBillet` varchar(50) NOT NULL,
  `prixBillet` int(11) NOT NULL,
  `imageBillet` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `type_billet`
--

INSERT INTO `type_billet` (`nomTypeBillet`, `prixBillet`, `imageBillet`) VALUES
('2 jours', 70, NULL),
('Journée', 49, NULL),
('Totalité du festival', 90, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `type_event`
--

CREATE TABLE `type_event` (
  `nomTypeEvent` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `type_event`
--

INSERT INTO `type_event` (`nomTypeEvent`) VALUES
('Atelier'),
('Concert'),
('Conférence'),
('Débat'),
('Dédicace'),
('Exposition'),
('Projection'),
('Rencontre'),
('Spectacle');

-- --------------------------------------------------------

--
-- Table structure for table `type_lien`
--

CREATE TABLE `type_lien` (
  `nomTypeLien` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `type_lien`
--

INSERT INTO `type_lien` (`nomTypeLien`) VALUES
('Réseau'),
('Vidéo');

-- --------------------------------------------------------

--
-- Table structure for table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `nom` varchar(25) NOT NULL,
  `password` varchar(80) NOT NULL,
  `monRole` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `utilisateur`
--

INSERT INTO `utilisateur` (`nom`, `password`, `monRole`) VALUES
('adm', '86f65e28a754e1a71b2df9403615a6c436c32c42a75a10d02813961b86f1e428', 'Administrateur'),
('salut', 'ec9c3a34e791bda21bbcb69ea0eb875857497e0d48c75771b3d1adb5073ce791', 'Utilisateur');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `artiste`
--
ALTER TABLE `artiste`
  ADD PRIMARY KEY (`nomArtiste`),
  ADD KEY `groupeArtiste` (`groupeArtiste`),
  ADD KEY `styleArtiste` (`styleArtiste`);

--
-- Indexes for table `billet`
--
ALTER TABLE `billet`
  ADD PRIMARY KEY (`idAchat`),
  ADD KEY `typeBillet` (`typeBillet`),
  ADD KEY `nomUser` (`nomUser`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`idEvent`),
  ADD KEY `typeEvent` (`typeEvent`),
  ADD KEY `lieuEvent` (`lieuEvent`),
  ADD KEY `journeeEvent` (`journeeEvent`);

--
-- Indexes for table `festival`
--
ALTER TABLE `festival`
  ADD PRIMARY KEY (`nomFestival`);

--
-- Indexes for table `groupe`
--
ALTER TABLE `groupe`
  ADD PRIMARY KEY (`nomGroupe`),
  ADD KEY `styleGroupe` (`styleGroupe`);

--
-- Indexes for table `journee`
--
ALTER TABLE `journee`
  ADD PRIMARY KEY (`idJournee`),
  ADD KEY `nomFestivalJournee` (`nomFestivalJournee`),
  ADD KEY `lieuJournee` (`lieuJournee`);

--
-- Indexes for table `lien`
--
ALTER TABLE `lien`
  ADD PRIMARY KEY (`idLien`),
  ADD KEY `typeLien` (`typeLien`);

--
-- Indexes for table `lien_artiste`
--
ALTER TABLE `lien_artiste`
  ADD PRIMARY KEY (`nomArtiste`,`idLien`),
  ADD UNIQUE KEY `idLien` (`idLien`);

--
-- Indexes for table `lien_groupe`
--
ALTER TABLE `lien_groupe`
  ADD PRIMARY KEY (`nomGroupe`,`idLien`),
  ADD UNIQUE KEY `idLien` (`idLien`);

--
-- Indexes for table `lieu`
--
ALTER TABLE `lieu`
  ADD PRIMARY KEY (`nomLieu`);

--
-- Indexes for table `logement`
--
ALTER TABLE `logement`
  ADD PRIMARY KEY (`idLogement`);

--
-- Indexes for table `participer_artiste`
--
ALTER TABLE `participer_artiste`
  ADD PRIMARY KEY (`nomArtiste`,`idEvent`),
  ADD UNIQUE KEY `idEvent` (`idEvent`),
  ADD KEY `idLogement` (`idLogement`);

--
-- Indexes for table `participer_groupe`
--
ALTER TABLE `participer_groupe`
  ADD PRIMARY KEY (`nomGroupe`,`idEvent`),
  ADD UNIQUE KEY `idEvent` (`idEvent`),
  ADD KEY `idLogement` (`idLogement`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`nomRole`);

--
-- Indexes for table `style_musique`
--
ALTER TABLE `style_musique`
  ADD PRIMARY KEY (`nomStyleMusique`);

--
-- Indexes for table `type_billet`
--
ALTER TABLE `type_billet`
  ADD PRIMARY KEY (`nomTypeBillet`);

--
-- Indexes for table `type_event`
--
ALTER TABLE `type_event`
  ADD PRIMARY KEY (`nomTypeEvent`);

--
-- Indexes for table `type_lien`
--
ALTER TABLE `type_lien`
  ADD PRIMARY KEY (`nomTypeLien`);

--
-- Indexes for table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`nom`),
  ADD KEY `monRole` (`monRole`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `billet`
--
ALTER TABLE `billet`
  MODIFY `idAchat` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `idEvent` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `journee`
--
ALTER TABLE `journee`
  MODIFY `idJournee` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `lien`
--
ALTER TABLE `lien`
  MODIFY `idLien` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `logement`
--
ALTER TABLE `logement`
  MODIFY `idLogement` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `artiste`
--
ALTER TABLE `artiste`
  ADD CONSTRAINT `artiste_ibfk_1` FOREIGN KEY (`groupeArtiste`) REFERENCES `groupe` (`nomGroupe`),
  ADD CONSTRAINT `artiste_ibfk_2` FOREIGN KEY (`styleArtiste`) REFERENCES `style_musique` (`nomStyleMusique`);

--
-- Constraints for table `billet`
--
ALTER TABLE `billet`
  ADD CONSTRAINT `billet_ibfk_1` FOREIGN KEY (`typeBillet`) REFERENCES `type_billet` (`nomTypeBillet`),
  ADD CONSTRAINT `billet_ibfk_2` FOREIGN KEY (`nomUser`) REFERENCES `utilisateur` (`nom`);

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_1` FOREIGN KEY (`typeEvent`) REFERENCES `type_event` (`nomTypeEvent`),
  ADD CONSTRAINT `event_ibfk_2` FOREIGN KEY (`lieuEvent`) REFERENCES `lieu` (`nomLieu`),
  ADD CONSTRAINT `event_ibfk_3` FOREIGN KEY (`journeeEvent`) REFERENCES `journee` (`idJournee`);

--
-- Constraints for table `groupe`
--
ALTER TABLE `groupe`
  ADD CONSTRAINT `groupe_ibfk_1` FOREIGN KEY (`styleGroupe`) REFERENCES `style_musique` (`nomStyleMusique`);

--
-- Constraints for table `journee`
--
ALTER TABLE `journee`
  ADD CONSTRAINT `journee_ibfk_1` FOREIGN KEY (`nomFestivalJournee`) REFERENCES `festival` (`nomFestival`),
  ADD CONSTRAINT `journee_ibfk_2` FOREIGN KEY (`lieuJournee`) REFERENCES `lieu` (`nomLieu`);

--
-- Constraints for table `lien`
--
ALTER TABLE `lien`
  ADD CONSTRAINT `lien_ibfk_1` FOREIGN KEY (`typeLien`) REFERENCES `type_lien` (`nomTypeLien`);

--
-- Constraints for table `lien_artiste`
--
ALTER TABLE `lien_artiste`
  ADD CONSTRAINT `lien_artiste_ibfk_1` FOREIGN KEY (`nomArtiste`) REFERENCES `artiste` (`nomArtiste`),
  ADD CONSTRAINT `lien_artiste_ibfk_2` FOREIGN KEY (`idLien`) REFERENCES `lien` (`idLien`);

--
-- Constraints for table `lien_groupe`
--
ALTER TABLE `lien_groupe`
  ADD CONSTRAINT `lien_groupe_ibfk_1` FOREIGN KEY (`nomGroupe`) REFERENCES `groupe` (`nomGroupe`),
  ADD CONSTRAINT `lien_groupe_ibfk_2` FOREIGN KEY (`idLien`) REFERENCES `lien` (`idLien`);

--
-- Constraints for table `participer_artiste`
--
ALTER TABLE `participer_artiste`
  ADD CONSTRAINT `participer_artiste_ibfk_1` FOREIGN KEY (`nomArtiste`) REFERENCES `artiste` (`nomArtiste`),
  ADD CONSTRAINT `participer_artiste_ibfk_2` FOREIGN KEY (`idEvent`) REFERENCES `event` (`idEvent`),
  ADD CONSTRAINT `participer_artiste_ibfk_3` FOREIGN KEY (`idLogement`) REFERENCES `logement` (`idLogement`);

--
-- Constraints for table `participer_groupe`
--
ALTER TABLE `participer_groupe`
  ADD CONSTRAINT `participer_groupe_ibfk_1` FOREIGN KEY (`nomGroupe`) REFERENCES `groupe` (`nomGroupe`),
  ADD CONSTRAINT `participer_groupe_ibfk_2` FOREIGN KEY (`idEvent`) REFERENCES `event` (`idEvent`),
  ADD CONSTRAINT `participer_groupe_ibfk_3` FOREIGN KEY (`idLogement`) REFERENCES `logement` (`idLogement`);

--
-- Constraints for table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD CONSTRAINT `utilisateur_ibfk_1` FOREIGN KEY (`monRole`) REFERENCES `role` (`nomRole`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
