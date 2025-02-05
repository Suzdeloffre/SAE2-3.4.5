#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_casque = Blueprint('admin_type_casque', __name__,
                        template_folder='templates')

@admin_type_casque.route('/admin/type-casque/show')
def show_type_casque():
    mycursor = get_db().cursor()
    sql = '''     SELECT id_type_casque, libelle_type_casque, COUNT(id_casque) AS nbr_casques FROM type_casque
                LEFT JOIN casque ON type_casque.id_type_casque = casque.type_casque_id
                GROUP BY id_type_casque'''
    mycursor.execute(sql)
    types_casque = mycursor.fetchall()
    return render_template('admin/type_casque/show_type_casque.html', types_casque=types_casque)

@admin_type_casque.route('/admin/type-casque/add', methods=['GET'])
def add_type_casque():
    return render_template('admin/type_casque/add_type_casque.html')

@admin_type_casque.route('/admin/type-casque/add', methods=['POST'])
def valid_add_type_casque():
    libelle = request.form.get('libelle', '')
    mycursor = get_db().cursor()
    sql = ''' INSERT INTO type_casque (id_type_casque, libelle_type_casque) VALUES (NULL, %s); '''
    mycursor.execute(sql, libelle)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-casque/show') #url_for('show_type_casque')

@admin_type_casque.route('/admin/type-casque/delete', methods=['GET'])
def delete_type_casque():
    id_type_casque = request.args.get('id_type_casque', '')
    mycursor = get_db().cursor()

    flash(u'suppression type casque , id : ' + id_type_casque, 'alert-success')
    return redirect('/admin/type-casque/show')

@admin_type_casque.route('/admin/type-casque/edit', methods=['GET'])
def edit_type_casque():
    id_type_casque = request.args.get('id_type_casque', '')
    mycursor = get_db().cursor()
    sql = ''' SELECT id_type_casque, libelle_type_casque AS libelle FROM type_casque WHERE id_type_casque = %s '''
    mycursor.execute(sql, (id_type_casque,))
    type_casque = mycursor.fetchone()
    return render_template('admin/type_casque/edit_type_casque.html', type_casque=type_casque)

@admin_type_casque.route('/admin/type-casque/edit', methods=['POST'])
def valid_edit_type_casque():
    libelle = request.form['libelle']
    id_type_casque = request.form.get('id_type_casque', '')
    tuple_update = (libelle, id_type_casque)
    mycursor = get_db().cursor()
    sql = ''' UPDATE type_casque SET libelle_type_casque = %s WHERE id_type_casque = %s '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type casque modifié, id: ' + id_type_casque + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-casque/show')








