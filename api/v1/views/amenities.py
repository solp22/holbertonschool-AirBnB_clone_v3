#!/usr/bin/python3
"""handle RESTful API in amenity"""
from models.amenity import Amenity
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'])
def retrieve_list():
    """Retrives the list of all amenities"""
    amen_list = []
    amenities = storage.all(Amenity)
    for amen in amenities.values():
        amen_list.append(amen.to_dict())
    return jsonify(amen_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def retrieve_amenity(amenity_id):
    """If the id is not linked to any object, raise a 404 error"""
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    return jsonify(storage.get(Amenity, amenity_id).to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete amenity"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return {}, 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """Creates an amenity"""
    object_data = request.get_json()

    if not object_data:
        abort(400, "Not a JSON")

    if "name" not in object_data:
        abort(400, "Missing name")

    obj = Amenity(**object_data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update amenity object"""
    obj = storage.get(Amenity, amenity_id)
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
