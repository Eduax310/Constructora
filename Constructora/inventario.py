from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error  
from db import get_db_connection  

inventario_bp = Blueprint('inventario', __name__)
@inventario_bp.route("/index")
def inventario_index():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT i.id, m.nombre, i.cantidad_disponible, i.umbral_minimo 
                    FROM inventario i
                    JOIN materiales m ON i.material_id = m.id
                """)
                datos = cursor.fetchall()
            
            datos_con_alerta = []
            for item in datos:
                inventario_id, material_nombre, cantidad_disponible, umbral_minimo = item
                mostrar_alerta = cantidad_disponible <= umbral_minimo
                datos_con_alerta.append((inventario_id, material_nombre, cantidad_disponible, umbral_minimo, mostrar_alerta))
            
            return render_template('inventario/index.html', lista=datos_con_alerta)
        except mysql.connector.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        except Exception as e:
            print(f"Error inesperado: {e}")
            return "Error inesperado."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."
    
@inventario_bp.route("/agregar", methods=["GET", "POST"])
def inventario_agregar():
    conn = get_db_connection()
    if conn:
        try:
            if request.method == "GET":
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nombre FROM materiales") 
                    materiales = cursor.fetchall()  
                
                return render_template("inventario/agregar.html", materiales=materiales)
            
          
            material_id = request.form['material_id']
            cantidad_disponible = request.form['cantidad_disponible']
            umbral_minimo = request.form['umbral_minimo']
            
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM materiales WHERE id = %s", (material_id,))
                result = cursor.fetchone()
                
                if not result:
                    return "El Material ID no existe en la tabla de materiales."
            
            if material_id and cantidad_disponible and umbral_minimo:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Inventario (Material_ID, Cantidad_Disponible, Umbral_Minimo)
                        VALUES (%s, %s, %s)
                    """, (material_id, cantidad_disponible, umbral_minimo))
                    conn.commit()
                return redirect(url_for('inventario.inventario_index'))
            else:
                return "Todos los campos son requeridos."
        except mysql.connector.Error as e:  
            print(f"Error al ejecutar la consulta: {e}")
            return "Error al ejecutar la consulta."
        except Exception as e:  
            print(f"Error inesperado: {e}")
            return "Error inesperado."
        finally:
            conn.close()
    else:
        return "Error al conectar a la base de datos."

@inventario_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def inventario_editar(id):
    conn = get_db_connection()
    if request.method == "GET":
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM Inventario WHERE id=%s", (id,))
                    inventario = cursor.fetchone()
                if inventario:
                    return render_template("inventario/editar.html", inventario=inventario)
                else:
                    return "Registro de inventario no encontrado."
            except mysql.connector.Error as e:  
                print(f"Error al ejecutar la consulta: {e}")
                return "Error al ejecutar la consulta."
            except Exception as e:  
                print(f"Error inesperado: {e}")
                return "Error inesperado."
            finally:
                conn.close()
        else:
            return "Error al conectar a la base de datos."

    if request.method == "POST":
        material_id = request.form['material_id']
        cantidad_disponible = request.form['cantidad_disponible']
        umbral_minimo = request.form['umbral_minimo']
        if conn:
            try:
                if material_id and cantidad_disponible and umbral_minimo:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            UPDATE Inventario SET Material_ID=%s, Cantidad_Disponible=%s, Umbral_Minimo=%s
                            WHERE id=%s
                        """, (material_id, cantidad_disponible, umbral_minimo, id))
                        conn.commit()
                    return redirect(url_for('inventario.inventario_index'))
                else:
                    return "Todos los campos son requeridos."
            except mysql.connector.Error as e:  
                print(f"Error al ejecutar la consulta: {e}")
                return "Error al ejecutar la consulta."
            except Exception as e:  
                print(f"Error inesperado: {e}")
                return "Error inesperado."
            finally:
                conn.close()
        else:
            return "Error al conectar a la base de datos."

@inventario_bp.route("/eliminar/<int:id>", methods=["POST", "GET"])
def inventario_eliminar(id):
    conn = get_db_connection()
    if request.method == "GET":
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM Inventario WHERE id=%s", (id,))
                    inventario = cursor.fetchone()
                if inventario:
                    return render_template("inventario/eliminar.html", inventario=inventario)
                else:
                    return "Registro de inventario no encontrado."
            except mysql.connector.Error as e:  
                print(f"Error al ejecutar la consulta: {e}")
                return "Error al ejecutar la consulta."
            except Exception as e:  
                print(f"Error inesperado: {e}")
                return "Error inesperado."
            finally:
                conn.close()
        else:
            return "Error al conectar a la base de datos."

    if request.method == "POST":
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM Inventario WHERE id=%s", (id,))
                    conn.commit()
                return redirect(url_for('inventario.inventario_index'))
            except mysql.connector.Error as e:  
                print(f"Error al ejecutar la consulta: {e}")
                return "Error al ejecutar la consulta."
            except Exception as e:  
                print(f"Error inesperado: {e}")
                return "Error inesperado."
            finally:
                conn.close()
        else:
            return "Error al conectar a la base de datos."
