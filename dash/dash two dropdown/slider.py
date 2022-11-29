import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd

data = pd.DataFrame({
    'Age': list(range(18, 61, 5))
})

app = dash.Dash(__name__)

app.layout = dbc.Col([
    html.Div(id='Title_Slider', children='''Milo na ena LOLA'''),
    dcc.RangeSlider(id='ageslider', min=18, max=60, step=1, value=[18, 60],
                    marks={str(Age): str(Age) for Age in data.Age.unique()}
                    ),
    dcc.Dropdown(id='dropdown1',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                 value='NYC'
                 ),
    dcc.Graph(id='bar-1'),
    html.Div(id='output-text'),
])


@app.callback(
    Output('bar-1', 'figure'),
    Output('output-text', 'children'),
    Input('dropdown1', 'value'),
    Input('ageslider', 'value'),
    # Input('binat','value')
)
def update_line_chart(dropdown_value, slide_value):  # , bi_value):
    print('min_val:', slide_value[0])
    print('max_val:', slide_value[1])
    fig = go.Figure(data=[go.Bar(x=[1, 2], y=slide_value)])
    text = f"{dropdown_value}: min: {slide_value[0]}, max: {slide_value[1]}"
    return fig, text


if __name__ == '__main__':
    app.run_server(debug=True)
