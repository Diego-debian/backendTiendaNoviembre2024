from flask import Flask, render_template, request, redirect, url_for
import requests
from blueprints.usuarios import usuarios_bp  # Importamos el Blueprint de usuarios
from blueprints.productos import productos_db  # Importamos el Blueprint de productos

app = Flask(__name__)
app.register_blueprint(usuarios_bp, url_prefix="/api")  # Registramos el Blueprint con prefijo /api

app.register_blueprint(productos_db, url_prefix="/api")  # Registramos el Blueprint con prefijo /api

# Cambiamos la URL del backend para usar el Blueprint de usuarios
backend_url_usuarios = "http://127.0.0.1:5000/api/usuarios"

# Cambiamos la URL del backend para usar el Blueprint de productos
backend_url_productos = "http://127.0.0.1:5000/api/productos"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/productos")
def listar_productos():
    response = requests.get(backend_url_productos)
    productos = response.json() if response.status_code == 200 else []
    return render_template("productos.html", productos=productos)


@app.route("/producto/<int:id>")
def producto_detalle(id):
    response = requests.get(f"{backend_url_productos}/{id}")
    if response.status_code == 200:
        producto = response.json()
        return render_template("editar_producto.html", producto=producto)
    else:
        return redirect(url_for("listar_productos"))

@app.route("/crear_producto", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":
        producto = {
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"]
        }
        response = requests.post(backend_url_productos, json=producto)
        if response.status_code == 201:
            return redirect(url_for("listar_productos"))
    return render_template("crear_producto.html")

@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if request.method == "POST":
        # Obtener datos del formulario y actualizar el producto
        producto = {
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"]
        }
        response = requests.put(f"{backend_url_productos}/{id}", json=producto)
        if response.status_code == 200:
            return redirect(url_for("listar_productos"))
        else:
            return "Error al actualizar el producto", response.status_code

    # GET request: Fetch the products details for editing
    response = requests.get(f"{backend_url_productos}/{id}")
    try:
        producto = response.json()
        return render_template("editar_producto.html", producto=producto)
    except:
        # En caso de error, mostrar un mensaje y redirigir al índice
        return redirect(url_for("listar_productos")), 404
        


@app.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):
    response = requests.delete(f"{backend_url_productos}/{id}")
    return redirect(url_for("listar_productos"))



@app.route("/usuarios")
def listar_usuarios():
    response = requests.get(backend_url_usuarios)
    usuarios = response.json() if response.status_code == 200 else []
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuario/<int:id>")
def usuario_detalle(id):
    response = requests.get(f"{backend_url_usuarios}/{id}")
    if response.status_code == 200:
        usuario = response.json()
        return render_template("editar_usuario.html", usuario=usuario)
    else:
        return redirect(url_for("listar_usuarios"))

@app.route("/crear_usuario", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        usuario = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"]
        }
        response = requests.post(backend_url_usuarios, json=usuario)
        if response.status_code == 201:
            return redirect(url_for("listar_usuarios"))
    return render_template("crear_usuario.html")

@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if request.method == "POST":
        # Obtener datos del formulario y actualizar el usuario
        usuario = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"]
        }
        response = requests.put(f"{backend_url_usuarios}/{id}", json=usuario)
        if response.status_code == 200:
            return redirect(url_for("listar_usuarios"))
        else:
            return "Error al actualizar el usuario", response.status_code

    # GET request: Fetch the user details for editing
    response = requests.get(f"{backend_url_usuarios}/{id}")
    try:
        usuario = response.json()
        return render_template("editar_usuario.html", usuario=usuario)
    except:
        # En caso de error, mostrar un mensaje y redirigir al índice
        return redirect(url_for("listar_usuarios")), 404
        


@app.route("/eliminar_usuario/<int:id>", methods=["POST"])
def eliminar_usuario(id):
    response = requests.delete(f"{backend_url_usuarios}/{id}")
    return redirect(url_for("listar_usuarios"))


if __name__ == "__main__":
    app.run(debug=True)