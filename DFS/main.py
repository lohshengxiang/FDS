from flask import Flask
import psycopg2

from __init__ import login_manager
from views import view

app = Flask(__name__)

# Routing
app.register_blueprint(view)


# Config


# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{username}:{password}@{host}:{port}/{database}"\
#     .format(
#         username="postgres",
#         password="welcome1",
#         host="localhost",
#         port=5432,
#         database="postgres"
#     )
app.config["SECRET_KEY"] = "f39ju29gtn0"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['DEBUG'] = True

# Initialize other components
login_manager.init_app(app)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="localhost",
        port=5000
    )
