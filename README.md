# Meatwatch_model
Klasifikasi kesegaran daging menggunakan 3 jenis daging
Dataset : https://drive.google.com/file/d/1lvRFYWOo86pGOOFdSCBTvaQ7ywmdDqut/view?usp=sharing

# How to run on windows:
## create virtual environment
python -m venv venv

## install dependencies
pip install -r requirements.txt

## run app.py
python app.py

## open postman
method [POST] http://localhost:5000/predict

form-data: file → select photos
![image](https://github.com/user-attachments/assets/3a73fe39-48ed-4a93-9462-8a6c97dabc85)

