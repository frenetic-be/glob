'''
.. module:: glob.dbmodels
.. moduleauthor:: Julien Spronck
.. created:: September 2017

Module containing all SQLAlchemy classes corresponding to database tables.
'''

__version__ = '0.1'

import config

import json
import os
import re
from sqlalchemy import (Column, ForeignKey, BigInteger, Boolean, Date, DateTime,
                        Float, Integer, SmallInteger, String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select, func, and_

class CommonBase(object):
    '''Methods and attribute common to all classes
    '''
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def as_json(self):
        return json.dumps(self.as_dict())

Base = declarative_base(cls=CommonBase)
HASHLEN = 87

#################
### LOCATIONS ###
#################

class Locations(Base):
    '''The `location` Table contains the locations of all items.
    '''
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    address = Column(String(250))
#
#     def as_dict(self):
#         dic = {'lat': self.lat,
#                'lon': self.lon,
#                'address': self.address}
#         return dic

#############
### USERS ###
#############

class Devices(Base):
    '''The `devices` Table contains the device unique id for all users.
    '''
    __tablename__ = 'devices'

    decide_id = Column(Integer, primary_key=True)
    device_udid = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

class UserStatusTypes(Base):
    '''The `user_status_types` Table contains the possible statuses of a user:
    - active
    - warned
    - blocked
    - pending
    '''
    __tablename__ = 'user_status_types'

    status_id = Column(Integer, primary_key=True)
    status_name = Column(String(32), nullable=False, unique=True)


class Users(Base):
    '''The `users` Table contains all users and their information.
    '''
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email_address = Column(String(HASHLEN), nullable=False)
    secondary_login = Column(String(HASHLEN))
    password = Column(String(HASHLEN), nullable=False)

    account_creation_date = Column(Date)

    status_id = Column(Integer, ForeignKey('user_status_types.status_id'))
    status = relationship(UserStatusTypes)

    posts = relationship("Posts", back_populates="user")

    friends_from = relationship("Users",
        secondary="user_relationships",
        primaryjoin="and_(Users.user_id==user_relationships.c.first_user_id,"
                    "user_relationships.c.type_id==1)",
        secondaryjoin="Users.user_id==user_relationships.c.second_user_id",
        backref="friends_to"
    )

    likes = relationship("Posts", secondary="post_likes")

    comments = relationship("PostComments", back_populates="user")

    @validates('email_address', 'secondary_login', 'password')
    def validate_field(self, key, field):
        assert len(field) == HASHLEN
        return field

    @property
    def friends(self):
        return self.friends_to+self.friends_from

    def as_dict(self, friends=False):
        dic = {'account_creation_date': self.account_creation_date.isoformat(),
               'status': self.status.status_name,
               'posts': [post.as_dict(all_fields=True) for post in self.posts],
               'user_id': self.user_id,
               'comments': [comment.as_dict() for comment in self.comments],
               'likes': [like.as_dict(with_item=True) for like in self.likes]}
        if friends:
            dic['friends'] = [friend.as_dict(friends=False)
                              for friend in self.friends]

        return dic

##############
### PHOTOS ###
##############

class Photos(Base):
    '''The `photos` Table contains the photo file names and
    their corresponding post.
    '''
    __tablename__ = 'photos'

    photo_id = Column(Integer, primary_key=True)
    file_name = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    post = relationship("Posts", back_populates="photos")

    def as_dict(self):
        dic = {'photo_id': self.photo_id,
               'file_name': self.file_name}
        return dic


#############
### POSTS ###
#############


class Categories(Base):
    '''The `categories` Table contains the post categories (Hike, Artist,
    Restaurant, ...)
    '''
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(64), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.category_id'))
    parent = relationship('Categories', remote_side=[category_id])

    items = relationship('Items', back_populates="category")

    @property
    def complete_string(self):
        if self.parent is None:
            return self.category_name
        return self.parent.complete_string + '\\' + self.category_name

    def as_dict(self, with_items=False):
        dic = {'category_id': self.category_id,
               'category_name': self.complete_string}
        if with_items:
            dic['items'] = [item.as_dict() for item in self.items]
        return dic

# Table saying what tag is in what posts
t_posts_tags = Table('posts_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.post_id')),
    Column('tag_id', Integer, ForeignKey('tags.tag_id')),
)


class Tags(Base):
    '''The `tags` Table contains all existing (hash)tags.
    '''
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(64), nullable=False, unique=True)

    posts = relationship("Posts", secondary=t_posts_tags)

    @validates('tag_name')
    def validate_tag(self, key, tag):
        '''tags should be case-insensitive
        '''
        return tag.lower()

    @property
    def number_of_posts(self):
        return len(self.posts)

    @hybrid_property
    def h_number_of_posts(self):
        return self.posts.count()

    @h_number_of_posts.expression
    def h_number_of_posts(cls):
        return (select([func.count(t_posts_tags.c.post_id)]).
                where(t_posts_tags.c.tag_id == cls.tag_id).
                label("h_number_of_posts")
                )

    def as_dict(self, with_posts=False):
        dic = {'tag_id': self.tag_id,
               'tag_name': self.tag_name,
               'number_of_posts': self.number_of_posts}
        if with_posts:
            dic['posts'] = [post.as_dict(with_item=True) for post in self.posts]
        return dic

class Items(Base):
    '''The `Items` Table contains all items that have been rated.
    '''
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(250), nullable=False)

    category_id = Column(Integer, ForeignKey('categories.category_id'),
                         nullable=False)
    category = relationship(Categories, back_populates="items")

    location_id = Column(Integer, ForeignKey('locations.location_id'))
    location = relationship(Locations)

    posts = relationship("Posts", back_populates="item")

    @property
    def rating(self):
        rated_posts = [post for post in self.posts if post.rating is not None]
        if not rated_posts:
            return None
        return float(sum(post.rating
                         for post in rated_posts))/float(len(rated_posts))

    def as_dict(self, with_posts=False):
        dic = {'item_id': self.item_id,
               'item_name': self.item_name,
               'category': self.category.complete_string,
               'location': self.location.as_dict() if self.location else {},
               'rating': self.rating}
        if with_posts:
            dic['posts'] = [post.as_dict() for post in self.posts]
        return dic


class Posts(Base):
    '''The `Posts` Table contains all posts/ratings/reviews.
    '''
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True)
    post_datetime = Column(DateTime(timezone=True), nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'),
                     nullable=False)
    user = relationship(Users, back_populates="posts")

    item_id = Column(Integer, ForeignKey('items.item_id'),
                     nullable=False)
    item = relationship(Items, back_populates='posts')

    rating = Column(SmallInteger)

    review = Column(String(250))

    photos = relationship("Photos", back_populates="post")

    is_favorite = Column(Boolean, default=False)

    is_interested = Column(Boolean, default=False)

    tags = relationship("Tags", secondary=t_posts_tags)

    liked_by = relationship("Users", secondary="post_likes")

    comments = relationship("PostComments", back_populates="post")

    @property
    def tag_string(self):
        return ', '.join(tag.tag_name for tag in self.tags)

    def as_dict(self, with_item=False, all_fields=False):
        dic = {'post_id': self.post_id,
               'rating': self.rating,
               'review': self.review,
               'post_datetime': self.post_datetime.isoformat(),
               'tags': [tag.as_dict() for tag in self.tags],
               'photos': [photo.as_dict() for photo in self.photos]}
        if with_item or all_fields:
            dic['item'] = self.item.as_dict()
        if all_fields:
            dic['is_favorite'] = self.is_favorite
            dic['is_interested'] = self.is_interested
            dic['liked_by'] = [user.user_id for user in self.liked_by]
            dic['comments'] = [comment.as_dict() for comment in self.comments]
        return dic

######################
### SOCIAL NETWORK ###
######################


class UserRelationshipTypes(Base):
    '''The `user_relationship_types` Table contains the possible relationship
    types between two users:
    - friends
    - pending_first_second
    - pending_second_first
    - blocked_first_second
    - blocked_second_first
    - blocked_both
    '''
    __tablename__ = 'user_relationship_types'

    relationship_id = Column(Integer, primary_key=True)
    relationship_name = Column(String(32), nullable=False, unique=True)


class UserRelationships(Base):
    '''The `user_relationships` Table contains all user relationships.
    '''
    __tablename__ = 'user_relationships'

    first_user_id = Column(Integer, ForeignKey('users.user_id'),
                           primary_key=True)
    first_user = relationship(Users, foreign_keys=[first_user_id])

    second_user_id = Column(Integer, ForeignKey('users.user_id'),
                            primary_key=True)
    second_user = relationship(Users, foreign_keys=[second_user_id])

    type_id = Column(Integer,
                     ForeignKey('user_relationship_types.relationship_id'))
    type = relationship(UserRelationshipTypes)


class PostLikes(Base):
    '''The `post_likes` Table contains all the info about
    what user liked what post.
    '''
    __tablename__ = 'post_likes'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user = relationship(Users)

    post_id = Column(Integer, ForeignKey('posts.post_id'), primary_key=True)
    post = relationship(Posts)


class PostComments(Base):
    '''The `post_comments` Table contains all the info about comments for a
    given post.
    '''
    __tablename__ = 'post_comments'

    comment_id = Column(Integer, primary_key=True)
    comment = Column(String(250), nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user = relationship(Users, back_populates="comments")

    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    post = relationship(Posts, back_populates="comments")

    datetime = Column(DateTime(timezone=True), nullable=False)

    def as_dict(self):
        dic = super(PostComments, self).as_dict()
        dic['datetime'] = dic['datetime'].isoformat()
        return dic

def set_up_database(path=''):

    if config.DBLOCAL:
        engine = create_engine('sqlite:///'+os.path.join(path, config.DBFILE))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    user_status_types = ['active', 'warned', 'blocked', 'pending']
    for status in user_status_types:
        obj = UserStatusTypes(status_name=status)
        try:
            session.add(obj)
            session.commit()
        except IntegrityError:
            session.rollback()


    user_relationship_types = ['friends', 'pending_first_second',
                               'pending_second_first', 'blocked_first_second',
                               'blocked_second_first', 'blocked_both']
    for rel_type in user_relationship_types:
        obj = UserRelationshipTypes(relationship_name=rel_type)
        try:
            session.add(obj)
            session.commit()
        except IntegrityError:
            session.rollback()
