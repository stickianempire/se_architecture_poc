import pymongo
import sqlite3

from flask import current_app, g
from flask_pymongo import PyMongo

def get_mongo_db_connection(connection_url="mongodb://localhost:27017/stickian_empire_db", db_name="stickian_empire_db"):
    """Fetches the Mongo DB connection
    
    :param connection_url: is the connection URL of the database 
    :param db_name: is the name of the database we're accessing
    :returns: the database connection 
    :raises:
    """
    if 'mongo_db' not in g:
        client = pymongo.MongoClient(connection_url)
        g.mongo_db = client[db_name]
    return g.mongo_db

def get_mongo_db_collection_connection(db_connection, collection_name="player_data"):
    """Fetches the a Mongo DB collection connection variables out of the EXISTING collections

    :param db_connection: the connection to the MongoDB database
    :param collection_name: the collection name to fetch
    :returns: the collection connection
    :raises: inexistant collection
    """
    listed_collections = db_connection.list_collection_names()
    if collection_name in listed_collections:
        return db_connection[collection_name]
    raise ValueError("Inexistant collection of name {0} at DB {1}.".format(collection_name, db_connection.name))

def init_app(app):
    """To ensure context actions are added to the app."""
    with app.app_context():
        get_mongo_db_connection()