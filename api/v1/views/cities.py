#!/usr/bin/python3
"""handle RESTful API in state"""
from models.city import City
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_by_state(state_id):
    """Return cities in state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_id(city_id):
    """Return city with id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Dele city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return ({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City: POST /api/v1/states/<state_id>/cities"""
    obj_data = request.get_json()
    if not obj_data:
        abort(400, "Not a JSON")

    if "name" not in obj_data:
        abort(400, "Missing name")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    obj_data['state_id'] = state.id
    obj = City(**obj_data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Returns the City object with the status code 200"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    obj_data = request.get_json()
    if not obj_data:
        abort(400, "Not a JSON")

    for key, value in obj_data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
