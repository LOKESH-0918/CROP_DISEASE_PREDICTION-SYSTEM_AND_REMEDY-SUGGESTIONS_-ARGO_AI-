# Agro AI Project

This project now includes:

- Improved signup and signin frontend
- Flask backend with stronger auth validation
- MongoDB user storage plus separate prediction history storage for each user
- TensorFlow/Keras disease prediction pipeline
- Remedy, prevention, and pesticide guidance in result pages

## Project Structure

- `frontend/` static HTML, CSS, image assets
- `backend/` Flask backend and auth APIs
- `models/` training and inference code
- `data/dataset/` training images, grouped by class
- `data/artifacts/` trained model files and logs
- `run.py` root entry for Flask app
- `train_model.py` root entry for model training
- `prepare_dataset.py` copies supported public dataset classes into your project dataset folders

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Set environment values from `.env.example`.
4. Start MongoDB locally or update `MONGODB_URI`.
5. Run the app:
   `python run.py`

## Authentication

- Sign up uses full name, username, email, password, and confirm password.
- Password requires uppercase, lowercase, and a number.
- Login works with username or email.

## Per-user Data

- Main database stores account information.
- Each user gets a separate MongoDB database for prediction history:
  `agro_ai_user_<username>`

## ML Training

- Put leaf images in `data/dataset/<class_name>/...`
- Use one folder per label, such as `Tomato Early Blight`, `Tomato Healthy`, or `Rice Blast`.
- The trainer uses every non-empty class folder in `data/dataset`; the labels are learned from those folder names.
- Run training:
  `python train_model.py`
- Training uses ImageNet-pretrained MobileNetV2, image augmentation, class weighting, and fine-tuning.
- Training saves:
  - `data/artifacts/model.keras`
  - `data/artifacts/labels.json`
  - `data/artifacts/training_log.csv`
  - `data/artifacts/training_metrics.json`

### Dataset coverage and accuracy

- A prediction is limited to the crop and disease labels represented in the training folders. A model cannot reliably recognize an unsupported crop or disease just because it is given a leaf photo.
- The current saved model has 13 classes across apple, grape, maize, potato, and tomato. Add labeled image folders for each additional crop and disease before retraining.
- The reported validation score uses a random image-level split. It is not a measure of accuracy on field photos; near-duplicate images or controlled backgrounds can make that score optimistic.
- For better field performance, include independently collected phone photos with varied lighting, backgrounds, growth stages, and symptom severity. Keep a separate set of field photos out of training for an honest evaluation.
- The first PlantVillage-based model is a baseline. Field performance needs separate field-image training and evaluation.

## Accuracy Note

High accuracy depends on:

- large and clean dataset
- correct class labels
- balanced number of images per disease
- clear leaf images during inference

The code is upgraded for better training, top-3 prediction output, and low-confidence warnings, but true accuracy still depends on good real dataset quality.

## Important Reality Check

- No model can identify "every Indian crop disease" correctly without a large labeled dataset covering those crops and diseases.
- If you want near-production accuracy, collect many clear images per class from real field conditions:
  - different lighting
  - different growth stages
  - early and severe infection stages
  - healthy leaves for each crop
- Best results usually need hundreds or thousands of images per class, not just a few samples.

## Prepared Dataset Template

The project already contains empty folders for major crop classes inside `data/dataset/`, including:

- Rice
- Wheat
- Maize
- Tomato
- Potato
- Cotton
- Chilli
- Grape
- Sugarcane
- Apple
- Banana

You only need to copy disease-wise leaf images into those folders and then run training.

## Public Dataset Preparation

If PlantVillage is downloaded into `data/raw/PlantVillage-Dataset-master`, you can auto-copy supported classes into your training folders:

`python prepare_dataset.py`

## Routes

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/history`
- `POST /api/predict`
- `GET /health`
