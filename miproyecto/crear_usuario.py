import sqlite3
import bcrypt

conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

usuario = "admin"
contraseña = "admin123"

contraseña_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

# Guardamos la contraseña en formato binario, no como texto
cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (?, ?)", (usuario, contraseña_encriptada.decode('utf-8')))
conexion.commit()
conexion.close()

print("Usuario creado exitosamente: admin / admin123")