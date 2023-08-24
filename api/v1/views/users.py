#!/usr/bin/python3
"""handle RESTful API in user"""
from models.user import User
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'])
def retrieve_user_list():
    """Retrives the list of all users"""
    user_list = []
    users = storage.all(User)
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def retrieve_user(user_id):
    """If the id is not linked to any object, raise a 404 error"""
    if storage.get(User, user_id) is None:
        abort(404)
    return jsonify(storage.get(User, user_id).to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return {}, 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """Creates a user"""
    object_data = request.get_json()

    if not object_data:
        abort(400, "Not a JSON")

    if "email" not in object_data:
        abort(400, "Missing email")

    if "password" not in object_data:
        abort(400, "Missing password")

    obj = User(**object_data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user object"""
    obj = storage.get(User, user_id)
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
