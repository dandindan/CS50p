from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go


df = pd.read_parquet('dash/data/data.parquet.gzip')
list_metabolites = df.Metabolite.unique()

# matabolite_list = df['Metabolite'].unique()


app = Dash(__name__, )
app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H2('Metabolite Upper Limit!', style={
                        "margin-bottom": "0px", 'color': 'white'}),
                html.H4('2021-2023',
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
                         value='Alanine',
                         placeholder='Select Matabolite',
                         options=[{'label': c, 'value': c}
                                  for c in list_metabolites], className='dcc_compon'),

            html.P('Select Repetition:', className='fix_label',
                   style={'color': 'white'}),
            dcc.RadioItems(id='reps',
                           inline=True,
                           labelStyle={
                              # 'display': 'block',
                               # 'writing-mode': 'vertical_rl',
                               'padding-left': 20,
                               # 'transform': 'rotate(20deg)',
                               # 'transform-origin': 'left',
                           },
                           # multi=False,
                           #    clearable=False,
                           #    disabled=False,
                           #    style={'display': True},
                           #    placeholder='Select Repetition',
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


@ app.callback(
    Output('reps', 'options'),
    Input('metabo', 'value'))
def get_reps_options(metabo):
    df_met = df.loc[df["Metabolite"] == metabo].sort_values(
        by='Number', ascending=True)
    return [{'label': i, 'value': i} for i in df_met['Number'].unique()]


@ app.callback(
    Output('reps', 'value'),
    Input('reps', 'options'))
def get_reps_value(reps):
    return [k['value'] for k in reps][0]

# Create scatterplot chart


@ app.callback(Output('scatter_chart', 'figure'),
               [Input('metabo', 'value')],
               [Input('reps', 'value')])
def update_graph(metabo, reps):
    # Data for scatter plot
    plot_data = df.loc[(df["Metabolite"] == metabo) & (df['Number'] == reps)]
    fig = px.line(plot_data, x="Time",
                  y="OD600",
                  color="Strain",
                  hover_name="Number",
                  # title=metabo,
                  # marginal_x='histogram',
                  # marginal_x='box',
                  range_y=[-.1, 1.8],
                  labels={
                      "Time": "Time(h)",
                      "OD600": "Abs(OD600)",
                  },
                  # height=600,
                  # width=1000,
                  template="plotly_dark",
                  animation_frame="Concentration",
                  animation_group="OD600")
    fig.update_layout(
        yaxis=dict(
            tickmode='linear',
            # tick0=0.0,
            dtick=0.4
        )
    )
    fig.update_layout(
        title={
            'text': metabo,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig

# pie chart#######################################################


@app.callback(Output('pie_chart', 'figure'),
              [Input('metabo', 'value')])
def update_graph(metabo):
    plot_data = df.loc[(df["Metabolite"] == metabo)].sort_values(
        by='Number', ascending=True)
    #max_number = plot_data.Number.max()
    # fig = px.scatter(plot_data,
    #                  x='Number',
    #                  y='Concentration',

    #                  #range_x=[0, max_number+1],
    #                  # template="presentation",
    #                  template="plotly_dark",
    #                  # width=300,
    #                  # symbol="Number",
    #                  color='Concentration',
    #                  hover_name=('OD600'))
    # height=600)
    # fig.update_traces(mode='markers', marker_line_width=.1,
    #                   marker_size=5, opacity=1)
    # fig.update_layout(title="Metabolite Concentration distribution")
    #fig.update_layout(coloraxis_showscale=False, margin_pad=0)
    fig = px.pie(plot_data,  names='Number', template="plotly_dark",
                 color='Number', hole=.4, title=f'% reps {metabo}')  # hover_name=df.value_counts())
    fig.update_traces(textposition='outside', textinfo='percent+label+value')
    fig.update_layout(legend=dict(  # bgcolor = 'yellow',
        orientation='h',
        # yanchor='top', y=1.2,
        # xanchor='left', x=0.2),)
        # legend_font_color="green")
    ))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)