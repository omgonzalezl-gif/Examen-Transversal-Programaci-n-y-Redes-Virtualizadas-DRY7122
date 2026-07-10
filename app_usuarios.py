from flask import Flask, request, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB_NAME = "usuarios.db"


def crear_base_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def insertar_usuario(nombre, password):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    hash_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)",
        (nombre, hash_password)
    )

    conexion.commit()
    conexion.close()


def validar_usuario(nombre, password):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT password_hash FROM usuarios WHERE nombre = ?",
        (nombre,)
    )

    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        return check_password_hash(resultado[0], password)

    return False


def cargar_integrantes():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    cantidad = cursor.fetchone()[0]
    conexion.close()

    if cantidad == 0:
        insertar_usuario("Omar Gonzalez", "omar123")
        insertar_usuario("Misael Pereira", "misael123")


@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":
        nombre = request.form["nombre"]
        password = request.form["password"]

        if validar_usuario(nombre, password):
            mensaje = f"Usuario {nombre} validado correctamente."
        else:
            mensaje = "Usuario o contraseña incorrectos."

    pagina = """
    <html>
    <head>
        <title>Validación de Usuarios</title>
    </head>
    <body>
        <h1>Ingreso de Usuarios - Examen DRY7122</h1>

        <form method="POST">
            <label>Nombre de usuario:</label><br>
            <input type="text" name="nombre" required><br><br>

            <label>Contraseña:</label><br>
            <input type="password" name="password" required><br><br>

            <button type="submit">Validar Usuario</button>
        </form>

        <h3>{{ mensaje }}</h3>
    </body>
    </html>
    """

    return render_template_string(pagina, mensaje=mensaje)


if __name__ == "__main__":
    crear_base_datos()
    cargar_integrantes()
    app.run(host="0.0.0.0", port=5800, debug=True)
