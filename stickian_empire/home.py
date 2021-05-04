from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from . import auth, db

bp = Blueprint('home', __name__, url_prefix='/')

#@auth.login_required
@bp.route('/hello')
def hello():
    stolen_values = db.get_mongo_db_collection_connection(db.get_mongo_db_connection()).find()
    return str([doc for doc in stolen_values])