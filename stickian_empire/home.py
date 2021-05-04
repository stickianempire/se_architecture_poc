from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from . import auth, db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def hello():
    return  render_template('base.html')