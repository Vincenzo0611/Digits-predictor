# Digit Predictor

An AI-powered full-stack web application for handwritten digit recognition using a custom-trained deep learning model.

The project allows users to upload digit images, receive predictions from a TensorFlow model, and provide feedback for incorrect classifications. Misclassified samples are stored for future dataset improvement and model retraining.

---

# Live Demo

Frontend:
`http://digit-predictor-frontend.s3-website.eu-north-1.amazonaws.com/`

Backend API Docs:
`http://13.61.178.26:8000/docs`

---

# Features

## Authentication & Authorization

* JWT authentication
* User registration & login
* Admin role support

## AI Digit Prediction

* Upload handwritten digit images
* Custom preprocessing pipeline using OpenCV
* TensorFlow CNN model inference
* Confidence score returned with prediction

## Feedback System

* Mark predictions as correct or incorrect
* Save incorrectly classified samples
* Store:
  * predicted digit
  * correct digit
  * confidence
  * uploaded image
  * processed image
  * user information

## Dashboard

### User Dashboard

* View personal predictions
* Delete predictions

### Admin Dashboard

* View all users' predictions
* View users associated with predictions
* Delete any prediction
* Monitor incorrectly classified samples

## Cloud Integration

* Image storage using AWS S3
* Backend deployed on AWS EC2
* Frontend hosted using AWS S3 Static Hosting

---

# Tech Stack

## Frontend

* Angular
* TypeScript
* HTML/CSS

## Backend

* FastAPI
* SQLAlchemy
* JWT Authentication
* PostgreSQL

## Machine Learning

* TensorFlow / Keras
* OpenCV
* NumPy

## Cloud & DevOps

* AWS EC2
* AWS S3
* Docker
* Docker Compose

---

# Machine Learning Model

The model was trained on a custom dataset of handwritten digit images. The training script can be found in `ML-train/train.py`, and the trained model achieves approximately **90% accuracy**.

### Dataset

* **Source:** Independently collected by the author
* **Location:** The dataset is stored in the `ML-train/Digits` folder
* ~3000 images
* Custom preprocessing
* Train / Validation / Test split

### Preprocessing Pipeline

* Gaussian Blur
* Morphological Operations
* Thresholding
* Normalization
* Resize to 100x100

---
# Demo Accounts

## User Account

Email:

```txt
guest@guest.com
```

Password:

```txt
12345
```

---

## Admin Account

Email:

```txt
admin@admin.com
```

Password:

```txt
12345
```

---

# AWS Deployment

## Backend

* AWS EC2
* Dockerized FastAPI + PostgreSQL

## Frontend

* AWS S3 Static Website Hosting

## Images

* AWS S3 Bucket Storage

---

# Future Improvements

* Model retraining pipeline
* Better CNN architecture
* Mobile support
* Domain support

---

# Project Goal

The purpose of this project was to build a complete cloud-ready AI application combining:

* Machine Learning
* Full-stack development
* Authentication systems
* Cloud infrastructure
* Docker deployment

while learning production-oriented software architecture and deployment practices.

---

# Author

Created by Vincenzo Piras
