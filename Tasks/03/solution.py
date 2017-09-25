import math
from uuid import uuid4
from datetime import datetime
from collections import deque


class UserDoesNotExistError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UsersNotConnectedError(Exception):
    pass


class Post:
    def __init__(self, uuid, content):
        self._author = uuid
        self._published_at = datetime.now()
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
    def __init__(self, full_name):
        self._full_name = full_name
        self._uuid = uuid4()
        self._posts = deque([], maxlen=50)

    @property
    def uuid(self):
        return self._uuid

    def add_post(self, post_content):
        """Create a new post for the user."""
        self._posts.append(Post(self.uuid, post_content))

    def get_post(self):
        """Return generator over the user`s posts."""
        return (post for post in self._posts)


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
        """Return the distance to the farthest \
           user from user with user_uuid.
        """
        # Return the last vertex with it`s level
        return self.__bfs(user_uuid)[-1][1]

    def min_distance(self, from_user_uuid, to_user_uuid):
        """Return the shortest path between two users in the graph."""
        distance = math.inf
        for user_uuid, level in self.__bfs(from_user_uuid):
            if user_uuid == to_user_uuid:
                distance = level
                break
        return distance

    def nth_layer_followings(self, user_uuid, n):
        """Return all users followed by user_uuid at
           distance n.
        """
        return {
            user
            for user, level in self.__bfs(user_uuid)
            if level == n
        }

    def generate_feed(self, user_uuid, offset=0, limit=10):
        """Return iterable over the most recent posts,
           from user_uuid`s followees.
        """
        user = self.__find_by_user_uuid(user_uuid)
        followees = [followee for followee in self._graph[user]]
        all_posts = [post for followee in followees
                     for post in followee.get_post()]
        return sorted(
            all_posts,
            key=lambda post: post.published_at,
            reverse=True
        )[offset:][0:limit]

    def __bfs(self, start, end=None):
        """Perform BFS on the graph."""
        result = []
        vertices = deque([(start, 0)])
        visited = set()
        while len(vertices) > 0:
            vertex, level = vertices.popleft()
            if vertex not in visited:
                result.append((vertex, level))
                visited.add(vertex)
                neighbours = [
                    (followee, level + 1)
                    for followee in self.following(vertex)
                    if followee not in visited
                    ]
                vertices.extend(neighbours)
        return result
