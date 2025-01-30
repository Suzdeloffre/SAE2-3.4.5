#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_casque = Blueprint('client_casque', __name__,
                        template_folder='templates')


@client_casque.route('/client/index')
@client_casque.route('/client/casque/show')              # remplace /client
def client_casque_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    recherche = request.form.get('filter_word','')
    checked_list = request.form.getlist('filter_types')
    prix_min = request.form.get('filter_prix_min','')
    prix_max = request.form.get('filter_prix_max','')


    if prix_min == "":
        prix_min = 0
    if prix_max == "":
        sql = '''   SELECT MAX(prix_casque) AS filter_prix_max
                    FROM casque;'''
        mycursor.execute(sql)
        prix_max = mycursor.fetchone()['filter_prix_max']

    sql = '''   SELECT * FROM type_casque
                ORDER BY id_type_casque;'''
    mycursor.execute(sql)
    checked_type_casque = mycursor.fetchall()


    nom_recherche = "%" + recherche + "%"

    if checked_list == []:
        sql = '''   SELECT * FROM casque
                    JOIN type_casque 
                    ON casque.type_casque_id = type_casque.id_type_casque
                    WHERE nom_casque LIKE %s AND (prix_casque >= %s AND prix_casque <= %s);'''
        tuple_filter = (nom_recherche, prix_min, prix_max)
        mycursor.execute(sql, tuple_filter)

    else:
        sql = '''   SELECT * FROM casque
                    JOIN type_casque
                    ON casque.type_casque_id = type_casque.id_type_casque
                    WHERE (nom_casque LIKE %s) AND (type_casque_id IN %s) AND (prix_casque >= %s AND prix_casque <= %s);'''
        tuple_filter = (nom_recherche, checked_list, prix_min, prix_max)
        mycursor.execute(sql, tuple_filter)
    casques = mycursor.fetchall()
    #types_casque = []

    sql = '''   SELECT id_casque, casque.prix_casque AS prix, quantite, casque.nom_casque AS nom, casque.stock FROM ligne_panier 
                JOIN casque ON ligne_panier.casque_id = casque.id_casque
                WHERE utilisateur_id = %s '''
    mycursor.execute(sql, id_client)
    casques_panier = mycursor.fetchall()

    if len(casques_panier) >= 1:
        sql = '''   SELECT SUM(casque.prix_casque*quantite) AS prix_total FROM ligne_panier
                    JOIN casque ON ligne_panier.casque_id = casque.id_casque
                    WHERE utilisateur_id = %s '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()["prix_total"]
    else:
        prix_total = None
    return render_template('client/boutique/panier_casque.html'
                           , casques=casques
                           , casques_panier=casques_panier
                           , prix_total=prix_total
                           , checked_type_casque = checked_type_casque
                           , prix_max = prix_max
                           , prix_min = prix_min
                           )
