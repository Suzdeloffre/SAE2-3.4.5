#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_casque =  request.args.get('id_casque', None)
    sql = '''    requête admin_type_article_1    '''
    commentaires = {}
    sql = '''   requête admin_type_article_1_bis   '''
    casque = []
    sql = '''   requête admin_type_article_1_3   '''
    nb_commentaires = []
    return render_template('admin/article/show_article_commentaires.html'
                           , commentaires=commentaires
                           , casque=casque
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/casque/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_casque = request.form.get('id_casque', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_article_2   '''
    tuple_delete=(id_utilisateur,id_casque,date_publication)
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
    id_utilisateur = session['id_user']   #1 admin
    id_casque = request.form.get('id_casque', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_article_3   '''
    get_db().commit()
    return redirect('/admin/casque/commentaires?id_casque='+id_casque)


@admin_commentaire.route('/admin/casque/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_casque = request.args.get('id_casque', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_article_4   '''
    get_db().commit()
    return redirect('/admin/casque/commentaires?id_casque='+id_casque)