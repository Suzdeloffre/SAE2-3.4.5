#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_casque = request.form.get('id_casque')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_casque=request.form.get('id_declinaison_casque',None)
    id_declinaison_casque = 1

# ajout dans le panier d'une déclinaison d'un casque (si 1 declinaison : immédiat sinon => vu pour faire un choix
    sql = '''   SELECT * FROM ligne_panier WHERE casque_id = %s AND utilisateur_id = %s '''
    mycursor.execute(sql, (id_casque, id_client))
    casque_panier = mycursor.fetchone()

    mycursor.execute(''' SELECT * FROM casque WHERE id_casque = %s ''', (id_casque))
    casques = mycursor.fetchone()
    if not (casque_panier is None )and casques['stock'] >= int(quantite):
        tuple_update = (quantite, id_casque, id_client)
        sql = ''' UPDATE ligne_panier SET quantite = quantite+%s WHERE casque_id = %s AND utilisateur_id = %s  '''
        mycursor.execute(sql, tuple_update)
        sql = ''' UPDATE casque SET stock = stock-%s WHERE id_casque = %s '''
        mycursor.execute(sql, (quantite, id_casque))
    else:
        if casques['stock'] >= int(quantite):
            tuple_insert = (id_casque, id_client, quantite)
            sql = ''' INSERT INTO ligne_panier (casque_id, utilisateur_id, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp) '''
            mycursor.execute(sql, tuple_insert)
            sql = ''' UPDATE casque SET stock = stock-%s WHERE id_casque = %s '''
            mycursor.execute(sql, (quantite, id_casque))
        else:
            flash(u"Le stock n'est pas suffisant, il y a moins de "+quantite+" article(s) en stock", 'alert-danger')

    get_db().commit()

    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_casque = declinaisons[0]['id_declinaison_casque']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_casque))
    #     casquecasque = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_casque.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , casquecasque=casquecasque)

# ajout dans le panier d'un casque


    return redirect('/client/casque/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_casque = request.form.get('id_casque','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison du casque
    # id_declinaison_casque = request.form.get('id_declinaison_casque', None)

    sql = ''' SELECT * FROM ligne_panier WHERE casque_id = %s AND utilisateur_id = %s '''
    mycursor.execute(sql, (id_casque, id_client))
    casque_panier = mycursor.fetchone()

    if not(casque_panier is None) and casque_panier['quantite'] > 1:
        tuple_update = (id_casque, id_client)
        sql = ''' UPDATE ligne_panier SET quantite = quantite-1 WHERE casque_id = %s AND utilisateur_id = %s  '''
        mycursor.execute(sql, tuple_update)
        sql = ''' UPDATE casque SET stock = stock+1 WHERE id_casque = %s '''
        mycursor.execute(sql, (id_casque))
    else:
        sql = ''' DELETE FROM ligne_panier WHERE casque_id = %s AND utilisateur_id = %s '''
        mycursor.execute(sql, (id_casque, id_client))
        sql = ''' UPDATE casque SET stock = stock+1 WHERE id_casque = %s '''
        mycursor.execute(sql, (id_casque))

    # mise à jour du stock du casque disponible
    get_db().commit()
    return redirect('/client/casque/show')

@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s '''
    mycursor.execute(sql, (client_id))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = ''' DELETE FROM ligne_panier WHERE casque_id = %s AND utilisateur_id = %s '''
        mycursor.execute(sql, (item["casque_id"], client_id))

        sql2 = ''' UPDATE casque SET stock = stock+%s WHERE id_casque = %s '''
        mycursor.execute(sql2, (item["quantite"], item["casque_id"]))

        get_db().commit()
    return redirect('/client/casque/show')

@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_casque = request.form.get('id_casque')
    #id_declinaison_casque = request.form.get('id_declinaison_casque')

    sql = ''' SELECT quantite FROM ligne_panier WHERE casque_id = %s AND utilisateur_id = %s '''
    mycursor.execute(sql, (id_casque, id_client))
    quantite = mycursor.fetchone()["quantite"]

    sql = ''' DELETE FROM ligne_panier WHERE casque_id = %s AND utilisateur_id = %s '''
    mycursor.execute(sql, (id_casque, id_client))
    get_db().commit()
    sql2= ''' UPDATE casque SET stock = stock+%s WHERE id_casque = %s '''
    mycursor.execute(sql2, (quantite, id_casque))

    get_db().commit()
    return redirect('/client/casque/show')

@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    id_client = session['id_user']
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'Votre mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'Votre mot recherché doit être composé d''au moins 2 lettres')
            else:
                session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types
    return redirect('/client/casque/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    return redirect('/client/casque/show')
