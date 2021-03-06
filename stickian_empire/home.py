from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from stickian_empire.auth import login_required

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
@login_required
def home():
    """Route to return the home page template

    :returns: rendered home template
    """

    return  render_template('game/home.html')

@bp.route('/game/windows/profile')
@login_required
def profile_window():
    """Route to return the profile windowed page template

    :returns: rendered profile template
    """

    return  render_template('game/windows/profile.html')

@bp.route('/game/windows/map')
@login_required
def map_window():
    """Route to return the map windowed page template
    
    :returns: rendered maps template
    """
    
    return  render_template('game/windows/map.html', map_values=[[1, 0, 1], [0, 0, 1], [0, 1, 1]])

@bp.route('/game/windows/overview')
@login_required
def overview_window():
    """Route to return the overview windowed page template
    
    :returns: rendered overview template
    """
    
    troops = {
        "swordsman": 1,
        "bowman": 2,
        "lancer": 10
    }
    return  render_template('game/windows/overview.html', troops=troops)

@bp.route('/game/windows/detail')
@login_required
def detail_window():
    """Route to return the detail windowed page template
    
    :returns: rendered detail template
    """
    
    return  render_template('game/windows/detail.html')