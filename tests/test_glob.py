#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for glob
'''
import sys
import os
import binascii
import datetime
from passlib.hash import pbkdf2_sha256 as pb256

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'glob'))

from dbmodels import *
import unittest

DBFILE = 'sqlalchemy_test.db'

if os.path.exists(DBFILE):
    os.remove(DBFILE)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///'+DBFILE)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# session = Session()

PHOTO = Photos(file_name="Blahblah.jpg")

SF = Locations(lat=37.7749, lon=-122.4194, address="San Francisco, CA, USA")
NYC = Locations(lat=40.7128, lon=-74.0059, address="New York City, NY, USA")

USER_STATUS_ACTIVE = UserStatusTypes(status_name='active')
USER_STATUS_WARNED = UserStatusTypes(status_name='warned')
USER_STATUS_BLOCKED = UserStatusTypes(status_name='blocked')

CAT_PLACE = Categories(category_name="Place")
CAT_BUSINESS = Categories(category_name="Business", parent_id=1)
CAT_HOTEL = Categories(category_name="Hotel", parent_id=2)
CAT_SPORT = Categories(category_name="Sport")
CAT_HIKE = Categories(category_name="Hike", parent_id=4)

IT_LYTRAIL = Items(item_name="Some trail", category=CAT_HIKE, location=SF)

email_address = pb256.hash('joe@mail.com')
secondary_login = pb256.hash('0000000000')
password = pb256.hash('blahblah')
JOE = Users(email_address=email_address,
            secondary_login=secondary_login,
            password=password,
            account_creation_date=datetime.date.today())
JOE.status = USER_STATUS_ACTIVE
email_address = pb256.hash('jane@mail.com')
secondary_login = pb256.hash('0000000000')
password = pb256.hash('blahblah')
JANE = Users(email_address=email_address,
             secondary_login=secondary_login,
             password=password,
             account_creation_date=datetime.date.today(),
             status=USER_STATUS_ACTIVE)
email_address = pb256.hash('jack@mail.com')
secondary_login = pb256.hash('0000000000')
password = pb256.hash('blahblah')
JACK = Users(email_address=email_address,
             secondary_login=secondary_login,
             password=password,
             account_creation_date=datetime.date.today(),
             status=USER_STATUS_ACTIVE)

session = Session()
session.add_all([USER_STATUS_ACTIVE, USER_STATUS_WARNED, USER_STATUS_BLOCKED])
session.add_all([CAT_PLACE, CAT_BUSINESS, CAT_HOTEL, CAT_SPORT, CAT_HIKE])
session.add_all([JOE, JANE, JACK])
session.add_all([SF, NYC])
session.add_all([IT_LYTRAIL])
session.commit()

TAG_COOL = Tags(tag_name="cool")
TAG_AWESOME = Tags(tag_name="awesome")
TAG_BOF = Tags(tag_name="bof")
session.add_all([TAG_COOL, TAG_AWESOME, TAG_BOF])
session.commit()

POST = Posts(post_datetime=datetime.datetime.now(),
             user=JOE,
             item=IT_LYTRAIL,
             rating=4,
             is_interested=True,
             tags=[TAG_COOL, TAG_AWESOME],
             liked_by = [JACK])
POST2 = Posts(post_datetime=datetime.datetime.now(),
              user=JOE,
              item=IT_LYTRAIL,
              rating=3,
              tags=[TAG_BOF])
POST3 = Posts(post_datetime=datetime.datetime.now(),
              user=JANE,
              item=IT_LYTRAIL,
              rating=4,
              tags=[TAG_AWESOME],
              liked_by = [JOE, JACK],
              photos=[PHOTO])

session.add_all([PHOTO, POST, POST2, POST3])
session.commit()

USER_REL_FRIENDS = UserRelationshipTypes(relationship_name='friends')
USER_REL_PENDING_1_2 = UserRelationshipTypes(relationship_name='pending_first_second')


REL1 = UserRelationships(first_user=JANE,
                         second_user=JACK,
                         type=USER_REL_FRIENDS)
REL2 = UserRelationships(first_user=JOE,
                         second_user=JACK,
                         type=USER_REL_FRIENDS)
REL3 = UserRelationships(first_user=JOE,
                         second_user=JANE,
                         type=USER_REL_PENDING_1_2)

session.add_all([USER_REL_FRIENDS, REL1, REL2, REL3])
session.commit()

COMMENT1 = PostComments(comment="That was AWESOME",
                        post=POST,
                        user=JOE,
                        datetime=datetime.datetime.now())

COMMENT2 = PostComments(comment="I didn't like it at all",
                        post=POST,
                        user=JANE,
                        datetime=datetime.datetime.now())

COMMENT3 = PostComments(comment="Meh",
                        post=POST3,
                        user=JOE,
                        datetime=datetime.datetime.now())
session.add_all([COMMENT1, COMMENT2, COMMENT3])
session.commit()

DIC_PHOTO = {'file_name': u'Blahblah.jpg', 'photo_id': 1}

DIC_COMMENT_2 = {'comment': u'I didn\'t like it at all',
                 'post_id': 1,
                 'comment_id': 2,
                 'user_id': 2,
                 'datetime': COMMENT2.datetime.isoformat()}

DIC_COMMENT_3 = {'comment': u'Meh',
                 'post_id': 3,
                 'comment_id': 3,
                 'user_id': 1,
                 'datetime': COMMENT3.datetime.isoformat()}

DIC_TAG_1 = {'tag_id': 1,
             'tag_name': 'cool',
             'number_of_posts': 1}

DIC_TAG_2 = {'tag_id': 2,
             'tag_name': 'awesome',
             'number_of_posts': 2}

DIC_LOCATION = {'lat': 37.7749,
                'lon': -122.4194,
                'address': u'San Francisco, CA, USA',
                'location_id': 1}

DIC_ITEM_1 = {'item_id': 1,
              'item_name': 'Some trail',
              'location': DIC_LOCATION,
              'category': u'Sport\\Hike',
              'rating': 3.6666666666666665}

DIC_POST_3 = {'rating': 4,
              'photos': [DIC_PHOTO],
              'review': None,
              'tags': [DIC_TAG_2],
              'post_id': 3,
              'post_datetime': POST3.post_datetime.isoformat()}

DIC_POST_1_ITEM = {'rating': 4,
                   'photos': [],
                   'review': None,
                   'tags': [DIC_TAG_1, DIC_TAG_2],
                   'post_id': 1,
                   'post_datetime': POST.post_datetime.isoformat(),
                   'item': DIC_ITEM_1}

DIC_POST_3_ITEM = {'rating': 4,
                   'photos': [DIC_PHOTO],
                   'review': None,
                   'tags': [DIC_TAG_2],
                   'post_id': 3,
                   'post_datetime': POST3.post_datetime.isoformat(),
                   'item': DIC_ITEM_1}

DIC_POST_3_ALL = {'rating': 4,
                  'is_interested': False,
                  'liked_by': [1, 3],
                  'photos': [DIC_PHOTO],
                  'review': None,
                  'tags': [DIC_TAG_2],
                  'comments': [DIC_COMMENT_3],
                  'post_id': 3,
                  'is_favorite': False,
                  'post_datetime': POST3.post_datetime.isoformat(),
                  'item': DIC_ITEM_1}

DIC_USER_3_NOFRIENDS = {'user_id': 3,
                        'status': 'active',
                        'likes': [DIC_POST_1_ITEM, DIC_POST_3_ITEM],
                        'comments': [],
                        'posts': [],
                        'account_creation_date': JACK.account_creation_date.isoformat()}

DIC_USER_2 = {'user_id': 2,
              'status': 'active',
              'likes': [],
              'comments': [DIC_COMMENT_2],
              'posts': [DIC_POST_3_ALL],
              'friends': [DIC_USER_3_NOFRIENDS],
              'account_creation_date': JANE.account_creation_date.isoformat()}

class TestUser(unittest.TestCase):

    def setUp(self):
        self.session = Session()
#         self.session.add_all([USER_STATUS_ACTIVE,
#                               USER_STATUS_WARNED,
#                               USER_STATUS_BLOCKED])

    def test_status(self):
        self.assertEqual(JOE.status_id, USER_STATUS_ACTIVE.status_id)

    def test_missing_email(self):
        email_address = pb256.hash('joe@mail.com')
        secondary_login = pb256.hash('0000000000')
        password = pb256.hash('blahblah')
        jane = Users(secondary_login=secondary_login,
                     password=password,
                     account_creation_date=datetime.date.today())
        self.session.add(jane)
        with self.assertRaises(IntegrityError):
            self.session.commit()

    def test_missing_password(self):
        email_address = pb256.hash('joe@mail.com')
        secondary_login = pb256.hash('0000000000')
        password = pb256.hash('blahblah')
        jane = Users(secondary_login=secondary_login,
                     email_address=email_address,
                     account_creation_date=datetime.date.today())
        self.session.add(jane)
        with self.assertRaises(IntegrityError):
            self.session.commit()

    def test_wrong_email(self):
        email_address = pb256.hash('joe@mail.com')
        secondary_login = pb256.hash('0000000000')
        password = pb256.hash('blahblah')
        with self.assertRaises(AssertionError):
            jane = Users(email_address=email_address+'@',
                         password=password,
                         account_creation_date=datetime.date.today())

    def test_wrong_password(self):
        email_address = pb256.hash('joe@mail.com')
        secondary_login = pb256.hash('0000000000')
        password = pb256.hash('blahblah')
        with self.assertRaises(AssertionError):
            jane = Users(email_address=email_address,
                         password=password+'@',
                         account_creation_date=datetime.date.today())

    def tearDown(self):
        self.session.close()


class TestCategories(unittest.TestCase):

    def test_direct_parent(self):
        self.assertEqual(CAT_HOTEL.parent, CAT_BUSINESS)

    def test_grand_parent(self):
        self.assertEqual(CAT_HOTEL.parent.parent, CAT_PLACE)

    def test_none_parent(self):
        self.assertIsNone(CAT_PLACE.parent)

    def test_complete_string(self):
        self.assertEqual(CAT_HOTEL.complete_string, 'Place\\Business\\Hotel')


class TestTags(unittest.TestCase):

    def test_uppercase_tag(self):
        tag = Tags(tag_name="Tag")
        self.assertEqual(tag.tag_name, 'tag')

    def test_number_of_posts(self):
        self.assertEqual(TAG_COOL.number_of_posts, 1)
        self.assertEqual(TAG_AWESOME.number_of_posts, 2)
        self.assertEqual(TAG_BOF.number_of_posts, 1)

class TestItems(unittest.TestCase):

    def test_category(self):
        self.assertEqual(IT_LYTRAIL.category.complete_string, 'Sport\\Hike')

    def test_empty_location(self):
        self.assertEqual(IT_LYTRAIL.location, SF)

    def test_posts(self):
        self.assertEqual(IT_LYTRAIL.posts, [POST, POST2, POST3])

    def test_rating(self):
        self.assertEqual(IT_LYTRAIL.rating, 11./3.)


class TestPost(unittest.TestCase):

    def test_category(self):
        self.assertEqual(POST.item.category.complete_string, 'Sport\\Hike')

    def test_user(self):
        self.assertEqual(POST.user, JOE)

    def test_user_posts(self):
        self.assertEqual(JOE.posts, [POST, POST2])

    def test_tags(self):
        self.assertEqual(POST.tags, [TAG_COOL, TAG_AWESOME])
        self.assertEqual(POST2.tags, [TAG_BOF])
        self.assertEqual(TAG_COOL.posts, [POST])
        self.assertEqual(len(TAG_AWESOME.posts), 2)
        self.assertIn(POST, TAG_AWESOME.posts)
        self.assertIn(POST3, TAG_AWESOME.posts)
        self.assertEqual(TAG_BOF.posts, [POST2])


class TestRelationship(unittest.TestCase):

    def test_friends_from(self):
        self.assertEqual(JOE.friends_from, [JACK])
        self.assertEqual(JANE.friends_from, [JACK])
        self.assertEqual(JACK.friends_from, [])

    def test_friends_to(self):
        self.assertEqual(JOE.friends_to, [])
        self.assertEqual(JANE.friends_to, [])
        self.assertEqual(JACK.friends_to, [JANE, JOE])

    def test_friends(self):
        self.assertEqual(JOE.friends, [JACK])
        self.assertEqual(JANE.friends, [JACK])
        self.assertEqual(JACK.friends, [JANE, JOE])

    def test_likes(self):
        self.assertEqual(JOE.likes, [POST3])
        self.assertEqual(JANE.likes, [])
        self.assertEqual(JACK.likes, [POST, POST3])

class TestComments(unittest.TestCase):

    def test_posts(self):
        self.assertEqual(POST.comments, [COMMENT1, COMMENT2])
        self.assertEqual(POST2.comments, [])
        self.assertEqual(POST3.comments, [COMMENT3])

    def test_users(self):
        self.assertEqual(JOE.comments, [COMMENT1, COMMENT3])
        self.assertEqual(JANE.comments, [COMMENT2])
        self.assertEqual(JACK.comments, [])

class GeneralTests(unittest.TestCase):

    def test_item(self):
        self.assertEqual(IT_LYTRAIL.item_name, 'Some trail')
        self.assertEqual(IT_LYTRAIL.category, CAT_HIKE)
        self.assertEqual(IT_LYTRAIL.category.complete_string, 'Sport\\Hike')
        self.assertEqual(IT_LYTRAIL.posts, [POST, POST2, POST3])
        self.assertEqual(IT_LYTRAIL.rating, 11./3.)
        self.assertEqual(IT_LYTRAIL.location.lat, 37.7749)
        self.assertEqual(IT_LYTRAIL.location.lon, -122.4194)
        self.assertEqual(IT_LYTRAIL.location.address, 'San Francisco, CA, USA')

    def test_tags(self):
        self.assertEqual(TAG_COOL.tag_name, 'cool')
        self.assertEqual(TAG_AWESOME.tag_name, 'awesome')
        self.assertEqual(TAG_BOF.tag_name, 'bof')
        self.assertEqual(TAG_COOL.number_of_posts, 1)
        self.assertEqual(TAG_COOL.posts, [POST])
        self.assertEqual(TAG_AWESOME.number_of_posts, 2)
        self.assertIn(POST, TAG_AWESOME.posts)
        self.assertIn(POST3, TAG_AWESOME.posts)
        self.assertEqual(TAG_BOF.number_of_posts, 1)
        self.assertEqual(TAG_BOF.posts, [POST2])

    def test_comments(self):
        self.assertEqual(COMMENT1.comment, "That was AWESOME")
        self.assertEqual(COMMENT1.user, JOE)
        self.assertEqual(COMMENT1.post, POST)
        self.assertEqual(COMMENT2.comment, "I didn't like it at all")
        self.assertEqual(COMMENT2.user, JANE)
        self.assertEqual(COMMENT2.post, POST)
        self.assertEqual(COMMENT3.comment, "Meh")
        self.assertEqual(COMMENT3.user, JOE)
        self.assertEqual(COMMENT3.post, POST3)

    def test_post1(self):
        self.assertEqual(POST.user, JOE)
        self.assertEqual(POST.item, IT_LYTRAIL)
        self.assertEqual(POST.rating, 4)
        self.assertIsNone(POST.review)
        self.assertFalse(POST.is_favorite)
        self.assertTrue(POST.is_interested)
        self.assertEqual(POST.tags, [TAG_COOL, TAG_AWESOME])
        self.assertEqual(POST.liked_by, [JACK])
        self.assertEqual(POST.comments, [COMMENT1, COMMENT2])
        self.assertEqual(POST.photos, [])

    def test_post2(self):
        self.assertEqual(POST2.user, JOE)
        self.assertEqual(POST2.item, IT_LYTRAIL)
        self.assertEqual(POST2.rating, 3)
        self.assertIsNone(POST2.review)
        self.assertFalse(POST2.is_favorite)
        self.assertFalse(POST2.is_interested)
        self.assertEqual(POST2.tags, [TAG_BOF])
        self.assertEqual(POST2.liked_by, [])
        self.assertEqual(POST2.comments, [])
        self.assertEqual(POST2.photos, [])

    def test_post3(self):
        self.assertEqual(POST3.user, JANE)
        self.assertEqual(POST3.item, IT_LYTRAIL)
        self.assertEqual(POST3.rating, 4)
        self.assertIsNone(POST3.review)
        self.assertFalse(POST3.is_favorite)
        self.assertFalse(POST3.is_interested)
        self.assertEqual(POST3.tags, [TAG_AWESOME])
        self.assertEqual(POST3.liked_by, [JOE, JACK])
        self.assertEqual(POST3.comments, [COMMENT3])
        self.assertEqual(POST3.photos, [PHOTO])

    def test_user_joe(self):
        self.assertEqual(JOE.status, USER_STATUS_ACTIVE)
        self.assertEqual(JOE.posts, [POST, POST2])
        self.assertEqual(JOE.friends_from, [JACK])
        self.assertEqual(JOE.friends_to, [])
        self.assertEqual(JOE.friends, [JACK])
        self.assertEqual(JOE.likes, [POST3])
        self.assertEqual(JOE.comments, [COMMENT1, COMMENT3])

    def test_user_jane(self):
        self.assertEqual(JANE.status, USER_STATUS_ACTIVE)
        self.assertEqual(JANE.posts, [POST3])
        self.assertEqual(JANE.friends_from, [JACK])
        self.assertEqual(JANE.friends_to, [])
        self.assertEqual(JANE.friends, [JACK])
        self.assertEqual(JANE.likes, [])
        self.assertEqual(JANE.comments, [COMMENT2])

    def test_user_jack(self):
        self.assertEqual(JACK.status, USER_STATUS_ACTIVE)
        self.assertEqual(JACK.posts, [])
        self.assertEqual(JACK.friends_from, [])
        self.assertEqual(JACK.friends_to, [JANE, JOE])
        self.assertEqual(JACK.friends, [JANE, JOE])
        self.assertEqual(JACK.likes, [POST, POST3])
        self.assertEqual(JACK.comments, [])


class TestDicts(unittest.TestCase):

    def test_photo(self):
        self.assertEqual(PHOTO.as_dict(), DIC_PHOTO)

    def test_location(self):
        self.assertEqual(SF.as_dict(), DIC_LOCATION)

    def test_tag(self):
        self.assertEqual(TAG_COOL.as_dict(), DIC_TAG_1)
        self.assertEqual(TAG_AWESOME.as_dict(), DIC_TAG_2)

    def test_comment(self):
        self.assertEqual(COMMENT2.as_dict(), DIC_COMMENT_2)
        self.assertEqual(COMMENT3.as_dict(), DIC_COMMENT_3)

    def test_item(self):
        self.assertEqual(IT_LYTRAIL.as_dict(), DIC_ITEM_1)

    def test_post(self):
        self.assertEqual(POST.as_dict(with_item=True), DIC_POST_1_ITEM)
        self.assertEqual(POST3.as_dict(), DIC_POST_3)
        self.assertEqual(POST3.as_dict(with_item=True), DIC_POST_3_ITEM)
        self.assertEqual(POST3.as_dict(all_fields=True), DIC_POST_3_ALL)

    def test_user(self):
        self.assertEqual(JANE.as_dict(friends=True), DIC_USER_2)


if __name__ == '__main__':
    unittest.main()

