import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import config
import psycopg2
import dash
from dash import dcc, html
# from app import app

params_ = config()
conn = psycopg2.connect(**params_)
cur = conn.cursor()

# setting the margins
layout = go.Layout(
    margin=go.layout.Margin(
        l=40,  # left margin
        r=40,  # right margin
        b=10,  # bottom margin
        t=35  # top  margin
    )
)


def o_modified():
    layout1 = dict(
        width=900,
        height=300,
    )
    html.H1('All Modified Events', style={'text-align': 'centre'}),
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'modified'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    table_chart = dcc.Graph(
        figure=go.Figure(layout=layout1).add_trace(go.Table(
            header=dict(values=list(df1.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                       fill_color='lavender',
                       align='left'))
        ))
    return table_chart


def o_created():
    layout2 = dict(
        width=900,
        height=300,
    )
    html.H1('All Create Events', style={'text-align': 'centre'}),
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'created'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    table_chart = dcc.Graph(
        figure=go.Figure(layout=layout2).add_trace(go.Table(
            header=dict(values=list(df1.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                       fill_color='lavender',
                       align='left'))
        ))
    return table_chart


def o_moved():
    layout3 = dict(
        width=900,
        height=300,
    )
    html.Div([html.H1('All Moved/Renamed Events', style={'text-align': 'centre'})])
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'moved'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    table_chart = dcc.Graph(
        figure=go.Figure(layout=layout3).add_trace(go.Table(
            header=dict(values=list(df1.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                       fill_color='lavender',
                       align='left'))
        ))
    return table_chart


def o_deleted():
    layout4 = dict(
        width=900,
        height=300,
    )
    html.H1('All Deleted Events', style={'text-align': 'centre'}),
    cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'deleted'")
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
    table_chart = dcc.Graph(
        figure=go.Figure(layout=layout4).add_trace(go.Table(
            header=dict(values=list(df1.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
                       fill_color='lavender',
                       align='left'))
        ))
    return table_chart


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Finter', style={'text-align': 'centre'}),
    o_created(),
    o_modified(),
    o_created(),
    o_deleted()
])

if __name__ == '__main__':
    app.run_server(debug=True)

# class time_dropdown():
#
#     @staticmethod
#     def o_alll():
#         cur.execute('SELECT id, date, time, event, path FROM logs_table')
#         tablee = cur.fetchall()
#         df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
#         df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
#         table_chart = dcc.Graph(
#             figure=go.Figure(data=[go.Table(
#                 header=dict(values=list(df1.columns),
#                             fill_color='paleturquoise',
#                             align='left'),
#                 cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
#                            fill_color='lavender',
#                            align='left'))
#             ]))
#         return table_chart
#
#     @staticmethod
#     def o_modified():
#         cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'modified'")
#         tablee = cur.fetchall()
#         df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
#         df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
#         table_chart = dcc.Graph(
#             figure=go.Figure(data=[go.Table(
#                 header=dict(values=list(df1.columns),
#                             fill_color='paleturquoise',
#                             align='left'),
#                 cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
#                            fill_color='lavender',
#                            align='left'))
#             ]))
#         return table_chart
#
# @staticmethod
# def o_created():
#     cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'created'")
#     tablee = cur.fetchall()
#     df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
#     df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
#     table_chart = dcc.Graph(
#         figure=go.Figure(data=[go.Table(
#             header=dict(values=list(df1.columns),
#                         fill_color='paleturquoise',
#                         align='left'),
#             cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
#                        fill_color='lavender',
#                        align='left'))
#         ]))
#     return table_chart
#
#     @staticmethod
#     def o_deleted():
#         cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'deleted'")
#         tablee = cur.fetchall()
#         df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
#         df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
#         table_chart = dcc.Graph(
#             figure=go.Figure(data=[go.Table(
#                 header=dict(values=list(df1.columns),
#                             fill_color='paleturquoise',
#                             align='left'),
#                 cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
#                            fill_color='lavender',
#                            align='left'))
#             ]))
#         return table_chart
#
#     @staticmethod
#     def o_moved():
#         cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'moved'")
#         tablee = cur.fetchall()
#         df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
#         df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
#         table_chart = dcc.Graph(
#             figure=go.Figure(data=[go.Table(
#                 header=dict(values=list(df1.columns),
#                             fill_color='paleturquoise',
#                             align='left'),
#                 cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
#                            fill_color='lavender',
#                            align='left'))
#             ]))
#         return table_chart
#
#     @staticmethod
#     def o_closed():
#         cur.execute("SELECT id, date, time, event, path  FROM logs_table WHERE event = 'closed'")
#         tablee = cur.fetchall()
#         df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
#         df1.rename(columns={0: 'id', 1: 'date', 2: 'time', 3: 'event', 4: 'path'}, inplace=True)
#         table_chart = dcc.Graph(
#             figure=go.Figure(data=[go.Table(
#                 header=dict(values=list(df1.columns),
#                             fill_color='paleturquoise',
#                             align='left'),
#                 cells=dict(values=[df1.id, df1.date, df1.time, df1.event, df1.path],
#                            fill_color='lavender',
#                            align='left'))
#             ]))
#         return table_chart
#
#     html.Div([
#
#         html.Br(),
#         html.Div(id='data_idk'),
#         html.Br(),
#
#         html.Label(['Choose column:'], style={'font-weight': 'bold', "text-align": "center"}),
#         dcc.Dropdown(id='event_dropdown',
#                      options=[
#                          {'label': 'All', 'value': 'only_alll'},
#                          {'label': 'Modified', 'value': 'o_modified'},
#                          {'label': 'Created', 'value': 'o_created'},
#                          {'label': 'Deleted', 'value': 'o_deleted'},
#                          {'label': 'Moved', 'value': 'o_moved'},
#                          {'label': 'Closed', 'value': 'o_closed'},
#                      ],
#                      optionHeight=25,
#                      value='all',
#                      disabled='False',
#                      multi='False',
#                      searchable=True,
#                      search_value='',
#                      placeholder='Please Select',
#                      clearable=True,
#                      style={'width': "100%"},
#                      className='select_box',
#                      persistence=True,
#                      persistence_type='memory'
#                      ),
#     ], className='three columns')
#
#
# def event_dropdown():
#     val = (
#         f"""
#         SELECT * FROM logs_table
#         WHERE date > now() - INTERVAL '24 HOURS' """
#     )
#

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Finter', style={'text-align': 'centre'}),

])

