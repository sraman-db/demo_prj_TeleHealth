import os
import json
import joblib
import numpy as np
import pandas as pd
from .text_extractor import extract_features


# -------------------------------------------------------------------
# 🔧 Locate model + encoder
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
candidate_dirs = [BASE_DIR, os.path.dirname(BASE_DIR), os.getcwd()]

MODEL_PATH, ENCODER_PATH = None, None
for d in candidate_dirs:
    mpath = os.path.join(d, "best_pipeline.joblib")
    epath = os.path.join(d, "label_encoder.joblib")
    if MODEL_PATH is None and os.path.exists(mpath):
        MODEL_PATH = mpath
    if ENCODER_PATH is None and os.path.exists(epath):
        ENCODER_PATH = epath
    if MODEL_PATH and ENCODER_PATH:
        break

try:
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    print(f"✅ Loaded model from {MODEL_PATH} and encoder from {ENCODER_PATH}")
except Exception as e:
    print(f"⚠️ Error loading model or encoder: {e}")
    model, label_encoder = None, None


# -------------------------------------------------------------------
# 📘 Load features
# -------------------------------------------------------------------
FEATURE_PATH = os.path.join(BASE_DIR, "features.json")
with open(FEATURE_PATH, "r", encoding="utf-8") as f:
    FEATURES = json.load(f)


# -------------------------------------------------------------------
# 🔍 Predict disease
# -------------------------------------------------------------------
def predict_from_text(text):
    """
    Takes user text (symptom description),
    extracts features using text_extractor,
    predicts the most likely disease,
    and returns a structured dictionary with department info.
    """
    if not model or not label_encoder:
        return {"error": "Model or encoder not loaded"}

    # Step 1️⃣: Extract features
    try:
        keys, vector = extract_features(text)
    except Exception as e:
        return {"error": f"Feature extraction failed: {e}"}

    print(f"\n🩺 Input text: {text}")
    print(f"✅ Extracted features: {keys}")
    print(f"🔢 Feature vector sum: {np.sum(vector)} active features")

    # Step 2️⃣: Align vector with model feature order
    try:
        X_input = pd.DataFrame([vector], columns=FEATURES)
    except Exception as e:
        return {"error": f"Failed to prepare input DataFrame: {e}"}

    # Step 3️⃣: Model prediction
    try:
        pred = model.predict(X_input)[0]
        probs = model.predict_proba(X_input)[0]
        top_confidence = float(np.max(probs))
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}

    # Step 4️⃣: Decode numeric label → disease
    try:
        disease_name = label_encoder.inverse_transform([pred])[0]
    except Exception:
        disease_name = str(pred)

    # -------------------------------------------------------------------
    # 🧩 Step 4.1 — Handle low-confidence case (Top 2 likely diseases)
    # -------------------------------------------------------------------
    alternate_diseases = []
    if probs is not None and top_confidence < 0.6:
        # Get indices of top 2 probable diseases
        top2_idx = np.argsort(probs)[-2:][::-1]
        top2_labels = label_encoder.inverse_transform(top2_idx)
        alternate_diseases = list(top2_labels)
        print(f"⚠️ Low confidence ({top_confidence:.3f}) → Top 2 likely: {alternate_diseases}")

    # Step 5️⃣: Load Department Mapping (from JSON)
    DEPT_PATH = os.path.join(BASE_DIR, "Department_Prediction.json")
    department = None
    if os.path.exists(DEPT_PATH):
        try:
            with open(DEPT_PATH, "r", encoding="utf-8") as f:
                dept_map = json.load(f)
            # Case-insensitive lookup
            for k, v in dept_map.items():
                if k.strip().lower() == disease_name.strip().lower():
                    department = v
                    break
        except Exception as e:
            print(f"⚠️ Department mapping load error: {e}")

    # Step 6️⃣: Category fallback (broad)
    found = set(keys)
    category_hint = None

    if any(k in found for k in ["chest_pain", "breathlessness", "fast_heart_rate", "sweating"]):
        category_hint = "Cardiology"
    elif any(k in found for k in ["abdominal_pain", "vomiting", "nausea", "diarrhoea", "indigestion"]):
        category_hint = "Gastroenterology"
    elif any(k in found for k in ["itching", "skin_rash", "blister", "red_spots_over_body"]):
        category_hint = "Dermatology"
    elif any(k in found for k in ["burning_micturition", "dark_urine", "yellow_urine", "pain_during_bowel_movements"]):
        category_hint = "Urology"
    elif any(k in found for k in ["dizziness", "headache", "loss_of_balance", "weakness_in_limbs", "blurred_and_distorted_vision"]):
        category_hint = "Neurology"
    elif any(k in found for k in ["joint_pain", "knee_pain", "swelling_joints", "movement_stiffness"]):
        category_hint = "Orthopedics"
    elif any(k in found for k in ["high_fever", "chills", "fatigue", "malaise", "sweating"]):
        category_hint = "General Medicine"
    elif any(k in found for k in ["anxiety", "depression", "irritability", "restlessness"]):
        category_hint = "Psychiatry"

    # Prefer department from JSON, else category hint
    if not department and category_hint:
        department = category_hint

    if not department:
        department = "General Physician"

    # Step 7️⃣: Return structured prediction
    result = {
        "prediction": disease_name.capitalize(),
        "confidence": round(top_confidence, 3) if top_confidence else None,
        "probabilities": probs.tolist() if probs is not None else None,
        "extracted": list(found),
        "department": department,
        "alternates": alternate_diseases  # 👈 added key
    }

    # Debug log
    print(f"🧠 Predicted Disease: {disease_name.capitalize()}")
    print(f"🏥 Department: {department}")
    if alternate_diseases:
        print(f"🩶 Alternate suggestions: {alternate_diseases}")

    return result


# -------------------------------------------------------------------
# 🧪 Local Testing
# -------------------------------------------------------------------
if __name__ == "__main__":
    examples = [
        "I have had fever and severe joint pain for two days. No chest pain.",
        "Vomiting and nausea since morning, mild fever.",
        "I feel weakness in my limbs and dizziness.",
        "My head hurts and I feel a bit cold.",
        "No vomiting, but I have a sore throat and cough.",
        "I have yellow eyes and dark urine.",
        "There are itchy rashes and red spots on my arms."
    ]
    for t in examples:
        print("\nInput:", t)
        result = predict_from_text(t)
        print(result)
