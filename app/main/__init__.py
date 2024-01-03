from flask import Blueprint
Bp = Blueprint("main", __name__)
from app.main import routes
