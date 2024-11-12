from flask import Blueprint, request, jsonify
from db_utils import get_db_connection

productos_db = Blueprint("productos", __name__)

@productos_db.route("/productos", methods=["POST"])
def create_producto():
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Productos(nombre, descripcion)
            VALUES (?,?)
        """, (data["nombre"], data.get("descripcion")))
        conn.commit()
        return jsonify({"Mensaje":"Producto creado exitosamente"}), 201
    
@productos_db.route("/productos", methods=["GET"])
def get_productos():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        return jsonify([dict(producto) for producto in productos]), 200
    
@productos_db.route("/productos/<int:id>", methods=["GET"])
def get_producto(id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Productos WHERE idProducto=?
        """, (id,))
        producto = cursor.fetchone()
        return jsonify(dict(producto)) if producto else jsonify({"mensaje": "Producto no encontrado"}), 404

@productos_db.route("/productos/<int:id>", methods=["PUT"])
def update_producto(id):
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE Productos SET nombre = ?, descripcion=? WHERE idProducto=?
        """, (data["nombre"], data.get("descripcion"), id))
        conn.commit()
        return jsonify({"mensaje":"Producto actualizado exitosamente"}), 200

@productos_db.route("/productos/<int:id>", methods=["DELETE"])
def delete_producto(id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE Idproducto = ?", (id,))
        conn.commit()
        return jsonify({"message": "Producto eliminado exitosamente"}), 200