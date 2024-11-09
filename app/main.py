# main.py
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import numpy as np
from model import SimpleModel

# Initialize the Dash app
app = dash.Dash(__name__)
model = SimpleModel()

# Dummy training data for the model
X_train = np.array([[1], [2], [3], [4]])
y_train = np.array([1, 2, 3, 4])
model.train(X_train, y_train)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Simple Prediction App"),
    dcc.Input(id="input-value", type="number", placeholder="Enter a number", debounce=True),
    html.Button("Predict", id="predict-button"),
    html.Div(id="output", children="Prediction will appear here.")
])

# Callback to handle prediction
@app.callback(
    Output("output", "children"),
    Input("predict-button", "n_clicks"),
    Input("input-value", "value")
)
def update_prediction(n_clicks, input_value):
    if n_clicks is None or input_value is None:
        return "Enter a value and click Predict."
    prediction = model.predict(np.array([[input_value]]))[0]
    return f"Prediction: {prediction:.2f}"

# Run the app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
