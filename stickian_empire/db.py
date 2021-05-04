import pymongo
import sqlite3
import click

from flask import current_app, g
from flask_pymongo import PyMongo

def get_mongo_db_connection(connection_url="mongodb://localhost:27017/stickian_empire_db"):
    """Fetches the Mongo DB connection
    
    :param connection_url: is the connection URL of the database 
    :returns: the database connection 
    :raises:
    """
    if 'mongo_db' not in g:
        client = pymongo.MongoClient(connection_url)
        g.mongo_db = client
    return g.mongo_db

def get_mongo_db_collection_connection(db_connection, db_name, collection_name):
    """Fetches the a Mongo DB collection connection variables out of the EXISTING collections

    :param db_connection: the connection to the MongoDB database
    :param db_name: is the name of the database we're accessing
    :param collection_name: the collection name to fetch
    :returns: the collection connection
    :raises: inexistant collection
    """
    db_connection = db_connection[db_name]
    listed_collections = db_connection.list_collection_names()
    if collection_name in listed_collections:
        return db_connection[collection_name]
    raise ValueError("Inexistant collection of name {0} at DB {1}.".format(collection_name, db_connection.name))

def close_mongo_db(e=None):
    """Closes the Mongo DB connection
    """
    db_connection = g.pop('mongo_db', None)
    if db_connection is not None:
        db_connection.close()

def init_app(app):
    """Register DB functions to run in app

    :param app: the Flask app
    """
    app.teardown_appcontext(close_mongo_db)