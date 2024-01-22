from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Pemilih, User # Import model Pemilih dari models.py
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Ganti dengan URL database yang sesuai
app.config['SECRET_KEY'] = 'miqlbw02'
db.init_app(app)
def create_app():
    with app.app_context():
        db.create_all()
        admin_user = User(nama='Admin', email='admin@mail.com', password='admin_password', role='Admin')
        input_user = User(nama='Input', email='input@mail.com', password='input_password', role='Input')
        db.session.add(admin_user)
        db.session.commit()

    return app
@app.route('/')
def home():
    if 'email' in session:
        # Pengguna sudah login, mungkin diarahkan ke halaman lain
        return redirect(url_for('display'))
    return render_template('login.html')

@app.route('/display')
def display():
    if 'email' in session:
        # Ambil data Pemilih dari database
        pemilih_list = Pemilih.query.all()
        return render_template('display.html', pemilih_list=pemilih_list)
    else:
        return redirect(url_for('login'))


@app.route('/input', methods=['GET', 'POST'])
def input():
    if 'email' in session:
        if request.method == 'POST':
            return redirect(url_for('display'))
        else:
            return render_template('input.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'email' in session:
        # Logika untuk edit
        return render_template('edit.html')
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # Proses autentikasi di sini, gantilah sesuai dengan kebutuhan Anda
    email = request.form['email']
    password = request.form['password']

    # autentikasi user
    user = User.query.filter_by(email=email, password=password).first()
    if user is not None:
        # login berhasil
        session['email'] = email
        return redirect(url_for('display'))
    else:
        return render_template('login.html', message='Login failed. Username atau Password salah.')


if __name__ == '__main__':
    create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
