from flask import Flask
from routes.auth import auth
from routes.tareas import tareas
from routes.inicio import inicio


app = Flask(__name__, static_folder='static')
app.register_blueprint(auth)
app.register_blueprint(tareas)
app.register_blueprint(inicio)