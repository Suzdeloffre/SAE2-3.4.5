#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' SELECT * FROM utilisateur WHERE id_utilisateur=%s'''
    mycursor.execute(sql, (id_client))
    utilisateur=mycursor.fetchone()

    sql = '''   SELECT adresse.nom, adresse.adresse, adresse.code_postal, adresse.ville, COUNT(commande.id_commande) AS nbr_commande, adresse.favori FROM adresse
                LEFT JOIN commande
                ON commande.adresse_id = adresse.id_adresse
                WHERE adresse.utilisateur_id = %s
                GROUP BY adresse.id_adresse;'''
    mycursor.execute(sql, (id_client))
    adresses = mycursor.fetchall()


    sql = '''   SELECT COUNT(id_adresse) AS nbre_adresse
                FROM adresse
                WHERE utilisateur_id = %s;'''
    mycursor.execute(sql, (id_client))
    nb_adresses = mycursor.fetchone()
    nb_adresses = nb_adresses['nbre_adresse'] if nb_adresses else 0
    if nb_adresses >= 4:
        message = u'Le maximum de 4 adresses a été atteint'
        flash(message, 'alert-success')

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    return render_template('client/coordonnee/edit_coordonnee.html'
                           #,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    utilisateur = None
    if utilisateur:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               #, user=user
                               )


    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.form.get('id_adresse')

    sql = '''   DELETE FROM adresse WHERE id_adresse=%s AND utilisateur_id = %s;'''
    tuple_delete = (id_adresse, id_client)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()

    message = u'adresse supprimée, id_adresse:' + id_adresse
    flash(message, 'alert-danger')

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' SELECT * FROM utilisateur WHERE id_utilisateur=%s; '''
    mycursor.execute(sql, (id_client))
    utilisateur = mycursor.fetchone()
    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    adresse = request.form.get('adresse')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    sql = ''' SELECT id_adresse FROM adresse WHERE utilisateur_id=%s AND favori=1 '''
    mycursor.execute(sql, (id_client,))
    adresse_favorite = mycursor.fetchone()

    if adresse_favorite:
        sql = '''   UPDATE adresse SET favori=0 WHERE id_adresse=%s;'''
        mycursor.execute(sql, (adresse_favorite['id_adresse'],))

    sql = '''   INSERT INTO adresse (nom, adresse, code_postal, ville, utilisateur_id, favori) VALUES (%s, %s, %s, %s, %s, 1);'''
    tuple_insert = (nom, adresse, code_postal, ville, id_client)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    message = u'adresse ajoutée, nom:' + nom + '- adresse: ' + adresse + '- code_postal: ' + code_postal + '- ville: ' + ville
    flash(message, 'alert-success')

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    sql = ''' SELECT * FROM utilisateur WHERE id_utilisateur=%s; '''
    mycursor.execute(sql, (id_client))
    utilisateur = mycursor.fetchone()

    sql = '''   SELECT * FROM adresse WHERE id_adresse=%s;'''
    mycursor.execute(sql, (id_adresse))
    adresse = mycursor.fetchone()

    return render_template('/client/coordonnee/edit_adresse.html'
                           ,utilisateur=utilisateur
                           ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    adresse = request.form.get('adresse')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    sql = '''   UPDATE adresse SET nom=%s, adresse=%s, code_postal=%s, ville=%s WHERE id_adresse=%s;'''
    tuple_insert = (nom, adresse, code_postal, ville, id_adresse)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    message = u'adresse modifiée, nom:' + nom + '- adresse: ' + adresse + '- code_postal: ' + code_postal + '- ville: ' + ville
    flash(message, 'alert-success')

    return redirect('/client/coordonnee/show')
