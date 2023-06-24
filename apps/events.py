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


# app = dash.Dash(__name__)

# layout = go.Layout(
#     margin=go.layout.Margin(
#         l=40,  # left margin
#         r=40,  # right margin
#         b=10,  # bottom margin
#         t=35  # top  margin
#     )
# )


def o_modified():
    layout1 = dict(
        title='All File Modified Events',
        font_color='#FFFFFF',
        paper_bgcolor='#342A41',
        title_font_color='#FFFFFF',
        width=1400,
        height=700
    )
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'modified'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout1).add_trace(go.Table(
                header=dict(values=list(df1.columns),
                            fill_color='#342A41',
                            line_color='#FFFFFF',
                            font=dict(color="#FFFFFF", size=16),
                            align='left'),
                cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                           fill_color='#342A41',
                           line_color='#FFFFFF',
                           font=dict(color='#FFFFFF', size=15),
                           height=70,
                           align='left'))
            ))
    ], className='dash-chart')
    return app.layout


def o_created():
    layout2 = dict(
        title='All Created Events',
        font_color='#FFFFFF',
        paper_bgcolor='#342A41',
        title_font_color='#FFFFFF',
        width=1400,
        height=700
    )
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'created'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout2).add_trace(go.Table(
                header=dict(values=list(df1.columns),
                            fill_color='#342A41',
                            # line_color='#372C44',
                            line_color='#FFFFFF',
                            font=dict(color="#FFFFFF", size=16),
                            align='left'),
                cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                           fill_color='#342A41',
                           # line_color='#372C44',
                           line_color='#FFFFFF',
                           font=dict(color='#FFFFFF', size=15),
                           height=70,
                           align='left'))
            ))
    ], className='dash-chart')
    return app.layout


def o_moved():
    layout = dict(
        title='All Moved/Renamed Events',
        font_color='#FFFFFF',
        paper_bgcolor='#342A41',
        title_font_color='#FFFFFF',
        width=1400,
        height=700
    )
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'moved'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout).add_trace(go.Table(
                header=dict(values=list(df1.columns),
                            fill_color='#342A41',
                            line_color='#FFFFFF',
                            font=dict(color="#FFFFFF", size=16),
                            align='left'),
                cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                           fill_color='#342A41',
                           line_color='#FFFFFF',
                           font=dict(color='#FFFFFF', size=15),
                           height=70,
                           align='left'))
            ))
    ], className='dash-chart')
    return app.layout


def o_deleted():
    layout = dict(
        title='All Deleted Events',
        font_color='#FFFFFF',
        paper_bgcolor='#342A41',
        title_font_color='#FFFFFF',
        width=1400,
        height=700
    )
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'deleted'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout).add_trace(go.Table(
                header=dict(values=list(df1.columns),
                            fill_color='#342A41',
                            line_color='#FFFFFF',
                            font=dict(color="#FFFFFF", size=16),
                            align='left'),
                cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                           fill_color='#342A41',
                           line_color='#FFFFFF',
                           font=dict(color='#FFFFFF', size=15),
                           height=70,
                           align='left'))
            ))
    ], className='dash-chart')
    return app.layout


app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.Div([
            o_created(),
        ], className='flex-container')])
    ]),
    dbc.Row([
        dbc.Col([html.Div([
            o_modified(),
        ], className="flex-container")])
    ]),
    dbc.Row([
        dbc.Col([html.Div([
            o_deleted(),
        ], className="flex-container")])
    ]),
    dbc.Row([
        dbc.Col([html.Div([
            o_moved(),
        ], className="flex-container")])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
