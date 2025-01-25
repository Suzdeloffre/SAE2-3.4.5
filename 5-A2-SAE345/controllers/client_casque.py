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

    sql = '''   SELECT * FROM casque   '''
    #faire le filtre
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    mycursor.execute(sql)
    casques =mycursor.fetchall()


    # pour le filtre
    sql = '''   SELECT * FROM  type_casque  '''
    mycursor.execute(sql)
    types_casque = mycursor.fetchall()
    #types_casque = []


    casques_panier = []

    if len(casques_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_casque.html'
                           , casques=casques
                           , casques_panier=casques_panier
                           #, prix_total=prix_total
                           , items_filtre=types_casque
                           )
