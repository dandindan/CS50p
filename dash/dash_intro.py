# Dash skeleton structure
#################################################################


# 1. Imports
from dash import Dash
import dash_html_components as html


################################################################

# 2.App instalation


app = Dash(__name__)


################################################################

# 3. App Layout

app.layout = html.Div([
    html.H1('this is h1'),
    html.H2('this is the h2'),
    html.P('this is the p componant'),
    html.Strong('strong'),
    html.Ul([
        html.Li('1'),
        html.Li('2'),
        html.Li('3'),
        html.Li('4'),
        html.Li('5'),
        html.Li([
            html.A('Google', href='https://google.com')
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
