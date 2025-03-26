5#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_casque_stock():
    mycursor = get_db().cursor()
    sql = '''SELECT  type_casque.id_type_casque, 
             libelle_type_casque AS libelle, 
             COUNT(DISTINCT com.id_commantaire ) AS nbr_commentaires
             FROM type_casque
             LEFT JOIN casque c ON type_casque.id_type_casque = c.type_casque_id
             left join commentaire com on c.id_casque = com.casque_id
             GROUP BY type_casque.id_type_casque'''

    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['libelle']) for row in datas_show]
    values = [int(row['nbr_commentaires']) for row in datas_show]
    total_commentaires = sum(values)

    sql = '''SELECT tc.id_type_casque, 
                        tc.libelle_type_casque AS libelle, 
                        IFNULL(COUNT(c2.id_commantaire), 0) AS nbr_commentaires_total
                 FROM type_casque tc
                 LEFT JOIN casque c ON tc.id_type_casque = c.type_casque_id
                 left join commentaire c2 on c.id_casque = c2.casque_id
                 GROUP BY tc.id_type_casque'''

    mycursor.execute(sql)
    types_casques_nb = mycursor.fetchall()
    nbr_commentaires_total = [int(row['nbr_commentaires_total']) for row in types_casques_nb]

    print(nbr_commentaires_total)

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values
                           ,types_casques_nb=types_casques_nb
                           ,nbr_commentaires_total=nbr_commentaires_total)


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


