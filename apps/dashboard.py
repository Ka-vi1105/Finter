import dash_bootstrap_components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import config
import psycopg2
import dash
from dash import dash_table
from dash import dcc, html
from collections import deque
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

# from app import app

params_ = config()
conn = psycopg2.connect(**params_)
cur = conn.cursor()


# setting the margins
# layout = go.Layout(
#     margin=go.layout.Margin(
#         l=5,  # left margin
#         r=5,  # right margin
#         b=5,  # bottom margin
#         t=5  # top  margin
#     )
# )


def bar_chart():
    # layout = dict(
    #     width=500,
    #     height=500
    # )
    cur.execute('SELECT event,COUNT(*) AS "Count of Event" FROM logs_table GROUP BY event')
    rows = cur.fetchall()
    df = pd.DataFrame([[ij for ij in i] for i in rows])
    df.rename(columns={0: 'event', 1: 'event_count'}, inplace=True)
    barChart = dcc.Graph(id='live-graph', animate=True, figure=go.Figure(layout=layout).add_trace(go.Bar(x=df['event'],
                                                                                                         y=df[
                                                                                                             'event_count'],
                                                                                                         )).update_layout(
        title='Event_Count', showlegend=True),
                         style={'width': '30%', 'height': '40vh', 'display': 'inline-block', 'color': 'event_count'})
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=0
    )

    @app.callback(
        Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')]
    )
    def update_graph(n):
        return bar_chart()

    return barChart


def line_chart():
    layout = dict(
        font_color='#FFFFFF',
        paper_bgcolor='#232323',
        plot_bgcolor='#2B2845',
        xaxis_gridcolor='rgba(0,0,0,0)',
        yaxis_gridcolor='rgb(56, 45, 69)',
        title_font_color='#FFFFFF',
        width=600,
        height=500
    )
    cur.execute('SELECT event,COUNT(*) AS "Count of Event" FROM logs_table GROUP BY event')
    rows = cur.fetchall()
    df0 = pd.DataFrame([[ij for ij in i] for i in rows])
    df0.rename(columns={0: 'event', 1: 'event_count'}, inplace=True)
    # fig0 = px.line(df0, x='date', y='event')
    # fig0.show()
    app.layout = html.Div([
        dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Scatter(x=df0['event'],
                                                                       y=df0['event_count'],
                                                                       )).update_layout(
            title='Event Count'),
            style={'display': 'inline-block'})
    ], className='chart-line')
    return app.layout


def event_count():
    layout = dict(
        title='Event Count Table',
        font_color='#000000',
        paper_bgcolor='#232323',
        title_font_color='#FFFFFF',
        # width=600,
        height=500
    )
    cur.execute('SELECT event,COUNT(*) AS "Count of Event" FROM logs_table GROUP BY event')
    rows = cur.fetchall()
    df0 = pd.DataFrame([[ij for ij in i] for i in rows])
    df0.rename(columns={0: 'Event', 1: 'Event_count'}, inplace=True)
    # fig0 = px.line(df0, x='date', y='event')
    # fig0.show()
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout).add_trace(go.Table(
                header=dict(values=list(df0.columns),
                            fill_color='#D04AFA',
                            line_color='#372C44',
                            font=dict(color='#FFFFFF', size=16),
                            align='left'),
                cells=dict(values=[df0.Event, df0.Event_count],
                           fill_color='#D04AFA',
                           line_color='#372C44',
                           font=dict(color='#FFFFFF', size=15),
                           height=62,
                           align='left'))
            ))
    ], className='dash-chart-2')
    return app.layout


def line_chart2():
    # layout = dict(
    #     width=500,
    #     height=500
    # )
    cur.execute('SELECT id, date, event from logs_table')
    rows = cur.fetchall()
    df0 = pd.DataFrame([[ij for ij in i] for i in rows])
    df0.rename(columns={0: 'id', 1: 'date', 2: 'event'}, inplace=True)
    # fig0 = px.line(df0, x='date', y='event')
    # fig0.show()
    lineChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Scatter(x=df0['date'],
                                                                               y=df0['event'],
                                                                               )).update_layout(
        title='Page Views'),
        style={'display': 'inline-block'})
    return lineChart


def tables():
    layout = dict(
        title='All Events',
        font_color='#000000',
        paper_bgcolor='#232323',
        title_font_color='#FFFFFF',
        width=1200,
        height=700
    )
    cur.execute('SELECT id, date, time, event, path FROM logs_table')
    tablee = cur.fetchall()
    df1 = pd.DataFrame([[ij for ij in i] for i in tablee])
    df1.rename(columns={0: 'Id', 1: 'Date', 2: 'Time', 3: 'Event', 4: 'Path'}, inplace=True)
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout).add_trace(go.Table(
                header=dict(values=list(df1.columns),
                            fill_color='#D04AFA',
                            line_color='#372C44',
                            font=dict(color="#FFFFFF", size=16),
                            align='left'),
                cells=dict(values=[df1.Id, df1.Date, df1.Time, df1.Event, df1.Path],
                           fill_color='#D04AFA',
                           line_color='#372C44',
                           font=dict(color='#FFFFFF', size=15),
                           height=70,
                           align='left'))
            ))
    ], className='dash-chart')
    return app.layout


def pie_chart():
    layout = dict(
        font_color='#FFFFFF',
        # paper_bgcolor='#C495FD',
        paper_bgcolor='#232323',
        title_font_color='#FFFFFF',
        plot_bgcolor='blue',
        height=500
    )
    cur.execute('SELECT event,COUNT(*) AS "Count of Event" FROM logs_table GROUP BY event')
    pie = cur.fetchall()
    df2 = pd.DataFrame([[ij for ij in i] for i in pie])
    df2.rename(columns={0: 'event', 1: 'event_count'}, inplace=True)
    app.layout = html.Div([
        dcc.Graph(
            figure=go.Figure(layout=layout).add_trace(go.Pie(
                labels=df2['event'],
                values=df2['event_count'],
                marker=dict(
                    line=dict(color='#ffffff', width=2)))).update_layout(title='Events',
                                                                         showlegend=True),
            style={'display': 'inline-block'})
    ], className='chart_pie')

    return app.layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.Div([pie_chart()]),
        html.Div([event_count()]),
        html.Div([line_chart()])
    ], className='flex-container'),
    html.Div([
        tables(),
    ], className='single-chart-flex')
], className='card-chart')

# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([html.Div([
#             pie_chart(),
#             event_count(),
#             line_chart(),
#         ], className='flex-container')]),
#         # html.Div([
#         #     pie_chart(),
#         #     event_count(),
#         #     line_chart(),
#         # ], className='flex-container')
#     ]),
#     dbc.Row([
#         html.Div([
#             tables(),
#         ], className='single-chart-flex')
#     ])
# ])


if __name__ == '__main__':
    app.run_server()
