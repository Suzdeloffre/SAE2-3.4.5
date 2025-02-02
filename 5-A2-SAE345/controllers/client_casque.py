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

    sql = '''   SELECT * FROM type_casque;'''
    mycursor.execute(sql)
    checked_type_casque = mycursor.fetchall()

    list_param = []
    condition_and = ""

    sql = '''   SELECT * FROM casque'''
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if "filter_word" in session:
        sql = sql + " nom_casque LIKE %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + " prix_casque BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session["filter_types"][-1]
        for item in session["filter_types"]:
            sql = sql + " type_casque_id = %s "
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    tuple_sql = tuple(list_param)
    mycursor.execute(sql, tuple_sql)
    casques = mycursor.fetchall()

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
                           # , prix_max = prix_max
                           # , prix_min = prix_min
                           )
