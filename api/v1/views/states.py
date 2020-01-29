#!/usr/bin/python3
""" New view for states """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
import models


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def showStates():
    """ Shows all states db storage """
    myList = []
    for value in models.storage.all("State").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def showStateId(state_id):
    """ Shows all states db storage """
    state = models.storage.get("State", state_id)
    if state:
        return state.to_dict()
    abort(404)


@app_views.route(
    '/states/<state_id>',
    strict_slashes=False,
    methods=['DELETE'])
def deleteStateId(state_id):
    """ Deletes a state in db storage """
    state = models.storage.get("State", state_id)
    if state:
        state.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
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
            return state.to_dict(), 201
        data = {"error": "Missing name"}
        return (jsonify(data), 400)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def updateState(state_id):
    """ Updates a state in db storage """
    state = models.storage.get("State", state_id)
    if state and request.is_json:
        try:
            data = request.get_json()
        except BaseException:
            data = {"error": "Not a JSON"}
            return data, 400
        for key, value in data.items():
            if key == 'name':
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
    abort(404)
