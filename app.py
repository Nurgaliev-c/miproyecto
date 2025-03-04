# app.py
from flask import Flask
from routes.auth import auth  # Importamos el blueprint
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Registramos el blueprint
app.register_blueprint(auth)

if __name__ == '__main__':
    # Opcional: verificar si database.db existe, etc.
    app.run(debug=True)
