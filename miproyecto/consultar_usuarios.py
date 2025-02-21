import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Consultar los usuarios
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

# Mostrar resultados
print("ID | Nombre de usuario | Contraseña encriptada | Equipo")
print("-" * 80)
for usuario in usuarios:
    print(usuario)

# Cerrar conexión
conn.close()