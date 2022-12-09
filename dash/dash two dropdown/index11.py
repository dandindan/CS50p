from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import linregress

df = pd.read_parquet('/Users/maozlahav/Documents/GitHub/CS50p/dash/data/all_matabolites_7_11_22.parquet.gzip')
list_metabolites = df.Metabolite.unique()
metabo = 'Alanine'
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

             html.P('Select:  ', className='fix_label', style={
                 'color': 'white', 'margin-left': '1%'}),
             html.Div([
                 html.Div(['Regression', dcc.Input(id='range1', type='number', min=2, max=12,
                                                   step=1, value=5)]),
                 html.Div(['Length', dcc.Input(
                     id='range2', type='number', min=0, max=20, step=1, value=2, )]),
                 html.Div(['Percent', dcc.Input(
                     id='range3', type='number', min=5, max=100, step=5, value=25, )]),
                 html.Div(['Mean', dcc.Input(id='range4', type='number', min=0.1, max=5,
                                             step=0.1, value=0.5, )]),
             ], className='input_range'),
             #  html.Pre('  A      B      C     D', className='pre_label', style={
             #      'color': 'white', 'margin-left': '1%'}),

             ], className="create_container three columns"),

        ####################################################################################################


        html.Div([
            dcc.Graph(id='scatter_chart',
                      config={'displayModeBar': 'hover'},
                      style={"height": "100%", "width": "100%", }),

        ], className="create_container six columns"),

        html.Div([
            # dcc.Graph(id='pie_chart',
            #           config={'displayModeBar': 'hover'}),
            html.Iframe(
                id='frame', src="https://pubchem.ncbi.nlm.nih.gov/compound/"+metabo+"#section=3D-Conformer&embed=true",
                style={"height": "100%", "width": "100%", }),
        ], className="create_container three columns"),

    ], className="row flex-display"),
    ##############################################################################################
    #                                   end of first row
    ##############################################################################################
    html.Div([
        html.Div([
            dcc.Graph(id='chart_2',
                      config={'displayModeBar': 'hover'},
                      clickData={'points': [{'x': 0}, {'x': 0}]}),


        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='chart_3',
                      config={'displayModeBar': 'hover'},
                      clickData={'points': [{'x': 0}, {'x': 0}]}),

        ], className="create_container six columns"),

    ], className="row flex-display"),

    ##############################################################################################
    #                                   end of second row
    ##############################################################################################

    html.Div([
        html.Div([
            dcc.Graph(id='chart_4',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='chart_5',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

    ], className="row flex-display"),

    ##############################################################################################
    #                                   end of third row
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
####                         scatter chart       #1            ####
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
####                       Molecule display                    ####
###################################################################


@ app.callback(Output('frame', 'src'),
               [Input('metabo', 'value')],)
def update_graph(metabo):
    if metabo == 'AspaticAcid':
        metabo = 'Aspartic Acid'
    else:
        metabo = metabo

    if metabo == 'Tymine':
        metabo = 'Thymine'
    else:
        metabo = metabo

    if metabo == 'Tryptopan':
        metabo = 'Tryptophan'
    else:
        metabo = metabo

    if metabo == 'Adenine Hemi':
        metabo = 'Adenine'
    else:
        metabo = metabo

    return f'https://pubchem.ncbi.nlm.nih.gov/compound/{metabo}#section=3D-Conformer&embed=true'


###################################################################
####                        linear chart   #2                  ####
###################################################################


@ app.callback(Output('chart_2', 'figure'),
               [Input('metabo', 'value'),
               Input('reps', 'value'),
               Input('range1', 'value'),
               Input('range3', 'value'),
               Input('select_time', 'value')])
def update_graph(metabo, reps, range1, range3, select_time):
    plot_data = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == 'WT') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]
    plot_data_152 = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == '152') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]
    upper_title = ''

    def find_slope(x, y):
        slope = 0
        w = range1
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

    percent = range3/100

    try:
        y_line = max(all_slopes)*percent
    except ValueError:
        y_line = 0

    try:
        y_line_152 = max(all_slopes_152)*percent
    except ValueError:
        y_line_152 = 0

    # y_line_152 = max(all_slopes_152)*0.25
    # y_line_152 = np.percentile(all_slopes, 25)# return the percentile of the list
    # list_all_slopes = all_slopes.tolist()
    # upper_limit = filter(lambda x: x > list_all_slopes, y_line)
    # print(upper_limit)
    upper_limit = [i for i in all_slopes if i <= y_line]
    # for i in all_slopes:
    #     if i <=y_line:
    if upper_limit:

        index = [n for n, i in enumerate(all_slopes) if i < y_line][0]

        upper_title = f'  The upper limit is between {con[index-1]} and {con[index]}mM'

    else:

        upper_title = 'There is NO Upper Limit!!!'

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

        title=metabo+" #"+str(reps)+" "+upper_title+" ",
        template="plotly_dark",
        xaxis_title="Concentration(mM)",
        yaxis_title="Slope",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))
    # fig.update_traces(
    #     marker=dict(size=8, symbol="diamond", line=dict(
    #         width=2, color="DarkSlateGrey")),
    #     selector=dict(mode="markers"),)
    fig.add_hline(y=y_line, line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Min Slope + "+str(range3) + "% = "+str(round(y_line, 4)), annotation_position="bottom right")

    fig.add_hline(y=y_line_152, line_width=3, line_dash="dot", line_color='#EF553B', name='152-Line',
                  annotation_text="   152 Min Slope +"+str(range3) + "% = "+str(round(y_line_152, 4)), annotation_position="top right")

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig


###################################################################
####                          logaritmic chart    #3           ####
###################################################################


@ app.callback(Output('chart_3', 'figure'),
               [Input('metabo', 'value'),
               Input('reps', 'value'),
                Input('range1', 'value'),
               Input('range3', 'value'),
               Input('range4', 'value'),
               Input('select_time', 'value')])
def update_graph(metabo, reps, range1, range3, range4, select_time):
    plot_data = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == 'WT') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]
    plot_data_152 = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Strain'] == '152') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]

    upper_title = ''

    def find_slope(x, y):
        slope = 0
        w = range1
        z = range4
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

    percent = range3/100

    try:
        y_line = max(all_slopes)*percent
    except ValueError:
        y_line = 0

    try:
        y_line_152 = max(all_slopes_152)*percent
    except ValueError:
        y_line_152 = 0

    upper_limit = [i for i in all_slopes if i <= y_line]

    if upper_limit:

        index = [n for n, i in enumerate(all_slopes) if i < y_line][0]

        upper_title = f'  The upper limit is between {con[index-1]} and {con[index]}mM'

    else:

        upper_title = 'There is NO Upper Limit!!!'
    # y_line_152 = max(all_slopes_152)*0.25
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

        title=metabo+" #"+str(reps) +
        " logaritmic scale - ln = log e "+upper_title,
        template="plotly_dark",
        xaxis_title="Concentration(mM)",
        yaxis_title="Slope",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))

    fig.add_hline(y=y_line, line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Min Slope +" + str(range3) + "% = "+str(round(y_line, 4)), annotation_position="bottom right")

    fig.add_hline(y=y_line_152, line_width=3, line_dash="dot", line_color='#EF553B', name='152-Line',
                  annotation_text="   152 Min Slope +" + str(range3)+"% = "+str(round(y_line_152, 4)), annotation_position="top right")

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig

###################################################################
####                          linear chart #4                  ####
###################################################################


@ app.callback(Output('chart_4', 'figure'),
               [Input('metabo', 'value'),
               Input('reps', 'value'),
               Input('range1', 'value'),
               Input('range2', 'value'),
               Input('select_time', 'value'),
               Input('chart_2', 'clickData')])
def update_graph(metabo, reps, range1, range2, select_time, clickData):

    plot_data = df.loc[(df["Metabolite"] == metabo) & (df['Concentration'] == (clickData['points'][0]['x'])) & (df['Number'] == reps) & (
        df['Strain'] == 'WT') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]

    plot_data_152 = df.loc[(df["Metabolite"] == metabo) & (df['Concentration'] == (clickData['points'][1]['x'])) & (df['Number'] == reps) & (
        df['Strain'] == '152') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]

    conc_value = str(clickData['points'][1]['x'])

    x = plot_data['Time'].values
    y = plot_data['OD600'].values

    x_152 = plot_data_152['Time'].values
    y_152 = plot_data_152['OD600'].values

    slope = 0
    w = range1
    extend_line = range2
    t_slope = 0
    for t in range(0, x.size-w):
        x_t, y_t = x[t:t+w], y[t:t+w]
        res = linregress(x_t, y_t)
        if res.slope > slope:
            slope = res.slope
            intercept = res.intercept
            t_slope = t

        x_range = np.arange(x[t_slope]-extend_line, x[t_slope]+extend_line)

    # print(clickData['points'][0]['x'])
    # print(type(clickData))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,
                                 angleref="previous",
                             ),))
    fig.add_trace(go.Scatter(x=x_152, y=y_152,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,
                                 angleref="previous",
                             ),))
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=intercept + slope * x_range,
            name='y='+str(round(slope, 3))+'X'+str(round(intercept, 3)),
            mode='lines+markers'))

    fig.add_vline(x=x[t_slope], line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Slope = "+str(round(x[t_slope], 4)), annotation_position="top left")

    fig.update_layout(

        title=metabo+" #"+str(reps) +
        " linear scale  Concentration "+conc_value+' mM',
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="ln(OD600)",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig

###################################################################
####                          logaritmic chart  #5             ####
###################################################################


@ app.callback(Output('chart_5', 'figure'),
               [Input('metabo', 'value'),
               Input('reps', 'value'),
               Input('range1', 'value'),
               Input('range2', 'value'),
               Input('range4', 'value'),
               Input('select_time', 'value'),
               Input('chart_3', 'clickData')])
def update_graph(metabo, reps, range1, range2, range4, select_time, clickData):

    plot_data = df.loc[(df["Metabolite"] == metabo) & (df['Concentration'] == (clickData['points'][0]['x'])) & (df['Number'] == reps) & (
        df['Strain'] == 'WT') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]

    plot_data_152 = df.loc[(df["Metabolite"] == metabo) & (df['Concentration'] == (clickData['points'][1]['x'])) & (df['Number'] == reps) & (
        df['Strain'] == '152') & (df['Time'] >= min(select_time)) & (df['Time'] <= max(select_time))]

    conc_value = str(clickData['points'][1]['x'])

    x = plot_data['Time'].values
    y = np.log(abs(plot_data['OD600'].values))

    x_152 = plot_data_152['Time'].values
    y_152 = np.log(abs(plot_data_152['OD600'].values))

    x_range = []
    t_slope = []
    intercept = 0
    slope = 0
    w = range1
    z = range4
    extend_line = range2
    t_slope = 0
    for t in range(0, x.size-w):
        x_t, y_t = x[t:t+w], y[t:t+w]
        res = linregress(x_t, y_t)
        if abs(sum(y_t))/w < z and res.slope > slope:
            slope = res.slope
            intercept = res.intercept
            t_slope = t

        x_range = np.arange(x[t_slope]-extend_line, x[t_slope]+(extend_line))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,
                                 angleref="previous",
                             ),))
    fig.add_trace(go.Scatter(x=x_152, y=y_152,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,
                                 angleref="previous",
                             ),))
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=intercept + slope * x_range,
            name='y='+str(round(slope, 3))+'X'+str(round(intercept, 3)),
            mode='lines+markers'))

    fig.add_vline(x=x[t_slope], line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Slope = "+str(round(x[t_slope], 4)), annotation_position="top left")

    fig.update_layout(

        title=metabo+" #"+str(reps) +
        " logaritmic scale - ln = log e  Concentration "+conc_value+' mM',
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="ln(OD600)",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
