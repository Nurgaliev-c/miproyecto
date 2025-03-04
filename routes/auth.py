from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_bcrypt import Bcrypt  # Se usa flask_bcrypt en lugar de bcrypt

auth = Blueprint('auth', __name__)


#* Función para obtener conexión a la base de datos 
def obtener_conexion():
    return sqlite3.connect("database.db", check_same_thread=False)

#*Función para verificar credenciales
def verificar_usuario(usuario, contraseña):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT contraseña FROM usuarios WHERE nombre_usuario = ?", (usuario,))
    usuario_encontrado = cursor.fetchone()
    conexion.close()

    if usuario_encontrado:
        contraseña_guardada = usuario_encontrado[0].encode('utf-8')
        if bcrypt.check_password_hash(contraseña_guardada, contraseña):  # Comparación segura
            return True
    return False


@auth.route('/')
def index():
    usuario = session.get('usuario')
    return render_template('index.html', usuario=usuario)

@auth.route('/calendario')
def calendario():
    return render_template('calendario.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')

        if verificar_usuario(usuario, contraseña):
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            mensaje = "Usuario o contraseña incorrectos"

    return render_template('login.html', mensaje=mensaje)



#* Ruta para registrar un nuevo usuario en la base de datos
@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    conexion = obtener_conexion()
    cursor = conexion.cursor()









@auth.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))