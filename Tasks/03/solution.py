import uuid
import datetime


class UserDoesNotExistError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UsersNotConnectedError(Exception):
    pass


class Post:
    def __init__(self, uuid, content):
        self._author = uuid
        self._published_at = datetime.datetime.now()
        self._content = content

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    @property
    def published_at(self):
        return self._published_at


class User:
    MAX_POSTS = 50

    def __init__(self, full_name):
        self._full_name = full_name
        self._uuid = uuid.uuid4()
        self._posts = []

    @property
    def uuid(self):
        return self._uuid

    def add_post(self, post_content):
        """Create a new Post for the User."""
        if len(self._posts) == type(self).MAX_POSTS:
            del self._posts[0]
        self._posts.append(Post(self.uuid, post_content))

    def get_post(self):
        """Return generator over the User`s Posts."""
        for post in self._posts:
            yield post


class SocialGraph:
    def __init__(self):
        self._graph = {}

    def __find_by_user_uuid(self, uuid):
        """Return User with uuid=uuid"""
        user = [_ for _ in self._graph if _.uuid == uuid]
        if not user:
            raise UserDoesNotExistError
        return user[0]

    def add_user(self, user):
        """Add an user in the graph."""
        if user in self._graph:
            raise UserAlreadyExistsError
        self._graph[user] = []

    def get_user(self, user_uuid):
        """Return User object matching user_uuid"""
        return self.__find_by_user_uuid(user_uuid)
    
    def delete_user(self, user_uuid):
        """Delete a User object with a given user_uuid"""
        user = self.__find_by_user_uuid(user_uuid)
        del self._graph[user]

    def follow(self, follower_uuid, followee_uuid):
        follower = self.__find_by_user_uuid(follower_uuid)
        followee = self.__find_by_user_uuid(followee_uuid)
        self._graph[follower].append(followee)

    def unfollow(self, follower_uuid, followee_uuid):
        follower = self.__find_by_user_uuid(follower_uuid)
        followee = self.__find_by_user_uuid(followee_uuid)
        if self.is_following(follower_uuid, followee_uuid):
            followee_index = self._graph[follower].index(followee)
            del self._graph[follower][followee_index]

    def is_following(self, follower_uuid, followee_uuid):
        """Return True if follower follows followee."""
        follower = self.__find_by_user_uuid(follower_uuid)
        followee = self.__find_by_user_uuid(followee_uuid)
        return followee in self._graph[follower]

    def followers(self, user_uuid):
        """Return set of all users` uuids following user_uuid."""
        user = self.__find_by_user_uuid(user_uuid)
        return {_.uuid for _ in self._graph
                if user in self._graph[_]}

    def following(self, user_uuid):
        """Return set of all users` uuids followed by user_uuid."""
        user = self.__find_by_user_uuid(user_uuid)
        return {_.uuid for _ in self._graph[user]}

    def friends(self, user_uuid):
        """Return set of all users` uuids that are friends with user_uuid."""
        return {_.uuid for _ in self._graph if
                self.is_following(_.uuid, user_uuid) and
                self.is_following(user_uuid, _.uuid)}

    def max_distance(self, user_uuid):
        pass

    def min_distance(self, user_uuid):
        pass

    def nth_layer_followings(self, user_uuid, n):
        pass

    def generate_feed(self, user_uuid, offset=0, limit=10):
        pass
