from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from stickian_empire.auth import login_required

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
@login_required
def home():
    return  render_template('game/home.html')