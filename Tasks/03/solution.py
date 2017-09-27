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
        self.links[user.uuid] = set()

    @__check_user_exists
    def get_user(self, user):
        """Return User object matching user."""
        return self.users[user]

    @__check_user_exists
    def delete_user(self, user):
        """Delete a User object matching user."""
        # Make sure the deleted user is not following nor
        # followed by another user anymore:
        for follower in self.followers(user).copy():
            self.unfollow(follower, user)
        for followee in self.following(user).copy():
            self.unfollow(user, followee)
        del self.users[user]

    @__check_user_exists
    def follow(self, follower, followee):
        """Make User with uuid: follower to follow
           User with uuid: followee.
        """
        self.links[follower].add(followee)

    @__check_user_exists
    def unfollow(self, follower, followee):
        """Make User with uuid: follower to unfollow
           User with uuid: followee.
        """
        if self.is_following(follower, followee):
            self.links[follower].remove(followee)

    @__check_user_exists
    def is_following(self, follower, followee):
        """Return True if follower follows followee."""
        return followee in self.links[follower]

    @__check_user_exists
    def followers(self, user):
        """Return set of all users` uuids following user."""
        return {follower for follower in self.links
                if user in self.links[follower]}

    @__check_user_exists
    def following(self, user):
        """Return set of all users` uuids followed by user."""
        return self.links[user]

    @__check_user_exists
    def friends(self, user):
        """Return set of all users` uuids that are friends with user."""
        return {_ for _ in self.links if
                self.is_following(_, user) and
                self.is_following(user, _)}

    @__check_user_exists
    def max_distance(self, user):
        """Return the distance to the farthest \
           user from user.
        """
        # Return the last vertex with it`s level
        return self.__bfs(user)[-1][1]

    @__check_user_exists
    def min_distance(self, from_user, to_user):
        """Return the shortest path between two users in the graph."""
        distance = math.inf
        for user, level in self.__bfs(from_user):
            if user == to_user:
                distance = level
                break
        if distance == math.inf:
            raise UsersNotConnectedError
        return distance

    @__check_user_exists
    def nth_layer_followings(self, user, n):
        """Return all users followed by user at
           distance n.
        """
        return {usr for usr, level
                in self.__bfs(user)
                if level == n}

    @__check_user_exists
    def generate_feed(self, user, offset=0, limit=10):
        """Return iterable over the most recent posts,
           from user`s followees.
        """
        followees = [followee for followee in self.links[user]]
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
