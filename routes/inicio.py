from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_bcrypt import Bcrypt  # Se usa flask_bcrypt en lugar de bcrypt

auth = Blueprint('auth', __name__)