#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_casque = Blueprint('admin_declinaison_casque', __name__,
                         template_folder='templates')


@admin_declinaison_casque.route('/admin/declinaison_casque/add')
def add_declinaison_casque():
    id_casque=request.args.get('id_casque')
    mycursor = get_db().cursor()
    casque=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/article/add_declinaison_article.html'
                           , casque=casque
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_casque.route('/admin/declinaison_casque/add', methods=['POST'])
def valid_add_declinaison_casque():
    mycursor = get_db().cursor()

    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')
    # attention au doublon
    get_db().commit()
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_casque.route('/admin/declinaison_casque/edit', methods=['GET'])
def edit_declinaison_casque():
    id_declinaison_casque = request.args.get('id_declinaison_casque')
    mycursor = get_db().cursor()
    declinaison_casque=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/article/edit_declinaison_casque.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_casque=declinaison_casque
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_casque.route('/admin/declinaison_casque/edit', methods=['POST'])
def valid_edit_declinaison_casque():
    id_declinaison_casque = request.form.get('id_declinaison_casque','')
    id_casque = request.form.get('id_casque','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_article modifié , id:' + str(id_declinaison_casque) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/casque/edit?id_casque=' + str(id_casque))


@admin_declinaison_casque.route('/admin/declinaison_casque/delete', methods=['GET'])
def admin_delete_declinaison_casque():
    id_declinaison_casque = request.args.get('id_declinaison_casque','')
    id_casque = request.args.get('id_casque','')

    flash(u'declinaison supprimée, id_declinaison_casque : ' + str(id_declinaison_casque),  'alert-success')
    return redirect('/admin/casque/edit?id_casque=' + str(id_casque))
