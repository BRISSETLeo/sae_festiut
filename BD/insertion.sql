-- STYLE_MUSIQUE
INSERT INTO STYLE_MUSIQUE (id_styleM, type_styleM) VALUES
(1, 'Rock'),
(2, 'Pop'),
(3, 'Electro'),
(4, 'Classique'),
(5, 'Jazz');

-- ROLE
INSERT INTO ROLE (id_role, nom_role) VALUES
(1, 'Administrateur'),
(2, 'Spectateur'),
(3, 'Artiste');

-- HEBERGEMENT
INSERT INTO HEBERGEMENT (id_hebergement, nom_Hebergement, nbr_places) VALUES
(1, 'Hôtel de Ville', 100),
(2, 'Salle des Fêtes', 500),
(3, 'Stade Municipal', 1000);

-- LIEN_VIDEO
INSERT INTO LIEN_VIDEO (id_lien_video, video_lien) VALUES
(1, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
(2, 'https://www.youtube.com/watch?v=MeWLb3L8t1Y'),
(3, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ');

-- EVENEMENT
INSERT INTO EVENEMENT (id_event, capacite, est_gratuit) VALUES
(1, 1000, FALSE),
(2, 500, TRUE),
(3, 100, FALSE);

-- BILLET_TYPE
INSERT INTO BILLET_TYPE (type_billet, nom_billet) VALUES
('1jour', 'Billet journée'),
('2jours', 'Billet 2 jours'),
('FestivalComplet', 'Billet');

-- LIEN_RESEAU
INSERT INTO LIEN_RESEAU (id_lien_reseau, reseau_lien) VALUES
(1, 'https://www.facebook.com/myevent'),
(2, 'https://www.instagram.com/myevent'),
(3, 'https://www.twitter.com/myevent');

-- UTILISATEUR
INSERT INTO UTILISATEUR (id_utilisateur, nom_user, tel, mail, age, mot_de_passe, id_role) VALUES
(1, 'John Doe', '+33612345678', '', 30, 'password', 2),
(2, 'Jane Doe', '+33687654321', '', 25, 'password', 2),
(3, 'Admin', '+337987654321', '', 40, 'password', 1);

-- BILLET
INSERT INTO BILLET (id_billet, prix_billet, description_billet, type_billet, id_event) VALUES
(1, 20.00, 'Billet standard', 'STANDARD', 1),
(2, 30.00, 'Billet VIP', 'VIP', 1),
(3, 10.00, 'Billet enfant', 'ENFANT', 1);


-- SPECTATEUR
INSERT INTO SPECTATEUR (id_spectateur, id_billet, id_utilisateur) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 2);

-- GROUPE
INSERT INTO GROUPE (id_groupe, nom_groupe, description_groupe, photo, jourHeurArr, jourHeurDep, dureeConcert, tempsMontage, tempsDemontage, id_lien_reseau, id_lien_video, id_hebergement, id_styleM) VALUES
(1, 'My Band', 'This is my band', 'https://example.com/myband.jpg', '2023-10-21 18:00:00', '2023-10-21 20:00:00', 120, 60, 30, 1, 2, 3, 1);

-- ARTISTE
INSERT INTO ARTISTE (id_artiste, nom_artiste, id_groupe) VALUES
(1, 'John Doe', 1),
(2, 'Jane Doe', 1);

-- INSTRUMENT
INSERT INTO INSTRUMENT (id_instrument, nom_instrument, id_groupe, id_artiste) VALUES
(1, 'Guitare', 1, 1),
(2, 'Batterie', 1, 2),
(3, 'Basse', 1, 1);

-- JOUER_INSTRUMENT
INSERT INTO JOUER_INSTRUMENT (id_artiste, id_instrument) VALUES
(1, 1),
(2, 2),
(1, 3);

-- GROUPE_FAVORIS
INSERT INTO GROUPE_FAVORIS (id_groupe, id_spectateur) VALUES
(1, 1),
(1, 2);



-- TRUC A FAIRE OU VERIFIER:
-- consulter la programmation par journ ́ee (une journ ́ee peut commencer a
-- 14h et se terminer a 4h00 du matin) et par lieux, par artiste,.. 
-- Triggers pour l'heure et pour nombre de personne