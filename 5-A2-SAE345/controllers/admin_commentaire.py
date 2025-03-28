#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/casque/commentaires', methods=['GET'])
def admin_casque_details():
    mycursor = get_db().cursor()
    id_casque =  request.args.get('id_casque', None)
    sql = '''   SELECT *, u.nom, u.login, casque_id AS id_casque
                FROM commentaire 
                INNER JOIN utilisateur u ON commentaire.utilisateur_id = u.id_utilisateur
                WHERE casque_id = %s
                ORDER BY 
                    date_publication DESC, 
                    CASE 
                        WHEN utilisateur_id = 1 THEN 1 
                        ELSE 0
                    END;
    '''
    mycursor.execute(sql, id_casque)
    commentaires = mycursor.fetchall()
    date_publication = [commentaire['date_publication'] for commentaire in commentaires]

    sql = '''  SELECT nom_casque as nom, id_casque,
                AVG(note) as moyenne_notes, 
                COUNT(note) as nb_notes
                FROM note
                inner join casque c on note.casque_id = c.id_casque
                where id_casque=%s '''
    mycursor.execute(sql, id_casque)
    casque = mycursor.fetchone()

    sql = '''  SELECT 
                COUNT(CASE WHEN validation = 1 THEN 1 END) as nb_commentaires_valider, 
                COUNT(*) as nb_commentaire_total
                FROM commentaire
                WHERE casque_id = %s
                 '''
    mycursor.execute(sql, id_casque)
    nb_commentaires = mycursor.fetchone()
    nb_commentaire_total = nb_commentaires['nb_commentaire_total']
    if nb_commentaire_total == None:
        nb_commentaires['nb_commentaire_total'] = 0
    nb_commentaires_valider = nb_commentaires['nb_commentaires_valider']
    if nb_commentaires_valider== None :
        nb_commentaires['nb_commentaires_valider'] = 0

    return render_template('admin/casque/show_casque_commentaires.html'
                           , commentaires=commentaires
                           , casque=casque
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/casque/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_casque = request.form.get('id_casque', None)
    id_utilisateur = request.form.get('id_utilisateur', None)
    date_publication = request.form.get('date_publication', None)
    sql = ''' DELETE  FROM commentaire WHERE date_publication=%s and casque_id = %s and utilisateur_id = %s '''
    tuple_insert = (date_publication, id_casque, id_utilisateur)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/admin/casque/commentaires?id_casque='+id_casque)


@admin_commentaire.route('/admin/casque/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_casque = request.args.get('id_casque', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/casque/add_commentaire.html',id_utilisateur=id_utilisateur,id_casque=id_casque,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']
    id_casque = request.form.get('id_casque', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''INSERT INTO commentaire (validation, libelle_comm, utilisateur_id, casque_id, date_publication) 
             VALUES (%s, %s, %s, %s, %s)'''

    tuple_insert = (1,commentaire, id_utilisateur, id_casque, date_publication)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/admin/casque/commentaires?id_casque='+id_casque)


@admin_commentaire.route('/admin/casque/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_casque = request.args.get('id_casque', None)
    mycursor = get_db().cursor()
    sql = '''  UPDATE commentaire SET validation = 1
                WHERE casque_id= %s '''
    mycursor.execute(sql, id_casque)
    flash(u'commentaires validés', 'alert-success')
    get_db().commit()
    return redirect('/admin/casque/commentaires?id_casque='+id_casque)