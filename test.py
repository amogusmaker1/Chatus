import app
from app import db, creaApp
from app.models import User, Post
from datetime import datetime, timedelta
from config import Config
from unittest import TestCase
import jwt
from time import time
import unittest

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    CURRENTTESTING = True

class Test(TestCase):
    def setUp(self):
        self.app = creaApp(TestConfig)
        self.appContext = self.app.app_context()
        self.appContext.push()
        db.create_all()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.appContext.pop()
    def test_passChange(self):
        user = User(username = "Sigma", email = "sigma@gmail.com", age = "4")
        user.set_password("Sigma123")
        self.assertFalse(user.check_password("Sigma2281337488"))
        self.assertTrue(user.check_password("Sigma123"))
    def test_avatar(self):
         user = User(username = "Sigma", email = "sigma@gmail.com", age = "4")
         self.assertEqual(user.avatar(64),"https://www.gravatar.com/avatar/96d6967f449ca585220966f2c8797e3c?s=64&d=https%3A%2F%2Fi.pinimg.com%2F564x%2Fc0%2Fa7%2Fa6%2Fc0a7a613e35143a9606521beee386ccf.jpg")
    def test_follow(self):
        user1 = User(username = "Sigmer", email = "sigmer@gmail.com", age = "2")
        user2 = User(username = "Sigmarist", email = "sigmarist@gmail.com", age = "-e2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user1.followers.all(), [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 1)
        self.assertEqual(user1.followed.first().username, "Sigmarist")
        self.assertEqual(user2.followers.first().username, "Sigmer")
        self.assertEqual(user2.followers.count(), 1)

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 0)
        self.assertEqual(user2.followers.count(), 0)
    def test_followed_posts(self):
        user1 = User(username="Sigmar", email="ohio@gmail.com", age = "14")
        user2 = User(username="ohioaner", email="sigmarist@gmail.com", age = "-3")
        user3 = User(username="Sigma Halal Burger", email="halalburger@gmail.com", age = "14")
        user4= User(username="Kai Cenat", email="Kaicenatohio@gmail.com", age = "-3")
        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()
        post1 = Post(body = "The Burger is not sigma halal", author = user1, timestamp = datetime.utcnow() + timedelta(seconds=1))
        post2 = Post(body = "The Bunger is certified sigma halal", author = user2, timestamp = datetime.utcnow() + timedelta(seconds=4))
        post3 = Post(body = "certified sigma", author = user3, timestamp = datetime.utcnow() + timedelta(seconds=3))
        post4 = Post(body = "c", author = user4, timestamp = datetime.utcnow() + timedelta(seconds=2))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        user1.follow(user2)
        user1.follow(user3)
        user1.follow(user4)

        user2.follow(user3)

        user3.follow(user4)
        user3.follow(user2)

        db.session.commit()

        self.assertEqual(user1.followed_posts().all(), [post2, post3, post4, post1])
        self.assertEqual(user2.followed_posts().all(), [post2, post3])
        self.assertEqual(user3.followed_posts().all(), [post2, post3, post4])
        self.assertEqual(user4.followed_posts().all(), [post4])

        '''self.assertEqual(user1.notFollowedPosts().all(), [])
        self.assertEqual(user2.notFollowedPosts().all(), [post4, post1])
        self.assertEqual(user3.notFollowedPosts().all(), [post1])
        self.assertEqual(user4.notFollowedPosts().all(), [post2, post3, post1])'''

    def test_GrPT(self):    #Test Get reset Password token
        user = User(username="Antoha6654", email="Ant@oha.gmail")
        user.set_password(password="ant")
        db.session.add(user)
        db.session.commit()

        token = user.get_reset_password_token()
        self.assertEqual(user, User.verify_reset_password_token(token))

if __name__ == "__main__":
    unittest.main(verbosity=2)

