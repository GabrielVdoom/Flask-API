from main import app
from flask import render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app.json.ensure_ascii = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def homepage():
    return jsonify({"message": "Bem-vindo à API"})

@app.route('/users', methods=['GET'])# Rota para obter a lista de todos os usuários
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(users_list)


@app.route('/users_list_html')
def users_html():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user_form():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if User.query.filter_by(name=name).first():
            return "Usuário já existe!", 409

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return "Usuário cadastrado com sucesso!"

    # Se for GET, apenas mostra o formulário
    return render_template('add_user.html')


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']

    user = User.query.filter_by(name=name).first()  # busca só pelo nome

    # Verifica se o usuário existe e se a senha confere, tudo em uma linha
    if user and check_password_hash(user.password, password):
        return f"Bem-vindo, {user.name}!"
    else:
        return "Nome ou senha incorretos!", 401


