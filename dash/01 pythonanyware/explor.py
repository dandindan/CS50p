from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go


df = pd.read_csv(
    'https://raw.githubusercontent.com/dandindan/CS50p/main/all_metabolites.csv')
# df = pd.read_csv('/home/dandin/mysite/data/21-12-22.csv')
# df = pd.read_parquet('/home/dandin/mysite/data/all_matabolites_21_12_22.parquet.gzip')


def set_dtypes(df):
    df['Time'] = df['Time'].astype('float32')
    # ###df['Strain'] = df['Strain'].astype('category')
    df['Strain'] = df['Strain'].astype('category')
    df['Metabolite'] = df['Metabolite'].astype('category')
    df['Concentration'] = df['Concentration'].astype('float32')
    df['Date'] = df['Date'].astype('category')
    # ####df["Date"] = pd.to_datetime(df["Date"], format='%d%m%y')
    df['Number'] = df['Number'].astype('int32')
    # ###df['Number'] = df['Number'].astype('category')
    df['OD600'] = df['OD600'].astype('float32')
    return df


df = set_dtypes(df)  # set datatypes


list_metabolites = df.Metabolite.unique()

app = Dash(__name__, )
server = app.server
app.title = 'Metabolite'
explor_layout = html.Div([

    html.Div([
        ##############################################################################################
        #                                   Upper Limit Chart
        ##############################################################################################
        html.Div([
            dcc.Graph(id='chart_violin',
                      config={'displayModeBar': 'hover'},

                      ),

        ], className="create_container twelve columns"),

    ], className="row flex-display"),

    ##############################################################################################
    #                                   3/12 left column of selection
    ##############################################################################################
    html.Div([
        html.Div([
            html.P('Select Metabolite:', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='metabo',
                         multi=False,
                         clearable=False,
                         disabled=False,
                         style={'display': True},
                         value='Alanine',
                         placeholder='Select Matabolite',
                         options=[{'label': c, 'value': c}
                                  for c in list_metabolites], className='dcc_compon'),

            html.P('Select Repetition:', className='fix_label',
                   style={'color': 'white'}),
            dcc.RadioItems(id='reps',
                           inline=True,
                           labelStyle={
                               'padding-left': 20},
                           options=[],
                           className='dcc_compon'),


            html.P('Select Concentration:', className='fix_label', style={
                'color': 'white', 'margin-left': '1%'}),

            dcc.RangeSlider(id='select_conc',
                            min=0,
                            max=500,
                            tooltip={"placement": "topLeft",
                                     "always_visible": True},
                            value=[0, 500],
                            updatemode='drag'),

            html.P('The Concentration: (mM)', className='fix_label', style={
                'color': 'white', 'margin-left': '1%'}),

            html.P(id='list_rep_conc', className='fix_label', style={
                'color': 'white',  'fontSize': 14, 'margin-left': '1%'}),

        ], className="create_container three columns"),

        ####################################################################################################
        #                           6/12     Upper Limit Chart
        ####################################################################################################
        html.Div([
            dcc.Loading(children=[
                dcc.Graph(id='scatter_chart',
                          config={'displayModeBar': 'hover'}),
            ], color="#119DFF", type="default", fullscreen=False)

        ], className="create_container six columns"),
        ####################################################################################################
        #                              9/12  pie Chart
        ####################################################################################################
        html.Div([
            dcc.Graph(id='pie_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container three columns"),

    ], className="row flex-display"),


    ##############################################################################################
    #                                   Chart 2 & 3 of the Metabolite
    ##############################################################################################
    html.Div([
        html.Div([
            dcc.Graph(id='chart_2',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='chart_3',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

    ], className="row flex-display"),


    ##############################################################################################
    #                              All Metabolite Chart
    ##############################################################################################
    html.Div([

        html.Div([
            dcc.Graph(id='chart_ex4',
                      config={'displayModeBar': 'hover'},

                      ),

        ], className="create_container twelve columns"),

    ], className="row flex-display"),


], id="mainContainer1", style={"display": "flex", "flex-direction": "column"})
