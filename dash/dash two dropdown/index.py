from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go


df = pd.read_parquet('dash/data/data.parquet.gzip')
list_metabolites = df.Metabolite.unique()

#matabolite_list = df['Metabolite'].unique()


app = Dash(__name__, )
app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('Metabolite Upper Limit!', style={
                        "margin-bottom": "0px", 'color': 'white'}),
                html.H5('2021-2023',
                        style={"margin-top": "0px", 'color': 'white'}),

            ]),
        ], className="six column", id="title")

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),



    html.Div([
        html.Div([
            html.P('Select Metabolie:', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='metabo',
                         multi=False,
                         clearable=False,
                         disabled=False,
                         style={'display': True},
                         value='Cysteine',
                         placeholder='Select Matabolite',
                         options=[{'label': c, 'value': c}
                                  for c in list_metabolites], className='dcc_compon'),

            html.P('Select Repetition:', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='reps',
                         multi=False,
                         clearable=False,
                         disabled=False,
                         style={'display': True},
                         placeholder='Select Repetition',
                         options=[], className='dcc_compon'),

            html.P('Select Concentration:', className='fix_label', style={
                   'color': 'white', 'margin-left': '1%'}),
            dcc.RangeSlider(id='select_years',
                            min=0,
                            max=100,
                            dots=False,
                            value=[20, 80]),

        ], className="create_container three columns"),

        html.Div([
            dcc.Graph(id='scatter_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='pie_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container three columns"),

    ], className="row flex-display"),

], id="mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(
    Output('reps', 'options'),
    Input('metabo', 'value'))
def get_reps_options(metabo):
    df_met = df.loc[df["Metabolite"] == metabo].sort_values(
        by='Number', ascending=True)
    return [{'label': i, 'value': i} for i in df_met['Number'].unique()]


@app.callback(
    Output('reps', 'value'),
    Input('reps', 'options'))
def get_reps_value(reps):
    return [k['value'] for k in reps][0]

# Create scatterplot chart


@app.callback(Output('scatter_chart', 'figure'),
              [Input('metabo', 'value')],
              [Input('reps', 'value')])
def update_graph(metabo, reps):
    # Data for scatter plot
    plot_data = df.loc[(df["Metabolite"] == metabo) & (df['Number'] == reps)]
    fig = px.scatter(plot_data, x="Time",
                     y="OD600",
                     color="Strain",
                     hover_name="Number",
                     title=metabo,
                     # height=600,
                     # width=1000,
                     template="plotly_dark",
                     animation_frame="Concentration",
                     animation_group="OD600",)
    return fig


@app.callback(Output('pie_chart', 'figure'),
              [Input('metabo', 'value')])
def update_graph(metabo):
    plot_data = df.loc[(df["Metabolite"] == metabo)].sort_values(
        by='Number', ascending=True)
    fig = px.pie(plot_data,  names='Number', template="plotly_dark",
                 color='Number', hole=.4, title=f'% reps {metabo}')  # hover_name=df.value_counts())
    fig.update_traces(textposition='outside', textinfo='percent+label+value')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
