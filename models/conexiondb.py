# models/conexiondb.py
import sqlite3
from flask_bcrypt import Bcrypt

# Bcrypt para hashear y verificar contraseñas (sin usar app)
bcrypt = Bcrypt()

def inicializar_bd():
    """Crea la tabla 'usuarios' si no existe."""
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            equipo TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

def obtener_conexion():
    """Retorna una conexión a la base de datos."""
    return sqlite3.connect("database.db", check_same_thread=False)

def verificar_usuario(usuario, contraseña_plana):
    """
    Verifica si el usuario existe y la contraseña coincide.
    Devuelve True si las credenciales son válidas, de lo contrario False.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT contraseña FROM usuarios WHERE nombre_usuario = ?", (usuario,))
    fila = cursor.fetchone()
    conexion.close()

    if fila:
        contraseña_hash = fila[0].encode('utf-8')
        # Compara la contraseña hasheada con la ingresada
        if bcrypt.check_password_hash(contraseña_hash, contraseña_plana):
            return True
    return False

def crear_usuario(usuario, contraseña_plana, equipo):
    """Inserta un nuevo usuario en la BD con contraseña hasheada."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Hashear la contraseña
    contraseña_hash = bcrypt.generate_password_hash(contraseña_plana).decode('utf-8')

    cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña, equipo) VALUES (?, ?, ?)",
                   (usuario, contraseña_hash, equipo))
    conexion.commit()
    conexion.close()
