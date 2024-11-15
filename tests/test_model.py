# tests/test_model.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from model import SimpleModel
import numpy as np





def test_model_prediction():
    model = SimpleModel()
    X_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([1, 2, 3, 4])
    model.train(X_train, y_train)
    
    # Test prediction for a known input
    prediction = model.predict(np.array([[5]]))[0]
    assert abs(prediction - 5) < 0.1, f"Expected ~5, but got {prediction}"
