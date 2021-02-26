import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from pathlib import Path
from flask import g
import datetime as dt
import plotly
import plotly.graph_objects as go
import json

##### Create Connection pool ######
def conn_pool(minconn, maxconn, /, host='localhost', database='phonebook', user='postgres', password=1):

    return ThreadedConnectionPool(minconn,
                                  maxconn,
                                  host=host,
                                  database=database,
                                  user=user,
                                  password=password)


############ query func  ##########
def query(query, vals=""):

    query = "sql/" + query + ".sql"
    path = Path(query)

    with open(path, 'r') as f:
        query_text = str(f.read())

    cur = g.conn.cursor(cursor_factory=DictCursor)
    cur.execute(query_text, vals)
    return cur


############## convet date and time to datetime ############

def conv_datetime(date, time):
    date = str(date)
    time = str(time)
    # # reference for date formatting
    # %d	Day of the month (decimal number)
    # %m	Month (decimal number)
    # %b	Month (abbreviated)
    # %B	Month (full name)
    # %y	Year (2 digit)
    # %Y	Year (4 digit)
    return dt.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')


def plotter(rows):
    try:
        actions = [row['action'] for row in rows]
        dates = [row['datetime'] for row in rows]
        notes = [row['description'] for row in rows]

        lenght = range(1, len(actions)+1)

        fig = go.Figure()
        
        for i, j, k, l in zip(dates, actions, notes, lenght):

            # fig.add_trace(go.Scatter(mode='text', x=[i], y=[l+0.25], text=[j],  showlegend=True))
            # ignore the notes for now

            fig.add_trace(go.Scatter(mode='text', x=[i], y=[l+0.25], text=[j],  showlegend=True))
            fig.add_trace(go.Scatter(mode='lines', x=[i], y=[0], line_color='black'))
            fig.add_trace(go.Scatter(mode='markers', x=[i], y=[0], marker=dict(color='black',
                                    line=dict(color='black')), name=j))
                                    
            fig.add_shape(x1=i, x0=i, y1=l, y0=0, line=dict(color='black'))

        fig.update_layout(template="plotly_white", showlegend=False,
                        yaxis=dict(showgrid=False, range=[0, len(actions)+2], visible=False),
                        xaxis=dict(showgrid=False, visible=True, showline=True, zeroline=True, zerolinewidth=2))

        # JSONify:
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    except:
        return {}


