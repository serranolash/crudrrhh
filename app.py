from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

import requests

app = Flask(__name__)
app.secret_key = 'SUPER_ALEX'



login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

API_URL = "http://190.220.155.74:8008/api.Dragonfish/"
HEADERS = {
    "IdCliente": "APIALEX",
    "BaseDeDatos": "",
    "Authorization": ""
}
# Modelo de usuario para el login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar las credenciales del usuario
        if username == 'admin' and password == 'admin123':
            # Crear un objeto User y registrar la sesión del usuario
            user = User(1)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas', 'error')

    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("index"))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        funcion = request.form['funcion']
        if funcion == 'alta_vendedor':
            HEADERS['BaseDeDatos'] = request.form['base_de_datos']
            return render_template('alta_vendedor.html')
        elif funcion == 'alta_empleados':
            HEADERS['BaseDeDatos'] = request.form['base_de_datos']
            return render_template('alta_empleados.html')

    return render_template('index.html')

@app.route('/alta_vendedor', methods=['POST'])
@login_required
def alta_vendedor():
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    numero_documento = request.form['numero_documento']

    payload = {
        "Codigo": codigo,
        "Nombre": nombre,
        "NroDocumento": numero_documento
    }

    response = requests.post(API_URL + "Vendedor/", headers=HEADERS, json=payload)

    print("Respuesta de la API:", response.status_code, response.text)

    if response.status_code == 201:  # Cambiamos el código de respuesta esperado a 201 (Created)
        flash("Vendedor dado de alta correctamente", "success")
        return redirect(url_for('index'))
    elif response.status_code == 409:
        return "El número ingresado ya está asignado a otro empleado"
    else:
        return "Error al dar de alta al vendedor"


@app.route('/alta_empleados', methods=['POST'])
@login_required
def alta_empleados():
    codigo = request.form['codigo']
    primer_nombre = request.form['primer_nombre']
    apellido = request.form['apellido']
    numero_documento = request.form['numero_documento']

    payload = {
        "Codigo": codigo,
        "PrimerNombre": primer_nombre,
        "Apellido": apellido,
        "NroDocumento": numero_documento
    }

    response = requests.post(API_URL + "Cliente/", headers=HEADERS, json=payload)

    print("Respuesta de la API:", response.status_code, response.text)

    if response.status_code == 201:  # Cambiamos el código de respuesta esperado a 201 (Created)
        flash("Empleado dado de alta correctamente", "success")
        return redirect(url_for('index'))  # Redirige al index.html
    elif response.status_code == 409:
        return "El número de documento ingresado ya está asignado a otro empleado"
    else:
        return "Error al dar de alta al empleado"



if __name__ == '__main__':
    app.run()
