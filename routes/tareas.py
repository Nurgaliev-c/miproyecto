from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_bcrypt import Bcrypt  # Se usa flask_bcrypt en lugar de bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/create')
def create():
    return render_template('create.html')


@auth.route('/delete')
def create():
    return render_template('delete.html')


@auth.route('/update')
def create():
    return render_template('update.html')



@auth.route('/read')
def create():
    return render_template('read.html')