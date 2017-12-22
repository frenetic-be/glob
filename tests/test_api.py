#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for glob.queries
'''
import datetime
import os
import random
import requests
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'glob'))

ROOT = u'http://127.0.0.1:5000/api/v1.0/'

DATE = datetime.datetime.now().isoformat()

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
        if key.endswith('id'):
            obj = key.split('_')[0]
            newdic['uri'] = ROOT+obj+'s/{}/'.format(val)
        else:
            newdic[key] = val
    return newdic

DIC_PHOTO_1_ID = {'file_name': u'some_photo.jpg',
                  'photo_id': 1}
DIC_PHOTO_1 = make_public(DIC_PHOTO_1_ID)

DIC_LOC_1_ID = {'lat': 37.7749,
             'lon': -122.4194,
             'address': 'San Francisco, CA, USA',
             'location_id': 1}
DIC_LOC_2_ID = {'lat': 1.45,
             'lon': 5.67,
             'address': 'Blah',
             'location_id': 4}
DIC_LOC_1 = make_public(DIC_LOC_1_ID)
DIC_LOC_2 = make_public(DIC_LOC_2_ID)

DIC_TAG_1_ID = {'tag_id': 1,
             'tag_name': u'cool',
             'number_of_posts': 2}
DIC_TAG_2_ID = {'tag_id': 2,
             'tag_name': u'awesome',
             'number_of_posts': 5}
DIC_TAG_3_ID = {'tag_id': 3,
             'tag_name': u'bof',
             'number_of_posts': 4}

DIC_TAG_1 = make_public(DIC_TAG_1_ID)
DIC_TAG_2 = make_public(DIC_TAG_2_ID)
DIC_TAG_3 = make_public(DIC_TAG_3_ID)

DIC_ITEM_1_ID = {'item_id': 1,
                 'category': u'Sport\\Hike',
                 'item_name': u'Some trail',
                 'location': DIC_LOC_1_ID,
                 'rating': 3.75}
DIC_ITEM_2_ID = {'item_id': 2,
                 'category': u'Place\\Business\\Hotel',
                 'item_name': u'Hotel California',
                 'location': {},
                 'rating': 3.0}
DIC_ITEM_3_ID = {'item_id': 3,
                 'category': u'Animals\\Cats',
                 'item_name': u'Awesome stuff',
                 'location': DIC_LOC_2_ID,
                 'rating': None}
DIC_ITEM_4_ID = {'item_id': 4,
                 'category': u'Place\\Business\\Hotel',
                 'item_name': u'Cool stuff',
                 'location': {},
                 'rating': None}

DIC_ITEM_1 = make_public(DIC_ITEM_1_ID)
DIC_ITEM_1['location'] = DIC_LOC_1
DIC_ITEM_2 = make_public(DIC_ITEM_2_ID)
DIC_ITEM_3 = make_public(DIC_ITEM_3_ID)
DIC_ITEM_3['location'] = DIC_LOC_2
DIC_ITEM_4 = make_public(DIC_ITEM_4_ID)

DIC_POST_1_ID = {'post_id': 1,
                 'item': DIC_ITEM_1_ID,
                 'post_datetime': datetime.datetime(2017, 9, 19, 14, 57, 13, 8087).isoformat(),
                 'rating': 4,
                 'review': None,
                 'photos': [],
                 'tags': [DIC_TAG_1_ID, DIC_TAG_2_ID]}
DIC_POST_2_ID = {'post_id': 2,
                 'item': DIC_ITEM_2_ID,
                 'post_datetime': datetime.datetime(2017, 9, 19, 14, 57, 13, 8492).isoformat(),
                 'rating': 3,
                 'review': None,
                 'photos': [],
                 'tags': [DIC_TAG_3_ID, DIC_TAG_2_ID]}
DIC_POST_3_ID = {'post_id': 3,
                 'item': DIC_ITEM_1_ID,
                 'post_datetime': datetime.datetime(2017, 9, 19, 19, 57, 13, 8685).isoformat(),
                 'rating': 4,
                 'review': None,
                 'photos': [DIC_PHOTO_1_ID],
                 'tags': [DIC_TAG_2_ID]}
DIC_POST_4_ID = {'post_id': 4,
                 'item': DIC_ITEM_2_ID,
                 'post_datetime': datetime.datetime(2017, 9, 20, 19, 0, 1).isoformat(),
                 'rating': 3,
                 'review': None,
                 'photos': [],
                 'tags': [DIC_TAG_2_ID, DIC_TAG_3_ID, DIC_TAG_1_ID]}
DIC_POST_5_ID = {'post_id': 5,
                 'item': DIC_ITEM_1_ID,
                 'post_datetime': datetime.datetime(2017, 9, 20, 19, 0, 2).isoformat(),
                 'rating': 2,
                 'review': None,
                 'photos': [],
                 'tags': [DIC_TAG_3_ID]}
DIC_POST_6_ID = {'post_id': 6,
                 'item': DIC_ITEM_1_ID,
                 'post_datetime': datetime.datetime(2017, 9, 20, 19, 0, 3).isoformat(),
                 'rating': 5,
                 'review': None,
                 'photos': [],
                 'tags': [DIC_TAG_2_ID, DIC_TAG_3_ID]}

DIC_POST_1 = make_public(DIC_POST_1_ID)
DIC_POST_1['tags'] = [DIC_TAG_1, DIC_TAG_2]
DIC_POST_1['item'] = DIC_ITEM_1
DIC_POST_2 = make_public(DIC_POST_2_ID)
DIC_POST_2['tags'] = [DIC_TAG_3, DIC_TAG_2]
DIC_POST_2['item'] = DIC_ITEM_2
DIC_POST_3 = make_public(DIC_POST_3_ID)
DIC_POST_3['tags'] = [DIC_TAG_2]
DIC_POST_3['item'] = DIC_ITEM_1
DIC_POST_3['photos'] = [DIC_PHOTO_1]
DIC_POST_4 = make_public(DIC_POST_4_ID)
DIC_POST_4['tags'] = [DIC_TAG_2, DIC_TAG_3, DIC_TAG_1]
DIC_POST_4['item'] = DIC_ITEM_2
DIC_POST_5 = make_public(DIC_POST_5_ID)
DIC_POST_5['tags'] = [DIC_TAG_3]
DIC_POST_5['item'] = DIC_ITEM_1
DIC_POST_6 = make_public(DIC_POST_6_ID)
DIC_POST_6['tags'] = [DIC_TAG_2, DIC_TAG_3]
DIC_POST_6['item'] = DIC_ITEM_1

DIC_POST_4_FULL = {'post_id': 4,
                   'item': DIC_ITEM_2_ID,
                   'post_datetime': datetime.datetime(2017, 9, 20, 19, 0, 1).isoformat(),
                   'rating': 3,
                   'review': None,
                   'photos': [],
                   'tags': [DIC_TAG_2_ID, DIC_TAG_3_ID, DIC_TAG_1_ID],
                   'is_interested': False,
                   'is_favorite': False,
                   'liked_by': [],
                   'comments': []}
DIC_USER_3 = {'user_id': 3,
              'status': 'active',
              'account_creation_date': u'2017-09-19',
              'posts': [DIC_POST_4_FULL],
              'comments': [],
              'likes': [DIC_POST_1_ID, DIC_POST_3_ID]}

def find_dic_diff(dic1, dic2):
    keys = set(dic1.keys()+dic2.keys())
    for key in keys:
        if key not in dic1:
            print 'Missing key in dic1: {}'.format(key)
            return
        elif key not in dic2:
            print 'Missing key in dic2: {}'.format(key)
            return
        else:
            if dic1[key] != dic2[key]:
                print 'Different values for key `{}`:'.format(key)
                print dic1[key]
                print dic2[key]
                return
    print 'They are equal'

class TestGet(unittest.TestCase):

    def test_get_category(self):
        url = ROOT+u'categories/1/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {u'category': {u'items': [],
                                             u'uri': url,
                                             u'category_name': u'Place'}})

    def test_get_nonexisting_category(self):
        url = ROOT+u'categories/3743/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

    def test_get_categories(self):
        url = ROOT+u'categories/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        cats = res.json()['categories']
        self.assertEqual(cats[:5], [{u'uri': url+'8/',
                                     u'category_name': u'Animals'},
                                    {u'uri': url+'9/',
                                     u'category_name': u'Animals\\Cats'},
                                    {u'uri': url+'1/',
                                     u'category_name': u'Place'},
                                    {u'uri': url+'2/',
                                     u'category_name': u'Place\\Business'},
                                    {u'uri': url+'3/',
                                     u'category_name': u'Place\\Business\\Hotel'}])

    def test_get_tag(self):
        url = ROOT+u'tags/1/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        shouldbe = {'tag': DIC_TAG_1.copy()}
        shouldbe['tag']['posts'] = [DIC_POST_1, DIC_POST_4]
        self.assertEqual(res.json(), shouldbe)

    def test_get_nonexisting_tag(self):
        url = ROOT+u'tags/3743/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

    def test_get_tags(self):
        url = ROOT+u'tags/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        tags = res.json()['tags']
        self.assertEqual(tags[:3], [DIC_TAG_2, DIC_TAG_3, DIC_TAG_1])

    def test_get_item(self):
        url = ROOT+u'items/3/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        shouldbe = {"item": DIC_ITEM_3.copy()}
        shouldbe['item']['posts'] = []
        self.assertEqual(res.json(), shouldbe)

    def test_get_nonexisting_item(self):
        url = ROOT+u'items/3743/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

    def test_get_items(self):
        url = ROOT+u'items/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        shouldbe = [DIC_ITEM_3, DIC_ITEM_4, DIC_ITEM_2]
        self.assertEqual(res.json()['items'][:3], shouldbe)

    def test_get_post(self):
        url = ROOT+u'posts/1/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        shouldbe = {"post": DIC_POST_1}
        self.assertEqual(res.json(), shouldbe)

    def test_get_nonexisting_post(self):
        url = ROOT+u'posts/3743/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

    def test_get_posts(self):
        url = ROOT+u'posts/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        shouldbe = {'posts': [DIC_POST_6, DIC_POST_5, DIC_POST_4, DIC_POST_3,
                              DIC_POST_2, DIC_POST_1]}
        self.assertEqual(res.json()['posts'][-6:], shouldbe['posts'])

    def test_get_user(self):
        url = ROOT+u'users/3/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        shouldbe = {"user": DIC_USER_3}
        self.assertEqual(res.json(), shouldbe)

    def test_get_nonexisting_user(self):
        url = ROOT+u'users/3743/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

class TestPost(unittest.TestCase):

    def test_post_category_no_data(self):
        url = ROOT+u'categories/'
        data = {}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_category_wrong_data(self):
        url = ROOT+u'categories/'
        data = {'category_name': "ZZZ Category " + DATE}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_category_missing_arg(self):
        url = ROOT+u'categories/'
        data = {'category': {'name': "ZZZ Category " + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_category_too_many_args(self):
        url = ROOT+u'categories/'
        data = {'category': {'category_name': "ZZZ Category " + DATE,
                             'parent_id': 9,
                             'other_arg': 3}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_category_no_parent(self):
        url = ROOT+u'categories/'
        data = {'category': {'category_name': "Test API Category " + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_category(self):
        url = ROOT+u'categories/'
        data = {'category': {'category_name': "Test API Category " + DATE,
                             'parent_id': 1}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_tag_no_data(self):
        url = ROOT+u'tags/'
        data = {}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_tag_wrong_data(self):
        url = ROOT+u'tags/'
        data = {'category_name': "Test API Tag " + DATE}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_tag_missing_arg(self):
        url = ROOT+u'tags/'
        data = {'tag': {'name': "Test API Tag " + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_tag_too_many_args(self):
        url = ROOT+u'tags/'
        data = {'tag': {'tag_name': "Test API Tag " + DATE,
                        'other_arg': 3}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_tag(self):
        url = ROOT+u'tags/'
        DATE = datetime.datetime.now().isoformat()
        data = {'tag': {'tag_name': "Test API Tag " + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        # Tags should be unique and cannot be created twice
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

        DATE = datetime.datetime.now().isoformat()
        data = {'tag': {'tag_name': "Test API Tag " + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_photo_no_data(self):
        url = ROOT+u'photos/'
        data = {}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_photo_wrong_data(self):
        url = ROOT+u'photos/'
        data = {'category_name': "Test API Photo " + DATE}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_photo_missing_arg(self):
        url = ROOT+u'photos/'
        data = {'photo': {'name': "Test API Tag " + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_photo_too_many_args(self):
        url = ROOT+u'photos/'
        data = {'photo': {'file_name': "Test API Tag " + DATE,
                          'other_arg': 3}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_photo(self):
        url = ROOT+u'photos/'
        data = {'photo': {'file_name': "Test API Tag " + DATE,
                          'post_id': 1}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_comment_no_data(self):
        url = ROOT+u'comments/'
        data = {}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_comment_wrong_data(self):
        url = ROOT+u'comments/'
        data = {'category_name': "Test API Photo " + DATE}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_comment_missing_arg(self):
        url = ROOT+u'comments/'
        data = {'comment': {'comment': "Test API Tag " + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_comment_too_many_args(self):
        url = ROOT+u'comments/'
        data = {'comment': {'comment': "Test API Tag " + DATE,
                            'user_id': 2,
                            'post_id': 5,
                            'other_arg': 3}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_comment(self):
        url = ROOT+u'comments/'
        data = {'comment': {'comment': "Test API Tag " + DATE,
                            'user_id': 2,
                            'post_id': 5}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_like_no_data(self):
        url = ROOT+u'likes/'
        data = {}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_like_wrong_data(self):
        url = ROOT+u'likes/'
        data = {'category_name': "Test API Photo " + DATE}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_like_missing_arg(self):
        url = ROOT+u'likes/'
        data = {'like': {'post_id': 5}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_like_too_many_args(self):
        url = ROOT+u'likes/'
        data = {'like': {'user_id': 2,
                         'post_id': 5,
                         'other_arg': 3}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_location_no_data(self):
        url = ROOT+u'locations/'
        data = {}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_location_wrong_data(self):
        url = ROOT+u'locations/'
        data = {'lat': random.randrange(-90, 90)}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_location_missing_arg(self):
        url = ROOT+u'locations/'
        data = {'location': {'lat': random.randrange(-90, 90)}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_location_too_many_args(self):
        url = ROOT+u'locations/'
        data = {'location': {'lat': random.randrange(-90, 90),
                             'lon': random.randrange(-180, 180),
                             'country': 'BEL'}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_location(self):
        url = ROOT+u'locations/'
        data = {'location': {'lat': random.randrange(-90, 90),
                             'lon': random.randrange(-180, 180),
                             'address': 'Test API Adress'}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_item_no_data(self):
        url = ROOT+u'items/'
        data = {}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_item_wrong_data(self):
        url = ROOT+u'items/'
        data = {'item': 'blah'}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_item_missing_arg(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_item_too_many_args(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {},
                         'blah': 'blah'}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_item_missing_category_arg(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'id': 5}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_item_wrong_category_type(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': 5}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_item_category_id(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_id': 5}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_item_category_name(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_name': 'Test API Category '
                                      + DATE}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_item_category_id_wrong_location(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_id': 5},
                         'location': 1}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 400)

    def test_post_item_category_id_location_id(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_id': 5},
                         'location': {'location_id': 1}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_item_category_name_location_id(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_name': 'Test API Category '
                                      + DATE},
                         'location': {'location_id': 1}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_item_category_id_location(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_id': 5},
                         'location': {'lat': random.randrange(-90, 90),
                                      'lon': random.randrange(-180, 180),
                                      'address': 'Test API Adress'}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_item_category_name_location_(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_name': 'Test API Category '
                                      + DATE},
                         'location': {'lat': random.randrange(-90, 90),
                                      'lon': random.randrange(-180, 180),
                                      'address': 'Test API Adress'}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_post_1(self):
        url = ROOT+u'posts/'
        post = dict(item={'item_id': 1}, user_id=1, review="Test")
        data = dict(post=post)
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_post_2(self):
        url = ROOT+u'posts/'
        post = dict(item={'item_name': 'Test queries.py',
                          'category': {'category_id': 3}}, user_id=1)
        data = dict(post=post)
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_post_3(self):
        url = ROOT+u'posts/'
        post = dict(item={'item_id': 4}, user_id=1, is_favorite=True,
                    is_interested=True, review="Test - Was awesome")
        data = dict(post=post)
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_post_with_photos(self):
        url = ROOT+u'posts/'
        post = dict(item={'item_id': 4}, user_id=1, is_favorite=True,
                    is_interested=True, review="Test - Was Awesome",
                    photos=['Test Photo2 '+DATE, {'photo_id': 2},
                            {'file_name': 'Test Photo3 '+DATE}])
        data = dict(post=post)
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

    def test_post_post_with_tags(self):
        url = ROOT+u'posts/'
        post = dict(item={'item_id': 4}, user_id=1, is_favorite=True,
                    is_interested=True, review="Test - Was Awesome",
                    tags=['Test PostTag3 '+DATE, {'tag_id': 4},
                          {'tag_name': 'Test PostTag '+DATE},
                          {'tag_name': 'Test PostTag4 '+DATE}])
        data = dict(post=post)
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

class TestDelete(unittest.TestCase):

    def test_delete_tag(self):
        url = ROOT+u'tags/'
        data = {'tag': {'tag_name': 'Test API tag for deletion' + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        obj_id = res.json()['tag']['tag_id']
        url += '{0}/'.format(obj_id)
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)

        res = requests.delete(url)
        self.assertEqual(res.status_code, 400)

    def test_delete_category(self):
        url = ROOT+u'categories/'
        data = {'category': {'category_name':
                             'Test API category for deletion' + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        obj_id = res.json()['category']['category_id']
        url += '{0}/'.format(obj_id)
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)

        res = requests.delete(url)
        self.assertEqual(res.status_code, 400)

    def test_delete_location(self):
        url = ROOT+u'locations/'
        data = {'location': {'lat': 3, 'lon': 4,
                             'address': 'Test location for deletion' + DATE}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        obj_id = res.json()['location']['location_id']
        url += '{0}/'.format(obj_id)
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)

        res = requests.delete(url)
        self.assertEqual(res.status_code, 400)

    def test_delete_photo(self):
        url = ROOT+u'photos/'
        data = {'photo': {'file_name': "Test API Tag " + DATE,
                          'post_id': 1}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        obj_id = res.json()['photo']['photo_id']
        url += '{0}/'.format(obj_id)
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)

        res = requests.delete(url)
        self.assertEqual(res.status_code, 400)

    def test_delete_comment(self):
        url = ROOT+u'comments/'
        data = {'comment': {'comment': "Test API Tag " + DATE,
                            'user_id': 2,
                            'post_id': 5}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        obj_id = res.json()['comment']['comment_id']
        url += '{0}/'.format(obj_id)
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)

        res = requests.delete(url)
        self.assertEqual(res.status_code, 400)

    def test_delete_like(self):
        url = ROOT+u'likes/'
        data = {'like': {'user_id': 2, 'post_id': 5}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        post_id = res.json()['like']['post_id']
        user_id = res.json()['like']['user_id']
        url += '{0}/{1}/'.format(post_id, user_id)
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)

        res = requests.delete(url)
        self.assertEqual(res.status_code, 400)

    def test_delete_item(self):
        url = ROOT+u'items/'
        data = {'item': {'item_name': 'Test API Item '+DATE,
                         'category': {'category_id': 5},
                         'location': {'location_id': 1}}}
        res = requests.post(url, json=data)
        self.assertEqual(res.status_code, 201)

        obj_id = res.json()['item']['item_id']
        url += '{0}/'.format(obj_id)
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)

        res = requests.delete(url)
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
