# routes/inicio.py
from flask import Blueprint, render_template, session

inicio_bp = Blueprint('inicio_bp', __name__)

@inicio_bp.route('/')
def index():
    usuario = session.get('usuario')
    # Muestra la página de inicio
    return render_template('index.html', usuario=usuario)
