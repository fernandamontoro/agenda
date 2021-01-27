from flask import * 
import mysql.connector

db = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "root",
	database = "Proyecto"
)

cursor = db.cursor()

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

@app.route('/')
def presentacion():
	return render_template("presentacion.html")

@app.route("/index", methods=["GET", "POST"])
def index():
	
	if (request.method == "POST"):
		usuario = request.form['usuario']
		contrasena = request.form['contrasena']
		
		if ((usuario == "Fernanda") and (contrasena == "123")):
			return redirect(url_for("clientes"))
			
	return render_template("index.html")

@app.route('/registro', methods=['GET', 'POST'])
def registro():
	mensaje=""
	msg=""
	if request.method=='POST':
		pwd = request.form["pwd"]
		password = request.form["password"]
		if pwd != password:
			mensaje = "Contraseñas no coinciden, intenta de nuevo!"
			return render_template("registro.html", mensaje = mensaje)
		else:
			#Crear usuario en la base de datos
			nombre=request.form["nombre_usuario"]
			correo=request.form["email"]
			pwd = request.form["pwd"]
			print(nombre,correo,pwd)
			# Crear objeto para el registro del usuario
			usuario = Usuario(
				nombre = nombre,
				email = correo,
				pwd = bcrypt.generate_password_hash(pwd).decode('utf-8')
			)
			db.session.add(usuario)
			db.session.commit()

			mensaje = "Usuario registrado!"
			#Enviar correo
			msg = Message("Gracias por registrarte en ..", sender="AQUI_CORREO", recipients=[correo])
			msg.body = "Este es un email de prueba"
			msg.html = "<p>Este es un email</p>"
			mail.send(msg)
			return render_template("registro.html", mensaje = mensaje)
	return render_template("registro.html", mensaje = mensaje)

@app.route("/loginin" , methods=['GET','POST'])
def loginin():
	if request.method == 'POST':
		#Query filter_by por email
		email = request.form["email"]
		pwd = request.form["pwd"]
		usuario_exite = Usuario.query.filter_by(email=email).first()
		print(usuario_exite)
		mensaje= usuario_exite.email
		#Si lo encuentra entonces
		if usuario_exite != None:
			print("Existe")
			if bcrypt.check_password_hash(usuario_exite.pwd, pwd):
				print("Usuario autenticado")
				# Aquí se agregó el método login_user para vincular
				# el usuario autenticado a la sesión
				login_user(usuario_exite)
				
				if current_user.is_authenticated:
					flash("Inicio de Sesión Exitoso!!")
					return redirect("/principal")
					
		return render_template("login.html", mensaje = mensaje)
	print("Login in...")
	return render_template("login.html")

@app.route("/clientes", methods=["GET", "POST"])
def clientes():
	
	cursor.execute("select * from Cliente;")
	result = cursor.fetchall()
	
	if (request.method == "POST"):
		
		if (request.form['boton'] == "agregar"):
			nombre = request.form['c1f0']
			rfc = request.form['c2f0']
			telefono = request.form['c3f0']
			direccion = request.form['c4f0']
			celular = request.form['c5f0']
			correo = request.form['c6f0']
			
			cursor.execute(f"insert into Cliente values(null, '{nombre}', '{rfc}', '{telefono}', '{direccion}', '{celular}', '{correo}');")
			db.commit()
			
		else:
			for row in result:
				cadena = "eliminar"
				if (request.form['boton'] == f"eliminar{row[0]}"):
					cursor.execute(f"delete from Cliente where id = {row[0]}")
					db.commit()
					
				elif (request.form['boton'] == f"editar{row[0]}"):
					return render_template("clientes.html", result = result, update = row[0])
					
				elif (request.form['boton'] == f"aceptar{row[0]}"):
					#try:
					nombre = request.form[f'c1f{row[0]}']
					#except:
						#return("dsfsf")
					rfc = request.form[f'c2f{row[0]}']
					telefono = request.form[f'c3f{row[0]}']
					direccion = request.form[f'c4f{row[0]}']
					celular = request.form[f'c5f{row[0]}']
					correo = request.form[f'c6f{row[0]}']
					cursor.execute(f"update Cliente set nombre = '{nombre}', rfc = '{rfc}', telefono = '{telefono}', direccion = '{direccion}', celular = '{celular}', correo = '{correo}' where id = {row[0]};")
					db.commit()
					
		cursor.execute("select * from Cliente;")
		result = cursor.fetchall()
	return render_template("clientes.html", result = result, update = -1)

#@app.route('/registro')
#def registro():
#	return render_template("registro.html")

@app.route('/correo')
def correo():
	return render_template("correo.html")

if __name__ == "__main__":
	app.run(debug = True)
