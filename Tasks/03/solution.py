import uuid


class UserDoesNotExistError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UsersNotConnectedError(Exception):
    pass


class User:
    def __init__(self, full_name, uuid):
        pass

    def add_post(self, post_content):
        pass

    def get_post(self):
        pass


class Post:
    pass


class SocialGraph:
    def add_user(self, user):
        pass

    def get_user(self, user_uuid):
        pass

    def delete_user(self, user_uuid):
        pass

    def follow(self, follower, followee):
        pass

    def unfollow(self, follower, followee):
        pass

    def is_following(self, follower, followee):
        pass

    def followers(self, user_uuid):
        pass

    def following(self, user_uuid):
        pass

    def friends(self, user_uuid):
        pass

    def max_distance(self, user_uuid):
        pass

    def min_distance(self, user_uuid):
        pass

    def nth_layer_followings(self, user_uuid, n):
        pass

    def generate_feed(self, user_uuid, offset=0, limit=10):
        pass
