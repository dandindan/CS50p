# Dash skeleton structure
#################################################################


# 1. Imports
from dash import Dash, dcc, html, Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

################################################################

# 2.App instalation


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
df = pd.read_parquet('dash/data/data.parquet.gzip')

################################################################

# 3. App Layout

app.layout = html.Div([

    html.Label("Metabolite Upper Limit", style={
               'fontSize': 40, 'color': 'red', 'text-align': 'center'}),

    dcc.Dropdown(df.Metabolite.unique(), placeholder="Select a Matabolite",
                 id='dropdown-1',  style={'color': 'blue'}),

    html.Div(id='output-1', style={'color': 'green', 'fontSize': 20}),
])

################################################################

# 4. Callback Function


@app.callback(
    Output('output-1', 'children'),
    Input('dropdown-1', 'value'),

)
def update_output(value):
    return f'You have selected {value}'
################################################################


# 5. Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)


################################################################
