#!/usr/bin/python3
"""
handle RESTful API in Place.
Create a new view for Place objects that handles all default RESTFul API actions:
Method:
    ['GET']: For route /cities/<city_id>/places and /places/<place_id>
    ['DELETE']: For route /places/<place_id>
    ['POST']: For route /cities/<city_id>/places
    ['PUT']: For route /places/<place_id>
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_city(city_id):
    """
    Retrieves the list of all Place objects of a City:
    GET /api/v1/cities/<city_id>/places
    Return:
        places in city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for to_place in city.places:
        places_list.append(to_place.to_dict())
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """
    Retrieves a Place object. :
    GET /api/v1/places/<place_id>
    Return:
        places with id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete to place object with espepecified id
    Returns:
        An empty dictionary with the status code 200
    """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return ({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place: POST /api/v1/cities/<city_id>/places
    Return:
        Create to place object and add method to_dict
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    obj_data = request.get_json()
    if not obj_data:
        abort(400, "Not a JSON")

    if "user_id" not in obj_data:
        abort(400, "Missing user_id")

    usr = storage.get(User, request.get_json()["user_id"])
    if usr is None:
        abort(404)

    if "name" not in obj_data:
        abort(400, "Missing name")

    user = storage.get(User, obj_data['user_id'])
    obj_data['city_id'] = city.id
    obj_data['user_id'] = user.id
    obj = Place(**obj_data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object: PUT /api/v1/places/<place_id>
    Return:
        Update to place object and add method to_dict
    """
    obj = storage.get(Place, place_id)
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
