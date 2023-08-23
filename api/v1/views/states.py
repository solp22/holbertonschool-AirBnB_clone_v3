#!/usr/bin/python3
"""handle RESTful API in state"""
from models.state import State
from flask import abort
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
    if storage.get(State, state_id) is None:
        abort(404)
    return storage.get(State, state_id).to_dict()

