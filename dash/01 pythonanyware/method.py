from dash import Dash, dcc, html, Input, Output
app = Dash(__name__, )
server = app.server
app.title = 'Metabolite'
method_layout = html.Div([
    html.Br(),
    html.H2('Analysis of the upper limit of the wild type to the common metabolites',
            style={'color': 'white', 'font-weight': 'bold'}),
    html.H3('We aimed to identify for the first time the upper limit for metabolite overfeeding in wild-type cells. We have performed an extensive kinetic analysis of the yeast growth upon the supplementation of the metabolites of interest (twenty amino acids and five nucleobases) to the media. We developed a web- based application this site :) that allows for user-friendly exploration of our data. The application features two distinct sections, one dedicated to the examination of the upper limits of individual metabolites for each experiment, and the other providing an overall perspective of the entire dataset that was gathered. We have then calculated the upper limit for each metabolite as follows:',
            style={'color': 'white'}),
    html.Div([
        html.H3('    1. Determination the highest growth rate: For each concentration, the highest slope is determined, which corresponds to the exponential growth phase.', style={
                'color': 'white'}),
        html.H3('    2. Slope calculation: Starting at time zero, a user-adjustable window of time points, with a default value of five, is considered and the slope of OD (optical density) versus time is calculated using linear least-square regression and saved. The process is repeated by moving one time point and considering the next window of time points.',
                style={'color': 'white'}),
        html.H3('    3. All possible slopes are calculated, and the maximum slope is plotted against each concentration.', style={
                'color': 'white'}),
        html.H3('    4. Determination of minimum base line slope: A minimum slope line is determined by using 25% of the highest slope as the threshold. However, this percentage can be adjusted by the user.', style={
                'color': 'white'}),
        html.H3('    5. Determination of upper limit point: The upper limit point is determined by identifying the two points that cross the minimal line and fall within the range of the minimum slope on both edges.', style={
                'color': 'white'}),
        html.H3('    6. The concentrations associated with those points are used to establish the range of the upper limit.', style={
                'color': 'white'}),
    ], style={"margin-left": "5%"}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

], style={'padding': '5rem', 'font-family': "Times New Roman"})
