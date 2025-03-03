import sqlite3
import bcrypt

# Conectar a la base de datos
conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT UNIQUE NOT NULL,
        contraseña TEXT NOT NULL,
        equipo TEXT NOT NULL
    )
''')

# Lista actualizada de pilotos F1 2024
pilotos = [
    ("Max Verstappen", "Red Bull"),
    ("Sergio Pérez", "Red Bull"),
    ("Lewis Hamilton", "Mercedes"),
    ("George Russell", "Mercedes"),
    ("Charles Leclerc", "Ferrari"),
    ("Carlos Sainz", "Ferrari"),
    ("Lando Norris", "McLaren"),
    ("Oscar Piastri", "McLaren"),
    ("Fernando Alonso", "Aston Martin"),
    ("Lance Stroll", "Aston Martin"),
    ("Pierre Gasly", "Alpine"),
    ("Esteban Ocon", "Alpine"),
    ("Alexander Albon", "Williams"),
    ("Logan Sargeant", "Williams"),
    ("Yuki Tsunoda", "RB"),
    ("Daniel Ricciardo", "RB"),
    ("Kevin Magnussen", "Haas"),
    ("Nico Hülkenberg", "Haas"),
    ("Valtteri Bottas", "Sauber"),
    ("Zhou Guanyu", "Sauber")
]

# Función para insertar usuarios con bcrypt
def insertar_usuario(nombre, contraseña, equipo):
    contraseña_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña, equipo) VALUES (?, ?, ?)", 
                       (nombre, contraseña_encriptada, equipo))
        print(f"✅ Usuario '{nombre}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print(f"⚠️ El usuario '{nombre}' ya existe en la base de datos.")

# Insertar los pilotos con contraseña "123"
for piloto, equipo in pilotos:
    insertar_usuario(piloto, "123", equipo)

# Insertar usuario admin
insertar_usuario("admin", "admin123", "Administrador")

# Guardar cambios y cerrar conexión
conexion.commit()
conexion.close()

print("\n✅ Todos los pilotos y el usuario admin han sido insertados correctamente.")
