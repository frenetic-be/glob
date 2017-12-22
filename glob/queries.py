'''
.. module:: glob.queries
.. moduleauthor:: Julien Spronck
.. created:: September 2017

Module containing all the methods used to send queries to the databases.
'''

import datetime
import os

from passlib.hash import pbkdf2_sha256 as pb256

from dbmodels import *
import config

def get_obj(cls, obj_name, **kwargs):
    '''General function for retrieving database entries
    '''
    def wrapper(dbase, obj_id, return_object=False):
        '''Wrapper function
        '''
        obj = (dbase.session
                    .query(cls)
                    .filter(getattr(cls, obj_name+'_id') == obj_id)
                    .first())
        if not obj:
            return

        if return_object:
            ## return object itself
            return obj

        ## return dictionary
        return obj.as_dict(**kwargs)

    return wrapper

def get_all_obj(cls, order_by=None, **kwargs):
    '''General function for retrieving all database entries in a given table
    '''
    def wrapper(dbase):
        '''Wrapper function
        '''

        if callable(order_by) or order_by is None:
            objs = dbase.session.query(cls).all()
        else:
            objs = (dbase.session.query(cls)
                                 .order_by(order_by)
                                 .all())
        objs = [obj.as_dict(**kwargs) for obj in objs]
        if callable(order_by):
            return sorted(objs, key=order_by)
        return objs

    return wrapper

def create_obj(cls, required_keys=None, optional_keys=None):
    '''General decorator for creating database entries
    '''
    def decorator(function):
        '''Inner decorator (without arguments)
        '''
        def wrapper(dbase, **kwargs):
            '''Wrapper function
            '''
            kwargs_copy = kwargs.copy()
            commit = kwargs_copy.pop('commit', True)
            return_object = kwargs_copy.pop('return_object', False)
            ## Initialization
            required = required_keys
            if required is None:
                required = []
            optional = optional_keys
            if optional is None:
                optional = []

            ## Check for required fields
            for arg in required:
                orargs = arg.split('|')
                if len(orargs) == 1 and arg not in kwargs:
                    raise TypeError('Missing required argument')
                elif len(orargs) == 1:
                    kwargs_copy.pop(arg)
                elif len(orargs) > 1:
                    if not any([orarg in kwargs for orarg in orargs]):
                        raise TypeError('Missing required argument')
                    for orarg in orargs:
                        kwargs_copy.pop(orarg, None)

            ## Check that there is no additional field
            for arg in kwargs_copy:
                if arg not in optional:
                    raise TypeError('Too many arguments')

            kwdict = function(dbase, **kwargs)

            ## Create class instance
            obj = cls(**kwdict)

            if commit:
                ## Commit changes to database
                dbase.session.add(obj)
                try:
                    dbase.session.commit()
                except IntegrityError as err:
                    dbase.session.rollback()
                    raise
            if return_object:
                ## return object itself
                return obj

            ## return dictionary
            return obj.as_dict()

        return wrapper

    return decorator

def delete_obj(cls, obj_name):
    '''General function for deleting database entries
    '''
    def wrapper(dbase, obj_id, commit=True):
        '''Wrapper function
        '''
        obj = (dbase.session
                    .query(cls)
                    .filter(getattr(cls, obj_name+'_id') == obj_id)
                    .first())
        if not obj:
            raise ValueError('No object corresponding to the given id')
        if commit:
            dbase.session.delete(obj)
            try:
                dbase.session.commit()
            except IntegrityError:
                dbase.session.rollback()
                raise
        return 'OK'

    return wrapper

class DataBase(object):
    '''Class to handle database queries
    '''

    def __init__(self, path=''):
        '''Initialization method
        '''
        if config.DBLOCAL:
            self.engine = create_engine('sqlite:///' +
                                        os.path.join(path, config.DBFILE))

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    @property
    def USER_STATUS_ACTIVE(self):
        return (self.session
                    .query(UserStatusTypes)
                    .filter(UserStatusTypes.status_name == 'active')
                    .first())

    @property
    def USER_STATUS_PENDING(self):
        return (self.session
                    .query(UserStatusTypes)
                    .filter(UserStatusTypes.status_name == 'pending')
                    .first())

    @property
    def USER_STATUS_WARNED(self):
        return (self.session
                    .query(UserStatusTypes)
                    .filter(UserStatusTypes.status_name == 'warned')
                    .first())

    @property
    def USER_STATUS_BLOCKED(self):
        return (self.session
                    .query(UserStatusTypes)
                    .filter(UserStatusTypes.status_name == 'blocked')
                    .first())

    @property
    def USER_RELATIONSHIP_FRIENDS(self):
        return (self.session
                    .query(UserRelationshipTypes)
                    .filter(UserRelationshipTypes.relationship_name ==
                            u'friends')
                    .first())

    @property
    def USER_RELATIONSHIP_PENDING_1_2(self):
        return (self.session
                    .query(UserRelationshipTypes)
                    .filter(UserRelationshipTypes.relationship_name ==
                            u'pending_first_second')
                    .first())

    @property
    def USER_RELATIONSHIP_PENDING_2_1(self):
        return (self.session
                    .query(UserRelationshipTypes)
                    .filter(UserRelationshipTypes.relationship_name ==
                            u'pending_second_first')
                    .first())

    @property
    def USER_RELATIONSHIP_BLOCKED_1_2(self):
        return (self.session
                    .query(UserRelationshipTypes)
                    .filter(UserRelationshipTypes.relationship_name ==
                            u'blocked_first_second')
                    .first())

    @property
    def USER_RELATIONSHIP_BLOCKED_2_1(self):
        return (self.session
                    .query(UserRelationshipTypes)
                    .filter(UserRelationshipTypes.relationship_name ==
                            u'blocked_second_first')
                    .first())

    @property
    def USER_RELATIONSHIP_BLOCKED_BOTH(self):
        return (self.session
                    .query(UserRelationshipTypes)
                    .filter(UserRelationshipTypes.relationship_name ==
                            u'blocked_both')
                    .first())

    def get_recent_posts(self, n_posts=5):
        '''Get the most recent posts from the database
        '''
        posts = (self.session
                 .query(Posts)
                 .order_by(Posts.post_datetime.desc())
                 .limit(int(n_posts)))
        return [post.as_dict(with_item=True) for post in posts]

    ### CATEGORIES ###

    @create_obj(Categories, required_keys=['category_name'],
                optional_keys=['parent_id'])
    def create_category(self, commit=True, return_object=False, **kwargs):
        '''Creates a dictionary that is used by the create_obj decorator to
        create the actual database entry.
        '''
        return kwargs

    def get_category(self, obj_id, return_object=False):
        '''Get a category by its id
        '''
        func = get_obj(Categories, 'category', with_items=True)
        return func(self, obj_id, return_object=return_object)

    def get_all_categories(self):
        '''Get all categories from the database
        '''
        func = get_all_obj(Categories, order_by=lambda x: x['category_name'])
        return func(self)

    def delete_category(self, obj_id):
        '''Delete a category by its id
        '''
        obj = (self.session
                   .query(Categories.category_id)
                   .filter(Categories.parent_id == obj_id)
                   .all())
        for cat_id, in obj:
            self.delete_category(cat_id)
        return delete_obj(Categories, 'category')(self, obj_id)

    ### LOCATIONS ###

    @create_obj(Locations, required_keys=['lat', 'lon'],
                optional_keys=['address'])
    def create_location(self, commit=True, return_object=False, **kwargs):
        '''Creates a dictionary that is used by the create_obj decorator to
        create the actual database entry.
        '''
        return kwargs

    def get_location(self, obj_id, return_object=False):
        '''Get a location by its id
        '''
        func = get_obj(Locations, 'location')
        return func(self, obj_id, return_object=return_object)

    def delete_location(self, obj_id):
        '''Delete a location by its id
        '''
        referencing_items = (self.session
                             .query(Items)
                             .filter(Items.location_id == obj_id)
                             .first())
        if referencing_items:
            raise ValueError('Some rows in `items` are referencing this '
                             'location')
        return delete_obj(Locations, 'location')(self, obj_id)

    ### PHOTOS ###

    @create_obj(Photos, required_keys=['file_name'], optional_keys=['post_id'])
    def create_photo(self, commit=True, return_object=False, **kwargs):
        '''Creates a dictionary that is used by the create_obj decorator to
        create the actual database entry.
        '''
        return kwargs

    def get_photo(self, obj_id, return_object=True):
        '''Get a photo by its id
        '''
        return get_obj(Photos, 'photo')(self, obj_id,
                                        return_object=return_object)

    def delete_photo(self, obj_id):
        '''Delete a photo by its id
        '''
        return delete_obj(Photos, 'photo')(self, obj_id)


    ### ITEMS ###

    @create_obj(Items, required_keys=['item_name', 'category|category_id'],
                optional_keys=['location'])
    def create_item(self, commit=True, return_object=False, **kwargs):
        '''creates a new item. This function returns a dictionary that is used
        by the create_obj decorator to create the actual database entry.
        '''
        ## Make a copy of the keyword arguments dictionary
        kwdict = kwargs.copy()
        if 'location' in kwdict:
            location = kwdict['location']
            if isinstance(location, Locations):
                ## Already in the right format, nothing to do
                pass
            elif not isinstance(location, dict):
                raise TypeError('Wrong data type for `location`')
            else:
                if 'location_id' in location:
                    kwdict['location_id'] = location['location_id']
                    del kwdict['location']
                else:
                    kwdict['location'] = self.create_location(return_object=True,
                                                              commit=commit,
                                                              **location)
        if 'category' in kwdict:
            category = kwdict['category']
            if isinstance(category, Categories):
                ## Already in the right format, nothing to do
                pass
            elif not isinstance(category, dict):
                raise TypeError('Wrong data type for `category`')
            else:
                if 'category_id' in category:
                    kwdict['category_id'] = category['category_id']
                    del kwdict['category']
                else:
                    kwdict['category'] = self.create_category(return_object=True,
                                                              commit=commit,
                                                              **category)
        return kwdict


    def get_item(self, obj_id):
        '''Get a item by its id
        '''
        return get_obj(Items, 'item', with_posts=True)(self, obj_id)

    def get_all_items(self):
        '''Get all items from the database
        '''
        return get_all_obj(Items, order_by=lambda x: x['item_name'])(self)

    def delete_item(self, obj_id):
        '''Delete an item by its id
        '''
#         location = (self.session.query(Items.location_id)
#                                 .filter(Items.item_id == obj_id)
#                                 .first())
        return delete_obj(Items, 'item')(self, obj_id)
#         if location:
#             self.delete_location(location.location_id)

    ### COMMENTS ###

    @create_obj(PostComments,
                required_keys=['comment', 'user|user_id', 'post|post_id'])
    def create_comment(self, commit=True, return_object=False, **kwargs):
        '''Creates a dictionary that is used by the create_obj decorator to
        create the actual database entry.
        '''
        kwdict = kwargs.copy()
        kwdict['datetime'] = datetime.datetime.utcnow()
        return kwdict

    def get_comment(self, obj_id, return_object=True):
        '''Get a comment by its id
        '''
        return get_obj(PostComments, 'comment')(self, obj_id,
                                                return_object=return_object)

    def delete_comment(self, obj_id):
        '''Delete a comment by its id
        '''
        return delete_obj(PostComments, 'comment')(self, obj_id)

    ### LIKES ###

    @create_obj(PostLikes,
                required_keys=['user|user_id', 'post|post_id'])
    def create_like(self, commit=True, return_object=False, **kwargs):
        '''Creates a dictionary that is used by the create_obj decorator to
        create the actual database entry.
        '''
        return kwargs

    def get_like(self, post_id=None, user_id=None, return_object=True):
        '''Get a like by its post_id and user_id
        '''
        if post_id is None or user_id is None:
            return
        obj = (self.session
                   .query(PostLikes)
                   .filter(PostLikes.post_id == post_id)
                   .filter(PostLikes.user_id == user_id)
                   .first())
        if not obj:
            return

        if return_object:
            ## return object itself
            return obj

        ## return dictionary
        return obj.as_dict(**kwargs)

    def delete_like(self, post_id=None, user_id=None, commit=True):
        '''Delete a like by its post_id and user_id
        '''
        if post_id is None or user_id is None:
            return
        obj = self.get_like(post_id=post_id, user_id=user_id,
                            return_object=True)
        if not obj:
            raise ValueError('No object corresponding to the given id')
        if commit:
            self.session.delete(obj)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                raise
        return 'OK'

    ### POSTS ###

    @create_obj(Posts, required_keys=['item|item_id', 'user_id'],
                optional_keys=['rating', 'review', 'is_favorite',
                               'is_interested', 'photos', 'tags'])
    def create_post(self, commit=True, return_object=False, **kwargs):
        '''creates a new post. This function returns a dictionary that is used
        by the create_obj decorator to create the actual database entry.
        '''
        ## Make a copy of the keyword arguments dictionary
        kwdict = kwargs.copy()

        if 'item' in kwdict:
            item = kwdict['item']
            if isinstance(item, Items):
                ## Already in the right format, nothing to do
                pass
            elif not isinstance(item, dict):
                raise TypeError('Wrong data type for `item`')
            else:
                if 'item_id' in item:
                    kwdict['item_id'] = item['item_id']
                    del kwdict['item']
                else:
                    kwdict['item'] = self.create_item(return_object=True,
                                                      commit=commit,
                                                      **item)

        kwdict['post_datetime'] = datetime.datetime.utcnow()

        if 'photos' in kwdict:
            photos = kwdict['photos']
            if isinstance(photos, Photos):
                kwdict['photos'] = [kwdict['photos']]
            elif not isinstance(photos, list):
                raise TypeError('Wrong data type for `photo`')
            else:
                for j, photo in enumerate(photos):
                    if isinstance(photo, Photos):
                        pass
                    elif isinstance(photo, (unicode, str)):
                        kwdict['photos'][j] = self.create_photo(
                                                      return_object=True,
                                                      commit=False,
                                                      file_name=photo)
                    elif isinstance(photo, dict):
                        if 'photo_id' in photo:
                            kwdict['photos'][j] = self.get_photo(
                                                      return_object=True,
                                                      obj_id=photo['photo_id'])
                        else:
                            kwdict['photos'][j] = self.create_photo(
                                                      return_object=True,
                                                      commit=False,
                                                      **photo)
        if 'tags' in kwdict:
            tags = kwdict['tags']
            if isinstance(tags, Tags):
                kwdict['tags'] = [kwdict['tags']]
            elif not isinstance(tags, list):
                raise TypeError('Wrong data type for `tags`')
            else:
                for j, tag in enumerate(tags):
                    if isinstance(tag, Tags):
                        pass
                    elif isinstance(tag, (unicode, str)):
                        newtag = self.get_tag(tag_name=tag)
                        if newtag:
                            kwdict['tags'][j] = newtag
                        else:
                            kwdict['tags'][j] = self.create_tag(
                                                      return_object=True,
                                                      commit=commit,
                                                      tag_name=tag)
                    elif isinstance(tag, dict):
                        if 'tag_id' in tag:
                            kwdict['tags'][j] = self.get_tag(
                                                      return_object=True,
                                                      obj_id=tag['tag_id'])
                        else:
                            newtag = self.get_tag(tag_name=tag['tag_name'],
                                                  return_object=True)
                            if newtag:
                                kwdict['tags'][j] = newtag
                            else:
                                kwdict['tags'][j] = self.create_tag(
                                                      return_object=True,
                                                      commit=commit,
                                                      **tag)

        return kwdict

    def get_post(self, obj_id, return_object=False):
        '''Get a post by its id
        '''
        return get_obj(Posts, 'post',
                       with_item=True)(self, obj_id,
                                       return_object=return_object)

    def get_all_posts(self):
        '''Get all posts from the database
        '''
        return get_all_obj(Posts, order_by=Posts.post_datetime.desc(),
                           with_item=True)(self)

    def delete_post(self, obj_id):
        '''Delete a post by its id
        '''
        post = self.get_post(obj_id, return_object=True)
        for photo in post.photos:
            self.delete_photo(photo.photo_id)
        for comment in post.comments:
            self.delete_comment(comment.comment_id)
        return delete_obj(Posts, 'post')(self, obj_id)

    ### TAGS ###

    @create_obj(Tags, required_keys=['tag_name'])
    def create_tag(self, commit=True, return_object=False, **kwargs):
        '''Creates a dictionary that is used by the create_obj decorator to
        create the actual database entry.
        '''
        return kwargs

    def get_tag(self, obj_id=None, tag_name=None, return_object=False):
        '''Get a tag by its id or by its tag name
        '''
        if tag_name is None and obj_id is None:
            return
        if tag_name is not None:
            tag = (self.session
                       .query(Tags)
                       .filter(Tags.tag_name == tag_name.lower())
                       .first())
            if not tag:
                return

            if return_object:
                ## return object itself
                return tag

            ## return dictionary
            return tag.as_dict(with_posts=True)

        func = get_obj(Tags, 'tag', with_posts=True)
        return func(self, obj_id, return_object=return_object)

    def get_all_tags(self):
        '''Get all tags from the database
        '''
        return get_all_obj(Tags, order_by=Tags.tag_name)(self)

    def delete_tag(self, obj_id):
        '''Delete a tag by its id
        '''
        return delete_obj(Tags, 'tag')(self, obj_id)

    def get_popular_tags(self, n_tags = 5):
        '''Get the most popular tags
        '''
        tags = (self.session
                .query(Tags)
                .order_by(Tags.h_number_of_posts.desc())
                .limit(int(n_tags)))
        return [tag.as_dict() for tag in tags]

    def get_trendy_tags(self, timediff=datetime.timedelta(hours=24), n_tags=5):
        '''Get the most popular tags in the last xx hours
        '''
        if type(timediff) != datetime.timedelta:
            raise TypeError('`timediff` must be a `datetime.timedelta` object')

        from collections import Counter

        time_limit = datetime.datetime.utcnow() - timediff
        tags = (self.session
                .query(Tags.tag_name)
                .filter(Posts.post_datetime > time_limit)
                .filter(Posts.post_id == t_posts_tags.c.post_id)
                .filter(Tags.tag_id == t_posts_tags.c.tag_id)
                .all())

        ctr = Counter(tag[0] for tag in tags)
        out = [{'tag_name': key,
                'number_of_posts': val} for key, val in ctr.iteritems()]
        out = sorted(out, key=lambda x: x['number_of_posts'], reverse=True)
        return out[:n_tags]

    def search_tags(self, string):
        '''Search for posts that have a particular string
        '''
        if not isinstance(string, (unicode, str)):
            raise TypeError('Argument must be a string')
        import re
        string = string.lower()
        if not re.match('^[\w ]*$', string):
            raise ValueError('Invalid input string')

        posts = self.session.query(Posts).order_by(Posts.post_datetime.desc())
        for sub in string.split():
            posts = posts.filter(Posts.tags.any(Tags.tag_name == sub))
        posts = posts.all()

        return [post.as_dict(with_item=True) for post in posts]

    ### USER ###

    @create_obj(Users,
                required_keys=['email_address', 'secondary_login',
                               'password'])
    def create_user(self, commit=True, return_object=False, **kwargs):
        '''Creates a dictionary that is used by the create_obj decorator to
        create the actual database entry.
        '''
        ## Make a copy of the keyword arguments dictionary
        kwdict = kwargs.copy()
        kwdict['email_address'] = pb256.hash(kwdict['email_address'])
        kwdict['secondary_login'] = pb256.hash(kwdict['secondary_login'])
        kwdict['password'] = pb256.hash(kwdict['password'])
        kwdict['account_creation_date'] = datetime.date.today()
        kwdict['status'] = self.USER_STATUS_ACTIVE
        return kwdict

    def get_user(self, obj_id):
        '''Get a user by its id (only for authorized users)
        '''
        return get_obj(Users, 'user')(self, obj_id)

    ## Add create_user to api.py and test it
    ## Add delete_user here and to api.py + tests
