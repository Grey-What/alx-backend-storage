#!/usr/bin/env python3
"""return a list of school based on having a specific topic"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """return a list of school based on having a specific topic"""
    return mongo_collection.find({"topics": topic})
