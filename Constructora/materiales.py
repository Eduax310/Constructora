from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from db import get_db_connection

materiales_bp = Blueprint('materiales', __name__)

@materiales_bp.route("/index", methods=["GET", "POST"])
def material_index():
    conn = get_db_connection()
    buscar = request.args.get('buscar', '')  
    
    if conn:
        try:
            with conn.cursor() as cursor:
                if buscar:
                    cursor.execute("""
                        SELECT m.id, m.nombre, p.nombre AS proveedor, m.precio_unitario 
                        FROM materiales m
                        JOIN proveedores p ON m.proveedor = p.id
                        WHERE m.id LIKE %s OR m.nombre LIKE %s OR p.nombre LIKE %s
                    """, ('%' + buscar + '%', '%' + buscar + '%', '%' + buscar + '%'))
                else:
                    cursor.execute("""
                        SELECT m.id, m.nombre, p.nombre AS proveedor, m.precio_unitario 
                        FROM materiales m
                        JOIN proveedores p ON m.proveedor = p.id
                    """)
                datos = cursor.fetchall()
            return render_template('materiales/index.html', lista=datos, buscar=buscar)
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."

@materiales_bp.route("/agregar", methods=["GET"])
def material_agregar_get():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM proveedores")
                proveedores = cursor.fetchall()  # Lista de tuplas (id, nombre)
            return render_template("materiales/agregar.html", proveedores=proveedores)
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al cargar los proveedores."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."

@materiales_bp.route("/agregar", methods=["POST"])
def material_agregar_post():
    conn = get_db_connection()
    if conn:
        try:
            v_nombre = request.form['nombre']
            v_proveedor = request.form['proveedor']
            v_precio_unitario = request.form['precio_unitario']
            
            if v_nombre and v_proveedor and v_precio_unitario:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO materiales (nombre, proveedor, precio_unitario) 
                        VALUES (%s, %s, %s)
                    """, (v_nombre, v_proveedor, v_precio_unitario))
                    conn.commit()
                return redirect(url_for('materiales.material_index'))
            else:
                return "Todos los campos son requeridos."
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."

@materiales_bp.route("/editar/<string:id>", methods=["GET"])
def material_editar_get(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM materiales WHERE id = %s", (id,))
                material = cursor.fetchone()
            if material:
                return render_template("materiales/editar.html", material=material)
            else:
                return "Material no encontrado."
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."

@materiales_bp.route("/editar/<string:id>", methods=["POST"])
def material_editar_post(id):
    conn = get_db_connection()
    if conn:
        try:
            v_nombre = request.form['nombre']
            v_proveedor = request.form['proveedor']
            v_precio_unitario = request.form['precio_unitario']
            
            if v_nombre and v_proveedor and v_precio_unitario:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE materiales 
                        SET nombre = %s, proveedor = %s, precio_unitario = %s 
                        WHERE id = %s
                    """, (v_nombre, v_proveedor, v_precio_unitario, id))
                    conn.commit()
                return redirect(url_for('materiales.material_index'))
            else:
                return "Todos los campos son requeridos."
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."

@materiales_bp.route("/eliminar/<string:id>", methods=["GET"])
def material_eliminar_get(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM materiales WHERE id = %s", (id,))
                material = cursor.fetchone()
            if material:
                return render_template("materiales/eliminar.html", material=material)
            else:
                return "Material no encontrado."
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."

@materiales_bp.route("/eliminar/<string:id>", methods=["POST"])
def material_eliminar_post(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM materiales WHERE id = %s", (id,))
                conn.commit()
            return redirect(url_for('materiales.material_index'))
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."
