# routes/tareas.py
from flask import Blueprint

tareas_bp = Blueprint('tareas_bp', __name__)

@tareas_bp.route('/tareas')
def tareas():
    return "Página de tareas"
