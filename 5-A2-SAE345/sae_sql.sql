DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS casque;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS type_casque;




DROP TABLE IF EXISTS utilisateur;


CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),

    est_actif tinyint(1),
    -- token_email VARCHAR(255), --validation et mdp oublié


    PRIMARY KEY (id_utilisateur)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE taille(
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(200),
    PRIMARY KEY (id_taille)
);

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle VARCHAR(200),
   PRIMARY KEY(id_etat)
);

CREATE TABLE type_casque(
    id_type_casque INT AUTO_INCREMENT,
    libelle_type_casque VARCHAR(200),
    PRIMARY KEY (id_type_casque)
);

CREATE TABLE casque(
    id_casque INT AUTO_INCREMENT,
    nom_casque VARCHAR(200),
    poids NUMERIC(6,2),
    couleur VARCHAR(200),
    prix_casque NUMERIC(6,2),
    taille_id INT,
    type_casque_id INT,
    fournisseur VARCHAR(200),
    marque VARCHAR(200),
    stock INT,
    image VARCHAR(200),
    PRIMARY KEY (id_casque),
    CONSTRAINT fk_casque_taille FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
    CONSTRAINT fk_casque_type_epoque FOREIGN KEY (type_casque_id) REFERENCES type_casque(id_type_casque)
);
CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat VARCHAR(200),
   id_utilisateur INT NOT NULL,
   id_etat INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
);


CREATE TABLE ligne_commande(
   id_commande INT,
   id_casque INT,
   prix NUMERIC(6,2),
   quantite INT,
   PRIMARY KEY(id_commande, id_casque),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
   FOREIGN KEY(id_casque) REFERENCES casque(id_casque)
);



CREATE TABLE ligne_panier(
   id_utilisateur INT,
   id_casque INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_utilisateur, id_casque, date_ajout),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_casque) REFERENCES casque(id_casque)
);








INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');





INSERT INTO taille (id_taille, libelle_taille) VALUES
(NULL, 'XXS'),
(NULL, 'XS'),
(NULL, 'S'),
(NULL, 'M'),
(NULL, 'L'),
(NULL, 'XL'),
(NULL, 'XXL');




INSERT INTO type_casque (id_type_casque, libelle_type_casque) VALUES
(NULL, 'Casque de vélo VTT'),
(NULL, 'Casque de vélo de route'),
(NULL, 'Casque de chantier'),
(NULL, 'Casque de ski / snowboard'),
(NULL, 'Casque de militaire'),
(NULL, 'Casque de moto avec visière'),
(NULL, 'Casque de moto sans visière');


INSERT INTO casque (id_casque, nom_casque, poids, couleur, prix_casque, taille_id, type_casque_id, fournisseur, marque, stock, image) VALUES
(NULL, 'Casque Integral Kenny Downhill', 730, 'Vert', 90.00, 7, 1, 'Sarenne Sports Boutique', 'Kenny', 1, 'casque_vtt_vert.jpeg'),
(NULL, 'Casque AirBikeBlue', 1050, 'Bleu', 89.99, 1, 1, 'Holland Bikes', 'Lazer Sphere',5, 'casque_vtt_bleu.jpg'),
(NULL, 'Casque VTT SCOTT Supra', 270,'Rouge', 49.90, 4, 1, 'Fun Sports Cycles', 'Scott',6, 'casque_vtt_rouge.jpg'),
(NULL, 'Casque AirBreaker', 200, 'Noir', 199.95, 4, 2, 'Material-velo', 'Abus',4,'casque_velo_route_noir.jpg'),
(NULL, 'Casque de Cyclisme Contre-le-montre', 410,'Blanc', 350.00, 4, 2, 'Motus', 'Met',2, 'casque_velo_route_blanc.jpg'),
(NULL, 'Casque Vélo Climbert', 250,'Rose', 129.00, 6, 2, 'Bjorka', 'Bjorka', 2,  'casque_velo_route_rose.jpeg'),
(NULL, 'Casque Changrutier', 1000, 'Jaune', 6.99, 5, 3, 'Austral Horizon', 'EPI-Equipements',1,  'casque_chantier_jaune.jpg'),
(NULL, 'Casque protection tête', 317, 'Bleu', 4.95, 7, 3, 'Charles Service',  'EP_Equipements',1, 'casque_chantier_bleu.jpeg'),
(NULL, 'Casque de chantier en polyéthylène', 317,'Orange', 3.30, 7, 3, 'Krenobat', 'SINGER Safety', 1, 'casque_chantier_orange.jpg'),
(NULL, 'Casque Storm 2.0', 550,'Noir', 74.50, 6, 4, 'Monti Sport', 'Briko', 2, 'casque_ski_noir.jpg'),
(NULL, 'Casque de ski Sentinel$',530, 'Vert', 148.00, 5, 4, 'Ultra-fun', 'Vola Racing', 2, 'casque_ski_vert.jpg'),
(NULL, 'Bolle casque de ski synergy', 490,'Violet', 109.00, 6, 4, 'Easy-gliss', 'Bollé',5,  'casque_ski_violet.jpeg'),
(NULL, 'Nvg Mount pour airsoft', 800, 'Noir', 107.28, 4, 5, 'Amazon', 'Avluz',3,  'casque_militaire_noir.jpg'),
(NULL, 'Casque militaire Warhammer style M88', 570,'Vert', 37.90, 3, 5, 'Action Airsoft', 'AG-Tactical',4,  'casque_militaire_vert.jpeg'),
(NULL, 'Casque militaire léger', 1200,'Marron', 149.90, 4, 5, 'Boutique Militaire', '',5, 'casque_militaire_marron_jpeg'),
(NULL, 'Casque moto vintage avec visière', 1300,'Jaune', 109.00, 2, 6, 'Outlet Moto', 'Premier',3, 'casque_moto_avec_visiere_jaune.jpg'),
(NULL, 'Casque Airoh Commander Boost', 1400,'Rouge', 469.99, 1, 6, 'Speedway', 'Airoh',4, 'casque_moto_avec_visiere_rouge.jpeg'),
(NULL, 'ZHEN Flip-Up', 1560,'Rose', 142.95, 2, 6, 'Amazon', 'ZHEN', 5,'casque_moto_avec_visere_rose.jpg'),
(NULL, 'Westt Vintage Casque Moto sans visière blanc', 1050,'Blanc', 62.95, 5, 7, 'Amazon', 'Westt', 1,'casque_moto_sans_visere_blanc.jpg'),
(NULL, 'Casque TEEN visor', 1300,'Gris', 59.99, 4, 7, 'Diezz', 'TEEN', 2, 'casque_moto_sans_visiere_gris.jpeg'),
(NULL, 'Casque Arctik sans visière', 960, 'Noir', 129.90, 2, 7, 'Diezz Sport', 'Diezz', 3,'casque_mot_sans_visiere_noir.png');


INSERT INTO etat (id_etat, libelle) VALUES
(NULL, 'en attente'),
(NULL, 'expédié'),
(NULL, 'validé'),
(NULL, 'confirmé');


INSERT INTO commande (id_commande, date_achat, id_utilisateur, id_etat) VALUES
(NULL, '10-01-2006', 1, 1),
(NULL, '26-09-2007', 3, 2),
(NULL, '24-11-2021', 2, 3),
(NULL, '28-02-2004', 3, 4);

INSERT INTO ligne_commande(id_commande, id_casque, prix, quantite) VALUES
(1, 1, 90.00, 1),
(1, 2, 89.99, 1),
(2, 3, 49.90, 1),
(2, 4, 199.95, 1),
(3, 5, 350.00, 1),
(3, 6, 129.00, 1),
(4, 7, 6.99, 1),
(4, 8, 4.95, 1),
(4, 9, 3.30, 1),
(4, 10, 74.50, 1),
(4, 18, 142.95, 1),
(4, 19, 62.95, 1),
(4, 20, 59.99, 1),
(4, 21, 129.90, 1);





#Affiche tous les casques
SELECT * FROM casque;

#Affiche tous les types de casques
SELECT * FROM type_casque;

#Affiche le nombre de casque
SELECT COUNT(id_casque) AS nb_casque
FROM casque;

#Affiche tous les casques dont le prix est plus grand que 150
SELECT *
FROM casque
WHERE prix_casque > 150;

#Affiche le nombre de casques dont la taille est M
SELECT COUNT(id_casque) AS nb_M
FROM casque
JOIN taille
ON casque.taille_id = taille.id_taille
WHERE libelle_taille = 'M';

#Affiche tous les casques qui a un type de vélo de type : Casque de vélo de route
SELECT * FROM casque
JOIN type_casque
ON casque.type_casque_id = type_casque.id_type_casque
WHERE libelle_type_casque = 'Casque de vélo de route';

#Affiche tous les casques de taille M et L, triés par prix décroissant
SELECT casque.nom_casque, casque.prix_casque, taille.libelle_taille
FROM casque
JOIN taille ON casque.taille_id = taille.id_taille
WHERE taille.libelle_taille IN ('M', 'L')
ORDER BY casque.prix_casque DESC;


#Affiche les casques les plus légers et les plus lourds pour chaque type de casque
SELECT type_casque.libelle_type_casque, MAX(casque.poids) AS max_poids, MIN(casque.poids) AS min_poids
FROM casque
JOIN type_casque ON casque.type_casque_id = type_casque.id_type_casque
GROUP BY type_casque.libelle_type_casque;


#Affiche les casques qui ont la plus grande différence de prix
SELECT type_casque.libelle_type_casque,
       MAX(casque.prix_casque) - MIN(casque.prix_casque) AS ecart_prix
FROM casque
JOIN type_casque ON casque.type_casque_id = type_casque.id_type_casque
GROUP BY type_casque.libelle_type_casque
ORDER BY ecart_prix ASC;



