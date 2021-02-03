from flask import * 
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
import os


db = mysql.connector.connect(
	host = "fernandamontoro.mysql.pythonanywhere-services.com", 
	user = "root",
	password = "root",
	database = "Proyecto"
)

cursor = db.cursor()

app = Flask(__name__)

app.secret_key = 'my unobvious secret key'
app.config['SERVER_NAME'] = 'localhost:5000'

app.config['MAIL_SERVER'] ='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']  = 'fernandamontoro7@gmail.com'
app.config['MAIL_PASSWORD']  = 'ficam40ph'

login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.login_message_category = 'info'

mail = Mail(app)

@app.route('/')
def presentacion():
	return render_template("presentacion.html")

@app.route("/index")
def index():
	if (len(session) == 0):
		return render_template("index.html")
	
	return redirect(url_for("clientes"))
			

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
					nombre = request.form[f'c1f{row[0]}']
					rfc = request.form[f'c2f{row[0]}']
					telefono = request.form[f'c3f{row[0]}']
					direccion = request.form[f'c4f{row[0]}']
					celular = request.form[f'c5f{row[0]}']
					correo = request.form[f'c6f{row[0]}']
					cursor.execute(f"update Cliente set nombre = '{nombre}', rfc = '{rfc}', telefono = '{telefono}', direccion = '{direccion}', celular = '{celular}', correo = '{correo}' where id = {row[0]};")
					db.commit()
					
		cursor.execute("select * from Cliente;")
		result = cursor.fetchall()
	if (len(session) == 0):
		return redirect(url_for('presentacion'))
	return render_template("clientes.html", result = result, update = -1)

@app.route('/registro', methods=["GET", "POST"])
def registro():
	if (request.method == "GET"):
		return render_template("registro.html")
	else:
		nombre = request.form['nombre_usuario']
		email = request.form['email']
		telefono = request.form['telefono']
		pwd = request.form['pwd']
		
		cursor.execute(f"INSERT INTO Usuario (nombre, email, telefono, pwd) VALUE('{nombre}', '{email}', '{telefono}', '{pwd}');")
		db.commit()

	msg = Message("Gracias por Registrarte", sender="fernandamontoro7@gmail.com", recipients=[email])
	msg.body = '''
	Bienvenid@ a tu agenda!!!
	'''
	mail.send(msg)

	return redirect(url_for('index'))

@app.route('/login', methods=["POST"])
def login():
		nombre = request.form['usuario']
		pwd = request.form['contrasena']
			
		cursor.execute(f"SELECT * FROM usuario WHERE nombre = '{nombre}' AND pwd = '{pwd}';")

		result = cursor.fetchall()

		if (len(result) == 0) :
			return redirect(url_for('index'))
		else :
			session['nombre'] = result[0][1]
			session['email'] = result[0][2]
			session['telefono'] = result[0][3]
			return redirect(url_for('clientes'))

@app.route('/logout')
def logout():
		session.clear()
		return redirect(url_for('presentacion'))


@app.route('/correo')
def correo():
	return render_template("correo.html")

if __name__ == "__main__":
	app.run(debug = True)
