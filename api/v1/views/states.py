#!/usr/bin/python3
"""handle RESTful API in state"""
from models.state import State
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'])
def retrieve_list():
    """Retrives the list of all states"""
    states_list = []
    states = storage.all(State)
    for state in states.values():
        states_list.append(state.to_dict())
    return states_list


@app_views.route('/states/<state_id>', methods=['GET'])
def retrieve_state(state_id):
    """Retrieve state object"""
    if storage.get(State, state_id) is None:
        abort(404)
    return storage.get(State, state_id).to_dict()


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete state"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return {}, 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates a State: POST /api/v1/states"""
    object_data = request.get_json()

    if not object_data:
        abort(400, "Not a JSON")

    if "name" not in object_data:
        abort(400, "Missing name")

    obj = State(**object_data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Returns the State object with the status code 200"""
    obj = storage.get(State, state_id)
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
