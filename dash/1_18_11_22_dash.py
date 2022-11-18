
from plotly.express import data
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_parquet('dash/data/data.parquet.gzip')
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
app.layout = html.Div([
    dcc.Dropdown(df.Metabolite.unique(), placeholder="Select a Matabolite", id='dropdown-1',
                 ),
    html.Div(id='output-1')
])


@app.callback(
    Output('output-1', 'children'),
    Input('dropdown-1', 'value')
)
def update_output(value):
    return f'You have selected {value}'

# # Build your components
# app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
# mytitle = dcc.Markdown(children='')
# mygraph = dcc.Graph(figure={})
# dropdown = dcc.Dropdown(options=df.Metabolite.unique(),
#                         value='Cysteine',  # initial value displayed when page first loads
#                         clearable=False)

# # Customize your own Layout
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([mytitle], width=6)
#     ], justify='center'),
#     dbc.Row([
#         dbc.Col([mygraph], width=12)
#     ]),
#     dbc.Row([
#         dbc.Col([dropdown], width=6)
#     ], justify='center'),

# ], fluid=True)

# # Callback allows components to interact


# @app.callback(
#     Output(mygraph, 'figure'),
#     Output(mytitle, 'children'),
#     Input(dropdown, 'value')
# )
# # function arguments come from the component property of the Input
# def update_graph(column_name):

#     fig = px.scatter(data_frame=df,
#                      locations='STATE',
#                      locationmode="USA-states",
#                      scope="usa",
#                      height=600,
#                      color=column_name,
#                      animation_frame='YEAR')

#     # returned objects are assigned to the component property of the Output
#     return fig, '# '+column_name


# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
