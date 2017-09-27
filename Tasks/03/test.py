import datetime
import unittest

import solution


class TestSocialGraph(unittest.TestCase):
    def setUp(self):
        self.terry = solution.User("Terry Gilliam")
        self.eric = solution.User("Eric Idle")
        self.graham = solution.User("Graham Chapman")
        self.john = solution.User("John Cleese")
        self.michael = solution.User("Michael Palin")
        self.graph = solution.SocialGraph()
        self.graph.add_user(self.terry)
        self.graph.add_user(self.eric)
        self.graph.add_user(self.graham)
        self.graph.add_user(self.john)

    def test_add_user(self):
        self.graph.add_user(self.michael)
        with self.assertRaises(solution.UserAlreadyExistsError):
            self.graph.add_user(self.michael)
        self.assertIn(self.michael.uuid, self.graph.users)

    def test_get_user(self):
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.get_user(self.michael.uuid)
        self.graph.add_user(self.michael)
        self.assertEqual(self.graph.get_user(self.michael.uuid), self.michael)

    def test_delete_user(self):
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.delete_user(self.michael.uuid)
        self.graph.add_user(self.michael)
        self.graph.delete_user(self.michael.uuid)
        self.assertNotIn(self.michael.uuid, self.graph.users)

    def test_follow(self):
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.follow(self.michael.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.assertTrue(
            self.graph.is_following(self.terry.uuid, self.eric.uuid))
        self.assertFalse(
            self.graph.is_following(self.eric.uuid, self.terry.uuid))

    def test_unfollow(self):
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.follow(self.michael.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.unfollow(self.terry.uuid, self.eric.uuid)
        self.assertFalse(self.graph.is_following(self.terry.uuid,
                                                 self.eric.uuid))

    def test_followers(self):
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.followers(self.michael.uuid)
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.john.uuid, self.eric.uuid)
        self.assertEqual({self.terry.uuid, self.john.uuid},
                         self.graph.followers(self.eric.uuid))

    def test_following(self):
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.following(self.michael.uuid)
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.john.uuid)
        self.assertEqual({self.eric.uuid, self.john.uuid},
                         self.graph.following(self.terry.uuid))

    def test_friends(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.assertNotIn(self.eric.uuid, self.graph.friends(self.terry.uuid))
        self.assertNotIn(self.terry.uuid, self.graph.friends(self.eric.uuid))
        self.graph.follow(self.eric.uuid, self.terry.uuid)
        self.assertIn(self.eric.uuid, self.graph.friends(self.terry.uuid))
        self.assertIn(self.terry.uuid, self.graph.friends(self.eric.uuid))

    def test_max_distance(self):
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.following(self.michael.uuid)
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.graham.uuid)
        self.graph.follow(self.graham.uuid, self.eric.uuid)
        self.graph.follow(self.eric.uuid, self.john.uuid)
        self.assertEqual(self.graph.max_distance(self.terry.uuid), 2)

    def test_min_distance(self):
        with self.assertRaises(solution.UsersNotConnectedError):
            self.graph.min_distance(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.graham.uuid)
        self.graph.follow(self.graham.uuid, self.eric.uuid)
        self.assertEqual(self.graph.min_distance(self.terry.uuid,
                                                 self.eric.uuid), 1)
        self.graph.follow(self.eric.uuid, self.john.uuid)
        self.assertEqual(self.graph.min_distance(self.terry.uuid,
                                                 self.john.uuid), 2)

    def test_nth_layer_followings(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.graham.uuid)
        self.assertEqual(self.graph.nth_layer_followings(self.terry.uuid, 1),
                         {self.eric.uuid, self.graham.uuid})
        self.graph.follow(self.graham.uuid, self.john.uuid)
        self.assertEqual(self.graph.nth_layer_followings(self.terry.uuid, 2),
                         {self.john.uuid})

    def test_generate_feed(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.john.uuid)
        self.eric.add_post("1")
        self.eric.add_post("2")
        self.john.add_post("3")
        self.john.add_post("4")
        result = self.graph.generate_feed(self.terry.uuid)
        result = list(map(lambda post: post.content, result))
        self.assertEqual(result, ["4", "3", "2", "1"])


class TestUser(unittest.TestCase):
    def setUp(self):
        self.michael = solution.User("Michael Palin")
        self.graph = solution.SocialGraph()

    def test_has_uuid(self):
        self.assertIsNotNone(getattr(self.michael, 'uuid'))

    def test_add_post(self):
        self.michael.add_post("larodi")
        post = next(self.michael.get_post())
        self.assertEqual(post.author, self.michael.uuid)
        self.assertEqual(post.content, "larodi")
        self.assertTrue(isinstance(post.published_at, datetime.datetime))

    def test_max_posts(self):
        for i in range(0, 50):
            self.michael.add_post("something")
        first_post = self.michael.get_post()
        self.michael.add_post("something")
        self.assertNotIn(first_post, self.michael._posts)

if __name__ == '__main__':
    unittest.main()
