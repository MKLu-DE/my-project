# model.py
import numpy as np
from sklearn.linear_model import LinearRegression

class SimpleModel:
    def __init__(self):
        # Initialize a simple linear regression model
        self.model = LinearRegression()
    
    def train(self, X, y):
        # Train the model with provided data
        self.model.fit(X, y)
    
    def predict(self, X):
        # Make predictions
        return self.model.predict(X)

# Example usage
if __name__ == "__main__":
    model = SimpleModel()
    X_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([1, 2, 3, 4])
    model.train(X_train, y_train)
    print("Prediction:", model.predict(np.array([[5]])))
