from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt

app = Flask(__name__, static_folder='static')
app.secret_key = 'tu_clave_secreta'

# Función para crear la base de datos si no existe
def inicializar_bd():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

inicializar_bd()

# Función para registrar un usuario con contraseña encriptada
def registrar_usuario(nombre_usuario, contraseña):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Encripta la contraseña antes de guardarla
    salt = bcrypt.gensalt()
    contraseña_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)

    cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (?, ?)", (nombre_usuario, contraseña_encriptada))
    conexion.commit()
    conexion.close()

    print("Usuario registrado correctamente")

# Función para verificar credenciales
def verificar_usuario(usuario, contraseña):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT contraseña FROM usuarios WHERE nombre_usuario = ?", (usuario,))
    usuario_encontrado = cursor.fetchone()
    conexion.close()

    if usuario_encontrado:
        # Convertimos la contraseña almacenada de str a bytes
        contraseña_guardada = usuario_encontrado[0].encode('utf-8')

        # Verificamos la contraseña ingresada con la almacenada
        if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_guardada):
            return True

    return False



@app.route('/')
def index():
    usuario = session.get('usuario')
    return render_template('index.html', usuario=usuario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = None  # Variable para mostrar mensajes de error
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        if verificar_usuario(usuario, contraseña):
            session['usuario'] = usuario  # Guardar sesión del usuario
            return redirect(url_for('index'))
        else:
            mensaje = "Usuario o contraseña incorrectos"

    return render_template('login.html', mensaje=mensaje)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        try:
            registrar_usuario(usuario, contraseña)
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            mensaje = "El usuario ya existe. Intente con otro nombre."
    
    return render_template('registro.html', mensaje=mensaje)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
