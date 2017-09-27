import math
import uuid
from datetime import datetime
from collections import deque


class UserDoesNotExistError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UsersNotConnectedError(Exception):
    pass


class Post:
    def __init__(self, user_uuid, content):
        self._author = user_uuid
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
        self._uuid = uuid.uuid4()
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
        self.users = {}
        self.links = {}

    def __check_user_exists(func):
        """Decorator function that checks user existance in the graph."""
        def checked_func(self, *uuids):
            # Use only the uuids arguments:
            uuids_only = [arg for arg in uuids if type(arg) is uuid.UUID]
            for user_uuid in uuids_only:
                if user_uuid not in self.users:
                    raise UserDoesNotExistError
            return func(self, *uuids)
        return checked_func

    def add_user(self, user):
        """Add an user in the graph."""
        if user.uuid in self.users:
            raise UserAlreadyExistsError
        self.users[user.uuid] = user
        self.links[user.uuid] = []

    @__check_user_exists
    def get_user(self, user_uuid):
        """Return User object matching user_uuid."""
        return self.users[user_uuid]

    @__check_user_exists
    def delete_user(self, user_uuid):
        """Delete a User object matching user_uuid."""
        del self.users[user_uuid]

    @__check_user_exists
    def follow(self, follower_uuid, followee_uuid):
        self.links[follower_uuid].append(followee_uuid)

    @__check_user_exists
    def unfollow(self, follower_uuid, followee_uuid):
        """Make User with uuid: follower_uuid to unfollow
           User with uuid: followee_uuid.
        """
        if self.is_following(follower_uuid, followee_uuid):
            self.links[follower_uuid].remove(followee_uuid)

    @__check_user_exists
    def is_following(self, follower_uuid, followee_uuid):
        """Return True if follower follows followee."""
        return followee_uuid in self.links[follower_uuid]

    @__check_user_exists
    def followers(self, user_uuid):
        """Return set of all users` uuids following user_uuid."""
        return {follower for follower in self.links
                if user_uuid in self.links[follower]}

    @__check_user_exists
    def following(self, user_uuid):
        """Return set of all users` uuids followed by user_uuid."""
        return set(self.links[user_uuid])

    @__check_user_exists
    def friends(self, user_uuid):
        """Return set of all users` uuids that are friends with user_uuid."""
        return {user for user in self.links if
                self.is_following(user, user_uuid) and
                self.is_following(user_uuid, user)}

    @__check_user_exists
    def max_distance(self, user_uuid):
        """Return the distance to the farthest \
           user from user with user_uuid.
        """
        # Return the last vertex with it`s level
        return self.__bfs(user_uuid)[-1][1]

    @__check_user_exists
    def min_distance(self, from_user_uuid, to_user_uuid):
        """Return the shortest path between two users in the graph."""
        distance = math.inf
        for user_uuid, level in self.__bfs(from_user_uuid):
            if user_uuid == to_user_uuid:
                distance = level
                break
        if distance == math.inf:
            raise UsersNotConnectedError
        return distance

    @__check_user_exists
    def nth_layer_followings(self, user_uuid, n):
        """Return all users followed by user_uuid at
           distance n.
        """
        return {user for user, level
                in self.__bfs(user_uuid)
                if level == n}

    @__check_user_exists
    def generate_feed(self, user_uuid, offset=0, limit=10):
        """Return iterable over the most recent posts,
           from user_uuid`s followees.
        """
        followees = [followee for followee in self.links[user_uuid]]
        all_posts = [post for followee in followees
                     for post in self.users[followee].get_post()]
        return sorted(
            all_posts,
            key=lambda post: post.published_at,
            reverse=True
        )[offset:][0:limit]

    @__check_user_exists
    def __bfs(self, start, end=None):
        """Perform BFS on the graph."""
        result = []
        vertices = deque([(start, 0)])
        visited = set()
        while vertices:
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
