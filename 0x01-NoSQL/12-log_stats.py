#!/usr/bin/env python3
"""
    python script to provide some stats about Nginx logs
    stored in MongoDB

    database: logs
    collection: nginx
"""

from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """ prints some stats about Nginx request logs """
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    for method in methods:
        count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, count))

    status_count = len(list(nginx_collection.find(
                        {'method': 'GET', 'path': '/status'})))

    print('{} status check'.format(status_count))


def run():
    """ main function """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)


if __name__ == '__main__':
    run()
