DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS casque;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS type_casque;
DROP TABLE IF EXISTS adresse;




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

CREATE TABLE adresse(
    id_adresse INT AUTO_INCREMENT,
    utilisateur_id INT,
    nom VARCHAR(200),
    adresse VARCHAR(200),
    code_postal INT,
    ville VARCHAR(200),
    primary key (id_adresse),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

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
   date_achat DATE,
   utilisateur_id INT NOT NULL,
   adresse_id INT,
   etat_id INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
   FOREIGN KEY (adresse_id) REFERENCES adresse(id_adresse)
);


CREATE TABLE ligne_commande(
   commande_id INT,
   casque_id INT,
   prix NUMERIC(6,2),
   quantite INT,
   PRIMARY KEY(commande_id, casque_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(casque_id) REFERENCES casque(id_casque)
);



CREATE TABLE ligne_panier(
   utilisateur_id INT,
   casque_id INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(utilisateur_id, casque_id, date_ajout),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(casque_id) REFERENCES casque(id_casque)
);

CREATE TABLE note(
    id_note INT AUTO_INCREMENT,
    utilisateur_id INT,
    casque_id INT,
    note INT,
    PRIMARY KEY (id_note, utilisateur_id, casque_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (casque_id) REFERENCES casque(id_casque)
);

CREATE TABLE commentaire(
     id_commantaire INT AUTO_INCREMENT,
     utilisateur_id INT,
     casque_id INT,
     libelle_comm VARCHAR(255),
     date_publication DATE,
     validation BOOLEAN,
     PRIMARY KEY (id_commantaire, casque_id, utilisateur_id, date_publication),
     FOREIGN KEY (utilisateur_id)REFERENCES utilisateur(id_utilisateur),
     FOREIGN KEY (casque_id) REFERENCES casque(id_casque)
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


INSERT INTO adresse(id_adresse, utilisateur_id, nom, adresse, code_postal, ville) VALUES
(NULL, 2, 'Paul', '2 rue de la liberté', 69000, 'Lyon'),
(NULL, 3, 'Pierre', '3 rue de la fraternité', 13000, 'Marseille');


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
(NULL, 'Casque moto vintage avec visière', 1300,'Jaune', 109.00, 2, 6, 'Outlet Moto', 'Premier',3, 'casque_moto_avec_visiere_jaune.jpg'),
(NULL, 'Casque Airoh Commander Boost', 1400,'Rouge', 469.99, 1, 6, 'Speedway', 'Airoh',4, 'casque_moto_avec_visiere_rouge.jpeg'),
(NULL, 'Casque TEEN visor', 1300,'Gris', 59.99, 4, 7, 'Diezz', 'TEEN', 2, 'casque_moto_sans_visiere_gris.jpeg');



INSERT INTO etat (id_etat, libelle) VALUES
(NULL, 'en cours de traitement'),
(NULL, 'expédié');


INSERT INTO commande (id_commande, date_achat, utilisateur_id,etat_id) VALUES
(NULL, '2006-01-10', 2, 1),
(NULL, '2007-09-26', 3, 2),
(NULL, '2021-11-24', 2, 2),
(NULL, '2004-02-28', 3, 1);

INSERT INTO ligne_commande(commande_id,casque_id, prix, quantite) VALUES
(1, 1, 90.00, 1),
(1, 2, 89.99, 1),
(2, 3, 49.90, 1),
(2, 4, 199.95, 1),
(3, 5, 350.00, 1),
(3, 6, 129.00, 1),
(4, 7, 20.97, 3),
(4, 8, 4.95, 1),
(4, 9, 3.30, 1),
(4, 10, 74.50, 1),
(4, 15, 218.00, 2),
(4, 17, 59.99, 1);

INSERT INTO note(id_note, utilisateur_id, casque_id, note)VALUES
(NULL,2, 2, 15),
(NULL, 3, 4, 13),
(NULL, 3, 15, 17),
(NULL, 2, 6, 12),
(NULL, 3, 3, 10);

INSERT INTO commentaire(id_commantaire, utilisateur_id, casque_id, libelle_comm, date_publication, validation) VALUES
(NULL,2, 2,'Parfait, le casque est confortable', '2020-02-07', 1),
(NULL, 3, 4, 'le casque à l\'air solide. La livraison était rapide !','2018-10-20' ,0),
(NULL, 3,15, 'Parfait', '2020-05-14', 1),
(NULL, 2,6, 'la livraison a pris plus d\'un mois... et la couleur n\'est pas la même que sur la photo', '2023-08-03', 1);


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