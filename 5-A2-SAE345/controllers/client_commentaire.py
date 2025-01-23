#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/casque/details', methods=['GET'])
def client_casque_details():
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_casque, id_client)

    sql = '''
    '''
    #mycursor.execute(sql, id_article)
    #casque = mycursor.fetchone()
    casque=[]
    commandes_casque=[]
    nb_commentaires=[]
    if casque is None:
        abort(404, "pb id casque")
    # sql = '''
    #
    # '''
    # mycursor.execute(sql, ( id_article))
    # commentaires = mycursor.fetchall()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_article))
    # commandes_casque = mycursor.fetchone()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_casque))
    # note = mycursor.fetchone()
    # print('note',note)
    # if note:
    #     note=note['note']
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_casque))
    # nb_commentaires = mycursor.fetchone()
    return render_template('client/casque_info/casque_details.html'
                           , casque=casque
                           # , commentaires=commentaires
                           , commandes_articles=commandes_casque
                           # , note=note
                           , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_casque = request.form.get('id_casque', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/casque/details?id_casque='+id_casque)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/casque/details?id_casque='+id_casque)

    tuple_insert = (commentaire, id_client, id_casque)
    print(tuple_insert)
    sql = '''  '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/casque/details?id_casque='+id_casque)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_casque = request.form.get('id_casque', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''   '''
    tuple_delete=(id_client,id_casque,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/casque/details?id_article='+id_casque)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_casque = request.form.get('id_casque', None)
    tuple_insert = (note, id_client, id_casque)
    print(tuple_insert)
    sql = '''   '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/casque/details?id_casque='+id_casque)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_casque = request.form.get('id_casque', None)
    tuple_update = (note, id_client, id_casque)
    print(tuple_update)
    sql = '''  '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/casque/details?id_casque='+id_casque)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_casque = request.form.get('id_casque', None)
    tuple_delete = (id_client, id_casque)
    print(tuple_delete)
    sql = '''  '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/casque/details?id_casque='+id_casque)
