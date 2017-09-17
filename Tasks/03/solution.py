import uuid
import datetime

class UserDoesNotExistError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UsersNotConnectedError(Exception):
    pass


class User:
    MAX_POSTS = 50

    def __init__(self, full_name):
        self._full_name = full_name
        self._uuid = uuid.uuid4()

    @property
    def uuid(self):
        return self._uuid

    def add_post(self, post_content):
        pass

    def get_post(self):
        pass


class Post:
    def __init__(self):
        pass


class SocialGraph:
    def __init__(self):
        self._graph = {}

    def _find_by_uuid(self, uuid):
        """Return User with uuid=uuid"""
        user = [_ for _ in self._graph if _.uuid == uuid]

    def add_user(self, user):
        """Add an user in the graph."""
        if user in self._graph:
            raise UserAlreadyExistsError
        self._graph[user] = []

    def get_user(self, user_uuid):
        """Return User object matching user_uuid"""
        for user in self._graph:
            if user.uuid == user_uuid:
                return user

    def delete_user(self, user_uuid):
        """Delete a User object with a given user_uuid"""
        user = [_ for _ in self._graph if _.uuid == user_uuid][0]
        del self._graph[user]

    def follow(self, follower_uuid, followee_uuid):
        follower = self._find_by_uuid(follower_uuid)
        followee = self._find_by_uuid(followee_uuid)
        self._graph[follower].append(followee)

    def unfollow(self, follower, followee):
        pass

    def is_following(self, follower_uuid, followee_uuid):
        """True if follower follows followee"""
        follower = self._find_by_uuid(follower_uuid)
        followee = self._find_by_uuid(followee_uuid)
        return followee in self._graph[follower]

    def followers(self, user_uuid):
        """Return set of all users following a given user with uuid=user_uuid"""
        pass

    def following(self, user_uuid):
        """Return set of all uuid`s followed by user with uuid=user_uuid"""
        pass

    def friends(self, user_uuid):
        """Return set of all users that are friends with user with uuid=user_uuid"""
        user = self._find_by_uuid(user_uuid)
        friends = {_ for _ in self._graph if self.is_following(_, user) and self.is_following(user, _)}
        return friends
        # friends if both users follow each other

    def max_distance(self, user_uuid):
        pass

    def min_distance(self, user_uuid):
        pass

    def nth_layer_followings(self, user_uuid, n):
        pass

    def generate_feed(self, user_uuid, offset=0, limit=10):
        pass
