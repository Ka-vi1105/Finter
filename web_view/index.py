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

cur.execute('SELECT event,COUNT(*) AS "Count of Event" FROM logs_table GROUP BY event')
pie = cur.fetchall()
df2 = pd.DataFrame([[ij for ij in i] for i in pie])
df2.rename(columns={0: 'event', 1: 'event_count'}, inplace=True)

# fetching info for all events table
cur.execute("SELECT * FROM logs_table ORDER BY id DESC")
table = cur.fetchall()
df3 = pd.DataFrame([[ij for ij in i] for i in table])
df3.rename(columns={0: 'Id', 1: 'Event', 2: 'Path', 3: 'Date', 4: 'Time'}, inplace=True)

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
    ], className='box-higher', style={'background-color': '#0000ff', 'width': '310px', 'border-radius': '15px',
                                      }),

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
    ], className='box-higher', style={'background-color': '#ffa500', 'width': '310px', 'border-radius': '15px',
                                      }),

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
    ], className='box-higher', style={'background-color': '#8d30eb', 'width': '310px', 'border-radius': '15px',
                                      }),

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
    ], className='box-higher', style={'background-color': '#ff0000', 'width': '310px', 'border-radius': '15px',
                                      }),

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
    ], className='box-higher', style={'background-color': '#008000', 'width': '310px', 'border-radius': '15px',
                                      }),

], className='counter-flexbox 5 columns')

layout = go.Layout(width=1000, height=600)

bar_chart_events = html.Div([
    dcc.Graph(
        id='all_bar_chart', figure=go.Figure(layout=layout).add_trace(go.Bar(
            x=df2['event'],
            y=df2['event_count'],
            width=0.2,
            marker={'color': '#6d40bd'}
        )).update_layout(
            title='All Events',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            yaxis_gridcolor='#efefef'
        ), style={'display': 'inline-block'}, config={'displayModeBar': False})
], className='bar-chart-container')

# line chart for last 5 days monitored

layout_line_5 = go.Layout(height=600, )

cur.execute('SELECT date, count(*) FROM logs_table GROUP BY date ORDER '
            'BY date desc LIMIT 5 OFFSET 0;')
line = cur.fetchall()
df4 = pd.DataFrame([[ij for ij in i] for i in line])
df4.rename(columns={0: 'date', 1: 'count'}, inplace=True)

line_chart_five_days = html.Div([
    dcc.Graph(figure=go.Figure(layout=layout_line_5).add_trace(go.Scatter(
        x=df4['date'],
        y=df4['count'],
        line={'color': '#6d40bd', 'width': 4},
        marker={'size': 10}
    )).update_layout(
        title='5 days',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        yaxis_gridcolor='#efefef'
    ), style={'display': 'inline-block'}, config={'displayModeBar': False})
], className='line_chart_5_d')

app.layout = \
    html.Div([
        html.Div([navbar]),
        html.Div([counters], className='flex-container'),
        html.Div([html.Div([
            html.P(id='event_table'),
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
        ], className='table-container')
        ], className='tabl_container'),

        html.Div([bar_chart_events,
                  line_chart_five_days], className='container-i'),
        dcc.Interval(
            id='interval_component',
            interval=1000,
            n_intervals=0
        )
    ])


@app.callback(Output('table', 'data'),
              [Input('interval_component', 'n_intervals')])
def update_table(n):
    cur.execute("SELECT * FROM logs_table ORDER BY id DESC")
    table = cur.fetchall()
    df3 = pd.DataFrame([[ij for ij in i] for i in table])
    df3.rename(columns={0: 'Id', 1: 'Event', 2: 'Path', 3: 'Date', 4: 'Time'}, inplace=True)
    return df3.to_dict('records')


# @app.callback(Output('all_bar_chart', 'figure'),
#               [Input('interval_component', 'n_intervals')])
# def update_all_bar_chart(self):
#     cur.execute('SELECT event,COUNT(*) AS "Count of Event" FROM logs_table GROUP BY event')
#     pie = cur.fetchall()
#     df2 = pd.DataFrame([[ij for ij in i] for i in pie])
#     df2.rename(columns={0: 'event', 1: 'event_count'}, inplace=True)
#     return figure


if __name__ == "__main__":
    app.run_server(debug=True)
