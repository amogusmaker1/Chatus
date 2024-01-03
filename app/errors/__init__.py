from flask import Blueprint
Bp = Blueprint("errors", __name__)
from app.errors import handlers
