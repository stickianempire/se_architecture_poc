import functools
import re
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from stickian_empire.db import get_mongo_db_connection, get_mongo_db_collection_connection
from bson.objectid import ObjectId

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Function to handle log in, handling the route for the get and the post method.
    
    :GET returns: login template
    :POST returns: redirect to index if successful login
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_collection = get_mongo_db_collection_connection(get_mongo_db_connection(), "stickian_empire_db", "user_login")
        error = None
        user = users_collection.find_one({"username": username})

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            # save a string of ObjectId
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index'))

        flash(error)

    # find a way to keep session
    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Function to handle registering, handling the route for the get and the post method.
    
    :GET returns: register template
    :POST returns: redirect for login page if successful registeration
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['cpassword']
        users_collection = get_mongo_db_collection_connection(get_mongo_db_connection(), "stickian_empire_db", "user_login")
        errors = []

        if not username:
            errors.append('Username is required.')
        elif not password:
            errors.append( 'Password is required.')
        elif not confirm_password:
            errors.append( 'Confirm the password.')
        else:
            if password != confirm_password:
                errors.append( 'Passwords do not match.')
            if users_collection.find_one({"username": username}) is not None:
                errors.append( 'User "{}" is already registered.'.format(username))
            if not is_password_strong(password):
                errors.append( 'Week password')

        if not errors:
            users_collection.insert_one({
                "username": username,
                "password": generate_password_hash(password)
            })
            return redirect(url_for('auth.login'))
        for error in errors:
            flash(error)

    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    """Function to handle logout, clearing the player session.
    
    :returns: redirect to index page
    """

    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    """Function to keep user id available in g for the request during the user session between app requests.
    """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        users_collection = get_mongo_db_collection_connection(get_mongo_db_connection(), "stickian_empire_db", "user_login")
        g.user = users_collection.find_one({"_id": ObjectId(user_id)}, {"username", "_id"})

def login_required(view):
    """Decorator for login_required
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def is_password_strong(password):
    """Function to keep user id available in g for the request during the user session between app requests.

    :params: password is the attempted password for registering
    :returns: boolean weather the password is strong enough or not
    """

    if len(password) < 8:
        return False
    if re.search(r"\d", password) is None:
        return False
    if re.search(r"[a-z]", password) is None and re.search(r"[A-Z]", password) is None:
        return False
    return True