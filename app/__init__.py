from flask import Flask

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

from app import views  # Ensure views.py is in the same directory
