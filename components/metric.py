from datetime import timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import streamlit as sl
from icecream import ic


@sl.cache_data
def total_monitored(df, label, reference=None, report=False):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=df,
            number={
                "font.size": 30,
                "font.color": "black",
            },
            title={
                "text": label,
                "font": {"size": 15, 'color':'black'},
            },
        )
    )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    
    if report:
        paper='rgba(42, 94, 179,1)'
        plot='rgba(42, 94, 179,1)'
    else:
        paper='rgba(248, 248, 255, 1)'
        plot='rgba(248, 248, 255, 1)'

    
    fig.update_layout(
        # margin=dict(t=30, b=0),
        showlegend=False,
        # modebar=False,
        paper_bgcolor=paper,
        plot_bgcolor=plot,
        height=100,
        width=250,
        template={
            "data": {
                "indicator": [
                    {
                        "mode": "number+delta",
                        "delta": {"reference": reference,
                                  "relative": True,
                                  "valueformat": ".1%",
                                  # "position": "right"
                                  },
                    }
                ]
            }
        },
        title={
            'text': 'vs previous week',
            'y': 0.12,
            'x': 0.38,
            'font': {'size': 12, 'color':'black'}
        },
    )

    return fig

@sl.cache_data
def total_monitored_rpt(df, label, reference=None):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=df,
            number={
                "font.size": 10,
                "font.color": "black",
            },
            title={
                "text": label,
                "font": {"size": 7, 'color':'black'},
            },
        )
    )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    
    # if report:
    #     paper='rgba(42, 94, 179,0.7)'
    #     plot='rgba(42, 94, 179,0.7)'
    # else:
    #     paper='rgba(248, 248, 255, 0)'
    #     plot='rgba(248, 248, 255, 0)'
    fig.add_shape(type="rect",
        xref="paper", yref="paper",
        x0=-23.5, y0=-9, x1=25, y1=12.8, 
        line=dict(
            #color="RoyalBlue",
            color='rgba(42, 94, 179,0.7)', #named colors from https://stackoverflow.com/a/72502441/8508004
            width=1,
        ),
        #fillcolor="LightSkyBlue",
    )

    

    if reference is None:
        message = ""
    else:
        message = "vs previous week"

    fig.update_layout(
        # margin=dict(t=30, b=0),
        showlegend=False,
        # modebar=False,
        paper_bgcolor='rgba(248, 248, 255, 0)',
        plot_bgcolor='rgba(248, 248, 255, 0)',
        height=45,
        width=100,
        template={
            "data": {
                "indicator": [
                    {
                        "mode": "number+delta",
                        "delta": {"reference": reference,
                                  "relative": True,
                                  "valueformat": ".1%",
                                  # "position": "right"
                                  },
                    }
                ]
            }
        },
        title={
            'text': message,
            'y': 0.12,
            'x': 0.50,
            'font': {'size': 5, 'color':'black'}
        },
    )

    return fig

@sl.cache_data
def plot(df, x, y, title, color=None, line=True):

    if line:
        fig = px.line(
            df,
            x=x,
            y=y,
            title=title,
            color=color,
            text=y
            # category_orders={'day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']},
        )
        fig.update_traces(textposition="top right")
    else: 
        fig = px.bar(
            df,
            x=x,
            y=y,
            orientation="h",
            title=title,
            color=color,
            text=x,
            barmode='group',
            
        )
    
    fig.update_xaxes(visible=True, 
                    title="", 
                    fixedrange=True,
                    categoryorder='array',
                    categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    )
    fig.update_yaxes(visible=True, title="", fixedrange=True, showticklabels=True)
    fig.update_layout(
        paper_bgcolor='rgba(248, 248, 255, 1)',
        plot_bgcolor='rgba(248, 248, 255, 1)',
        # paper_bgcolor='rgba(0, 0, 0, 0)',
        # plot_bgcolor='rgba(0, 0, 0, 0)',
        title=title,
        height=350,
        showlegend=False,
        # width=500,
        # template="plotly_white"
    )

    sl.plotly_chart(fig, use_container_width=True)

def plot_chart(df, x, y, title, color=None, line=True, text=None, margin_left=None, prev_week=None, week=None, not_school=False, reference=None):
    
    if prev_week is not None:
        if line:
            fig = go.Figure(
                data=[
                    go.Scatter(
                        name=f'Week {week}', 
                        x=df[x], 
                        y=df[y],
                        marker_color='#133884',
                        text=df[y]
                    ),
                    go.Scatter(
                        name=f'Week {int(week) - 1}', 
                        x=prev_week[x], 
                        y=prev_week[y],
                        marker_color='#df1010',
                        text=prev_week[y],
                        textposition='top center'
                    )
                ]
            )
        else:
            fig = go.Figure(
                data=[
                    go.Bar(
                        name=f'Week {int(week) - 1}', 
                        x=prev_week[x], 
                        y=prev_week[y],
                        marker_color='#df1010',
                        width=0.4,
                        text=prev_week[y],
                        textposition='auto',
                    ),
                    go.Bar(
                        name=f'Week {week}', 
                        x=df[x], 
                        y=df[y],
                        marker_color='#133884',
                        width=0.4,
                        text=df[y],
                        textposition='auto',
                    ),
                ]
            )
    else:
        if line:
            fig = px.line(
                df,
                x=x,
                y=y,
                title=title,
                color=color,
                color_discrete_sequence =['rgba(42, 94, 179,1)']*len(df),
                text=y,
                # category_orders={'day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
            )
            fig.update_traces(textposition="top right")
        else: 

            fig = px.bar(
                df,
                x=x,
                y=y,
                orientation="v",
                title=title,
                color=color,
                color_discrete_sequence =['rgba(42, 94, 179,1)']*len(df),
                text=text,
                # barmode='group',
                
            )

    if reference is not None:
        fig.add_hline(y=reference[0], line_dash="dash", line_color='red',
              annotation_text=f"Average: {reference[0]}", 
              annotation_position="top left")
    
    fig.update_xaxes(
        visible=True, 
        title="", 
        fixedrange=True, 
        showgrid=False,
        categoryorder='array',
        categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    )
    fig.update_yaxes(visible=True, title="", fixedrange=True, showticklabels=True, showgrid=False)
    fig.update_layout(
        paper_bgcolor='rgba(179, 149, 42, 0.6)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        # barmode='group',
        title=f"<span style='font-size:14px; font-weight:bold; color:black;'>{title}</span>",
        height=330 if not_school is False else 370,
        showlegend=True if prev_week is not None else False,
        width=750,
        margin=dict(l=margin_left,r=40,b=40 if not_school is False else 80,
                t=40,
        ),
        # template="plotly_white"
    )

    return fig

@sl.cache_data
def table(df, title):
    dfl = df[['class_date', 'class_time', 'lecturer', 'coursecode', 'week', 'reporter', 'observation']]
    dfls = df[['class_date', 'day', 'class_time', 'lecturer', 'coursecode', 'week', 'school', 'comment','observation','day_num']]

    dfl = dfl[(dfl['observation'] == 'The Class did not hold') | (dfl['observation'] == 'The Teacher was Absent From Class') | (dfl['observation'] == 'The Teacher was present but left early')]
    dfls = dfls[(dfls['observation'] == 'The Class did not hold') | (dfls['observation'] == 'The Teacher was Absent From Class') | (dfls['observation'] == 'The Teacher was present but left early')]

    dfl.columns = ['Date & Time', 'Class time', 'Lecturer Name', 'Course Code', 'Week', 'Reporter', 'Observation']
    dfls.columns = ['Date & Time', 'Day', 'Class time', 'Lecturer Name', 'Course Code', 'Week', 'School', 'Comment', 'Observation','day_num']

    dfl['Date & Time'] = dfl['Date & Time'].astype(str)
    dfls['Date & Time'] = dfls['Date & Time'].astype(str)

    dfls = dfls.drop("Observation", axis=1)

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]]
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=['Date & Time', 'Class time', 'Lecturer Name', 'Course Code', 'Week', 'Reporter', 'Observation'],
                font=dict(size=12),
                align='left'
            ),
            cells=dict(
                values=[dfl[i].tolist() for i in dfl.columns],
                align='left'
            )
        ),
        row=1, col=1
    )

    fig.update_layout(
        height=450,
        showlegend=False,
        title=title,
        paper_bgcolor='rgba(248, 248, 255, 1)',
        plot_bgcolor='rgba(248, 248, 255, 1)',
    )

    return dfls, dfl, fig

@sl.cache_data
def table_agent(df, title):
    dfl = df[['Reporter','Monday','Tuesday','Wednesday','Thursday','Friday']]

    dfl.columns = ['Reporter','Monday','Tuesday','Wednesday','Thursday','Friday']

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]]
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=['Reporter','Monday','Tuesday','Wednesday','Thursday','Friday'],
                font=dict(size=12),
                align='left'
            ),
            cells=dict(
                values=[dfl[i].tolist() for i in dfl.columns],
                align='left'
            )
        ),
        row=1, col=1
    )

    fig.update_layout(
        height=350,
        showlegend=False,
        title=title
    )

    sl.plotly_chart(fig, use_container_width=False)


def recode(value):
    if value == 'adedayo olayinka':
        return 'Adedayo Olayinka'
    elif value.startswith('kareem'):
        return 'Kareem Omowunmi'
    elif value.startswith('mrs ngozi'):
        return 'Ngozi Amanze'
    elif value == 'adeoye fikayo':
        return 'Adeoye Fikayo'
    elif value == 'good.' or value == 'in good standard.'\
        or value == 'good standard' or value == 'excellent.' or value == '':
        return 'Unspecified'
    elif value.startswith('ekeoma') or value.startswith('okechukwu'):
        return 'Ekeoma Okechukwu'
    elif value == 'amarachi ozumah':
        return 'Amarachi Ozumah'
    elif value.startswith('olarinmoye'):
        return 'Olarinmoye & Kingsley'
    elif value.startswith('shittu') or value.endswith('samuel'):
        return 'Shittu Adedayo Samuel'
    elif value == 'akintibu o.a':
        return 'Akintibu O.A'
    elif value.startswith('omowunmi'):
        return 'Omowunmi & Fikayo'
    elif value.startswith('adedayo') and value.endswith('lekan'):
        return 'Olayinka & Akintibu'
    elif value.startswith('osifo'):
        return 'Osifo Peter'
    else:
        return value
    
def recode_school(value):
    if value == 'BUTH' or value == 'buth' or value == 'BUTB' or value == 'BUTH ' or value == 'Ben-Carson Medical School':
        return 'BCMS'
    elif value == 'Babcock Business School(BBS)' or value == 'SMS ' or value == 'SMS':
        return 'SMS'
    elif value == 'Computing And Engineering Sciences(CES)' or value == 'CES' or value == 'SCES':
        return 'CES'
    elif value == 'VASSS ' or value == 'Vasss' or value == 'VASS': 
        return 'VASSS'
    elif value == 'LSS' or value == 'lss' or value == 'SOLASS':
        return 'LSS'
    elif value == 'Science And Technology(SAT)':
        return 'SAT'
    elif value == 'Education And Humanity(EAH)':
        return 'EAH'
    elif value == 'School of Public And Allied Health' or value == 'SOPAAH':
        return 'PAH'
    elif value == 'School of Nursing' or value == 'SON':
        return 'SNS'
    elif value == 'School of Engineering' or value == 'SOE' or value == 'SOES' or value == '--Select--':
        return 'SOE'
    else:
        return value

def clean_data():
    url = "https://academicplanning.babcock.edu.ng/classmonitor/reportapi.php"
    browse = requests.get(url)
    content = browse.json()

    # header = ['Sn', 'LectName', 'Studcount', 'Cscode', 'Venue', 'Ddate', 'Ctime',
    #           'Mtime', 'Department', 'School', 'Observation', 'Semester', 'Session',
    #           'Week', 'Classmood', 'Reporter', 'comment', 'RecordTime']
    
    header = ['serialNo', 'lecturer', 'students_count', 'coursecode', 'venue', 'class_date', 'class_time', 'reporter_timein', 'department', 'school', 'observation', 'semester', 'session',  'week', 'classmood', 'reporter', 'comment', 'timestamp']
    dfall = pd.DataFrame(content['data'], columns=header)

    dfall = dfall.iloc[4016:,:].copy()

    num = dfall.coursecode.str.split(r'[a-zA-Z ]+')
    dfall['cnum'] = num.str[1].str.strip()
    # dfall = dfall.loc[dfall['cnum'] >= '200',]
    # dfall.loc[dfall['cnum'] >= '200', "semester"] = "Second"
    # dfall.loc[dfall['cnum'] >= '200', "session"] = "2023/2024"
    dfall['school'] = dfall['school'].apply(recode_school)

    dfall['timestamp'] = pd.to_datetime(dfall['timestamp'], unit='s')
    
    
    dfall['session'] = dfall['session'].replace(['2023/2024'], ['2024/2025'])
    dfall['semester'] = dfall['semester'].replace(['Summer'], ['First'])
    # dfall['week'] = dfall['week'].replace(['13'], ['1'])
    
    dfall.drop_duplicates(subset=['lecturer', 'coursecode', 'class_time', 'week'], inplace=True)
    dfall['day'] = dfall['timestamp'].dt.day_name()
    dfall['day_num'] = dfall['timestamp'].dt.dayofweek

    dfall['reporter'] = dfall['reporter'].str.title().str.strip()
    dfall['department'] = dfall['department'].str.title().str.strip()
    # dfall['reporter'] = dfall['reporter'].replace(['07/02/2024'],['Olayinka & Akintibu'])

    # dfall['reporter'] = dfall['reporter'].apply(recode)

    # dfall['coursecode'] = dfall['coursecode'].str.lower()
    # dfall.loc[(dfall.coursecode.str.startswith('law')) & (dfall.reporter == 'Unspecified'), "reporter"] = "Osifo Peter"

    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,1,22)) & (dfall.timestamp <= pd.Timestamp(2024,1,27)), "week"] = "Week 1"
    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,1,29)) & (dfall.timestamp <= pd.Timestamp(2024,2,3)), "week"] = "Week 2"
    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,2,5)) & (dfall.timestamp <= pd.Timestamp(2024,2,10)), "week"] = "Week 3"
    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,2,12)) & (dfall.timestamp <= pd.Timestamp(2024,2,18)), "week"] = "Week 4"
    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,2,19)) & (dfall.timestamp <= pd.Timestamp(2024,2,24)), "week"] = "Week 5"
    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,2,26)) & (dfall.timestamp <= pd.Timestamp(2024,3,3)), "week"] = "Week 6"
    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,3,3)) & (dfall.timestamp < pd.Timestamp(2024,3,10)), "week"] = "Week 7"
    # dfall.loc[(dfall.timestamp >= pd.Timestamp(2024,3,10)) & (dfall.timestamp <= pd.Timestamp(2024,3,16)), "week"] = "Week 8"
    
    dfall['coursecode'] = dfall['coursecode'].str.upper()
    dfall['class_date'] = dfall['timestamp']

    dfall['Week Num'] = dfall['week'].str.split(' ').str[1]
    dfall['week'] = dfall['week'].astype(int)


    return dfall


def get_reference(week, df, held=None):
    if held == 'held':
        cur_week_df = df.loc[df.week == week]
        
        prev_week_num = int(cur_week_df['week'].unique()[0]) - 1
        
        prev_week_df = df.loc[df['week'] == prev_week_num]
        
        if prev_week_df.shape[0] > 0:
            prev_week_df = prev_week_df.loc[prev_week_df['observation'] == 'The Teacher was Present In Class']
            refs = prev_week_df.shape[0]
        else:
            refs = None
    elif held == 'not held':
        cur_week_df = df.loc[df.week == week]
        prev_week_num = int(cur_week_df['week'].unique()[0]) - 1
        prev_week_df = df.loc[df['week'] == prev_week_num]
        if prev_week_df.shape[0] > 0:
            prev_week_df = prev_week_df.loc[(prev_week_df['observation'] == 'The Class did not hold') | (prev_week_df['observation'] == 'The Teacher was Absent From Class') | (prev_week_df['observation'] == 'The Teacher was present but left early') | (prev_week_df['observation'] == '--Select--')]
            refs = prev_week_df.shape[0]
        else:
            refs = None
    else:
        cur_week_df = df.loc[df.week == week]
        prev_week_num = int(cur_week_df['week'].unique()[0]) - 1
        prev_week_df = df.loc[df['week'] == prev_week_num]
        if prev_week_df.shape[0] > 0:
            refs = prev_week_df.shape[0]
        else:
            refs = None

    return refs

def get_prev_week(week, df, session, semester):
    
    prev_week_num = int(week) - 1
    
    prev_week_df_filtered = df.loc[(df['week'] == prev_week_num) & (df['session'] == session) & (df['semester'] == semester)]
    # prev_week_df = df.loc[df['week'] == str(prev_week_num)]
    # ic(prev_week_df_filtered)
    return prev_week_df_filtered