from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Initialize database


@app.route('/')
def hello_world():
    return 'Hello, World!'


# Import CLI commands to make them available
import models  # This ensures models and CLI commands are loaded

if __name__ == '__main__':
    app.run(debug=True)  # Enables debugging mode for development
