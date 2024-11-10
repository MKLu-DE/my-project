import dash_bootstrap_components as dbc
from dash import html
from app import app


layout = html.Div(
    dbc.Container(
        [
            html.H1("Tomato Rootstock Seed Drying", className="display-3"),
            html.P(
                "The App is developed for 'Design of Experiments' (Doe) and "
                "'Soft Sensor'.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "* DoE: determine desired experimental variables based on predicted moisture profiles"
            ),
            html.P(
                "* Soft Sensor: predict moisture profiles of a running experiment and determine end point"
            ),
            # html.P(
            #     dbc.Button("Learn more", color="primary"), className="lead"
            # ),
            dbc.Carousel(
                items=[
                    {"key": "1", "src": "assets/growing_tomatoes.jpg"},
                    {"key": "2", "src": "assets/dreamstime_m.jpg"},
                    # {"key": "3", "src": "/static/images/slide3.svg"},
                ],
                controls=True,
                interval=5000,
                indicators=True,
                className="carousel-fade",
            ),
        ],
        fluid=True,
        className="py-3",
    ),

    className="p-3 bg-body-secondary rounded-3",
)