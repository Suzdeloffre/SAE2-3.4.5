#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s '''
    mycursor.execute(sql, (id_client))
    casque_panier = mycursor.fetchall()
    if len(casque_panier) >= 1:
        sql = '''   SELECT SUM(quantite*prix_casque) AS prix_total FROM ligne_panier 
                    JOIN casque ON ligne_panier.utilisateur_id = casque.id_casque
                    WHERE utilisateur_id = %s 
                    GROUP BY ligne_panier.utilisateur_id'''
        mycursor.execute(sql, (id_client))
        prix_total = mycursor.fetchone()
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , casque_panier=casque_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'casques dans le ligne_panier', 'alert-warning')
        return redirect('/client/casque/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    date_commande = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tuple_insert = (date_commande, id_client, '1')
    sql = ''' INSERT INTO commande(date_achat, utilisateur_id, etat_id) VALUES (%s, %s, %s)'''
    mycursor.execute(sql, tuple_insert)
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()
    print(commande_id, tuple_insert)

    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s AND casque_id = %s'''
        mycursor.execute(sql, (item['utilisateur_id'], item['casque_id']))
        sql = '''  SELECT prix_casque FROM casque WHERE id_casque = %s'''
        mycursor.execute(sql, item['casque_id'])
        prix_casque = mycursor.fetchone()
        sql = ''' INSERT INTO ligne_commande(commande_id, casque_id, quantite, prix) VALUES (%s, %s, %s, %s)'''
        tuple_insert = (commande_id['last_insert_id'], item['casque_id'], item['quantite'], prix_casque['prix_casque'])
        mycursor.execute(sql, tuple_insert)

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/casque/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''   SELECT commande.id_commande,
                        commande.date_achat, 
                        etat.libelle,
                        etat_id,
                        SUM(ligne_commande.prix) AS prix_total, 
                        SUM(ligne_commande.quantite) AS nbr_casques FROM commande
                JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
                JOIN utilisateur ON utilisateur.id_utilisateur = commande.utilisateur_id
                JOIN etat ON commande.etat_id = etat.id_etat
                WHERE utilisateur.id_utilisateur = %s
                GROUP BY commande.id_commande, date_achat, etat.libelle
                ORDER BY date_achat, libelle, etat_id'''
    mycursor.execute(sql, (id_client))
    commandes = mycursor.fetchall()

    casque_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' SELECT casque.nom_casque, ligne_commande.quantite, prix_casque AS prix, prix AS prix_ligne FROM ligne_commande
                    JOIN casque ON ligne_commande.casque_id = casque.id_casque
                    WHERE commande_id = %s'''
        mycursor.execute(sql, (id_commande))
        casque_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , casque_commande=casque_commande
                           , commande_adresses=commande_adresses
                           )

