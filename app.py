from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Inisialisasi app
app = Flask(__name__)
CORS(app)  # Biar bisa diakses dari frontend beda port

# Path model dan upload folder
MODEL_PATH = 'models/model.h5'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model
model = load_model(MODEL_PATH)

# List nama kelas sesuai urutan output model
class_names = ['Segar', 'Tidak Segar']

# Endpoint tes server jalan
@app.route('/')
def home():
    return 'MeatWatch API is running!'

# Endpoint prediksi gambar
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Simpan file upload ke folder uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Preprocessing gambar
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Prediksi
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    probability = float(np.max(predictions)) * 100  # jadi persentase
    probability = round(probability, 2)  # buletin 2 angka di belakang koma

    # Hapus gambar setelah diprediksi (opsional biar folder uploads gak numpuk)
    os.remove(file_path)

    # Return hasil
    return jsonify({
        'prediction': predicted_class,
        'probability (%)': probability
    })

# Run app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
