#!/usr/bin/env python

'''
.. module:: glob.api
.. moduleauthor:: Julien Spronck
.. created:: September 2017

Module for the Flask RESTful API.
'''

import queries
import config

from flask import Flask, jsonify, abort, make_response, url_for, request
from queries import IntegrityError
# from flask.ext.httpauth import HTTPBasicAuth

DATABASE = queries.DataBase()

APP = Flask(__name__, static_url_path="")
# auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python'
#     return None

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403)
#     # return 403 instead of 401 to prevent browsers from displaying
#     # the default auth dialog

@APP.errorhandler(400)
def not_found(error):
    '''Bad request (Error 400)
    '''
    return make_response(jsonify({'error': 'Bad request'}), 400)

@APP.errorhandler(404)
def not_found(error):
    '''Page not found (Error 404)
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)

def get_uri(funcname, obj_id):
    '''Get URI given an object id and the handler function
    '''
    return url_for(funcname, obj_id=obj_id, _external=True)

def make_public(obj):
    '''transform all ids in URI
    '''
    if not isinstance(obj, dict):
        return obj
    newdic = {}
    for key, val in obj.iteritems():
        if isinstance(val, dict):
            newdic[key] = make_public(val)
        elif isinstance(val, list):
            newdic[key] = [make_public(x) for x in val]
        elif key.endswith('id'):
            root = key.split('_')[0]
            newdic['uri'] = get_uri('get_'+root, val)
        else:
            newdic[key] = val
    return newdic

### TAGS ###

@APP.route('/api/v'+config.API_VERSION+'/tags', methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/tags/', methods=['GET'])
# @auth.login_required
def get_tags():
    '''Get all tags in JSON format
    '''
    tags = DATABASE.get_all_tags()
    if not tags:
        abort(404)
    return jsonify({'tags': [make_public(tag) for tag in tags]})

@APP.route('/api/v'+config.API_VERSION+'/tags', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/tags/', methods=['POST'])
# @auth.login_required
def post_tag():
    '''Create new tag
    '''
    content = request.get_json()
    if not content or 'tag' not in content:
        abort(400)
    tag = content['tag']
    try:
        tag = DATABASE.create_tag(**tag)
    except (TypeError, IntegrityError):
        abort(400)
    if not tag:
        abort(400)
    return jsonify({'tag': tag}), 201

@APP.route('/api/v'+config.API_VERSION+'/tags/<int:obj_id>', methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/tags/<int:obj_id>/', methods=['GET'])
# @auth.login_required
def get_tag(obj_id):
    '''Get a specific tag in JSON format
    '''
    tag = DATABASE.get_tag(obj_id=obj_id)
    if tag is None:
        abort(404)
    return jsonify({'tag': make_public(tag)})

@APP.route('/api/v'+config.API_VERSION+'/tags/<int:obj_id>',
           methods=['DELETE'])
@APP.route('/api/v'+config.API_VERSION+'/tags/<int:obj_id>/',
           methods=['DELETE'])
# @auth.login_required
def delete_tag(obj_id):
    '''Delete a specific tag
    '''
    try:
        response = DATABASE.delete_tag(obj_id)
    except (ValueError, IntegrityError):
        abort(400)
    return response

### CATEGORIES ###

@APP.route('/api/v'+config.API_VERSION+'/categories', methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/categories/', methods=['GET'])
# @auth.login_required
def get_categories():
    '''Get all categories in JSON format
    '''
    categories = DATABASE.get_all_categories()
    if not categories:
        abort(404)
    return jsonify({'categories': [make_public(category)
                                   for category in categories]})

@APP.route('/api/v'+config.API_VERSION+'/categories', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/categories/', methods=['POST'])
# @auth.login_required
def post_category():
    '''Create new category
    '''
    content = request.get_json()
    if not content or 'category' not in content:
        abort(400)
    category = content['category']
    try:
        category = DATABASE.create_category(**category)
    except (TypeError, IntegrityError):
        abort(400)
    if not category:
        abort(400)
    return jsonify({'category': category}), 201

@APP.route('/api/v'+config.API_VERSION+'/categories/<int:obj_id>',
           methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/categories/<int:obj_id>/',
           methods=['GET'])
# @auth.login_required
def get_category(obj_id):
    '''Get a specific category in JSON format
    '''
    category = DATABASE.get_category(obj_id)
    if category is None:
        abort(404)
    return jsonify({'category': make_public(category)})

@APP.route('/api/v'+config.API_VERSION+'/categories/<int:obj_id>',
           methods=['DELETE'])
@APP.route('/api/v'+config.API_VERSION+'/categories/<int:obj_id>/',
           methods=['DELETE'])
# @auth.login_required
def delete_category(obj_id):
    '''Delete a specific category
    '''
    try:
        response = DATABASE.delete_category(obj_id)
    except (ValueError, IntegrityError):
        abort(400)
    return response

### LOCATION ###

@APP.route('/api/v'+config.API_VERSION+'/locations/<int:obj_id>',
           methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/locations/<int:obj_id>/',
           methods=['GET'])
# @auth.login_required
def get_location(obj_id):
    '''Get a specific location in JSON format
    '''
    location = DATABASE.get_location(obj_id)
    if location is None:
        abort(404)
    return jsonify({'location': make_public(location)})

@APP.route('/api/v'+config.API_VERSION+'/locations', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/locations/', methods=['POST'])
# @auth.login_required
def post_location():
    '''Create new location
    '''
    content = request.get_json()
    if not content or 'location' not in content:
        abort(400)
    location = content['location']
    try:
        location = DATABASE.create_location(**location)
    except (TypeError, IntegrityError):
        abort(400)
    if not location:
        abort(400)
    return jsonify({'location': location}), 201

@APP.route('/api/v'+config.API_VERSION+'/locations/<int:obj_id>',
           methods=['DELETE'])
@APP.route('/api/v'+config.API_VERSION+'/locations/<int:obj_id>/',
           methods=['DELETE'])
# @auth.login_required
def delete_location(obj_id):
    '''Delete a specific location
    '''
    try:
        response = DATABASE.delete_location(obj_id)
    except (ValueError, IntegrityError):
        abort(400)
    return response

### PHOTO ###

@APP.route('/api/v'+config.API_VERSION+'/photos', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/photos/', methods=['POST'])
# @auth.login_required
def post_photo():
    '''Create new photo
    '''
    content = request.get_json()
    if not content or 'photo' not in content:
        abort(400)
    photo = content['photo']
    try:
        photo = DATABASE.create_photo(**photo)
    except (TypeError, IntegrityError):
        abort(400)
    if not photo:
        abort(400)
    return jsonify({'photo': photo}), 201

@APP.route('/api/v'+config.API_VERSION+'/photos/<int:obj_id>',
           methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/photos/<int:obj_id>/',
           methods=['GET'])
# @auth.login_required
def get_photo(obj_id):
    '''Get a specific photo in JSON format
    '''
    abort(404)

@APP.route('/api/v'+config.API_VERSION+'/photos/<int:obj_id>',
           methods=['DELETE'])
@APP.route('/api/v'+config.API_VERSION+'/photos/<int:obj_id>/',
           methods=['DELETE'])
# @auth.login_required
def delete_photo(obj_id):
    '''Delete a specific photo
    '''
    try:
        response = DATABASE.delete_photo(obj_id)
    except (ValueError, IntegrityError):
        abort(400)
    return response

### ITEMS ###

@APP.route('/api/v'+config.API_VERSION+'/items', methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/items/', methods=['GET'])
# @auth.login_required
def get_items():
    '''Get all items in JSON format
    '''
    items = DATABASE.get_all_items()
    if not items:
        abort(404)
    return jsonify({'items': [make_public(item) for item in items]})

@APP.route('/api/v'+config.API_VERSION+'/items', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/items/', methods=['POST'])
# @auth.login_required
def post_item():
    '''Create new item
    '''
    content = request.get_json()
    if not content or 'item' not in content:
        abort(400)
    item = content['item']
    try:
        item = DATABASE.create_item(**item)
    except (TypeError, IntegrityError):
        abort(400)
    if not item:
        abort(400)
    return jsonify({'item': item}), 201

@APP.route('/api/v'+config.API_VERSION+'/items/<int:obj_id>', methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/items/<int:obj_id>/', methods=['GET'])
# @auth.login_required
def get_item(obj_id):
    '''Get a specific item in JSON format
    '''
    item = DATABASE.get_item(obj_id)
    if item is None:
        abort(404)
    return jsonify({'item': make_public(item)})

@APP.route('/api/v'+config.API_VERSION+'/items/<int:obj_id>',
           methods=['DELETE'])
@APP.route('/api/v'+config.API_VERSION+'/items/<int:obj_id>/',
           methods=['DELETE'])
# @auth.login_required
def delete_item(obj_id):
    '''Delete a specific item
    '''
    try:
        response = DATABASE.delete_item(obj_id)
    except (ValueError, IntegrityError):
        abort(400)
    return response

### COMMENT ###

@APP.route('/api/v'+config.API_VERSION+'/comments', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/comments/', methods=['POST'])
# @auth.login_required
def post_comment():
    '''Create new comment
    '''
    content = request.get_json()
    if not content or 'comment' not in content:
        abort(400)
    comment = content['comment']
    try:
        comment = DATABASE.create_comment(**comment)
    except (TypeError, IntegrityError):
        abort(400)
    if not comment:
        abort(400)
    return jsonify({'comment': comment}), 201

@APP.route('/api/v'+config.API_VERSION+'/comments/<int:obj_id>',
           methods=['DELETE'])
@APP.route('/api/v'+config.API_VERSION+'/comments/<int:obj_id>/',
           methods=['DELETE'])
# @auth.login_required
def delete_comment(obj_id):
    '''Delete a specific comment
    '''
    try:
        response = DATABASE.delete_comment(obj_id)
    except (ValueError, IntegrityError):
        abort(400)
    return response

### LIKE ###

@APP.route('/api/v'+config.API_VERSION+'/likes', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/likes/', methods=['POST'])
# @auth.login_required
def post_like():
    '''Create new like
    '''
    content = request.get_json()
    if not content or 'like' not in content:
        abort(400)
    like = content['like']
    try:
        like = DATABASE.create_like(**like)
    except (TypeError, IntegrityError):
        abort(400)
    if not like:
        abort(400)
    return jsonify({'like': like}), 201

@APP.route('/api/v'+config.API_VERSION+'/likes/<int:post_id>/<int:user_id>',
           methods=['DELETE'])
@APP.route('/api/v'+config.API_VERSION+'/likes/<int:post_id>/<int:user_id>/',
           methods=['DELETE'])
# @auth.login_required
def delete_like(post_id, user_id):
    '''Delete a specific like
    '''
    try:
        response = DATABASE.delete_like(post_id, user_id)
    except (ValueError, IntegrityError):
        abort(400)
    return response

### POSTS ###

@APP.route('/api/v'+config.API_VERSION+'/posts', methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/posts/', methods=['GET'])
# @auth.login_required
def get_posts():
    '''Get all posts in JSON format
    '''
    posts = DATABASE.get_all_posts()
    if not posts:
        abort(404)
    return jsonify({'posts': [make_public(post) for post in posts]})

@APP.route('/api/v'+config.API_VERSION+'/posts', methods=['POST'])
@APP.route('/api/v'+config.API_VERSION+'/posts/', methods=['POST'])
# @auth.login_required
def post_post():
    '''Create new post
    '''
    content = request.get_json()
    if not content or 'post' not in content:
        abort(400)
    post = content['post']
    try:
        post = DATABASE.create_post(**post)
    except (TypeError, IntegrityError):
        abort(400)
    if not post:
        abort(400)
    return jsonify({'post': post}), 201

@APP.route('/api/v'+config.API_VERSION+'/posts/<int:obj_id>',
           methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/posts/<int:obj_id>/',
           methods=['GET'])
# @auth.login_required
def get_post(obj_id):
    '''Get a specific post in JSON format
    '''
    post = DATABASE.get_post(obj_id)
    if post is None:
        abort(404)
    return jsonify({'post': make_public(post)})

### USERS ###

@APP.route('/api/v'+config.API_VERSION+'/users/<int:obj_id>',
           methods=['GET'])
@APP.route('/api/v'+config.API_VERSION+'/users/<int:obj_id>/',
           methods=['GET'])
# @auth.login_required
def get_user(obj_id):
    '''Get a specific post in JSON format
    '''
    user = DATABASE.get_user(obj_id)
    if user is None:
        abort(404)
    return jsonify({'user': user})

### REST ###

@APP.route('/', defaults={'path': ''})
@APP.route('/<path:path>')
def catch_all(path):
    '''Only for debugging purposes
    '''
    return 'You want path: %s' % path

# @APP.route('/todo/api/v'+config.API_VERSION+'/tasks', methods=['POST'])
# @auth.login_required
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'obj_id': tasks[-1]['obj_id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': make_public_task(task)}), 201
#
# @APP.route('/todo/api/v'+config.API_VERSION+'/tasks/<int:task_id>',
#            methods = ['PUT'])
# @auth.login_required
# def update_task(task_id):
#     task = filter(lambda t: t['obj_id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != unicode:
#         abort(400)
#     if ('description' in request.json
#             and type(request.json['description']) is not unicode):
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description',
#                                               task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify({'task': make_public_task(task[0])})
#
# @APP.route('/todo/api/v'+config.API_VERSION+'/tasks/<int:task_id>',
#            methods=['DELETE'])
# @auth.login_required
# def delete_task(task_id):
#     task = filter(lambda t: t['obj_id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     tasks.remove(task[0])
#     return jsonify({'result': True})

if __name__ == '__main__':
    APP.run(debug=True)
