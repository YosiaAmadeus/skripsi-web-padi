from flask import Flask, render_template, request, redirect, url_for, send_file, session
import pandas as pd
import os
from werkzeug.utils import secure_filename
from clustering_functions import run_kmeans, run_fuzzy  # Import fungsi clustering

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'static/results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Endpoint untuk halaman home
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint untuk menjalankan clustering
@app.route('/run-clustering', methods=['POST'])
def run_clustering():
    # Mendapatkan data file yang diunggah, jumlah cluster, dan algoritma
    file = request.files['dataset']
    clusters = int(request.form['clusters'])
    algorithm = request.form['algorithm']
    
    # Menyimpan file yang diunggah
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filepath)
    
    # Membaca data yang diunggah pengguna
    data = pd.read_excel(filepath)
    
    # Menjalankan model sesuai pilihan user
    if algorithm == 'kmeans':
        result_path, fig_path = run_kmeans(data, clusters)
    elif algorithm == 'fuzzy':
        result_path, fig_path = run_fuzzy(data, clusters)
    
    # Menyimpan hasil dan gambar
    session['result_path'] = result_path
    session['fig_path'] = fig_path
    
    # Redirect ke halaman "Clustering"
    return redirect(url_for('clustering'))

# Endpoint untuk halaman Clustering
@app.route('/clustering')
def clustering():
    # Mendapatkan hasil dan visualisasi dari sesi
    result_path = session.get('result_path')
    fig_path = session.get('fig_path')
    
    return render_template('clustering.html', result_path=result_path, fig_path=fig_path)

if __name__ == '__main__':
    app.run(debug=True)
