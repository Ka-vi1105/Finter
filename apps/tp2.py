from dash import Dash, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import config
import psycopg2
import dash
from dash import dcc, html
# from app import app
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

params_ = config()
conn = psycopg2.connect(**params_)
cur = conn.cursor()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def o_deleted():
    layout = dict(
        width=900,
        height=300,
    )
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'deleted'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout).add_trace(go.Table(
                header=dict(values=list(df1.columns),
                            font_color='#FFFFFF',
                            fill_color='#212529',
                            align='left'),
                cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                           font_color='#FFFFFF',
                           fill_color='#212529',
                           align='left')
            ))
        ),
    ])
    return app.layout


def ok_deleted():
    layout = dict(
        width=900,
        height=300,
    )
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'deleted'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    app.layout = html.Div([
        html.Div(className='table-chart'),
        dcc.Graph(
            figure=go.Figure(layout=layout).add_trace(go.Table(
                header=dict(values=list(df1.columns),
                            font_color='#FFFFFF',
                            fill_color='#212529',
                            align='left'),
                cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                           font_color='#FFFFFF',
                           fill_color='#212529',
                           align='left'),
            ))
        ),
    ])
    return app.layout


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('All Events Table', style={'textAlign': 'center', 'color': '#FFFFFF'}),
        ], width=12),
        dbc.Col([
            o_deleted()
        ], className='chart-card', width='12')
    ], className='chart-card'),
    dbc.Row([
        dbc.Col([
            html.H1('All Events Table', style={'textAlign': 'center', 'color': '#FFFFFF'}),
            ok_deleted()
        ], width=12)
    ])
])
if __name__ == '__main__':
    app.run_server(debug=True)
