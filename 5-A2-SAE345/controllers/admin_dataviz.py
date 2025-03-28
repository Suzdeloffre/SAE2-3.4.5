5#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')


@admin_dataviz.route('/admin/dataviz/etat1', methods=['GET', 'POST'])
def show_type_casque_stock():
    mycursor = get_db().cursor()

    type_casque_id = request.args.get('type_casque', None)
    print(type_casque_id)

    sql = '''SELECT id_type_casque, libelle_type_casque as libelle FROM type_casque'''
    mycursor.execute(sql)
    type_casques = mycursor.fetchall()

    if type_casque_id != 'None' and None :
        sql = '''SELECT casque.nom_casque AS libelle,
                            COUNT(commentaire.id_commantaire) AS nbr_commentaires_total,
                            AVG(note.note) AS moyenne_notes,
                            COUNT(note.note) AS nb_notes
                     FROM casque
                     LEFT JOIN type_casque ON casque.type_casque_id = type_casque.id_type_casque
                     LEFT JOIN commentaire ON casque.id_casque = commentaire.casque_id
                     LEFT JOIN note ON casque.id_casque = note.casque_id
                     WHERE type_casque.id_type_casque = %s  
                     GROUP BY casque.id_casque'''
        mycursor.execute(sql, (type_casque_id,))
        print("ici")
    else:
        sql = '''SELECT type_casque.libelle_type_casque AS libelle,
                        type_casque.id_type_casque,
                        COUNT(commentaire.id_commantaire) AS nbr_commentaires_total,
                        AVG(note.note) AS moyenne_notes,
                        COUNT(note.note) AS nb_notes
                 FROM type_casque
                 LEFT JOIN casque ON type_casque.id_type_casque = casque.type_casque_id
                 LEFT JOIN commentaire ON casque.id_casque = commentaire.casque_id
                 LEFT JOIN note ON casque.id_casque = note.casque_id
                 GROUP BY type_casque.id_type_casque'''
        mycursor.execute(sql)

    datas_show = mycursor.fetchall()

    labels = [row['libelle'] for row in datas_show]
    values = [row['nbr_commentaires_total'] for row in datas_show]
    moyenne_notes = [row['moyenne_notes'] for row in datas_show ]

    nb_notes = [row['nb_notes'] for row in datas_show]


    mycursor.execute('SELECT COUNT(*) AS total_commentaires FROM commentaire')
    total_commentaires = mycursor.fetchone()['total_commentaires']

    return render_template('admin/dataviz/dataviz_etat_1.html',
                           labels=labels, values=values,
                           moyenne_notes=moyenne_notes, nb_notes=nb_notes,
                           total_commentaires=total_commentaires, datas_show=datas_show,
                           type_casques=type_casques, type_casque_id=type_casque_id)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


