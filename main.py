import pymysql
from app import app
from tables import ResultsPersona, ResultsRoles, ResultsEditorial, ResultsAutor, ResultsArea, ResultsTipo, ResultsCiudad,ResultsTPrestamo
from db_config import mysql
from flask import flash, render_template, request, redirect, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash

@app.after_request
def after_request(response):
    print(request.endpoint)
    pag= request.endpoint
    if pag != "login":
        if 'NombrePer' not in session:
            print("El usuario necesita login!")
            success_message="Necesita iniciar sesion"
            flash(success_message) 
            return redirect(url_for('login'))
    return response

@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/Sesion')
def index():
	if 'NombrePer' in session:
		return render_template('main.html') 
	return render_template('login.html',)

@app.route('/submit', methods=['POST'])
def login_submit():
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	# validate the received values
	if _email and _password and request.method == 'POST':
		#check user exists			
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "select p.nombre, p.matricula, CAST(u.pass AS CHAR(10000) CHARACTER SET utf8) as pass from persona p inner join usuarios u on p.Id=u.ID_Persona and matricula=%s"
		sql_where = (_email,)
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		if row:
			print(row[0])
			print(row[1])
			print(row[2])
			if check_password_hash(row[2], _password):
				session['Matricula'] = row[1]
				session['NombrePer']=row[0]
				cursor.close() 
				conn.close()
				return redirect('/Sesion')
			else:
				flash('Contraseña invalida!')
				return redirect('/login')
		else:
			flash('email o contraseña invalido!')
			return redirect('/login')

@app.route('/Selec')
def selec():
	_selec = request.args['Selec']

	if _selec=='Administrar Areas Academicas':
		return redirect('/Area')
	if _selec=='Administrar Ciudades':
		return redirect('/Ciudad')
	if _selec=='Administrar Tipo de Prestamo':
		return redirect('/TPrestamo')
	if _selec=='Administrar Personas':
		return redirect('/Users')
	if _selec=='Administrar Roles':
	
		return redirect('/Roles')
	if _selec=='Administrar Géneros':
		return redirect('/Tipo')
	if _selec=='Administrar Autores':
		return redirect('/Autor')
	if _selec=='Administrar Editoriales':
		return redirect('/Editorial')
	if _selec=='Cerrar Sesión':
		return redirect('/logout')

	return redirect('/main')
@app.route('/logout')
def logout():
	session.pop('NombrePer', None)
	session.pop('Matricula', None)
	return redirect('/')
@app.route('/main')
def main():
	return render_template('main.html')
		
@app.route('/Users/new_user')
def add_user_view():
	return render_template('Usr/add.html')
		
@app.route('/Users/add', methods=['POST'])
def add_user():
	conn = None
	cursor = None
	try:		
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		_apellido1 = request.form['inputApellido1']
		_apellido2 = request.form['inputApellido2']
		_matricula = request.form['inputMatricula']
		# validate the received values
		if _name and _email and _password and _apellido1 and _apellido2 and _matricula and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO Persona(nombre, apellido1, apellido2, matricula, Email) VALUES(%s, %s, %s, %s, %s)"
			data = (_name, _apellido1, _apellido2, _matricula, _email,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			sql = "INSERT INTO usuarios(Pass, ID_Persona) VALUES(%s,(select ID from persona where Email=%s))"
			data = ( _hashed_password, _email,)
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User added successfully!')
			return redirect('/Users')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Users')
def users():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("select p.Id, p.Nombre, p.Apellido1, p.Apellido2, p.Matricula, p.Email, CAST(u.pass AS CHAR(10000) CHARACTER SET utf8) as pass  from persona p join usuarios u on u.ID_persona= p.ID")
		rows = cursor.fetchall()
		table = ResultsPersona(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		return render_template('Usr/users.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/Users/edit/<int:id>')
def edit_view_user(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Persona WHERE id=%s", id)
		row = cursor.fetchone()
		print("Despues del Select")
		if row:
			return render_template('Usr/edit.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/Users/update', methods=['POST'])
def update_user():
	conn = None
	cursor = None
	try:		
		_name = request.form['inputName']
		_matricula = request.form['inputMatricula']
		_apellido1 = request.form['inputApellido1']
		_apellido2 = request.form['inputApellido2']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		_id = request.form['id']
		# validate the received values
		if _name and _email and _password and _id  and _apellido1 and _matricula and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE Persona SET nombre=%s, apellido1=%s, apellido2=%s, Email=%s, Matricula=%s WHERE id=%s"
			data = (_name, _apellido1, _apellido2, _email, _matricula, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			sql = "UPDATE Usuarios SET Pass=%s where ID_persona=%s"
			data = (_hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User updated successfully!')
			return redirect('/Users')
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Users/delete/<int:id>')
def delete_user(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM persona WHERE id=%s", (id,))
		conn.commit()
		flash('User deleted successfully!')
		return redirect('/Users')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		


# aqui comienza Roles

@app.route('/Roles/add', methods=['POST'])
def add_rol():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		_chec=request.form.getlist('inputChec')
		# validate the received values
		if _nombre and request.method == 'POST':
			# save edits
			sql = "INSERT INTO Roles(nombre) VALUES(%s)"
			data = (_nombre,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT Id FROM Roles WHERE nombre=%s", _nombre)
			rowId = cursor.fetchone()
			print("Aqui mero despues")
			NewRolId=rowId['Id']
			i=0
			while len(_chec)>i:
				sql = "INSERT INTO roles_has_permisos(permiso_ID, Rol_ID) VALUES(%s,%s)"
				data = (_chec[i],NewRolId)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				i+=1
			flash('Rol agregado exitosamente!')
			return redirect('/Roles')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Roles')
def roles():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id, Nombre FROM Roles")
		rows = cursor.fetchall()
		table = ResultsRoles(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		return render_template('Roles/rol.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/Roles/edit/<int:id>')
def edit_view_rol(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Roles WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('Roles/edit.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/Roles/update', methods=['POST'])
def update_rol():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		_id = request.form['id']
		# validate the received values
		if _nombre and request.method == 'POST':
			sql = "UPDATE Roles SET nombre=%s WHERE id=%s"
			data = (_nombre, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Rol Actualizado Exitosamente!')
			return redirect('/Roles')
		else:
			return 'Error al actualizar el Rol!'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Roles/delete/<int:id>')
def delete_rol(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Roles WHERE id=%s", (id,))
		conn.commit()
		flash('Rol Eliminado Exitosamente!')
		return redirect('/Roles')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/Roles/new_rol')
def add_rol_view():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id, Nombre FROM Permisos")
		rows = cursor.fetchall()
		return render_template('Roles/add.html', rows=rows, len=len(rows))   
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
	return render_template('Roles/add.html')

##aqui comienza EDITORIAL

@app.route('/Editorial/new_editorial')
def add_editorial_view():
	return render_template('Editorial/add.html')
		
@app.route('/Editorial/add', methods=['POST'])
def add_editorial():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		# validate the received values
		if _nombre and request.method == 'POST':
			# save edits
			sql = "INSERT INTO Editorial(nombre) VALUES(%s)"
			data = (_nombre,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Editorial agregada exitosamente!')
			return redirect('/Editorial')
		else:
			return 'Error mientras se agregaba la editorial'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Editorial')
def editorial():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id, Nombre FROM Editorial")
		rows = cursor.fetchall()
		table = ResultsEditorial(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		return render_template('Editorial/editorial.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/Editorial/edit/<int:id>')
def edit_view_editorial(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Editorial WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('Editorial/edit.html', row=row)
		else:
			return 'Error al cargar #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/Editorial/update', methods=['POST'])
def update_editorial():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		_id = request.form['id']
		# validate the received values
		if _nombre and request.method == 'POST':
			sql = "UPDATE Editorial SET nombre=%s WHERE id=%s"
			data = (_nombre, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Editorial Actualizada Exitosamente!')
			return redirect('/Editorial')
		else:
			return 'Error al actualizar la Editorial!'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Editorial/delete/<int:id>')
def delete_editorial(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Editorial WHERE id=%s", (id,))
		conn.commit()
		flash('Editorial Eliminada Exitosamente!')
		return redirect('/Editorial')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

##aqui comienza AUTORES

@app.route('/Autor/new_autor')
def add_autor_view():
	return render_template('Autor/add.html')
		
@app.route('/Autor/add', methods=['POST'])
def add_Autor():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		# validate the received values
		if _nombre and request.method == 'POST':
			# save edits
			sql = "INSERT INTO autor(nombre) VALUES(%s)"
			data = (_nombre,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Autor agregado exitosamente!')
			return redirect('/Autor')
		else:
			return 'Error mientras se agregaba el Autor'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Autor')
def autor():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id, Nombre FROM autor")
		rows = cursor.fetchall()
		table = ResultsAutor(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		print("aQUI borrame")
		return render_template('Autor/autor.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/Autor/edit/<int:id>')
def edit_view_autor(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Autor WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('Autor/edit.html', row=row)
		else:
			return 'Error al cargar #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/Autor/update', methods=['POST'])
def update_autor():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		_id = request.form['id']
		# validate the received values
		if _nombre and request.method == 'POST':
			sql = "UPDATE Autor SET nombre=%s WHERE id=%s"
			data = (_nombre, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Autor Actualizada Exitosamente!')
			return redirect('/Autor')
		else:
			return 'Error al actualizar el Autor!'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Autor/delete/<int:id>')
def delete_autor(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Autor WHERE id=%s", (id,))
		conn.commit()
		flash('Autor Eliminada Exitosamente!')
		return redirect('/Autor')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

##aqui comienza Areas

@app.route('/Area/new_area')
def add_area_view():
	return render_template('Areas/add.html')
		
@app.route('/Area/add', methods=['POST'])
def add_Area():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		# validate the received values
		if _nombre and  request.method == 'POST':
			# save edits
			sql = "INSERT INTO area(area) VALUES(%s)"
			data = (_nombre,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Area agregada exitosamente!')
			return redirect('/Area')
		else:
			return 'Error mientras se agregaba el Area'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Area')
def area():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id, area as Nombre FROM area")
		rows = cursor.fetchall()
		table = ResultsArea(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		return render_template('Areas/area.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/Area/edit/<int:id>')
def edit_view_area(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Area WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('Areas/edit.html', row=row)
		else:
			return 'Error al cargar #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/Area/update', methods=['POST'])
def update_area():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		_id = request.form['id']
		# validate the received values
		if _nombre and request.method == 'POST':
			sql = "UPDATE Area SET area=%s WHERE id=%s"
			data = (_nombre, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Area Actualizada Exitosamente!')
			return redirect('/Area')
		else:
			return 'Error al actualizar el Area!'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Area/delete/<int:id>')
def delete_area(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Area WHERE id=%s", (id,))
		conn.commit()
		flash('Area Eliminada Exitosamente!')
		return redirect('/Area')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


##aqui comienza Tipo/Genero

@app.route('/Tipo/new_area')
def add_tipo_view():
	return render_template('Tipo/add.html')
		
@app.route('/Tipo/add', methods=['POST'])
def add_tipo():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		_desc = request.form['inputDesc']
		# validate the received values
		if _nombre and _desc and request.method == 'POST':
			# save edits
			sql = "INSERT INTO tipo(tipo,Descr) VALUES(%s,%s)"
			data = (_nombre,_desc,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Género agregada exitosamente!')
			return redirect('/Tipo')
		else:
			return 'Error mientras se agregaba el Género'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Tipo')
def tipo():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id,Tipo,Descr FROM Tipo")
		rows = cursor.fetchall()
		table = ResultsTipo(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		return render_template('Tipo/Genero.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/Tipo/edit/<int:id>')
def edit_view_tipo(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Tipo WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('Tipo/edit.html', row=row)
		else:
			return 'Error al cargar #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/Tipo/update', methods=['POST'])
def update_tipo():
	conn = None
	cursor = None
	try:		
		_nombre = request.form['inputNombre']
		_desc = request.form['inputDesc']
		_id = request.form['id']
		# validate the received values
		if _nombre and request.method == 'POST':
			sql = "UPDATE tipo SET tipo=%s, descr=%s WHERE id=%s"
			data = (_nombre,_desc, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Género Actualizado Exitosamente!')
			return redirect('/Tipo')
		else:
			return 'Error al actualizar el Género!'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Tipo/delete/<int:id>')
def delete_tipo(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Tipo WHERE id=%s", (id,))
		conn.commit()
		flash('Género Eliminado Exitosamente!')
		return redirect('/Tipo')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


##aqui comienza CIUDAD

@app.route('/Ciudad/new_ciudad')
def add_ciudad_view():
	return render_template('Ciudad/add.html')
		
@app.route('/Ciudad/add', methods=['POST'])
def add_ciudad():
	conn = None
	cursor = None
	try:		
		_pais = request.form['inputPais']
		_ciudad = request.form['inputCiudad']
		# validate the received values
		if _pais and _ciudad and request.method == 'POST':
			# save edits
			sql = "INSERT INTO ciudad(Pais,Ciudad) VALUES(%s,%s)"
			data = (_pais, _ciudad,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Ciudad agregada exitosamente!')
			return redirect('/Ciudad')
		else:
			return 'Error mientras se agregaba la Ciudad'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Ciudad')
def ciudad():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id,Pais,Ciudad FROM Ciudad")
		rows = cursor.fetchall()
		table = ResultsCiudad(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		return render_template('Ciudad/Ciudad.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/Ciudad/edit/<int:id>')
def edit_view_ciudad(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Ciudad WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('Ciudad/edit.html', row=row)
		else:
			return 'Error al cargar #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/Ciudad/update', methods=['POST'])
def update_ciudad():
	conn = None
	cursor = None
	try:		
		_pais = request.form['inputPais']
		_ciudad = request.form['inputCiudad']
		_id = request.form['id']
		# validate the received values
		if _pais and _ciudad and request.method == 'POST':
			sql = "UPDATE ciudad SET pais=%s, ciudad=%s WHERE id=%s"
			data = (_pais,_ciudad, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Ciudad Actualizada Exitosamente!')
			return redirect('/Ciudad')
		else:
			return 'Error al actualizar la Ciudad!'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/Ciudad/delete/<int:id>')
def delete_ciudad(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM ciudad WHERE id=%s", (id,))
		conn.commit()
		flash('Ciudad Eliminada Exitosamente!')
		return redirect('/Ciudad')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

##aqui comienza TPrestamo

@app.route('/TPrestamo/new_tprestamo')
def add_tprestamo_view():
	return render_template('TPrestamo/add.html')
		
@app.route('/TPrestamo/add', methods=['POST'])
def add_tprestamo():
	conn = None
	cursor = None
	try:		
		_tipo = request.form['inputTipo']
		_descr = request.form['inputDescr']
		# validate the received values
		if _tipo and _descr and request.method == 'POST':
			# save edits
			sql = "INSERT INTO t_prestamo(tipo,Descripcion) VALUES(%s,%s)"
			data = (_tipo, _descr,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Tipo de prestamo agregado exitosamente!')
			return redirect('/TPrestamo')
		else:
			return 'Error mientras se agregaba el tipo de prestamo'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/TPrestamo')
def tprestamo():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id,Tipo,Descripcion FROM t_prestamo")
		rows = cursor.fetchall()
		table = ResultsTPrestamo(rows)
		table.border = True
		table.classes=["table table-bordered"]
		table.table_id='dataTable'
		return render_template('TPrestamo/TPrestamo.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/TPrestamo/edit/<int:id>')
def edit_view_tprestamo(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT Id,Tipo,Descripcion FROM T_Prestamo WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('TPrestamo/edit.html', row=row)
		else:
			return 'Error al cargar #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route('/TPrestamo/update', methods=['POST'])
def update_tprestamo():
	conn = None
	cursor = None
	try:		
		_tipo = request.form['inputTipo']
		_descr = request.form['inputDescr']
		_id = request.form['id']
		# validate the received values
		if _tipo and _descr and request.method == 'POST':
			sql = "UPDATE t_prestamo SET tipo=%s, descripcion=%s WHERE id=%s"
			data = (_tipo,_descr, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Tipo de prestamo Actualizado Exitosamente!')
			return redirect('/TPrestamo')
		else:
			return 'Error al actualizar el tipo de prestamo!'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/TPrestamo/delete/<int:id>')
def delete_tprestamo(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM t_prestamo WHERE id=%s", (id,))
		conn.commit()
		flash('tipo de prestamo eliminado Exitosamente!')
		return redirect('/TPrestamo')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

##aqui comienza Permisos


if __name__ == "__main__":
    app.run(port=5001, debug="true")
