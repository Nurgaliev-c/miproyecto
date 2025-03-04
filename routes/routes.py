# routes/routes.py
from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/calendario')
def calendario():
    return render_template('calendario.html')
