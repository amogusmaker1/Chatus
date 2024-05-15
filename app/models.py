from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from flask import current_app

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    avatarius = db.Column(db.Text)
    fileType = db.Column(db.Text)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    age = db.Column(db.String(20))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?s={}&d=https%3A%2F%2Fi.pinimg.com%2F564x%2Fc0%2Fa7%2Fa6%2Fc0a7a613e35143a9606521beee386ccf.jpg'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    def notFollowedPosts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.followed_id == self.id).union(self.posts)
        all_ = Post.query.filter_by()
        return all_.except_(followed).order_by(Post.timestamp.desc())

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.Text)
    fileType = db.Column(db.Text)
    coms = db.relationship('Com', backref='compost', lazy='dynamic')
    hashtags = db.Column(db.String(187), index=True)
    likes = db.relationship(
        'User', secondary=likes,
        primaryjoin=(likes.c.user_id == id),
        secondaryjoin=(likes.c.post_id == id),
        backref=db.backref('likes', lazy='dynamic'), lazy='dynamic')
    def like(self, user):
        if not self.is_liked(user):
            self.likes.append(user)

    def unlike(self, user):
        if self.is_liked(user):
            self.likes.remove(user)

    def is_liked(self, user):
        return self.likes.filter(
            likes.c.user_id == user.id).count() > 0

    def hashtag(self, hashhtag):
        return hashhtag in self.hashtags

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Com(db.Model):
    comid = db.Column(db.Integer, primary_key=True)
    combody = db.Column(db.String(2000))
    comtimestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    compost_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comimage = db.Column(db.Text)
    comfileType = db.Column(db.Text)
    comauthor_id = db.Column(db.Integer, index=True)
    comuser = db.Column(db.String(25), index=True)

    def __repr__(self):
        return '<Com {}>'.format(self.combody)
