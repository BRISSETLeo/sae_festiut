
-- Créer les tables
CREATE TABLE STYLE_MUSIQUE (
  id_styleM INT NOT NULL,
  type_styleM VARCHAR(255),
  PRIMARY KEY (id_styleM)
);

CREATE TABLE ROLE (
  id_role INT NOT NULL,
  nom_role VARCHAR(255),
  PRIMARY KEY (id_role)
);

CREATE TABLE HEBERGEMENT (
  id_hebergement INT NOT NULL,
  nom_Hebergement VARCHAR(255),
  nbr_places INT,
  PRIMARY KEY (id_hebergement)
);

CREATE TABLE LIEN_VIDEO (
  id_lien_video INT NOT NULL,
  video_lien VARCHAR(255),
  PRIMARY KEY (id_lien_video)
);

CREATE TABLE EVENEMENT (
  id_event INT NOT NULL,
  capacite INT,
  est_gratuit BOOLEAN,
  PRIMARY KEY (id_event)
);

CREATE TABLE BILLET_TYPE (
  type_billet VARCHAR(255) NOT NULL,
  nom_billet VARCHAR(255),
  PRIMARY KEY (type_billet)
);

CREATE TABLE LIEN_RESEAU (
  id_lien_reseau INT,
  reseau_lien VARCHAR(255),
  PRIMARY KEY (id_lien_reseau)
);

CREATE TABLE UTILISATEUR (
  id_utilisateur INT NOT NULL,
  nom_user VARCHAR(255),
  tel VARCHAR(255),
  mail VARCHAR(255),
  age INT,
  mot_de_passe VARCHAR(255),
  id_role INT NOT NULL,
  PRIMARY KEY (id_utilisateur),
  FOREIGN KEY (id_role) REFERENCES ROLE (id_role)
);

CREATE TABLE BILLET (
  id_billet INT NOT NULL,
  prix_billet DECIMAL(10,2),
  description_billet VARCHAR(255),
  type_billet VARCHAR(255),
  id_event INT,
  PRIMARY KEY (id_billet),
  FOREIGN KEY (id_event) REFERENCES EVENEMENT (id_event)
);

CREATE TABLE SPECTATEUR (
  id_spectateur INT NOT NULL,
  id_billet INT,
  id_utilisateur INT NOT NULL,
  PRIMARY KEY (id_spectateur),
  FOREIGN KEY (id_billet) REFERENCES BILLET (id_billet),
  FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR (id_utilisateur)
);

CREATE TABLE GROUPE (
  id_groupe INT NOT NULL,
  nom_groupe VARCHAR(255),
  description_groupe VARCHAR(255),
  photo VARCHAR(255),
  jourHeurArr DATETIME,
  jourHeurDep DATETIME,
  dureeConcert INT,
  tempsMontage INT,
  tempsDemontage INT,
  id_lien_reseau INT,
  id_lien_video INT,
  id_hebergement INT,
  id_styleM INT NOT NULL,
  PRIMARY KEY (id_groupe),
  FOREIGN KEY (id_lien_reseau) REFERENCES LIEN_RESEAU (id_lien_reseau),
  FOREIGN KEY (id_lien_video) REFERENCES LIEN_VIDEO (id_lien_video),
  FOREIGN KEY (id_hebergement) REFERENCES HEBERGEMENT (id_hebergement),
  FOREIGN KEY (id_styleM) REFERENCES STYLE_MUSIQUE (id_styleM)
);


CREATE TABLE ARTISTE (
  id_artiste INT NOT NULL,
  nom_artiste VARCHAR(255),
  id_groupe INT NOT NULL,
  PRIMARY KEY (id_artiste),
  FOREIGN KEY (id_groupe) REFERENCES GROUPE (id_groupe)
);

CREATE TABLE INSTRUMENT (
  id_instrument INT,
  nom_instrument VARCHAR(255),
  id_groupe INT NOT NULL,
  id_artiste INT NOT NULL,
  PRIMARY KEY (id_instrument),
  FOREIGN KEY (id_artiste) REFERENCES ARTISTE (id_artiste)
);

CREATE TABLE JOUER_INSTRUMENT(
  id_artiste int,
  id_instrument int,
  PRIMARY KEY(id_artiste,id_instrument),
  FOREIGN KEY(id_artiste) REFERENCES ARTISTE(id_artiste),
  FOREIGN KEY(id_instrument) REFERENCES INSTRUMENT(id_instrument)
);

CREATE TABLE GROUPE_FAVORIS(
  id_groupe int,
  id_spectateur int,
  PRIMARY KEY(id_groupe,id_spectateur),
  FOREIGN KEY(id_groupe) REFERENCES GROUPE(id_groupe),
  FOREIGN KEY(id_spectateur) REFERENCES SPECTATEUR(id_spectateur)
);