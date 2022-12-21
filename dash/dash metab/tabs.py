from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_parquet('dash/data/all_matabolites_21_12_22.parquet.gzip')
list_metabolites = df.Metabolite.unique()
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
app.title = 'Metabolite'
tabs_layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=1000,
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
            'border': '1px solid black'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },

        style_table={'height': '1200px', 'overflowY': 'auto'},
        fixed_rows={'headers': True},
        style_filter={
            'backgroundColor': 'rgb(180, 180, 180)',
            'color': 'black',
            'fontWeight': 'bold'

        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(100, 100, 100)',
                'color': 'white'
            }
        ],

        style_cell={'border': '1px solid grey'},)


], className="dbc dbc-row-selectable",)
