from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, Pemilih, User # Import model Pemilih dari models.py
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://lbw:miqlbw02@mysql/lbw?charset=utf8mb4&collation=utf8mb4_general_ci"  # Ganti dengan URL database yang sesuai
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:@localhost/lbw?charset=utf8mb4&collation=utf8mb4_general_ci"
app.config['SECRET_KEY'] = 'miqlbw02'
db.init_app(app)
def create_app():
    with app.app_context():
        db.create_all()

        # Cek apakah pengguna Admin dan Input sudah ada
        admin_user = User.query.filter_by(email='admin@mail.com').first()
        input_user = User.query.filter_by(email='input@mail.com').first()

        # Jika tidak ada, tambahkan ke database
        if not admin_user:
            admin_user = User(nama='Admin', email='admin@mail.com', password='admin_password', role='Admin')
            db.session.add(admin_user)

        if not input_user:
            input_user = User(nama='Input', email='input@mail.com', password='input_password', role='Input')
            db.session.add(input_user)

        db.session.commit()

    return app
@app.route('/')
def home():
    if 'email' in session:
        # Pengguna sudah login, mungkin diarahkan ke halaman lain
        return redirect(url_for('display'))
    return render_template('login.html')

# @app.route('/display')
# def display():
#     if 'email' in session:
#         # Ambil data Pemilih dari database
#         pemilih_list = Pemilih.query.all()

#         # Create a list of dictionaries from the Pemilih objects
#         pemilih_data = [
#             {
#                 'index': index + 1,
#                 'nama': pemilih.nama,
#                 'no_ktp': pemilih.no_ktp,
#                 'alamat': f"{pemilih.kecamatan} - {pemilih.kelurahan}",
#                 'koordinator': pemilih.koordinator,
#             }
#             for index, pemilih in enumerate(pemilih_list)
#         ]

#         # render the template and pass the JSON data as context
#         return render_template('display.html', pemilih_data=jsonify(pemilih_data))
#         # return jsonify(pemilih_data)
#     else:
#         return redirect(url_for('login'))


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
            # Ambil data dari formulir
            nama = request.form['nama']
            no_ktp = request.form['noKTP']
            kecamatan = request.form['Kecamatan']
            kelurahan = request.form['Kelurahan']
            koordinator = request.form['koordinator']
            existing_pemilih = Pemilih.query.filter_by(no_ktp=no_ktp).first()
            if existing_pemilih:
                # Jika sudah ada, berikan keterangan "DATA SAMA"
                existing_pemilih.keterangan = 'DATA SAMA'
                existing_koordinator = existing_pemilih.koordinator
                db.session.commit()
                print("masuk sini")
                return jsonify({'success': False, 'message': f'Data Sama dengan koordinator {existing_koordinator}'})
            else:
                
                # Simpan data ke dalam database
                new_pemilih = Pemilih(nama=nama, no_ktp=no_ktp, kecamatan=kecamatan, kelurahan=kelurahan, koordinator=koordinator)
                db.session.add(new_pemilih)
                db.session.commit()

            # Beri respons JSON bahwa penyimpanan berhasil
                return jsonify({'success': True, 'message': 'Data berhasil ditambahkan'})
        else:
            return render_template('input.html', success_message='Input Data')

    else:
        return redirect(url_for('login'))
    
@app.route('/edit/<no_ktp>', methods=['POST'])
def edit(no_ktp):
    if request.method == 'POST':
        # Ambil data yang dikirimkan dari form edit
        # edited_nama = request.form['editedNama']
        # edited_no_ktp = request.form['editedNoKTP']
        # edited_alamat = request.form['editedAlamat']
        # edited_koordinator = request.form['editedKoordinator']
        edited_tps = request.form['editedTPS']
        edited_keterangan = request.form['editedKeterangan']

        # Ambil data pemilih dari database berdasarkan no_ktp
        pemilih = Pemilih.query.filter_by(no_ktp=no_ktp).first()

        # Update nilai-nilai yang diubah
        # pemilih.nama = edited_nama
        # pemilih.no_ktp = edited_no_ktp
        # pemilih.alamat = edited_alamat
        # pemilih.koordinator = edited_koordinator
        pemilih.tps = edited_tps
        pemilih.keterangan = edited_keterangan

        # Commit perubahan ke dalam database
        db.session.add(pemilih)
        db.session.commit()

        # Redirect kembali ke halaman display setelah mengedit data
        return redirect(url_for('display'))
    
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
