import os
import sqlite3

import pandas as pd
from flask import Flask, request, jsonify, current_app, g as app_ctx

import time

from flask_caching import Cache

from pycom.sql.query_builder import PyComSQLQueryBuilder

# db_path = '/Users/philipp/DocumentsLocal/prot.db'
db_path = os.path.expanduser('~/DocumentsLocal/prot.db')

config = {
    "DEBUG": True,
    "JSONIFY_PRETTYPRINT_REGULAR": False,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    # "CACHE_DIR": "/tmp/pycom_cache",
}
app = Flask(__name__)
app.config.from_mapping(config)

cache = Cache(app)


# @app.before_request
# def before_request():
#     flask.g.start = time.time()
#
#
# @app.after_request
# def after_request(response):
#     diff = time.time() - flask.g.start
#     if (response.response and
#             (200 <= response.status_code < 300) and
#             (response.content_type.startswith('text/html'))):
#         response.set_data(response.get_data().replace(
#             b'__EXECUTION_TIME__', bytes(str(diff), 'utf-8')))
#     return response


@app.before_request
def before_request():
    app_ctx.start_time = time.perf_counter()


@app.after_request
def after_request(response):
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    current_app.logger.warning('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))

    return response


'''
id: entry.entryId = id
sequence: entry.sequence = sequence
min_length: entry.sequenceLength >= minlength
max_length: entry.sequenceLength <= maxlength
organism: organism.taxonomy LIKE '%organism%' => organism.organismId => entry.organismId
structhelix: entry.structhelix <= structhelix
structturn: entry.structturn <= structturn
structstrand: entry.structstrand <= structstrand
cath (A.B.C.D): cath_class.cath_1 = A, cath_class.cath_2 = B, cath_class.cath_3 = C, cath_class.cath_4 = D => cath_class.entryId => entry.entryId
enzyme (A.B.C.D): enzyme_class.enzyme_1 = A, enzyme_class.enzyme_2 = B, enzyme_class.enzyme_3 = C, enzyme_class.enzyme_4 = D => enzyme_class.entryId => entry.entryId
'''


@app.route('/test')
def run():
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    c = conn.cursor()

    query_builder = PyComSQLQueryBuilder()
    # query_builder.add_constraint('helixmin', 0.1046)

    results = fetch_from_db(*query_builder.build())

    # print(c.fetchall())
    print(len(results))

    # ['entryId', 'sequenceLength', 'organismId', 'structHelix', 'structTurn', 'structStrand', 'hasPTM']
    # print(results[0])

    # response = jsonify(results)

    return jsonify(results)


# @cache.memoize(50, cache_none=True)
def fetch_from_db(query, params):
    print("*** Accessing DB ***")
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    c = conn.cursor()

    c.execute(query, params)

    result = c.fetchall()

    # result: pd.DataFrame = pd.DataFrame(result, columns=['entryId', 'neff', 'sequenceLength', 'organismId',
    #                                                      'structHelix', 'structTurn', 'structStrand', 'hasPTM',
    #                                                      'sequence'])

    return result


if __name__ == '__main__':
    run()
