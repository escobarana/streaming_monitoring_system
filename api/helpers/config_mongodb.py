import pymongo
import os
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


# TODO: Define MongoDB Atlas URL
def get_client():
    if os.environ['ENVIRONMENT'] == 'LOCAL':
        client = pymongo.MongoClient("mongodb://localhost:27017/")
    elif os.environ['ENVIRONMENT'] == 'PRODUCTION':
        client = pymongo.MongoClient(f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:"
                                     f"{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@mongodb:27017/")
    else:
        client = None

    return client


def load_data_to_mongodb(document: dict, collection: str = 'data_sensors', db: str = 'monitoring'):
    """
        Function to load a document to MongoDB
    :param  db: Database name
    :param  collection: Collection name
    :param  document: Document to load to MongoDB
    :return: None
    """
    try:
        database = get_client()[db]
        collection = database[collection]

        logging.info(f"Loading data to database {database}, collection {collection} ...")

        collection.insert_one(document)
    except:
        logging.info(f"Cannot connect to database")


def get_data_from_mongodb(collection: str = 'data_sensors', db: str = 'monitoring'):
    """
        Function to retrieve documents from MongoDB
    :param  db: Database name
    :param  collection: Collection name
    :return: List of documents
    """
    my_list = []

    try:
        database = get_client()[db]
        col = database[collection]

        logging.info(f"Retrieving data from database {database}, collection {collection} ...")

        for each in col.find():
            my_list.append(each)
    except:
        logging.info(f"Cannot connect to database")

    return my_list
