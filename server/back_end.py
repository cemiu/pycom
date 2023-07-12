import os

import flask
from flask_caching import Cache
from flask_parameter_validation import ValidateParameters, Query

from werkzeug.security import safe_join

from pycom import PyCom, ProteinParams
from pycom.interface import _find_helper
from pycom.selector import MatrixFormat
from pycom.sql.constraints_utils import to_bool, to_int

config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = flask.Flask(__name__)

app.config.from_mapping(config)
app.json.sort_keys = False
app.json.compact = False

# set up caching
cache = Cache(app)
_find_helper.query_db = cache.memoize(timeout=360, cache_none=True)(_find_helper.query_db)

pycom_db_path = os.environ.get('PYCOM_DB_PATH', '~/docs/pycom.db')
pycom_mat_path = os.environ.get('PYCOM_MAT_PATH', '~/docs/pycom.mat')
pycom_aln_path = os.environ.get('PYCOM_ALN_PATH', '~/docs/aln')

pyc = PyCom(db_path=pycom_db_path, mat_path=pycom_mat_path)
valid_protein_params = set(ProteinParams)


@app.route('/api/find', methods=['GET'])
@ValidateParameters()
def find(
        # Search parameters:
        # uniprot_id, sequence, min_length, max_length, min_helix, max_helix, min_turn, max_turn, min_strand,
        # max_strand, organism_id, organism, cath, enzyme, has_substrate, has_ptm, has_pbd, disease, disease_id,
        # has_disease, cofactor, cofactor_id, has_cofactor

        # Output parameters:
        # matrix, page, page_size
        page: int = Query(1),
        page_size: int = Query(default=10, min_int=1, max_int=100)
):
    data = flask.request.args.to_dict()

    if flask.request.data not in {b'', None}:
        data_json = flask.request.get_json(force=True, silent=True)
        assert data_json is not None, 'Invalid JSON body'
        data.update(data_json)

    # parse parameters
    load_matrices = to_bool(data.pop('matrix', False), entry='matrix parameter')
    page = to_int(data.pop('page', page), entry='page parameter')
    page_size = to_int(data.pop('page_size', page_size), entry='page_size parameter')

    # validate that no invalid parameters are passed
    invalid_params = set(data) - valid_protein_params
    assert not invalid_params, f'Invalid parameters: {", ".join(invalid_params)}'

    if load_matrices:
        assert page_size <= 10, 'page_size cannot be larger than 10 when loading matrices'

    # Request validated, now build the response #

    entries = pyc.find(data)  # find entries matching the constraints
    selection = pyc.paginate(entries, page=page, per_page=page_size)

    if load_matrices:
        selection = pyc.load_matrices(selection, mat_format=MatrixFormat.JSON)
    else:
        selection = selection.drop(columns=['matrix'])

    if load_matrices:
        app.json.compact = True

    response = flask.jsonify({
        'results': selection.to_dict(orient='records'),
        'page': page,
        'total_pages': len(entries) // page_size + 1,
        'result_count': len(entries),
        'showing': f'{(page - 1) * page_size + 1}-{min(page * page_size, len(entries))}'
    })

    if load_matrices:
        app.json.compact = False

    return response


@app.route('/api/alignments', methods=['GET'])
def get_alignments_no_arg():
    assert flask.request.data not in {b'', None}, \
        'Please specify a uniprot_id: https://pycom.brunel.ac.uk/alignments/<uniprot_id>'

    data_json = flask.request.get_json(force=True, silent=True)
    assert data_json is not None, 'Invalid JSON body'
    assert 'uniprot_id' in data_json, 'Specify the uniprot_id: {"uniprot_id": "P12345"}'

    uniprot_id = data_json.get('uniprot_id', None)
    return get_alignments(uniprot_id)


@app.route('/api/alignments/<uniprot_id>/', methods=['GET'])
def get_alignments(uniprot_id):
    """
    Get alignments for a given uniprot_id

    :param uniprot_id:
    :return: alignment file
    """
    # assert that file exists
    aln_path = safe_join(pycom_aln_path, f'{uniprot_id}.aln')
    assert aln_path is not None and os.path.isfile(aln_path), f'No alignments found for {uniprot_id}'

    return flask.send_from_directory(pycom_aln_path, f'{uniprot_id}.aln', as_attachment=False)


@app.route('/api/get-disease-list', methods=['GET'])
def get_disease_list():
    """
    Get list of diseases

    :return: list of diseases
    """
    diseases = pyc.get_disease_list()
    return flask.jsonify(diseases.to_dict(orient='records'))


@app.route('/api/get-cofactor-list', methods=['GET'])
def get_cofactor_list():
    """
    Get list of cofactors

    :return: list of cofactors
    """
    cofactors = pyc.get_cofactor_list()
    return flask.jsonify(cofactors.to_dict(orient='records'))


@app.route('/api/get-organism-list', methods=['GET'])
def get_organism_list():
    """
    Get list of organisms

    :return: list of organisms
    """
    organisms = pyc.get_organism_list()
    return flask.jsonify(organisms.to_dict(orient='records'))


@app.errorhandler(AssertionError)
def handle_assertion_error(error):
    """Catch assertion errors and return them as JSON,
    with a 400 status code and a link to the documentation."""
    return flask.jsonify({
        'message': str(error),
        'documentation': 'TODO: add documentation link here'  # TODO
    }), 400


if __name__ == '__main__':
    app.run(debug=False, port=5351)
