import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretpassword1'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.mail.ru"
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "adm.mikrobloga@mail.ru"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'TuhJ91Sfvhw1jCY3isvg'
    ADMINS = ['adm.mikrobloga@mail.ru']
    POSTS_PER_PAGE = 10
