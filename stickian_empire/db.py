import pymongo
import sqlite3

from flask import current_app, g
from flask_pymongo import PyMongo

def get_mongo_db_connection(connection_url=current_app.config['MONGO_DB_URL'], db_name=current_app.config['MONGO_DB_STICKIAN_EMPIRE']):
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

def close_mongo_db_connection():
    """Closes the Mongo DB database connection. """
    mongo_db = g.pop('mongo_db', None)
    if mongo_db is not None:
        mongo_db.close()

def get_mongo_db_collection_connection(db_connection, collection_name=current_app.config['PLAYER_DATA_COLLECTION']):
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

