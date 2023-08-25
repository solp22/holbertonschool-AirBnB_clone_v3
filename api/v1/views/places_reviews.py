#!/usr/bin/python3
"""handle RESTful API in state"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    """Return reviews in place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_list = []
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """Return reviews with id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return ({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    obj_data = request.get_json()
    if not obj_data:
        abort(400, "Not a JSON")

    if "user_id" not in obj_data:
        abort(400, "Missing user_id")

    usr = storage.get(User, request.get_json()["user_id"])
    if usr is None:
        abort(404)

    if "text" not in obj_data:
        abort(400, "Missing text")

    obj = Review(**obj_data)
    obj.place_id = place_id
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update review"""
    obj = storage.get(Review, review_id)
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
