from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
import paho.mqtt.client as mqtt_client
import json
import requests
import datetime

# Config
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask-monitoring'

mysql = MySQL(app)

#Memanggil about
@app.route('/', methods=['GET'])
def about():

    return render_template('about.html')

#Ruangan Server 1

# Fungsi untuk mengubah data dashboard dalam format JSON
def to_json(temp, hum, getstatus):
    data = {'temp': temp, 'hum': hum, 'getstatus': getstatus}
    return json.dumps(data)

# Fungsi untuk mengirim data ke dashboard
@app.route('/data', methods=['GET'])
def data():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM data ORDER BY id DESC LIMIT 1')
    except Exception as e:
        return jsonify({"error": "Koneksi ke MySQL gagal"}), 500

    # Kirim data suhu dan kelembaban dari database MySQL ke halaman website
    data = cur.fetchone()
    temp = data[3]
    hum = data[4]
    getstatus = data[5]
    data = to_json(temp, hum, getstatus)
    return data

#Mengambil data untuk table
@app.route('/jsontable', methods=['GET'])
def tablechart():
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM data ORDER BY id DESC LIMIT 100")
    except Exception as e:
        return jsonify({"error": "Koneksi ke MySQL gagal"}), 500

    tabel = cur.fetchall()
    data = []
    for t in tabel:
        data.append({'id': t[0], 'tanggal': str(t[6]), 'temp': t[3], 'hum': t[4], 'gas': t[1], 'status': t[5] })
    return jsonify({'data':data})

#Mengambil data untuk grafik
@app.route('/json-chart', methods=['GET'])
def x_chart():
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM data ORDER BY id DESC LIMIT 50")
    except Exception as e:
        return jsonify({"error": "Koneksi ke MySQL gagal"}), 500

    tabel = cur.fetchall()
    data = []
    for t in tabel:
        data.append({'id': t[0], 'tanggal': str(t[6]), 'temp': t[3], 'hum': t[4], 'status': t[5], 'gas': t[1] })
    return jsonify({'data': data})

#Memanggil dahsboard
@app.route('/dash', methods=['GET'])
def dashboard():

    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True,)
