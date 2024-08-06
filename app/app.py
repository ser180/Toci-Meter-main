from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la clave secreta para el uso de flash
app.secret_key = 'supersecretkey'

# Conexión a la base de datos
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='mysql',  # nombre del servicio en docker-compose
            user='root',
            password='root',
            database='proyecto'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['txtUsuario']
        password = request.form['txtPass']
        role = request.form.get('role')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s AND role = %s', 
                           (usuario, password, role))
            account = cursor.fetchone()
            cursor.close()
            conn.close()

            if account:
                if role == 'admin':
                    return redirect(url_for('vistaadmin'))
                else:
                    return redirect(url_for('inicio'))
            else:
                flash('Usuario, contrasena o perfil incorrectos', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        fecha_nacimiento = request.form['txtFechaNacimiento']
        direccion = request.form['txtDireccion']
        telefono = request.form['txtTelefono']
        usuario = request.form['txtUsuario']
        email = request.form['txtEmail']
        contrasena = request.form['txtPass']
        role = request.form['role']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (nombre, fecha_nacimiento, direccion, telefono, usuario, email, contrasena, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                           (nombre, fecha_nacimiento, direccion, telefono, usuario, email, contrasena, role))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Usuario registrado satisfactoriamente', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edituser(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            nombre = request.form['txtNombre']
            fecha_nacimiento = request.form['txtFechaNacimiento']
            direccion = request.form['txtDireccion']
            telefono = request.form['txtTelefono']
            usuario = request.form['txtUsuario']
            email = request.form['txtEmail']
            contrasena = request.form['txtPass']
            role = request.form['role']

            cursor.execute('UPDATE usuarios SET nombre = %s, fecha_nacimiento = %s, direccion = %s, telefono = %s, usuario = %s, email = %s, contrasena = %s, role = %s WHERE id = %s',
                           (nombre, fecha_nacimiento, direccion, telefono, usuario, email, contrasena, role, id))
            conn.commit()
            flash('Usuario actualizado satisfactoriamente')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_usuarios'))

        cursor.execute('SELECT * FROM usuarios WHERE id = %s', [id])
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edituser.html', usuario=usuario)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = %s', [id])
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario eliminado satisfactoriamente')
    return redirect(url_for('admin_usuarios'))

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM plantas WHERE nombre LIKE %s OR descripcion LIKE %s', ('%' + query + '%', '%' + query + '%'))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('plantas.html', query=query, plantas=resultados)

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/admin_usuarios')
def admin_usuarios():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/vistaadmin')
def vistaadmin():
    return render_template('vistaadmin.html')

@app.route('/foro', methods=['GET', 'POST'])
def foro():
    if request.method == 'POST':
        contenido = request.form['contenido']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO publicaciones (contenido) VALUES (%s)', (contenido,))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Publicación exitosa', 'success')
            return redirect(url_for('foro'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM publicaciones ORDER BY fecha_publicacion DESC')
        publicaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('foro.html', publicaciones=publicaciones)

@app.route('/articulos')
def articulos():
    return render_template('articulos.html')

@app.route('/huertos')
def huertos():
    return render_template('huertos.html')

@app.route('/citas')
def citas():
    return render_template('citas.html')

@app.route('/citas', methods=['POST'])
def crear_cita():
    fecha_consulta = request.form['fecha_consulta']
    hora_consulta = request.form['hora_consulta']
    motivo = request.form['motivo']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO citas (fecha_consulta, hora_consulta, motivo) VALUES (%s, %s, %s)',
                           (fecha_consulta, hora_consulta, motivo))
            conn.commit()
            flash('Cita creada exitosamente', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al crear la cita: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('citas'))

@app.route('/plantas')
def plantas():
    return render_template('plantas.html')

@app.route('/huertos2')
def huertos2():
    return render_template('huertos2.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/get_publicaciones')
def get_publicaciones():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM publicaciones ORDER BY fecha_publicacion DESC')
        publicaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(publicaciones)

@app.route('/gestionar_huertos', methods=['GET', 'POST'])
def gestionar_huertos():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            try:
                nombre = request.form['nombre']
                descripcion = request.form['descripcion']
                cursor.execute('INSERT INTO huertas (nombre, descripcion) VALUES (%s, %s)',
                               (nombre, descripcion))
                conn.commit()

                # Obtener el ID de la nueva huerta
                huerta_id = cursor.lastrowid
                new_huerta = {'id': huerta_id, 'nombre': nombre, 'descripcion': descripcion}
                cursor.close()
                conn.close()
                return jsonify(success=True, huerta=new_huerta)
            except Exception as e:
                print(f"Error al añadir la huerta: {str(e)}")
                cursor.close()
                conn.close()
                return jsonify(success=False, error=str(e))

        cursor.execute('SELECT * FROM huertas')
        huertas = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_huertos.html', huertas=huertas)

@app.route('/huertos/delete/<int:id>', methods=['POST'])
def delete_huerto(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM huertas WHERE id = %s', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(success=True)
        except Exception as e:
            print(f"Error al eliminar la huerta: {str(e)}")
            cursor.close()
            conn.close()
            return jsonify(success=False, error=str(e))

@app.route('/huertos/edit/<int:id>', methods=['POST'])
def edit_huerto(id):
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE huertas SET nombre = %s, descripcion = %s WHERE id = %s', 
                           (nombre, descripcion, id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/inicio2')
def inicio2():
    return render_template('inicio2.html')

@app.route('/admin/usuarios')
def admin_usuario():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/plantas')
def admin_plantas():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM plantas')
        plantas = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_plantas.html', plantas=plantas)

@app.route('/admin/herramientas')
def admin_herramientas():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM herramientas')
        herramientas = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_herramientas.html', herramientas=herramientas)

@app.route('/admin/articulos')
def admin_articulos():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM articulos')
        articulos = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_articulos.html', articulos=articulos)

@app.route('/admin/huertos')
def admin_huertos():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM huertas')
        huertas = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_huertos.html', huertas=huertas)

@app.route('/admin/foro', methods=['GET', 'POST'])
def admin_foro():
    if request.method == 'POST':
        contenido = request.form['contenido']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO publicaciones (contenido) VALUES (%s)', (contenido,))
            conn.commit()
            cursor.close()
            conn.close()
            return '', 204  # Responder con No Content para indicar éxito sin redirigir

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM publicaciones ORDER BY fecha_publicacion DESC')
        publicaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_foro.html', publicaciones=publicaciones)

@app.route('/admin_foro/delete/<int:id>', methods=['POST'])
def admin_foro_delete(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM publicaciones WHERE id = %s', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/admin_foro/edit/<int:id>', methods=['POST'])
def admin_foro_edit(id):
    data = request.get_json()
    contenido = data.get('contenido', None)
    if not contenido:
        return jsonify({'success': False}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE publicaciones SET contenido = %s WHERE id = %s', (contenido, id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})


@app.route('/plantas2')
def plantas2():
    return render_template('plantas2.html')

@app.route('/herramientas')
def herramientas():
    return render_template('herramientas.html')

@app.route('/huertos3')
def huertos3():
    return render_template('huertos3.html')

@app.route('/herramientas2')
def herramientas2():
    return render_template('herramientas2.html')

@app.route('/articulos2')
def articulos2():
    return render_template('articulos2.html')

@app.route('/gestionar_plantas', methods=['GET', 'POST'])
def gestionar_plantas():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            try:
                # Insertar en la base de datos
                cursor.execute('INSERT INTO plantas (nombre, descripcion) VALUES (%s, %s)', (nombre, descripcion))
                conn.commit()
                # Obtener el ID de la nueva planta
                planta_id = cursor.lastrowid
                new_planta = {'id': planta_id, 'nombre': nombre, 'descripcion': descripcion}
                return jsonify(success=True, planta=new_planta)
            except Exception as e:
                print(f"Error al añadir la planta: {str(e)}")
                return jsonify(success=False, error=str(e))
        else:
            cursor.execute('SELECT * FROM plantas')
            plantas = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('gestionar_plantas.html', plantas=plantas)

@app.route('/plantas/edit/<int:id>', methods=['POST'])
def edit_planta(id):
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE plantas SET nombre = %s, descripcion = %s WHERE id = %s', 
                           (nombre, descripcion, id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/plantas/delete/<int:id>', methods=['POST'])
def delete_planta(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM plantas WHERE id = %s', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/gestionar_herramientas', methods=['GET', 'POST'])
def gestionar_herramientas():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            try:
                # Insertar en la base de datos
                cursor.execute('INSERT INTO herramientas (nombre, descripcion) VALUES (%s, %s)', (nombre, descripcion))
                conn.commit()
                # Obtener el ID de la nueva herramienta
                herramienta_id = cursor.lastrowid
                new_herramienta = {'id': herramienta_id, 'nombre': nombre, 'descripcion': descripcion}
                return jsonify(success=True, herramienta=new_herramienta)
            except Exception as e:
                print(f"Error al añadir la herramienta: {str(e)}")
                return jsonify(success=False, error=str(e))
        else:
            cursor.execute('SELECT * FROM herramientas')
            herramientas = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('gestionar_herramientas.html', herramientas=herramientas)
        
@app.route('/herramientas/edit/<int:id>', methods=['POST'])
def edit_herramienta(id):
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE herramientas SET nombre = %s, descripcion = %s WHERE id = %s', 
                           (nombre, descripcion, id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})
        
@app.route('/herramientas/delete/<int:id>', methods=['POST'])
def delete_herramienta(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM herramientas WHERE id = %s', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})
        
@app.route('/gestionar_articulos', methods=['GET', 'POST'])
def gestionar_articulos():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = request.form['precio']  # Nuevo campo

            try:
                # Insertar en la base de datos
                cursor.execute('INSERT INTO articulos (nombre, descripcion, precio) VALUES (%s, %s, %s)', (nombre, descripcion, precio))
                conn.commit()
                # Obtener el ID del nuevo artículo
                articulo_id = cursor.lastrowid
                new_articulo = {'id': articulo_id, 'nombre': nombre, 'descripcion': descripcion, 'precio': precio}  # Adaptado
                return jsonify(success=True, articulo=new_articulo)
            except Exception as e:
                print(f"Error al añadir el artículo: {str(e)}")
                return jsonify(success=False, error=str(e))
        else:
            cursor.execute('SELECT * FROM articulos')
            articulos = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('gestionar_articulos.html', articulos=articulos)

@app.route('/articulos/edit/<int:id>', methods=['POST'])
def edit_articulo(id):
    data = request.json
    nombre = data.get('nombre')  # Actualizado
    descripcion = data.get('descripcion')  # Actualizado
    precio = data.get('precio')  # Nuevo campo

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE articulos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s', 
                           (nombre, descripcion, precio, id))  # Adaptado
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/articulos/delete/<int:id>', methods=['POST'])
def delete_articulo(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM articulos WHERE id = %s', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/citas')
def admin_citas():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM citas ORDER BY fecha_consulta DESC')
        citas = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_citas.html', citas=citas)

@app.route('/citas/delete/<int:id>', methods=['POST'])
def delete_cita(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM citas WHERE id = %s', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/citas/edit/<int:id>', methods=['POST'])
def edit_cita(id):
    data = request.get_json()
    fecha_consulta = data.get('fecha_consulta')
    hora_consulta = data.get('hora_consulta')
    motivo = data.get('motivo')

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE citas SET fecha_consulta = %s, hora_consulta = %s, motivo = %s WHERE id = %s',
                           (fecha_consulta, hora_consulta, motivo, id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/ver_citas')
def ver_citas():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM citas ORDER BY fecha_consulta, hora_consulta')
        citas = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('ver_citas.html', citas=citas)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
