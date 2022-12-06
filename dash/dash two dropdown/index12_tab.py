from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import linregress

df = pd.read_parquet('dash/data/all_matabolites_5_11_22.parquet.gzip')
list_metabolites = df.Metabolite.unique()
metabo = 'Alanine'
app = Dash(__name__, )
app.title = 'Metabolite'
