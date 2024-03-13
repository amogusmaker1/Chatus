from app import db, creaApp
from app.models import User, Post

app = creaApp()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
