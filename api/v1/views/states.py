#!/usr/bin/python3
""" New view for states """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
import models


@app_views.route('/states', methods=['GET'])
def showStates():
    """ Shows all states db storage """
    myList = []
    for value in models.storage.all("State").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/states/<state_id>', methods=['GET'])
def showStateId(state_id):
    """ Shows all states db storage """
    state = models.storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleteStateId(state_id):
    """ Deletes a state in db storage """
    state = models.storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'])
def createState():
    """ Creates a state db storage """
    if request.is_json:
        try:
            data = request.get_json()
        except BaseException:
            data = {"error": "Not a JSON"}
            return data, 400
        if "name" in data:
            state = State(name=data["name"])
            state.save()
            return (jsonify(state.to_dict()), 201)
        data = {"error": "Missing name"}
        return (jsonify(data), 400)


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_states(state_id):
    """ Update a State object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for k, val in request.get_json().items():
        if k is not 'id' and k is not 'created_at' and k is not 'updated_at':
            setattr(state, k, val)
    state.save()
    return jsonify(state.to_dict()), 200
