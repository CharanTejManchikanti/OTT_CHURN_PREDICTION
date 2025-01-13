# OTT Churn Prediction

A machine learning project designed to predict customer churn for Over-The-Top (OTT) platforms. This project utilizes Python for data preprocessing, feature engineering, training various machine learning models, and deployment using Flask for API creation.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Model Evaluation Metrics](#model-evaluation-metrics)
- [Deployment](#deployment)
- [Results](#results)
- [Visualization](#visualization)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

Churn prediction is essential for businesses to identify customers likely to discontinue using their services. This project:
- Processes the customer dataset.
- Trains machine learning models to predict customer churn.
- Provides APIs for real-time prediction.

---

## Installation

To set up and run the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ott-churn-prediction.git
    cd ott-churn-prediction
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/MacOS
    venv\Scripts\activate     # For Windows
    ```

3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

4. Install Flask for deployment:
    ```bash
    pip install Flask
    ```

---

## Usage

1. Preprocess your data using the script:
    ```bash
    python preprocess.py
    ```

2. Train the machine learning model:
    ```bash
    python train_model.py
    ```

3. Evaluate the model:
    ```bash
    python evaluate_model.py
    ```

4. Deploy the model as an API:
    ```bash
    python app.py
    ```

5. Access the API at `http://127.0.0.1:5000`.

---

## Features

- Data preprocessing and feature engineering.
- Training multiple machine learning models (Logistic Regression, Random Forest, etc.).
- Evaluation metrics: Accuracy, Precision, Recall, F1-Score.
- Model deployment using Flask.

---

## Model Evaluation Metrics

| Metric       | Value     |
|--------------|-----------|
| Accuracy     | 92.5%     |
| Precision    | 90.2%     |
| Recall       | 88.3%     |
| F1-Score     | 89.2%     |

---

## Deployment

1. **Model Export**: The trained model is exported using `joblib`.
2. **API Creation**: A Flask-based API enables real-time predictions.
3. **Endpoint**: Submit data to `/predict` endpoint for predictions.

Example JSON payload for testing:
```json
{
    "customer_age": 25,
    "subscription_duration": 6,
    "number_of_logins": 15,
    "streaming_quality": "HD"
}
Results
The trained model effectively identifies customers likely to churn, enabling businesses to take preventive measures.

Visualization
Example Outputs:
Confusion Matrix

Feature Importance

Churn Probability Distribution

Contributing
Feel free to raise an issue or submit a pull request if you'd like to contribute. Contributions are always welcome!

License
This project is licensed under the MIT License.

