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
    id_casque = request.args.get('id_casque')
    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_casque, id_client)

    sql = '''SELECT nom_casque, prix_casque, image, id_casque
             FROM casque
             where id_casque =%s
    '''
    mycursor.execute(sql, id_casque)
    casque = mycursor.fetchone()

    commandes_casque=[]
    nb_commentaires=[]
    if casque is None:
        abort(404, "pb id casque")
    sql = ''' SELECT *, utilisateur.nom, utilisateur.login
                FROM commentaire
                inner join utilisateur on commentaire.utilisateur_id = utilisateur.id_utilisateur
                WHERE casque_id =%s
     '''
    mycursor.execute(sql, ( id_casque))
    commentaires = mycursor.fetchall()

    sql = '''SELECT sum(quantite) AS nb_commandes_casque
            FROM ligne_commande
            inner join commande c on ligne_commande.commande_id = c.id_commande
            where utilisateur_id=%s and casque_id=%s 
     '''
    mycursor.execute(sql, (id_client, id_casque))
    commandes_casque = mycursor.fetchone()
    nb_commandes_casque = commandes_casque['nb_commandes_casque'] if commandes_casque and commandes_casque['nb_commandes_casque'] is not None else 0

    sql = '''
        SELECT *
        FROM note
        WHERE utilisateur_id=%s and casque_id=%s
    '''
    mycursor.execute(sql, (id_client, id_casque))
    note = mycursor.fetchone()

    if note:
        note = note['note']

    sql_moyenne_notes = '''
        SELECT AVG(note) as moyenne_notes, COUNT(note) as nb_notes
        FROM note
        WHERE casque_id = %s
    '''
    mycursor.execute(sql_moyenne_notes, (id_casque,))
    result = mycursor.fetchone()
    if result:
        moyenne_notes = result['moyenne_notes'] if result['moyenne_notes'] is not None else None
        nb_notes = result['nb_notes'] if result['nb_notes'] is not None else 0
    else:
        moyenne_notes = None
        nb_notes = 0

    casque = {
        'id_casque': casque['id_casque'],
        'image': casque['image'],
        'note': note,
        'moyenne_notes': moyenne_notes,
        'nb_notes': nb_notes
    }

    sql = ''' SELECT COUNT(CASE WHEN utilisateur_id = %s THEN 1 END) AS nb_commentaires_utilisateur,
            COUNT(CASE WHEN utilisateur_id = %s THEN 1 END) AS nb_commentaires_utilisateur_valide,
            COUNT(*) AS nb_commentaires_total, 
            COUNT(CASE WHEN validation = 1 THEN 1 END) AS nb_commentaires_total_valide
            FROM commentaire
            WHERE casque_id = %s;
    '''
    mycursor.execute(sql, (id_client, id_client, id_casque))
    nb_commentaires= mycursor.fetchone()

    nb_commentaires = {
        'nb_commentaires_utilisateur': nb_commentaires['nb_commentaires_utilisateur']
        if nb_commentaires[ 'nb_commentaires_utilisateur'] is not None else 0,
        'nb_commentaires_utilisateur_valide': nb_commentaires['nb_commentaires_utilisateur_valide']
        if nb_commentaires['nb_commentaires_utilisateur_valide'] is not None else 0,
        'nb_commentaires_total': nb_commentaires['nb_commentaires_total']
        if nb_commentaires[ 'nb_commentaires_total'] is not None else 0,
        'nb_commentaires_total_valide': nb_commentaires['nb_commentaires_total_valide']
        if nb_commentaires[ 'nb_commentaires_total_valide'] is not None else 0
    }

    return render_template('client/casque_info/casque_details.html'
                           , casque=casque
                           , commentaires=commentaires
                           , commandes_casque=commandes_casque
                           , note=note
                           , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_casque = request.form.get('id_casque')

    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/casque/details?id_casque='+id_casque)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')
        return redirect('/client/casque/details?id_casque='+id_casque)

    tuple_insert = (commentaire, id_client, id_casque)
    sql = ''' INSERT INTO commentaire ( libelle_comm, utilisateur_id, casque_id, date_publication) VALUES (%s,%s,%s, CURRENT_DATE )'''

    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/casque/details?id_casque='+id_casque)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    print(f"Form data: {request.form}")
    id_client = session['id_user']
    id_casque = request.form.get('id_casque', None)
    date_publication = request.form.get('date_publication', None)

    sql = '''  DELETE  FROM commentaire WHERE utilisateur_id=%s and casque_id=%s and date_publication=%s;'''
    tuple_delete=(id_client,id_casque,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/casque/details?id_casque='+id_casque)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_casque = request.form.get('id_casque', None)
    tuple_insert = (note, id_client, id_casque)
    print(tuple_insert)
    sql = '''  INSERT INTO note (note, utilisateur_id, casque_id) VALUES (%s,%s,%s)'''
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
    sql = ''' UPDATE note SET note=%s WHERE utilisateur_id=%s and casque_id=%s; '''
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
    sql = ''' DELETE FROM note WHERE utilisateur_id=%s and casque_id=%s; '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/casque/details?id_casque='+id_casque)
