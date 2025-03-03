from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_bcrypt import Bcrypt  # Se usa flask_bcrypt en lugar de bcrypt

app = Flask(__name__, static_folder='static')
app.secret_key = 'tu_clave_secreta'
bcrypt = Bcrypt(app)  # Inicializar bcrypt

#* Función para inicializar la base de datos, se crean las tablas necesarias
def inicializar_bd():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            equipo TEXT  -- Se agrega la columna equipo
        )
    ''')
    conexion.commit()
    conexion.close()

inicializar_bd()

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

@app.route('/')
def index():
    usuario = session.get('usuario')
    return render_template('index.html', usuario=usuario)

@app.route('/calendario')
def calendario():
    return render_template('calendario.html')

#* Ruta para iniciar sesión en la aplicación web 
@app.route('/login', methods=['GET', 'POST'])
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
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    #* Obtener los equipos desde la tabla "equipo"
    cursor.execute("SELECT nombre FROM equipo")  #* Asegúrarse de que "nombre" es la columna correcta
    equipos = [fila[0] for fila in cursor.fetchall()]
    
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        equipo = request.form['equipo']  #* Captura el equipo seleccionado
        
        #* Verificar si el usuario ya existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre_usuario=?", (usuario,))
        resultado = cursor.fetchone()
        
        if resultado[0] > 0:
            return render_template('registro.html', mensaje="Error: El usuario ya existe.", equipos=equipos)
        
        #* Hashear la contraseña antes de guardarla en la BD
        contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        #* Registrar usuario con la contraseña encriptada
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña, equipo) VALUES (?, ?, ?)", 
                       (usuario, contraseña_hash, equipo))
        conexion.commit()
        conexion.close()
        
        flash("Usuario registrado con éxito", "success")
        return redirect(url_for('login'))
    
    return render_template('registro.html', equipos=equipos)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
