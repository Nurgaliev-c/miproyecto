# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.conexiondb import inicializar_bd, obtener_conexion, verificar_usuario, crear_usuario

auth = Blueprint('auth', __name__)

# Llamamos a inicializar_bd() solo una vez (o podrías hacerlo en app.py)
inicializar_bd()

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
            return redirect(url_for('auth.index'))
        else:
            mensaje = "Usuario o contraseña incorrectos"

    return render_template('login.html', mensaje=mensaje)

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Si tienes una tabla 'equipo' con columna 'nombre'
    cursor.execute("SELECT nombre FROM equipo")
    equipos = [fila[0] for fila in cursor.fetchall()]
    conexion.close()

    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        equipo = request.form['equipo']

        # Verificar si el usuario ya existe
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre_usuario=?", (usuario,))
        existe = cursor.fetchone()
        if existe[0] > 0:
            conexion.close()
            return render_template('registro.html', mensaje="Error: El usuario ya existe.", equipos=equipos)

        # Crear usuario con contraseña encriptada
        crear_usuario(usuario, contraseña, equipo)
        flash("Usuario registrado con éxito", "success")
        return redirect(url_for('auth.login'))

    return render_template('registro.html', equipos=equipos)

@auth.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('auth.index'))
