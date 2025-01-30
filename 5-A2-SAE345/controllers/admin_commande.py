#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''   SELECT u.login,date_achat, COUNT(casque_id) as nb_casque, SUM(prix) as prix_total, etat.libelle
                FROM ligne_commande
                inner join commande
                on commande.id_commande = ligne_commande.commande_id
                inner join etat
                on commande.etat_id = etat.id_etat
                inner join utilisateur u 
                on commande.utilisateur_id = u.id_utilisateur
                group by date_achat, u.login, etat.libelle
                order by date_achat desc
                '''
    mycursor.execute(sql)
    commande= mycursor.fetchall()

    id_commande = request.args.get('id_commande', None)
    print(id_commande)

    sql = '''   SELECT casque.nom_casque as nom, casque.couleur, lc.prix, lc.quantite, commande.date_achat, u.login
                   FROM ligne_commande lc
                   inner join commande
                   on commande.id_commande = lc.commande_id
                   inner join utilisateur u 
                   on commande.utilisateur_id = u.id_utilisateur
                   inner join casque 
                   on lc.casque_id = casque.id_casque
                   group by u.login, casque.nom_casque, casque.couleur, lc.prix, lc.quantite, commande.date_achat
                   '''
    mycursor.execute(sql, id_commande)
    casque_commande = mycursor.fetchall()

    sql=''' SELECT adresse, code_postal, ville, pays, u.login
            FROM commande
            inner join adresse
            on adresse.id_adresse = commande.adresse_id
    '''
    commande_adresses = None

    if id_commande != None:
        sql = '''  '''
        commande_adresses =mycursor.fetchall()

    return render_template('admin/commandes/show.html'
                           , commandes=commande
                           , casques_commande=casque_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''           '''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
