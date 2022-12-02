from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import linregress

df = pd.read_parquet('dash/data/data.parquet.gzip')
list_metabolites = df.Metabolite.unique()

app = Dash(__name__, )
app.title = 'Metabolite'
app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H2('Metabolite Upper Limit', style={
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

            html.P('The Concentration:', className='fix_label', style={
                   'color': 'white', 'margin-left': '1%'}),

             html.P(id='list_rep_conc', className='fix_label', style={
                 'color': 'white',  'fontSize': 14, 'margin-left': '1%'}),

             html.P('Select Time:', className='fix_label', style={
                 'color': 'white', 'margin-left': '1%'}),

             dcc.RangeSlider(id='select_time',
                             min=0,
                             max=60,
                             step=5,
                             tooltip={"placement": "topLeft",
                                      "always_visible": True},
                             value=[0, 60],
                             updatemode='drag'),

             ], className="create_container three columns"),

        ####################################################################################################


        html.Div([
            dcc.Graph(id='scatter_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='pie_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container three columns"),

    ], className="row flex-display"),
    ##############################################################################################
    #                                   end of first row
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
    #                                   end of second row
    ##############################################################################################

], id="mainContainer", style={"display": "flex", "flex-direction": "column"})


##############################################################################################
##########                              call backs!!!                                #########
##############################################################################################


# changes the radio button acording to the dropdown

@ app.callback(
    Output('reps', 'options'),
    Input('metabo', 'value'))
def get_reps_options(metabo):
    df_met = df.loc[df["Metabolite"] == metabo].sort_values(
        by='Number', ascending=True)
    return [{'label': i, 'value': i} for i in df_met['Number'].unique()]


# returns the value of the radio button with the first repitition

@ app.callback(
    Output('reps', 'value'),
    Input('reps', 'options'))
def get_reps_value(reps):
    return [k['value'] for k in reps][0]


# concentration slider callback
@ app.callback(
    Output('select_conc', 'value'),
    Output('select_conc', 'min'),
    Output('select_conc', 'max'),
    Output('list_rep_conc', 'children'),
    Input('metabo', 'value'),
    Input('reps', 'value'))
def get_conc_value(metabo, reps):
    if metabo:
        df_met = df.loc[(df["Metabolite"] == metabo) & (df['Number'] == reps)]
        df_met_conc = df_met['Concentration'].unique()[0:]
        global df_met_print
        df_met_print = df_met['Concentration'].unique()
        # [{'label': i, 'value': i} for i in df_met['Number'].unique()]
        lower = min(df_met['Concentration'].unique())
        upper = max(df_met['Concentration'].unique())
        concetration_string = ' , '.join(df_met_print.astype(str))

    return df_met_conc, lower, upper, concetration_string

    # Create scatterplot chart
###################################################################
####                         scatter chart                     ####
###################################################################


@ app.callback(Output('scatter_chart', 'figure'),
               [Input('metabo', 'value')],
               [Input('reps', 'value')],
               [Input('select_conc', 'value')],
               [Input('select_time', 'value')])
def update_graph(metabo, reps, select_conc, select_time):
    # Data for scatter plot

    plot_data = df.loc[(df["Metabolite"] == metabo) & (df['Number'] == reps) & (df['Concentration'] >= min(select_conc)) & (
        df['Concentration'] <= max(select_conc)) & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]
    fig = px.scatter(plot_data, x="Time",
                     y="OD600",
                     color="Strain",
                     hover_name="Concentration",
                     # marginal_y='histogram',
                     # marginal_y='violin',
                     range_y=[-.1, 1.8],
                     labels={
                         "Time": "Time(h)",
                         "OD600": "Abs(OD600)",
                     },
                     template="plotly_dark",
                     animation_frame="Concentration",
                     animation_group="OD600"
                     )
    fig.update_layout(
        yaxis=dict(
            tickmode='linear',
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

###################################################################
####                          pie chart                        ####
###################################################################


@ app.callback(Output('pie_chart', 'figure'),
               [Input('metabo', 'value')],
               [Input('select_time', 'value')])
def update_graph(metabo, select_time):
    plot_data = df.loc[(df["Metabolite"] == metabo) & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))].sort_values(
        by='Number', ascending=True)

    fig = px.pie(plot_data,  names='Number', template="plotly_dark",
                 color='Number', hole=.4, title=f'% reps {metabo}')  # hover_name=df.value_counts())
    fig.update_traces(textposition='outside', textinfo='percent+label+value')
    fig.update_layout(legend=dict(orientation='h'))

    return fig


###################################################################
####                          linear chart                     ####
###################################################################


@ app.callback(Output('chart_2', 'figure'),
               [Input('metabo', 'value'),
               Input('reps', 'value'),
               Input('select_time', 'value')])
def update_graph(metabo, reps, select_time):
    plot_data = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == 'WT') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]
    plot_data_152 = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == '152') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]

    def find_slope(x, y):
        slope = 0
        w = 12
        for t in range(0, x.size-w):
            x_t, y_t = x[t:t+w], y[t:t+w]
            res = linregress(x_t, y_t)
            if res.slope > slope:
                slope = res.slope
        return slope

    all_slopes = []
    all_slopes_152 = []
    con = plot_data.Concentration.unique()

    for i in range(0, len(con)):
        # conc=con[i]
        in_plot_data = plot_data.loc[plot_data['Concentration'] == con[i]]
        in_plot_data_152 = plot_data_152.loc[plot_data_152['Concentration'] == con[i]]

        x = in_plot_data['Time'].values
        y = in_plot_data['OD600'].values

        x_152 = in_plot_data_152['Time'].values
        y_152 = in_plot_data_152['OD600'].values

        alls = find_slope(x, y)
        alls_152 = find_slope(x_152, y_152)

        all_slopes.append(alls)
        all_slopes_152.append(alls_152)

    try:
        y_line = max(all_slopes)*0.25
    except ValueError:
        y_line = 0

    try:
        y_line_152 = max(all_slopes_152)*0.25
    except ValueError:
        y_line_152 = 0

    y_line_152 = max(all_slopes_152)*0.25
    # y_line_152 = np.percentile(all_slopes, 25)# return the percentile of the list
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=con, y=all_slopes,
                             mode='lines+markers', name='WT',
                             marker=dict(
                                 symbol="arrow",
                                 size=20,
                                 angleref="previous",
                             ),))

    fig.add_trace(go.Scatter(x=con, y=all_slopes_152,
                             mode='lines+markers', name='152',
                             marker=dict(
                                 symbol="arrow",
                                 size=20,
                                 angleref="previous",
                             ),))

    fig.update_layout(

        title=metabo+" #"+str(reps)+" ",
        template="plotly_dark",
        xaxis_title="Concentration(mM)",
        yaxis_title="Slope",
        legend_title="Strain",
        font=dict(family="Courier New, monospace", size=14, color="white"))
    fig.update_traces(
        marker=dict(size=8, symbol="diamond", line=dict(
            width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),)
    fig.add_hline(y=y_line, line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Min Slope + 25% = "+str(round(y_line, 4)), annotation_position="bottom left")

    fig.add_hline(y=y_line_152, line_width=3, line_dash="dot", line_color='#EF553B', name='152-Line',
                  annotation_text="   152 Min Slope + 25% = "+str(round(y_line_152, 4)), annotation_position="top left")

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig


###################################################################
####                          logaritmic chart                 ####
###################################################################


@ app.callback(Output('chart_3', 'figure'),
               [Input('metabo', 'value'),
               Input('reps', 'value'),
               Input('select_time', 'value')])
def update_graph(metabo, reps, select_time):
    plot_data = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == 'WT') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]
    plot_data_152 = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == '152') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]

    def find_slope(x, y):
        slope = 0
        w = 12
        z = 0.5
        for t in range(0, x.size-w):
            x_t, y_t = x[t:t+w], y[t:t+w]
            res = linregress(x_t, y_t)
            if abs(sum(y_t))/w < z and res.slope > slope:
                slope = res.slope
        return slope

    all_slopes = []
    all_slopes_152 = []
    con = plot_data.Concentration.unique()

    for i in range(0, len(con)):
        # conc=con[i]
        in_plot_data = plot_data.loc[plot_data['Concentration'] == con[i]]
        in_plot_data_152 = plot_data_152.loc[plot_data_152['Concentration'] == con[i]]

        x = in_plot_data['Time'].values
        y = np.log(abs(in_plot_data['OD600'].values))

        x_152 = in_plot_data_152['Time'].values
        y_152 = np.log(abs(in_plot_data_152['OD600'].values))

        alls = find_slope(x, y)
        alls_152 = find_slope(x_152, y_152)

        all_slopes.append(alls)
        all_slopes_152.append(alls_152)

    try:
        y_line = max(all_slopes)*0.25
    except ValueError:
        y_line = 0

    try:
        y_line_152 = max(all_slopes_152)*0.25
    except ValueError:
        y_line_152 = 0

    y_line_152 = max(all_slopes_152)*0.25
    # y_line_152 = np.percentile(all_slopes, 25)# return the percentile of the list
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=con, y=all_slopes,
                             mode='lines+markers', name='WT',
                             marker=dict(
                                 symbol="arrow",
                                 size=20,
                                 angleref="previous",
                             ),))

    fig.add_trace(go.Scatter(x=con, y=all_slopes_152,
                             mode='lines+markers', name='152',
                             marker=dict(
                                 symbol="arrow",
                                 size=20,
                                 angleref="previous",
                             ),))

    fig.update_layout(

        title=metabo+" #"+str(reps)+" logaritmic scale - ln = log e ",
        template="plotly_dark",
        xaxis_title="Concentration(mM)",
        yaxis_title="Slope",
        legend_title="Strain",
        font=dict(family="Courier New, monospace", size=14, color="white"))
    fig.update_traces(
        marker=dict(size=8, symbol="diamond", line=dict(
            width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),)
    fig.add_hline(y=y_line, line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Min Slope + 25% = "+str(round(y_line, 4)), annotation_position="bottom left")

    fig.add_hline(y=y_line_152, line_width=3, line_dash="dot", line_color='#EF553B', name='152-Line',
                  annotation_text="   152 Min Slope + 25% = "+str(round(y_line_152, 4)), annotation_position="top left")

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
