#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_casque = Blueprint('admin_casque', __name__,
                          template_folder='templates')


@admin_casque.route('/admin//show')
def show_casque():
    mycursor = get_db().cursor()
    sql = '''  requête admin_article_1
    '''
    mycursor.execute(sql)
    casque = mycursor.fetchall()
    return render_template('admin/casque/show_casque.html', casque=casque)


@admin_casque.route('/admin/casque/add', methods=['GET'])
def add_casque():
    mycursor = get_db().cursor()

    return render_template('admin/casque/add_casque.html'
                           #,types_casque=type_casque,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_casque.route('/admin/casque/add', methods=['POST'])
def valid_add_casque():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_casque_id = request.form.get('type_casque_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_article_2 '''

    tuple_add = (nom, filename, prix, type_casque_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'casque ajouté , nom: ', nom, ' - type_casque:', type_casque_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'casque ajouté , nom:' + nom + '- type_casque:' + type_casque_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/casque/show')


@admin_casque.route('/admin/casque/delete', methods=['GET'])
def delete_casque():
    id_casque=request.args.get('id_casque')
    mycursor = get_db().cursor()
    sql = ''' requête admin_article_3 '''
    mycursor.execute(sql, id_casque)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans ce casque : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_article_4 '''
        mycursor.execute(sql, id_casque)
        casque = mycursor.fetchone()
        print(casque)
        image = casque['image']

        sql = ''' requête admin_article_5  '''
        mycursor.execute(sql, id_casque)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un casque supprimé, id :", id_casque)
        message = u'un casque supprimé, id : ' + id_casque
        flash(message, 'alert-success')

    return redirect('/admin/casque/show')


@admin_casque.route('/admin/casque/edit', methods=['GET'])
def edit_casque():
    id_casque=request.args.get('id_casque')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_article_6    
    '''
    mycursor.execute(sql, id_casque)
    casque = mycursor.fetchone()
    print(casque)
    sql = '''
    requête admin_article_7
    '''
    mycursor.execute(sql)
    types_casque = mycursor.fetchall()

    # sql = '''
    # requête admin_article_6
    # '''
    # mycursor.execute(sql, id_casque)
    # declinaisons_casque = mycursor.fetchall()

    return render_template('admin/casque/edit_article.html'
                           ,casque=casque
                           ,types_casque=types_casque
                         #  ,declinaisons_casque=declinaisons_casque
                           )


@admin_casque.route('/admin/casque/edit', methods=['POST'])
def valid_edit_casque():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_casque = request.form.get('id_casque')
    image = request.files.get('image', '')
    type_casque_id = request.form.get('type_casque_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_article_8
       '''
    mycursor.execute(sql, id_casque)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  requête admin_article_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_casque_id, description, id_casque))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'casque modifié , nom:' + nom + '- type_casque :' + type_casque_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/casque/show')







@admin_casque.route('/admin/casque/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    casque=[]
    commentaires = {}
    return render_template('admin/casque/show_avis.html'
                           , casque=casque
                           , commentaires=commentaires
                           )


@admin_casque.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    casque_id = request.form.get('idCasque', None)
    userId = request.form.get('idUser', None)

    return admin_avis(casque_id)
