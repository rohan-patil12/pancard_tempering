import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # Make sure root is in path

from app import app

if __name__ == "__main__":
    app.run(debug=True)
