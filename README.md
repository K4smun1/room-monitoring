# Monitoring dengan flask

## Deskripsi
Website untuk monitoring ruangan.
- Menggunakan MySQL untuk database management
- Membuat windows service untuk menerima data dari broker MQTT dan menyimpan ke database
- Python WebApp sebagai GUI monitoring melalui browser

## Instalasi

### Instalasi Modul

```
$ pip install -r requirements.txt
```

### Membuat database
 * Install MySQL Server & MySQL Workbench
 * Buka MySQL Workbench lalu buat _schema_ baru dengan nama `flask-monitoring`
 * Buka _SQL Script_ lalu pilih `flask-monitoring.sql` pada folder `db`
 * Dobel klik _schema_ untuk mengaktifkan, lalu jalankan script

### Instalasi service
- Pada folder `service`, buka `listenerWrapper.py` dengan text editor lalu sesuaikan konfigurasi MySQL dan MQTT
- Jalankan `install-service.ps1`

```
$ .\service\install-service.ps1
```

### Memulai service

```
$ sc.exe start mqttlistener
```

### Memulai web
- Pada folder `app`, buka `app.py` dengan text editor lalu sesuaikan konfigurasi MySQL
- Jalankan `app.py` untuk memulai WebApp

```
$ python .\app\app.py
```

- Buka alamat yang dihasilkan WebApp dengan browser

### Menutup service

```
$ sc.exe stop mqttlistener
```
