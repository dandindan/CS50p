# Dash skeleton structure
#################################################################


# 1. Imports
from dash import Dash, html
import dash_bootstrap_components as dbc


################################################################

# 2.App instalation


app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])


################################################################

# 3. App Layout

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Spinner(color="warning"),
            html.H1('This is h1'),
            dbc.Spinner(color="danger"),
            html.H2('This is the h2'),
            dbc.Spinner(color="success")], lg=5, md=12),
        dbc.Spinner(color="primary"),
        dbc.Col([
            html.P('About:'),
            html.Ul([
                html.Li('1'),
                html.Li('2'),
                html.Li('3'),
                html.Li('4'),
                html.Li('5'),
                html.Li([
                    html.A('Google', href='https://google.com')])

            ])

        ])
    ])
])

################################################################

# 4. Callback Function


################################################################

# 5. Run app

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)


################################################################
