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


@admin_casque.route('/admin/casque/show')
def show_casque():
    mycursor = get_db().cursor()
    sql =''' SELECT * ,IFNULL(COUNT( distinct (c.id_commantaire)), 0) as nb_commentaires_nouveaux
            FROM casque
            left join commentaire c on casque.id_casque = c.casque_id and c.validation = 0
            group by casque.id_casque
            '''
    mycursor.execute(sql)
    casque = mycursor.fetchall()


    return render_template('admin/casque/show_casque.html', casques=casque)


@admin_casque.route('/admin/casque/add', methods=['GET'])
def add_casque():
    mycursor = get_db().cursor()
    sql = ''' SELECT id_type_casque, libelle_type_casque AS libelle FROM type_casque '''
    mycursor.execute(sql)
    type_casque = mycursor.fetchall()
    return render_template('admin/casque/add_casque.html'
                           ,types_casque=type_casque,
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
    stock = request.form.get('stock')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images-casque/', filename))
    else:
        print("erreur")
        filename=None

    sql = ''' INSERT INTO casque (id_casque, nom_casque, prix_casque, type_casque_id, stock, image) VALUES
            (NULL, %s, %s, %s, %s, %s) '''

    tuple_add = (nom, prix, type_casque_id, stock, filename)
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
    sql = ''' SELECT * FROM casque WHERE id_casque=%s '''
    mycursor.execute(sql, id_casque)
    nb_declinaison = mycursor.fetchone()
    nb_declinaison['nb_declinaison'] = 0 # /!\ A supprimer quand les déclinaison seront fait
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans ce casque : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' SELECT * FROM casque WHERE id_casque=%s '''
        mycursor.execute(sql, id_casque)
        casque = mycursor.fetchone()
        print(casque)
        image = casque['image']

        sql = ''' DELETE FROM casque WHERE id_casque=%s  '''
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
    SELECT id_casque, nom_casque AS nom, prix_casque AS prix, image, stock FROM casque WHERE id_casque=%s   
    '''
    mycursor.execute(sql, id_casque)
    casque = mycursor.fetchone()
    sql = '''
    SELECT id_type_casque, libelle_type_casque AS libelle FROM type_casque
    '''
    mycursor.execute(sql)
    types_casque = mycursor.fetchall()

    # sql = '''
    # requête admin_casque_6
    # '''
    # mycursor.execute(sql, id_casque)
    # declinaisons_casque = mycursor.fetchall()

    return render_template('admin/casque/edit_casque.html'
                           , casque=casque
                           , types_casque=types_casque
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
    stock = request.form.get('stock')
    print(stock)
    sql = '''
       SELECT image FROM casque WHERE id_casque=%s
       '''
    mycursor.execute(sql, id_casque)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images-casque/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images-casque/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images-casque/', filename))
            image_nom = filename

    sql = ''' UPDATE casque SET nom_casque= %s, image=%s, prix_casque=%s, type_casque_id=%s, stock=%s WHERE id_casque=%s '''
    mycursor.execute(sql, (nom, image_nom, prix, type_casque_id, stock, id_casque))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'casque modifié , nom:' + nom + '- type_casque :' + type_casque_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description + ' - stock:' + stock
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
