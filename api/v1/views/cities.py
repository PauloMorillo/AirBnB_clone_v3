#!/usr/bin/python3
""" New views for cities """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
import models


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['GET'])
def showCities(state_id):
    """ Shows all cities for a state in db storage """
    state = models.storage.get("State", state_id)
    if state:
        citiesList = []
        eachCity = models.storage.all("City")
        for value in eachCity.values():
            if value.state_id == state_id:
                citiesList.append(value.to_dict())
        return jsonify(citiesList)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def showCity(city_id):
    """ Shows a specific city in db """
    city = models.storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def deleteCity(city_id):
    """ Deletes a city in db storage """
    city = models.storage.get("City", city_id)
    if city:
        city.delete()
        models.storage.save()
        return {}
    abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['POST'])
def createCity(state_id):
    """ Creates a city for a state in db storage """
    if models.storage.get("State", state_id) is None:
        abort(404)
    if request.is_json:
        try:
            data = request.get_json()
        except BaseException:
            data = {"error": "Not a JSON"}
            return data, 400
        if "name" in data:
            city = City(name=data["name"])
            city.state_id = state_id
            city.save()
            return city.to_dict(), 201
        data = {"error": "Missing name"}
        return data, 400


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def updateCity(city_id):
    """ Updates a city in db storage """
    city = models.storage.get("City", city_id)
    if city and request.is_json:
        try:
            data = request.get_json()
        except BaseException:
            data = {"error": "Not a JSON"}
            return data, 400
        for key, value in data.items():
            if key == 'name':
                setattr(city, key, value)
        city.save()
        return city.to_dict()
    abort(404)
