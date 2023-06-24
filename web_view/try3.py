import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from config import config
import psycopg2
import pandas as pd
import plotly.graph_objects as go

params_ = config()
conn = psycopg2.connect(**params_)
cur = conn.cursor()

cur.execute("SELECT COUNT (*) FROM logs_table")
total_event_rows = cur.fetchall()
total_event_count_df = pd.DataFrame(total_event_rows)

cur.execute("SELECT COUNT(*) FROM logs_table WHERE event='created'")
created_event_count = cur.fetchall()

cur.execute("SELECT COUNT(*) FROM logs_table WHERE event='modified'")
modified_event_count = cur.fetchall()

cur.execute("SELECT COUNT(*) FROM logs_table WHERE event='deleted'")
deleted_event_count = cur.fetchall()

cur.execute("SELECT COUNT(*) FROM logs_table WHERE event='moved'")
moved_event_count = cur.fetchall()

cur.execute("SELECT COUNT(*) FROM logs_table WHERE event='closed'")
closed_event_count = cur.fetchall()

cur.execute("SELECT event,COUNT(*) FROM logs_table GROUP BY event")
date_count = cur.fetchall()
df3 = pd.DataFrame([[ij for ij in i] for i in date_count])
df3.rename(columns={0: 'event', 1: 'event_count'}, inplace=True)

cur.execute('SELECT event,COUNT(*) AS "Count of Event" FROM logs_table GROUP BY event')
pie = cur.fetchall()
df2 = pd.DataFrame([[ij for ij in i] for i in pie])
df2.rename(columns={0: 'event', 1: 'event_count'}, inplace=True)

# cur.execute("SELECT id, date, time, event, path FROM logs_table ORDER BY id DESC")
# table = cur.fetchall()
# df3 = pd.DataFrame([[ij for ij in i] for i in table])
# df3.rename(columns={0: 'Id', 1: 'Date', 2: 'Time', 3: 'Event', 4: 'Path'}, inplace=True)

cur.execute("SELECT * FROM logs_table ORDER BY id DESC")
table = cur.fetchall()
df3 = pd.DataFrame([[ij for ij in i] for i in table])
df3.rename(columns={0: 'Id', 1: 'Event', 2: 'Path', 3: 'Date', 4: 'Time'}, inplace=True)

layout_chart = dict(
    title='All Events',
    font_color='#000000',
    height=700
)

app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])

# Navigation bar
navbar = html.Div(
    children=[
        html.Button("Home", id="home_button", style={"marginLeft": "auto"},
                    ),

    ],
    className="navbar shadow",
)

# The Event Counters

counters = html.Div([
    html.Div([
        html.H4(children='Total Events',
                style={
                    'textAlign': 'center',
                    'color': '#FFFFFF',
                    'fontSize': '30px'
                }),
        html.P(f'{total_event_rows}',
               style={
                   'textAlign': 'center',
                   'color': '#FFFFFF',
                   'fontSize': '30px'
               })
    ], style={'background-color': '#0000ff', 'width': '310px', 'border-radius': '15px',
              'box-shadow': '2px 2px 2px 2px #060a09'}),

    html.Div([
        html.H6(children='Created Events',
                style={
                    'textAlign': 'center',
                    'color': '#FFFFFF',
                    'fontSize': '30px'
                }),
        html.P(f'{created_event_count}',
               style={
                   'textAlign': 'center',
                   'color': '#FFFFFF',
                   'fontSize': '30px'
               })
    ], style={'background-color': '#ffa500', 'width': '310px', 'border-radius': '15px',
              'box-shadow': '2px 2px 2px 2px #060a09'}),

    html.Div([
        html.H4(children='Modified Events',
                style={
                    'textAlign': 'center',
                    'color': '#FFFFFF',
                    'fontSize': '30px'
                }),
        html.P(f'{modified_event_count}',
               style={
                   'textAlign': 'center',
                   'color': '#CFFFFFF',
                   'fontSize': '30px'
               })
    ], style={'background-color': '#8d30eb', 'width': '310px', 'border-radius': '15px',
              'box-shadow': '2px 2px 2px 2px #060a09'}),

    html.Div([
        html.H4(children='Deleted Events',
                style={
                    'textAlign': 'center',
                    'color': '#FFFFFF',
                    'fontSize': '30px'
                }),
        html.P(f'{deleted_event_count}',
               style={
                   'textAlign': 'center',
                   'color': '#FFFFFF',
                   'fontSize': '30px'
               })
    ], style={'background-color': '#ff0000', 'width': '310px', 'border-radius': '15px',
              'box-shadow': '2px 2px 2px 2px #060a09'}),

    html.Div([
        html.H4(children='Moved Events',
                style={
                    'textAlign': 'center',
                    'color': '#FFFFFF',
                    'fontSize': '30px',
                }),
        html.P(f'{moved_event_count}',
               style={
                   'textAlign': 'center',
                   'color': '#FFFFFF',
                   'fontSize': '30px'
               })
    ], style={'background-color': '#008000', 'width': '310px', 'border-radius': '15px',
              'box-shadow': '2px 2px 2px 2px #060a09'}),

], className='counter-flexbox 5 columns')

# tables = go.Figure((go.Table(
#             header=dict(values=list(df3.columns),
#                         fill_color='#FFFFFF',
#                         line_color='#000000',
#                         font=dict(color="#000000", size=18),
#                         align='left'),
#             cells=dict(values=[df3.Id, df3.Date, df3.Time, df3.Event, df3.Path],
#                        fill_color='#FFFFFF',
#                        line_color='#000000',
#                        font=dict(color="#000000", size=16),
#                        height=69,
#                        align='left')
#         )))

# tables = html.Div([
#         html.Div([
#             dcc.Graph(figure=go.Figure(layout=layout_chart).add_trace(go.Table(
#                 header=dict(values=list(df3.columns),
#                             fill_color='#FFFFFF',
#                             line_color='#000000',
#                             font=dict(color="#000000", size=18),
#                             align='left'),
#                 cells=dict(values=[df3.Id, df3.Date, df3.Time, df3.Event, df3.Path],
#                            fill_color='#FFFFFF',
#                            line_color='#000000',
#                            font=dict(color="#000000", size=16),
#                            height=69,
#                            align='left')
#
#             )))
#         ], className='card_container3 twelve columns')
#     ])

app.layout = html.Div([
    html.Div([navbar]),
    html.Div([counters], className='flex-container'),
    html.Div([
        html.P(id='events_table'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i}
                     for i in df3.columns],
            data=df3.to_dict('records'),
            page_size=10,
            fixed_rows={'headers': True, 'data': 0},
            style_table={'overflowY': 'scroll', 'border-radius': '7px', 'maxHeight': '500'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#FFFFFF',
                }
            ],
            # style_header=dict(backgroundColor='red', fontWeight='bold', fontSize='20', lineHeight='25px'),
            # style_data=dict(backgroundColor='black', lineHeight='40px'),
            style_header={'background-color': '#b076ea', 'font-weight': 'bold',
                          'font-size': '18px', 'line-height': '40px',
                          'text-align': 'left'},

            style_data={'font-size': '15px', 'background-color': '#ebedef',
                        'line-height': '40px', 'color': 'black',
                        'text-align': 'left'}
        ),
    ], className='tabl_container')
])
if __name__ == "__main__":
    app.run_server(debug=True)
