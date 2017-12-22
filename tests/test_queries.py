#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for glob.queries
'''
import datetime
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'glob'))

import queries

db = queries.DataBase(path='../glob')

DATETIME = datetime.datetime.now().isoformat()

DIC_CAT_1 = {'items': [],
             'category_id': 1,
             'category_name': 'Place'}

DIC_PHOTO_1 = {'file_name': u'some_photo.jpg',
               'photo_id': 1}

DIC_LOC_1 = {'lat': 37.7749,
             'lon': -122.4194,
             'address': 'San Francisco, CA, USA',
             'location_id': 1}

DIC_TAG_1 = {'tag_id': 1,
             'tag_name': u'cool',
             'number_of_posts': 2}
DIC_TAG_2 = {'tag_id': 2,
             'tag_name': u'awesome',
             'number_of_posts': 5}
DIC_TAG_3 = {'tag_id': 3,
             'tag_name': u'bof',
             'number_of_posts': 4}

DIC_ITEM_1 = {'item_id': 1,
              'category': u'Sport\\Hike',
              'item_name': u'Some trail',
              'location': DIC_LOC_1,
              'rating': 3.75}

DIC_ITEM_2 = {'item_id': 2,
              'category': u'Place\\Business\\Hotel',
              'item_name': u'Hotel California',
              'location': {},
              'rating': 3}

DIC_POST_1 = {'post_id': 1,
              'item': DIC_ITEM_1,
              'post_datetime': datetime.datetime(2017, 9, 19, 14, 57, 13, 8087).isoformat(),
              'rating': 4,
              'review': None,
              'photos': [],
              'tags': [DIC_TAG_1, DIC_TAG_2]}
DIC_POST_2 = {'post_id': 2,
              'item': DIC_ITEM_2,
              'post_datetime': datetime.datetime(2017, 9, 19, 14, 57, 13, 8492).isoformat(),
              'rating': 3,
              'review': None,
              'photos': [],
              'tags': [DIC_TAG_3, DIC_TAG_2]}
DIC_POST_3 = {'post_id': 3,
              'item': DIC_ITEM_1,
              'post_datetime': datetime.datetime(2017, 9, 19, 19, 57, 13, 8685).isoformat(),
              'rating': 4,
              'review': None,
              'photos': [DIC_PHOTO_1],
              'tags': [DIC_TAG_2]}
DIC_POST_4 = {'post_id': 4,
              'item': DIC_ITEM_2,
              'post_datetime': datetime.datetime(2017, 9, 20, 19, 0, 1).isoformat(),
              'rating': 3,
              'review': None,
              'photos': [],
              'tags': [DIC_TAG_2, DIC_TAG_3, DIC_TAG_1]}
DIC_POST_5 = {'post_id': 5,
              'item': DIC_ITEM_1,
              'post_datetime': datetime.datetime(2017, 9, 20, 19, 0, 2).isoformat(),
              'rating': 2,
              'review': None,
              'photos': [],
              'tags': [DIC_TAG_3]}
DIC_POST_6 = {'post_id': 6,
              'item': DIC_ITEM_1,
              'post_datetime': datetime.datetime(2017, 9, 20, 19, 0, 3).isoformat(),
              'rating': 5,
              'review': None,
              'photos': [],
              'tags': [DIC_TAG_2, DIC_TAG_3]}

class TestGetCategory(unittest.TestCase):

    def test_get_category(self):
        cat = db.get_category(1)
        self.assertEqual(cat, DIC_CAT_1)

class TestGetPhoto(unittest.TestCase):

    def test_get_photo(self):
        photo = db.get_photo(1, return_object=False)
        self.assertEqual(photo, DIC_PHOTO_1)

class TestGetPost(unittest.TestCase):

    def test_get_recent_posts(self):
        posts = db.get_recent_posts(n_posts=300)[-6:-3]
        shouldbe = [DIC_POST_6, DIC_POST_5, DIC_POST_4]
        self.assertEqual(posts, shouldbe)


class TestGetTag(unittest.TestCase):

    def test_get_all_tags(self):
        tags = db.get_all_tags()
        self.assertEqual(tags[:3],
            [DIC_TAG_2, DIC_TAG_3, DIC_TAG_1])

    def test_get_popular_tags(self):
        tags = db.get_popular_tags(n_tags=2)
        self.assertEqual(tags, [DIC_TAG_2, DIC_TAG_3])

    def test_get_popular_tags_string_input(self):
        tags = db.get_popular_tags(n_tags="2")
        self.assertEqual(tags, [DIC_TAG_2, DIC_TAG_3])

    def test_get_popular_tags_wrong_string_input(self):
        with self.assertRaises(ValueError):
            tags = db.get_popular_tags(n_tags="2 or 1 = 1")

    def test_get_trendy_tags(self):
        post_dt = datetime.datetime(2017, 9, 20, 19, 0)
        td = datetime.datetime.utcnow() - post_dt + datetime.timedelta(hours=1)
        tags = db.get_trendy_tags(timediff=td, n_tags=2)
        self.assertEqual(tags, [{'number_of_posts': 3,
                                 'tag_name': u'bof'},
                                {'number_of_posts': 2,
                                 'tag_name': u'awesome'}])

    def test_get_trendy_tags_string_input(self):
        with self.assertRaises(TypeError):
            tags = db.get_popular_tags(timediff="2")

    def test_get_trendy_tags_number_input(self):
        with self.assertRaises(TypeError):
            tags = db.get_popular_tags(timediff=2)

    def test_get_popular_tags_wrong_string_input(self):
        with self.assertRaises(ValueError):
            tags = db.get_popular_tags(n_tags="2 or 1 = 1")

class TestSearch(unittest.TestCase):

    def test_get_trendy_invalid_input_type(self):
        with self.assertRaises(TypeError):
            posts = db.search_tags(5)
        with self.assertRaises(TypeError):
            posts = db.search_tags([5])
        with self.assertRaises(TypeError):
            posts = db.search_tags(["5"])
        with self.assertRaises(TypeError):
            posts = db.search_tags({"5": 5})

    def test_get_trendy_invalid_input_value(self):
        with self.assertRaises(ValueError):
            posts = db.search_tags("5 or 1 = 1")
        with self.assertRaises(ValueError):
            posts = db.search_tags("5 or 1=1")
        with self.assertRaises(ValueError):
            posts = db.search_tags("5; SELECT blah FROM blih")
        with self.assertRaises(ValueError):
            posts = db.search_tags("SELECT * FROM blih")
        posts = db.search_tags("SELECT Blah FROM blih")
        self.assertEqual(posts, [])

    def test_search_tag(self):
        self.assertEqual(db.search_tags("bof"),
                         [DIC_POST_6, DIC_POST_5, DIC_POST_4, DIC_POST_2])
        self.assertEqual(db.search_tags("cool"),
                         [DIC_POST_4, DIC_POST_1])
        self.assertEqual(db.search_tags("awesome"),
                         [DIC_POST_6, DIC_POST_4, DIC_POST_3, DIC_POST_2,
                          DIC_POST_1])

    def test_search_not_present(self):
        self.assertEqual(db.search_tags("of"),
                         [])
        self.assertEqual(db.search_tags("coo"),
                         [])
        self.assertEqual(db.search_tags("awesom"),
                         [])

    def test_search_2tags(self):
        self.assertEqual(db.search_tags("bof awesome"),
                         [DIC_POST_6, DIC_POST_4, DIC_POST_2])
        self.assertEqual(db.search_tags("cool awesome"),
                         [DIC_POST_4, DIC_POST_1])
        self.assertEqual(db.search_tags("bof cool"),
                         [DIC_POST_4])

    def test_search_3tags(self):
        self.assertEqual(db.search_tags("bof cool awesome"),
                         [DIC_POST_4])

class TestPosting(unittest.TestCase):

    def test_create_photo_string(self):
        with self.assertRaises(TypeError):
            db.create_photo("some tag name")

    def test_create_photo_wrong_kw(self):
        with self.assertRaises(TypeError):
            db.create_photo(name='some tag name')

    def test_create_photo_2_kw(self):
        with self.assertRaises(TypeError):
            db.create_photo(file_name="Blah", name='some tag name')

    def test_create_photo(self):
        photo = db.create_photo(file_name="Blah", commit=False)
        self.assertEqual(photo, {'file_name': 'Blah',
                                 'photo_id': None})

    def test_create_comment_string(self):
        with self.assertRaises(TypeError):
            db.create_comment("some tag name")

    def test_create_comment_missing_kw(self):
        with self.assertRaises(TypeError):
            db.create_comment(comment='some tag name')

    def test_create_comment_missing_kw_2(self):
        with self.assertRaises(TypeError):
            db.create_comment(comment='some tag name', post_id=3)

    def test_create_comment_post_user_id(self):
        post = db.create_post(item_id=4, user_id=1,
                              review="Test - Was awesome",
                              return_object=True)
        comment = db.create_comment(comment="Test", post=post, user_id=2)
        comment.pop('datetime')
        self.assertEqual(comment, {'comment': 'Test',
                                   'comment_id': comment['comment_id'],
                                   'post_id': post.post_id,
                                   'user_id': 2})

    def test_create_comment_post_id_user_id(self):
        comment = db.create_comment(comment="Test", post_id=2, user_id=2,
                                    commit=False)
        comment.pop('datetime')
        self.assertEqual(comment, {'comment': 'Test',
                                   'comment_id': None,
                                   'post_id': 2,
                                   'user_id': 2})

    def test_create_like_string(self):
        with self.assertRaises(TypeError):
            db.create_like("some tag name")

    def test_create_like_missing_kw(self):
        with self.assertRaises(TypeError):
            db.create_like(post_id='some tag name')

    def test_create_like_post(self):
        post = db.create_post(item_id=4, user_id=1,
                              review="Test - Was awesome",
                              return_object=True)
        like = db.create_like(post=post, user_id=2)
        self.assertEqual(like, {'post_id': post.post_id,
                                'user_id': 2})

    def test_create_like_post_id_user_id(self):
        post = db.create_post(item_id=4, user_id=1,
                              review="Test - Was awesome",
                              return_object=True)
        like = db.create_like(post_id=post.post_id, user_id=2)
        self.assertEqual(like, {'post_id': post.post_id,
                                'user_id': 2})

    def test_create_tag_string(self):
        with self.assertRaises(TypeError):
            db.create_tag("some tag name")

    def test_create_tag_wrong_kw(self):
        with self.assertRaises(TypeError):
            db.create_tag(name='some tag name')

    def test_create_tag_2_kw(self):
        with self.assertRaises(TypeError):
            db.create_tag(tag_name="Blah", name='some tag name')

    def test_create_tag(self):
        tag = db.create_tag(tag_name="Blah", commit=False)
        self.assertEqual(tag, {'tag_name': 'blah', 'number_of_posts': 0,
                               'tag_id': None})

    def test_create_cat_string(self):
        with self.assertRaises(TypeError):
            db.create_category("some category name")

    def test_create_cat_wrong_kw(self):
        with self.assertRaises(TypeError):
            db.create_category(name='some category name')

    def test_create_cat_1right1wrong_kw(self):
        with self.assertRaises(TypeError):
            db.create_category(category_name='some category name', parent=3)

    def test_create_cat(self):
        cat = db.create_category(category_name='some category name',
                                 parent_id=3, commit=False)
        self.assertEqual(cat, {'category_id': None,
                               'category_name': 'some category name'})

    def test_create_cat2(self):
        cat = db.create_category(category_name='some category name',
                                 parent_id=None, commit=False)
        self.assertEqual(cat, {'category_id': None,
                               'category_name': 'some category name'})

    def test_create_cat_obj(self):
        cat = db.create_category(category_name='some category name',
                                 parent_id=None, commit=False,
                                 return_object=True)
        self.assertEqual(cat.category_name, 'some category name')
        self.assertEqual(cat.category_id, None)
        self.assertEqual(cat.parent_id, None)

    def test_create_loc_wrong_kw(self):
        with self.assertRaises(TypeError):
            db.create_location(name='some name')

    def test_create_loc_missing_kw(self):
        with self.assertRaises(TypeError):
            db.create_location(lat=50.6326)

    def test_create_loc_too_many_kw(self):
        with self.assertRaises(TypeError):
            db.create_location(lat=50.6326, lon=5.5797, blah=56)

    def test_create_loc(self):
        loc = db.create_location(lat=50.6326, lon=5.5797, commit=False)
        self.assertEqual(loc, {'lat': 50.6326, 'lon': 5.5797, 'address': None,
                               'location_id': None})

    def test_create_loc2(self):
        loc = db.create_location(lat=50.6326, lon=5.5797,
                                 address=u"Liège, Belgium", commit=False)
        self.assertEqual(loc, {'lat': 50.6326, 'lon': 5.5797,
                               'address': u"Liège, Belgium",
                               'location_id': None})

    def test_create_loc_obj(self):
        loc = db.create_location(lat=50.6326, lon=5.5797,
                                 address=u"Liège, Belgium", commit=False,
                                 return_object=True)
        self.assertEqual(loc.lat, 50.6326)
        self.assertEqual(loc.location_id, None)
        self.assertEqual(loc.lon, 5.5797)
        self.assertEqual(loc.address, u"Liège, Belgium")

    def test_create_item_wrong_kw(self):
        with self.assertRaises(TypeError):
            db.create_item(name='some name')

    def test_create_item_missing_kw(self):
        with self.assertRaises(TypeError):
            db.create_item(item_name='some name')

    def test_create_item_with_category_id(self):
        item = db.create_item(item_name='some name', category_id=3,
                              commit=False, return_object=True)
        self.assertEqual(item.item_name, 'some name')
        self.assertEqual(item.category_id, 3)
        self.assertEqual(item.location_id, None)

    def test_create_item_no_loc_category_id(self):
        item = db.create_item(item_name='some name', category={'category_id': 3},
                              commit=False, return_object=True)
        self.assertEqual(item.item_name, 'some name')
        self.assertEqual(item.category_id, 3)
        self.assertEqual(item.location_id, None)

    def test_create_item_no_loc_category_name(self):
        item = db.create_item(item_name='some name',
                              category={'category_name': 'cats'},
                              commit=False, return_object=True)
        self.assertEqual(item.item_name, 'some name')
        self.assertEqual(item.category.category_name, 'cats')
        self.assertEqual(item.category.category_id, None)
        self.assertEqual(item.category.parent_id, None)
        self.assertEqual(item.location_id, None)

    def test_create_item_loc_id_category_id(self):
        item = db.create_item(item_name='some name',
                              category={'category_id': 3},
                              location={'location_id': 1},
                              commit=False, return_object=True)
        self.assertEqual(item.item_name, 'some name')
        self.assertEqual(item.category_id, 3)
        self.assertEqual(item.location_id, 1)

    def test_create_item_loc_id_category_name(self):
        item = db.create_item(item_name='some name',
                              category={'category_name': 'cats'},
                              location={'location_id': 1},
                              commit=False, return_object=True)
        self.assertEqual(item.item_name, 'some name')
        self.assertEqual(item.category.category_name, 'cats')
        self.assertEqual(item.category.category_id, None)
        self.assertEqual(item.category.parent_id, None)
        self.assertEqual(item.location_id, 1)

    def test_create_item_loc_category_id(self):
        item = db.create_item(item_name='some name',
                              category={'category_id': 3},
                              location={'lat': 1, 'lon': 4},
                              commit=False, return_object=True)
        self.assertEqual(item.item_name, 'some name')
        self.assertEqual(item.category_id, 3)
        self.assertEqual(item.location.location_id, None)
        self.assertEqual(item.location.lat, 1)
        self.assertEqual(item.location.lon, 4)


    def test_create_item_loc_category_name(self):
        item = db.create_item(item_name='some name',
                              category={'category_name': 'cats'},
                              location={'lat': 1, 'lon': 4},
                              commit=False, return_object=True)
        self.assertEqual(item.item_name, 'some name')
        self.assertEqual(item.category.category_name, 'cats')
        self.assertEqual(item.category.category_id, None)
        self.assertEqual(item.category.parent_id, None)
        self.assertEqual(item.location.location_id, None)
        self.assertEqual(item.location.lat, 1)
        self.assertEqual(item.location.lon, 4)

    def test_create_post_wrong_kw(self):
        with self.assertRaises(TypeError):
            db.create_item(name='some name')

    def test_create_post_missing_kw(self):
        with self.assertRaises(TypeError):
            db.create_post(item={'item_id': 1})

    def test_create_post_too_many_kw(self):
        with self.assertRaises(TypeError):
            db.create_post(item={'item_id': 1}, blah=56)

    def test_create_post_1(self):
        db.create_post(item={'item_id': 1}, user_id=1, review="Test")

    def test_create_post_2(self):
        db.create_post(item={'item_name': 'Test queries.py',
                             'category': {'category_id': 3}}, user_id=1)

    def test_create_post_3(self):
        post = db.create_post(item={'item_id': 4}, user_id=1, is_favorite=True,
                              is_interested=True, review="Test - Was awesome",
                              return_object=True)
        self.assertEqual(post.item_id, 4)

    def test_create_post_with_item_id(self):
        post = db.create_post(item_id=4, user_id=1,
                              review="Test - Was awesome",
                              return_object=True)
        self.assertEqual(post.item_id, 4)

    def test_create_post_with_photo(self):
        photo = queries.Photos(file_name="Test Photo "+DATETIME)
        db.create_post(item={'item_id': 4}, user_id=1, is_favorite=True,
                       is_interested=True, review="Test - Was Awesome",
                       photos=photo)

    def test_create_post_with_photos(self):
        photo = queries.Photos(file_name="Test Photo "+DATETIME)
        db.create_post(item={'item_id': 4}, user_id=1, is_favorite=True,
                       is_interested=True, review="Test - Was Awesome",
                       photos=[photo, 'Test Photo2 '+DATETIME,
                               {'photo_id': 2},
                               {'file_name': 'Test Photo3 '+DATETIME}])

    def test_create_post_with_tag(self):
        tag = queries.Tags(tag_name="Test PostTag "+DATETIME)
        db.create_post(item={'item_id': 4}, user_id=1, is_favorite=True,
                       is_interested=True, review="Test - Was Awesome",
                       tags=tag)

    def test_create_post_with_tags(self):
        tag = queries.Tags(tag_name="Test PostTag2 "+DATETIME)
        db.create_post(item={'item_id': 4}, user_id=1, is_favorite=True,
                       is_interested=True, review="Test - Was Awesome",
                       tags=[tag, 'Test PostTag3 '+DATETIME,
                               {'tag_id': 4},
                               {'tag_name': 'Test PostTag '+DATETIME},
                               {'tag_name': 'Test PostTag4 '+DATETIME}])

    def test_create_user_missing_email(self):
        with self.assertRaises(TypeError):
            db.create_user(secondary_login='000',
                           password='123')

    def test_create_user_missing_login(self):
        with self.assertRaises(TypeError):
            db.create_user(email_address='test',
                           password='123')

    def test_create_user_missing_pwd(self):
        with self.assertRaises(TypeError):
            db.create_user(secondary_login='000',
                           email_address='123')

    def test_create_user(self):
        db.create_user(email_address='test', secondary_login='000',
                       password='123')

class TestZDelete(unittest.TestCase):

    def test_delete_category(self):
        obj = db.create_category(category_name='Test for deletion',
                                 return_object=True)
        child1 = db.create_category(category_name='Test for deletion 2',
                                    parent_id=obj.category_id,
                                    return_object=True)
        child2 = db.create_category(category_name='Test for deletion 3',
                                    parent_id=obj.category_id,
                                    return_object=True)
        db.delete_category(obj.category_id)

    def test_delete_location(self):
        obj = db.create_location(lat=3.45, lon=6.78, return_object=True)
        db.delete_location(obj.location_id)

    def test_delete_photo(self):
        obj = db.create_photo(file_name='Blah blah', post_id=1,
                              return_object=True)
        db.delete_photo(obj.photo_id)

    def test_delete_item_dependencies(self):
        loc = db.create_location(lat=3.45, lon=6.78, return_object=True)
        cat = db.create_category(category_name='Test for deletion',
                                 return_object=True)
        item = db.create_item(item_name="Test delete item dependencies",
                              category=cat, location=loc, return_object=True)
        with self.assertRaises(ValueError):
            db.delete_location(loc.location_id)
        with self.assertRaises(queries.IntegrityError):
            db.delete_category(cat.category_id)
        db.delete_item(item.item_id)
        self.assertIsNone(db.get_item(item.item_id))
        db.delete_location(loc.location_id)
        self.assertIsNone(db.get_location(loc.location_id))
        db.delete_category(cat.category_id)
        self.assertIsNone(db.get_category(cat.category_id))

    def test_delete_comment(self):
        obj = db.create_comment(comment="Test", post_id=2, user_id=2,
                                return_object=True)
        db.delete_comment(obj.comment_id)

    def test_delete_like(self):
        obj = db.create_like(post_id=2, user_id=2,
                              return_object=True)
        db.delete_like(obj.post_id, obj.user_id)

    def test_delete_post_dependencies(self):
        loc = db.create_location(lat=3.45, lon=6.78, return_object=True)
        cat = db.create_category(category_name='Test for deletion',
                                 return_object=True)
        item = db.create_item(item_name="Test delete item dependencies",
                              category=cat, location=loc, return_object=True)
        post = db.create_post(item=item, photos=['Photo1', 'Photo2'], rating=2,
                              tags=['tag1_'+DATETIME], user_id=3,
                              return_object=True)
        self.assertEqual(len(post.photos), 2)
        self.assertEqual(len(post.tags), 1)
        db.delete_photo(post.photos[1].photo_id)
        self.assertEqual(len(post.photos), 1)
        db.delete_photo(post.photos[0].photo_id)
        self.assertEqual(len(post.photos), 0)
        db.delete_tag(post.tags[0].tag_id)
        self.assertEqual(len(post.tags), 0)
        with self.assertRaises(queries.IntegrityError):
            db.delete_item(item.item_id)
        db.delete_post(post.post_id)
        self.assertIsNone(db.get_post(post.post_id))
        db.delete_item(item.item_id)
        self.assertIsNone(db.get_item(item.item_id))
        db.delete_location(loc.location_id)
        self.assertIsNone(db.get_location(loc.location_id))
        db.delete_category(cat.category_id)
        self.assertIsNone(db.get_category(cat.category_id))

    def test_delete_post_with_comments_and_likes(self):

        loc = db.create_location(lat=3.45, lon=6.78, return_object=True)
        cat = db.create_category(category_name='Test for deletion',
                                 return_object=True)
        item = db.create_item(item_name="Test delete item dependencies",
                              category=cat, location=loc, return_object=True)
        post = db.create_post(item=item, photos=['Photo1', 'Photo2'], rating=2,
                              tags=['tag1_'+DATETIME], user_id=3,
                              return_object=True)
        comment = db.create_comment(comment="Test", post_id=post.post_id,
                                    user_id=3, return_object=True)
        like = db.create_like(post_id=post.post_id, user_id=2,
                              return_object=True)

        photo1 = post.photos[0].photo_id
        photo2 = post.photos[1].photo_id

        self.assertEqual(len(post.comments), 1)
        self.assertEqual(len(post.liked_by), 1)
        self.assertIsNotNone(db.get_like(post_id=post.post_id, user_id=2))
        db.delete_post(post.post_id)
        self.assertIsNone(db.get_post(post.post_id))
        self.assertIsNone(db.get_comment(comment.comment_id))
        self.assertIsNone(db.get_like(post_id=post.post_id, user_id=2))
        self.assertIsNone(db.get_photo(photo1))
        self.assertIsNone(db.get_photo(photo2))
        db.delete_item(item.item_id)
        db.delete_location(loc.location_id)
        db.delete_category(cat.category_id)

    def test_z_delete_all_tests(self):
        items = (db.session.query(queries.Items)
                   .filter(queries.Items.item_name.ilike('%test%')).all())
        for item in items:
            for post in item.posts:
                db.delete_post(post.post_id)
            db.delete_item(item.item_id)

        photos = (db.session.query(queries.Photos)
                   .filter(queries.Photos.file_name.ilike('%test%')).all())
        for photo in photos:
            db.delete_photo(photo.photo_id)

        comments = (db.session.query(queries.PostComments)
                   .filter(queries.PostComments.comment.ilike('%test%')).all())
        for comment in comments:
            db.delete_comment(comment.comment_id)

        posts = (db.session.query(queries.Posts)
                   .filter(queries.Posts.review.ilike('%test%')).all())
        for post in posts:
            db.delete_post(post.post_id)

        categories = (db.session.query(queries.Categories)
                        .filter(queries.Categories.category_name
                        .ilike('%test%')).all())
        for cat in categories:
            db.delete_category(cat.category_id)

        tags = (db.session.query(queries.Tags)
                        .filter(queries.Tags.tag_name
                        .ilike('%test%')).all())
        for tag in tags:
            db.delete_tag(tag.tag_id)

        locations = (db.session.query(queries.Locations)
                       .filter(queries.Locations.address
                       .ilike('%test%')).all())
        for obj in locations:
            db.delete_location(obj.location_id)

if __name__ == '__main__':
    unittest.main()

