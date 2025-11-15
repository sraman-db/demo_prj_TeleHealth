🏥 TeleHealth Connect

A Django-based web application that helps users quickly locate and access medical help centers such as hospitals, clinics, and pharmacies, and provides an intelligent diagnosis assistant that predicts the department based on user symptoms.

This project uses MySQL, integrates interactive maps, and includes an ML pipeline for department prediction.

🌟 Features
🔹 Medical Center Locator

Interactive map showing nearby hospitals, clinics, and pharmacies

Map markers with detailed information

Location-based filtering

🔹 Symptom-Based Department Prediction

User enters symptoms

ML model predicts the correct medical department

Uses .joblib pipeline + preprocessing scripts

Supports synonyms, cleaned text, and mapping via JSON dictionaries

🔹 User-Friendly Navigation

Clean interface

Organized template structure

Modern CSS and JavaScript interactions


🧰 Tech Stack
Layer	Technology
Backend	Django 5.x
Frontend	HTML, CSS, JavaScript
Database	MySQL
Machine Learning	Scikit-learn, Joblib
Map Integration	Leaflet / Google Maps / OSM

📁 Project Structure
project_root/
│── manage.py
│── requirements.txt
│── README.md
│── .env (ignored)
│
├── tele_medicine/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── predictor.py
│   ├── text_extractor.py
│   ├── features.json
│   ├── synonyms.json
│   ├── label_encoder.joblib
│   ├── best_pipeline.joblib
│   ├── Department_Prediction.json
│   ├── templates/tele_medicine/
│   └── static/tele_medicine/
│
└── TeleHealth/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/sraman-db/demo_prj_TeleHealth.git
cd demo_prj_TeleHealth

2️⃣ Create a virtual environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure MySQL

Create .env in the root folder:

DB_NAME=telehealth_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_django_secret_key
DEBUG=True


Update settings.py to load environment variables.

5️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create a superuser
python manage.py createsuperuser

7️⃣ Start the server
python manage.py runserver

🔮 ML Prediction Pipeline

This project contains:

best_pipeline.joblib – main model

label_encoder.joblib – department encoder

features.json – feature mapping

synonyms.json – symptom synonyms

text_extractor.py – cleans and prepares text

predictor.py – final prediction script

Workflow:

User enters symptoms

Text is cleaned + synonyms mapped

Features extracted

ML model predicts department

Output displayed on UI

🌐 Map Integration

The system uses a JavaScript-based frontend map (Leaflet/OSM or Google Maps).
Features include:

Markers for hospitals / clinics / pharmacies

Pop-ups with center details

Dynamic map movement



🚀 Future Enhancements

Real-time doctor availability

Emergency SOS button

REST API for mobile apps

Authentication for patients and doctors

Chatbot for medical queries

