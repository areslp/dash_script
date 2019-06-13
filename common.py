# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy
import plotly as py


def CreateTrajectory(df, groups, title):
    graph = dcc.Graph(
        id=title,
        figure=go.Figure(
            data=[
                go.Scattergl(
                    x=df[columns[0]],
                    y=df[columns[1]],
                    text=df['time'],
                    mode='lines',
                    name='',
                    hoverinfo='y+text+name',
                    hoverlabel={'namelength': -1},
                    line={'width': 1},
                    marker={'size': 2},
                    opacity=0.7
                ) for columns in groups
            ],

            layout=go.Layout(
                title=title,
                showlegend=True,
                xaxis={'title': 'x(m)'},
                yaxis={'title': 'y(m)'}
            )
        )
    )
    return graph


def CreateScatterGraph(df, columns, title, axis_labels, base_time):
    graph = dcc.Graph(
        id=title,
        figure=go.Figure(
            data=[
                go.Scattergl(
                    x=df['time']-base_time,
                    y=df[column],
                    text=df['time'],
                    mode='lines',
                    name=column,
                    hoverinfo='y+text+name',
                    hoverlabel={'namelength': -1},
                    line={'width': 1},
                    marker={'size': 2},
                    opacity=0.7
                ) for column in columns
            ],

            layout=go.Layout(
                title=title,
                showlegend=True,
                xaxis={'title': axis_labels[0]},
                yaxis={'title': axis_labels[1]}
            )
        )
    )
    return graph


def CreateSequenceScatterGraph(df, columns, segments, title, axis_labels, base_time):
    graph = dcc.Graph(
        id=title,
        figure=go.Figure(
            data=[
                go.Scattergl(
                    x=df['first_frame_timestamp']-base_time,
                    y=df[df.segment == segment][column],
                    text=df['first_frame_timestamp'],
                    mode='lines',
                    name=column + '_' + str(segment),
                    hoverinfo='y+text+name',
                    hoverlabel={'namelength': -1},
                    line={'width': 1},
                    marker={'size': 2},
                    opacity=0.7
                ) for segment in segments for column in columns
            ],

            layout=go.Layout(
                title=title,
                showlegend=True,
                xaxis={'title': axis_labels[0]},
                yaxis={'title': axis_labels[1]}
            )
        )
    )
    return graph


    
def CreateSequenceBoxGraph(df, columns, segments, title, axis_label):
    graph = dcc.Graph(
        id=title,
        figure=go.Figure(
            data=[
                go.Box(
                    y=df[df.segment == segment][column],
                    name=column + '_' + str(segment),
                    opacity=0.7,
                    hoverlabel={'namelength': -1},
                    boxmean='sd'
                ) for segment in segments for column in columns
            ],

            layout=go.Layout(
                title=title,
                showlegend=True,
                xaxis={'title': axis_label},
            )
        )
    )
    return graph


def CreateBoxGraph(df, columns, title, axis_label):
    graph = dcc.Graph(
        id=title,
        figure=go.Figure(
            data=[
                go.Box(
                    y=df[column],
                    name=column,
                    opacity=0.7,
                    hoverlabel={'namelength': -1},
                    boxmean='sd'
                ) for column in columns
            ],

            layout=go.Layout(
                title=title,
                showlegend=True,
                xaxis={'title': axis_label}
            )
        )
    )
    return graph
