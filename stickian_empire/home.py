from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from stickian_empire.auth import login_required

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
@login_required
def home():
    return  render_template('game/home.html')

@bp.route('/game/windows/profile')
@login_required
def profile():
    return  render_template('game/windows/profile.html')

@bp.route('/game/windows/map')
@login_required
def map():
    g.map_values = [[1, 0, 1], [0, 0, 1], [0, 1, 1]]
    return  render_template('game/windows/map.html')