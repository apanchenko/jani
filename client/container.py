import logging
import sys
import pymongo
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level="INFO",
        format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
    )

    # servives

    mongo_client = providers.Singleton(pymongo.MongoClient, 'mongo', 27017)
