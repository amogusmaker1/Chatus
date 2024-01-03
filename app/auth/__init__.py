from flask import Blueprint

Bp = Blueprint("auth", __name__)

from app.auth import routes
