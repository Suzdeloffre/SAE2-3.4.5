#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql=''' DROP TABLE IF EXISTS utilisateur;'''
    mycursor.execute(sql)

    sql = '''   DROP TABLE IF EXISTS casque;'''
    mycursor.execute(sql)

    sql = ''' DROP TABLE IF EXISTS type_casque; '''
    mycursor.execute(sql)

    sql = ''' DROP TABLE IF EXISTS taille;   '''
    mycursor.execute(sql)

    sql='''
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
    );  
    '''
    mycursor.execute(sql)

    sql=''' 
    CREATE TABLE taille(
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(200),
    PRIMARY KEY (id_taille)
    );
    '''
    mycursor.execute(sql)

    sql=''' 
    CREATE TABLE type_casque(
    id_type_casque INT AUTO_INCREMENT,
    libelle_type_casque VARCHAR(200),
    PRIMARY KEY (id_type_casque)
    );  
    '''
    mycursor.execute(sql)

    sql=''' 
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
    photo VARCHAR(200),
    PRIMARY KEY (id_casque),
    CONSTRAINT fk_casque_taille FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
    CONSTRAINT fk_casque_type_epoque FOREIGN KEY (type_casque_id) REFERENCES type_casque(id_type_casque)
    );
    '''
    mycursor.execute(sql)


    sql=''' 
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
    '''
    mycursor.execute(sql)

    sql = ''' 
    INSERT INTO taille (id_taille, libelle_taille) VALUES
    (NULL, 'XXS'),
    (NULL, 'XS'),
    (NULL, 'S'),
    (NULL, 'M'),
    (NULL, 'L'),
    (NULL, 'XL'),
    (NULL, 'XXL');
     '''
    mycursor.execute(sql)

    sql = ''' 
    INSERT INTO type_casque (id_type_casque, libelle_type_casque) VALUES
    (NULL, 'Casque de vélo VTT'),
    (NULL, 'Casque de vélo de route'),
    (NULL, 'Casque de chantier'),
    (NULL, 'Casque de ski / snowboard'),
    (NULL, 'Casque de militaire'),
    (NULL, 'Casque de moto avec visière'),
    (NULL, 'Casque de moto sans visière');
     '''
    mycursor.execute(sql)

    sql = ''' 
    INSERT INTO casque (id_casque, nom_casque, poids, couleur, prix_casque, taille_id, type_casque_id, fournisseur, marque, photo) VALUES
    (NULL, 'Casque Integral Kenny Downhill', 730, 'Vert', 90.00, 7, 1, 'Sarenne Sports Boutique', 'Kenny', 'casque_vtt_vert.jpeg'),
    (NULL, 'Casque AirBikeBlue', 1050, 'Bleu', 89.99, 1, 1, 'Holland Bikes', 'Lazer Sphere', 'casque_vtt_bleu.jpg'),
    (NULL, 'Casque VTT SCOTT Supra', 270,'Rouge', 49.90, 4, 1, 'Fun Sports Cycles', 'Scott', 'casque_vtt_rouge.jpg'),
    (NULL, 'Casque AirBreaker', 200, 'Noir', 199.95, 4, 2, 'Material-velo', 'Abus', 'casque_velo_route_noir.jpg'),
    (NULL, 'Casque de Cyclisme Contre-le-montre', 410,'Blanc', 350.00, 4, 2, 'Motus', 'Met', 'casque_velo_route_blanc.jpg'),
    (NULL, 'Casque Vélo Climbert', 250,'Rose', 129.00, 6, 2, 'Bjorka', 'Bjorka', 'casque_velo_route_rose.jpeg'),
    (NULL, 'Casque Changrutier', 1000, 'Jaune', 6.99, 5, 3, 'Austral Horizon', 'EPI-Equipements', 'casque_chantier_jaune.jpg'),
    (NULL, 'Casque protection tête', 317, 'Bleu', 4.95, 7, 3, 'Charles Service', 'EP_Equipements', 'casque_chantier_bleu.jpeg'),
    (NULL, 'Casque de chantier en polyéthylène', 317,'Orange', 3.30, 7, 3, 'Krenobat', 'SINGER Safety', 'casque_chantier_orange.jpg'),
    (NULL, 'Casque Storm 2.0', 550,'Noir', 74.50, 6, 4, 'Monti Sport', 'Briko', 'casque_ski_noir.jpg'),
    (NULL, 'Casque de ski Sentinel$',530, 'Vert', 148.00, 5, 4, 'Ultra-fun', 'Vola Racing', 'casque_ski_vert.jpg'),
    (NULL, 'Bolle casque de ski synergy', 490,'Violet', 109.00, 6, 4, 'Easy-gliss', 'Bollé', 'casque_ski_violet.jpeg'),
    (NULL, 'Nvg Mount pour airsoft', 800, 'Noir', 107.28, 4, 5, 'Amazon', 'Avluz', 'casque_militaire_noir.jpg'),
    (NULL, 'Casque militaire Warhammer style M88', 570,'Vert', 37.90, 3, 5, 'Action Airsoft', 'AG-Tactical', 'casque_militaire_vert.jpeg'),
    (NULL, 'Casque militaire léger', 1200,'Marron', 149.90, 4, 5, 'Boutique Militaire', '', 'casque_militaire_marron_jpeg'),
    (NULL, 'Casque moto vintage avec visière', 1300,'Jaune', 109.00, 2, 6, 'Outlet Moto', 'Premier', 'casque_moto_avec_visiere_jaune.jpg'),
    (NULL, 'Casque Airoh Commander Boost', 1400,'Rouge', 469.99, 1, 6, 'Speedway', 'Airoh', 'casque_moto_avec_visiere_rouge.jpeg'),
    (NULL, 'ZHEN Flip-Up', 1560,'Rose', 142.95, 2, 6, 'Amazon', 'ZHEN', 'casque_moto_avec_visere_rose.jpeg'),
    (NULL, 'Westt Vintage Casque Moto sans visière blanc', 1050,'Blanc', 62.95, 5, 7, 'Amazon', 'Westt', 'casque_moto_sans_visere_blanc.jpg'),
    (NULL, 'Casque TEEN visor', 1300,'Gris', 59.99, 4, 7, 'Diezz', 'TEEN', 'casque_moto_sans_visiere_gris.jpeg'),
    (NULL, 'Casque Arctik sans visière', 960, 'Noir', 129.90, 2, 7, 'Diezz Sport', 'Diezz', 'casque_mot_sans_visiere_noir.png');
         '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
