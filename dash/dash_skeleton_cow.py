# Dash skeleton structure
#################################################################


# 1. Imports
from dash import Dash, dcc, html, Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_vtk


# Get it here: https://github.com/plotly/dash-vtk/blob/master/demos/data/cow-nonormals.obj
obj_file = "dash/cow.obj"


txt_content = None
with open(obj_file, 'r') as file:
    txt_content = file.read()

content = dash_vtk.View([
    dash_vtk.GeometryRepresentation([
        dash_vtk.Reader(
            vtkClass="vtkOBJReader",
            parseAsText=txt_content,
        ),
    ]),
])
################################################################

# 2.App instalation


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


################################################################

# 3. App Layout

app.layout = html.Div(
    style={"width": "100%", "height": "400px"},
    children=[content],
)

################################################################

# 4. Callback Function


################################################################


# 5. Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)


################################################################
