#! /usr/bin/python
# -*- coding:utf-8 -*-
import os

from flask import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    db = get_db()
    mycursor = db.cursor()

    with open(os.environ.get('DB_FILE'), 'r', encoding='utf-8') as sql_file:
        sql_commands = sql_file.read()

    try:
        for command in sql_commands.split(';'):
            command = command.strip()
            if command:
                mycursor.execute(command)
        db.commit()
        flash("Database initialized successfully!", "success")
    except Exception as e:
        db.rollback()
        logging.error(f"Error during database initialization: {e}")
        flash("An error occurred during initialization.", "error")
    finally:
        mycursor.close()

    return redirect('/')