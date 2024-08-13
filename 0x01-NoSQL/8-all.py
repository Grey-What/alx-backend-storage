#!/usr/bin/env python3
"""list allthe documents in a collection using a python function"""


def list_all(mongo_collection):
    """returns all documents in a collection"""
    return [doc for doc in mongo_collection.find()]
