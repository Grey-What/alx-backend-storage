#!/usr/bin/env python3
"""
    insert a new document in a collection
    based on kwargs with python function
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """insert a new document in a collection"""
    return mongo_collection.insert_one(kwargs).inserted_id
