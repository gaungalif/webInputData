from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, Pemilih, User # Import model Pemilih dari models.py
from flask_sqlalchemy import SQLAlchemy
import requests
import time


app = Flask(__name__, static_folder='static', template_folder='templates')
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://lbw:miqlbw02@mysql/lbw?charset=utf8mb4&collation=utf8mb4_general_ci"  # Ganti dengan URL database yang sesuai
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:@localhost/lbw?charset=utf8mb4&collation=utf8mb4_general_ci"
app.config['SECRET_KEY'] = 'miqlbw02'
db.init_app(app)
def create_app():
    with app.app_context():
        db.create_all()

        # Cek apakah pengguna Admin dan Input sudah ada
        min0 = User.query.filter_by(email='min0').first()
        min1 = User.query.filter_by(email='min1').first()
        min2 = User.query.filter_by(email='min2').first()
        min3 = User.query.filter_by(email='min3').first()
        # Jika tidak ada, tambahkan ke database
        if not min0:
            admin_user = User(nama='Admin0', email='min0', password='mimin123', role='Admin')
            db.session.add(admin_user)
        if not min1:
            admin_user = User(nama='Admin1', email='min1', password='mimin123', role='Admin')
            db.session.add(admin_user)
        if not min2:
            admin_user = User(nama='Admin2', email='min2', password='mimin123', role='Admin')
            db.session.add(admin_user)
        if not min3:
            admin_user = User(nama='Admin3', email='min3', password='mimin123', role='Admin')
            db.session.add(admin_user)   

        db.session.commit()

    return app
@app.route('/')
def home():
    if 'email' in session:
        # Pengguna sudah login, mungkin diarahkan ke halaman lain
        return redirect(url_for('display'))
    return render_template('login.html')
  
# @app.route('/cek_data', methods=['POST'])
# def check_data():
#     data = request.json
#     nik = data['nik']
#     koordinator = data['koordinator']
    
#     existing_pemilih = Pemilih.query.filter_by(no_ktp=nik).first()
#     if existing_pemilih and existing_pemilih.koordinator == koordinator and existing_pemilih.tps is (not None or not ''):
#         return jsonify({'success': False, 'message': f'Data Sudah'})
    
#     elif existing_pemilih and existing_pemilih.koordinator != koordinator:
#         # Jika sudah ada, berikan keterangan "DATA SAMA"
#         existing_pemilih.keterangan = f'DATA SAMA dengan {koordinator}'
#         existing_koordinator = existing_pemilih.koordinator
#         db.session.commit()
#         return jsonify({'success': False, 'message': f'Data Sama dengan koordinator {existing_koordinator}'})
#     else:
#         url = "https://cek-dpt-online.p.rapidapi.com/api/v3/check"
#         querystring = {"nik": nik}
#         headers = {
#             # "X-RapidAPI-Key": "511faddf5fmsh9938236d6c2b247p16317bjsnbba1e102c7af",
#             "X-RapidAPI-Key": "95f507feb8msh5fd6388bd26f648p1af532jsnbe2f0dbd12d2",
#             "X-RapidAPI-Host": "cek-dpt-online.p.rapidapi.com"
#         }


#         response = requests.get(url, headers=headers, params=querystring)
#         return response.json()
# Endpoint untuk pengecekan data ganda
@app.route('/cek_data_ganda', methods=['POST'])
def check_data_ganda():
    data = request.json
    nik = data['nik']
    koordinator = data['koordinator']

    existing_pemilih = Pemilih.query.filter_by(no_ktp=nik).first()
    if existing_pemilih and existing_pemilih.koordinator == koordinator and existing_pemilih.tps is not None:
        return jsonify({'success': False, 'message': f'Data Sudah'})
    
    elif existing_pemilih and existing_pemilih.koordinator != koordinator:
        existing_pemilih.keterangan = f'DATA SAMA dengan {koordinator}'
        existing_koordinator = existing_pemilih.koordinator
        db.session.commit()
        return jsonify({'success': False, 'message': f'Data Sama dengan koordinator {existing_koordinator}'})
    
    else:
        return jsonify({'success': True, 'message': 'Data Tidak Sama'})

# Endpoint untuk pengecekan NIK DPT
@app.route('/cek_nik_dpt', methods=['POST'])
def check_nik_dpt():
    data = request.json
    nik = data['nik']

    existing_pemilih = Pemilih.query.filter_by(no_ktp=nik).first()
    if existing_pemilih:
        return jsonify({'success': False, 'message': 'NIK DPT sudah ada'})
    
    else:
        # Lakukan pengecekan ke API eksternal atau proses lainnya
        url = "https://cek-dpt-online.p.rapidapi.com/api/v3/check"
        querystring = {"nik": nik}
        headers = {
            "X-RapidAPI-Key": "95f507feb8msh5fd6388bd26f648p1af532jsnbe2f0dbd12d2",
            "X-RapidAPI-Host": "cek-dpt-online.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
# Route untuk menghapus data
@app.route('/delete/<int:no_ktp>', methods=['DELETE'])
def delete_pemilih(no_ktp):
    if request.method == 'DELETE':
        pemilih = Pemilih.query.filter_by(no_ktp=no_ktp).first()

        try:
            db.session.delete(pemilih)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Data berhasil dihapus'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return redirect(url_for('display'))

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
            tps = request.form['tps']
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
                new_pemilih = Pemilih(nama=nama, no_ktp=no_ktp, kecamatan=kecamatan, kelurahan=kelurahan, koordinator=koordinator,tps=tps)
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
def update_tps_data_batch(batch_size=2, delay_seconds=2):
    # Ambil data pemilih yang belum memiliki TPS
    pemilih_belum_tps = Pemilih.query.filter_by(tps=None).limit(batch_size).all()

    # List untuk menyimpan perubahan
    perubahan_data = []

    # Loop melalui setiap pemilih
    for pemilih in pemilih_belum_tps:
        # Request data dari API dengan delay
        time.sleep(delay_seconds)

        url = "https://cek-dpt-online.p.rapidapi.com/api/v3/check"
        querystring = {"nik": pemilih.no_ktp}
        headers = {
            "X-RapidAPI-Key": "95f507feb8msh5fd6388bd26f648p1af532jsnbe2f0dbd12d2",
            "X-RapidAPI-Host": "cek-dpt-online.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data_api = response.json()

        # Update data di database berdasarkan response dari API
        pemilih.nama = data_api.get('nama', pemilih.nama)
        pemilih.kecamatan = data_api.get('kecamatan', pemilih.kecamatan)
        pemilih.kelurahan = data_api.get('kelurahan', pemilih.kelurahan)
        if 'results' in data_api:
            # Periksa apakah 'realtime_data' ada dalam response
            realtime_data = data_api['results'].get('realtime_data')
            if realtime_data:
                # Periksa apakah 'findNikSidalih' ada dalam response
                findNikSidalih = realtime_data.get('findNikSidalih')
                if findNikSidalih:
                    # Periksa apakah 'tps' ada dalam response
                    pemilih.tps = findNikSidalih.get('tps', pemilih.tps)
                else:
                    # Jika valid = false, ganti nilai tps dengan "cek"
                    pemilih.tps = "cek dpt"

        # Tambahkan perubahan ke list
        perubahan_data.append({
            'nik': pemilih.no_ktp,
            'nama': pemilih.nama,
            'kecamatan': pemilih.kecamatan,
            'kelurahan': pemilih.kelurahan,
            'tps': pemilih.tps
        })
        db.session.commit()

    # Commit perubahan ke database

    return jsonify({'success': True, 'message': 'Data TPS telah diperbarui', 'perubahan_data': perubahan_data})

# Buat route untuk melakukan perubahan pada data
@app.route('/update_tps_data')
def update_tps_data():
    return update_tps_data_batch()


if __name__ == '__main__':
    create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
